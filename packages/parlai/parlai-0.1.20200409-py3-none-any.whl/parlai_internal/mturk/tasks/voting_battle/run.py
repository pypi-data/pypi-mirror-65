#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from parlai.core.loader import load_teacher_module
from parlai.core.params import ParlaiParser
from voting_manager import VotingManager
from worlds import \
    MTurkVotingBattleWorld, RoleOnboardWorld,\
    FULL_GAME, RESPONSE_ONLY, VOTE_ONLY, SOLO_QUAL, MULTI_QUAL,\
    MASTER_LIVE_QUAL, MASTER_SANDBOX_QUAL
from game_configs.default import DefaultGameConfig
from task_config import task_config
import os


def main():
    argparser = ParlaiParser(False, False)
    argparser.add_parlai_args()
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()

    argparser.add_argument('-nr', '--num_rounds', default=5, type=int,
                           help='number of rounds')
    argparser.add_argument('-np', '--num_players', default=5, type=int,
                           help='number of players in the game')
    argparser.add_argument('-mx_lbl_tm', '--max_label_time', default=60,
                           type=int,
                           help='time limit for labeling an example')
    argparser.add_argument('-mx_vt_tm', '--max_vote_time', default=30,
                           type=int,
                           help='time limit for voting on labels')
    argparser.add_argument('-mx_onb_time', '--max_onboard_time', type=int,
                           default=300, help='time limit for turker'
                           'in onboarding')
    argparser.add_argument('--auto-approve-delay', type=int,
                           default=3600*24*1, help='how long to wait for  \
                           auto approval')
    argparser.add_argument('--base_bonus', type=float, default=0.70,
                           help='the bonus (in USD) to be paid to players \
                                 for not disconnecting during the entire game \
                                 (timeouts under threshold OK)')
    argparser.add_argument('--participate_bonus', type=float, default=0.40,
                           help='the bonus (in USD) to be paid to players for \
                                 participating in every single round (aka not \
                                 timing out even once)')
    argparser.add_argument('-vb', '--vote_bonus', type=float,
                           default=0.15, help='the bonus (in USD) to be paid \
                                               to players for selecting the \
                                               winning response')
    argparser.add_argument('-rb', '--response_bonus', type=float,
                           default=0.25, help='the bonus (in USD) to be paid \
                                               to players for writing the \
                                               winning response')
    argparser.add_argument('--allowed_timeouts', type=int, default=1,
                           help='number of timeouts we allow before kicking \
                                 turker')
    argparser.add_argument('--warning_time', type=int, default=15,
                           help='amount of time left (in s) when message is \
                                 sent to remind player to respond')
    argparser.add_argument('--show_truth_label', type='bool', default=False,
                           help='whether to show the truth label along with \
                                 the player generated ones in voting round')
    argparser.add_argument('--single_player', type='bool', default=False,
                           help='if the game should be ran for only a single \
                                 Turker. Overrides num_players to 1.')
    argparser.add_argument('--game_mode', type=str, default=FULL_GAME,
                           choices=[FULL_GAME, RESPONSE_ONLY, VOTE_ONLY],
                           help='Choose your game mode')
    argparser.add_argument('--has_ground_truth', type='bool',
                           default=False,
                           help='Ex: SQuAD or VQA has a ground truth \
                                 Means we should allow you to vote for yourself, \
                                 , turn answers lowercase, and not check for collusion.')
    argparser.add_argument('--gen_init_offset', type=int,
                           default=-1,
                           help='What index the global generator starts at. \
                                 If -1, random examples will be used. Is not \
                                 compatible with full game yet.')
    argparser.add_argument('--num_turkers_set', type=int,
                           default=1,
                           help='Minimum number of turkers to evaluate a \
                                 given set of examples. Used with \
                                 single_player mode.')
    argparser.add_argument('--master_turkers_only', type='bool', default=False,
                            help='Only allow master turkers to complete the \
                                  HIT')
    argparser.add_argument('--use_version_quals', type='bool', default=False,
                            help='Use qualifications to prevent workers from \
                                  doing both a solo and multi HIT. You might \
                                  want to reset the workers with these quals.')
    game_config = DefaultGameConfig()
    argparser.add_task_args(game_config.TASK_NAME)
    opt = argparser.parse_args()

    directory_path = os.path.dirname(os.path.abspath(__file__))
    opt['task'] = os.path.basename(directory_path)
    if 'data_path' not in opt:
        opt['data_path'] = os.getcwd() + '/data/' + game_config.TASK_IDENTIFIER + \
                            ('_master' if opt['master_turkers_only'] else '')
        opt['current_working_dir'] = os.getcwd()
    opt.update(task_config)
    n_players = opt['num_players']
    if opt['single_player']:
        n_players = 1

    mturk_agent_ids = [DefaultGameConfig.PLAYER]*n_players

    mturk_manager = VotingManager(
        opt=opt,
        mturk_agent_ids=mturk_agent_ids
    )

    ex_class = load_teacher_module(game_config.TASK_NAME)

    mturk_manager.setup_server(task_directory_path=directory_path)

    try:
        mturk_manager.start_new_run()

        agent_qualifications = []

        if opt['use_version_quals'] and not opt['is_sandbox']:
            # don't let the same workers do single-player and multiplayer
            qual = MULTI_QUAL if opt['single_player'] else SOLO_QUAL
            agent_qualifications.append(
                {'QualificationTypeId': qual,
                 'Comparator': 'DoesNotExist',
                 'RequiredToPreview': True}
            )
        if opt['master_turkers_only']:
            qual =  MASTER_SANDBOX_QUAL if opt['is_sandbox'] else \
                    MASTER_LIVE_QUAL
            agent_qualifications.append(
                {'QualificationTypeId': qual,
                 'Comparator': 'Exists',
                 'RequiredToPreview': True}
            )

        mturk_manager.create_hits(qualifications=agent_qualifications)

        def run_onboard(worker):
            print("Onboarding Agent {}".format(worker.worker_id))
            world = RoleOnboardWorld(opt, worker)
            world.parley()
            world.shutdown()

        mturk_manager.set_onboard_function(onboard_function=run_onboard)
        mturk_manager.ready_to_accept_workers()

        def check_workers_eligibility(workers):
            if not opt.get('is_sandbox', True):
                valid_workers = {}
                for worker in workers:
                    worker_id = worker.worker_id
                    if worker_id not in valid_workers:
                        valid_workers[worker_id] = worker
                    if len(valid_workers) == n_players:
                        break
                return valid_workers.values() if len(valid_workers) == n_players else []
            else:
                return workers

        eligibility_function = {
            'func': check_workers_eligibility,
            'multiple': True,
        }

        if opt['gen_init_offset'] >= 0:
            master_generator = ex_class(opt)
            master_generator.reset()
            # some game_configs generate examples up to 25 from the offset,
            # so be careful about this - look at game_config.next_example()
            total_episodes = master_generator.num_episodes()
            num_wanted = opt['num_conversations'] // opt['num_turkers_set']
            if opt['gen_init_offset'] > total_episodes:
                opt['gen_init_offset'] = opt['gen_init_offset'] % total_episodes
            master_generator.episode_idx = -1

        def assign_worker_roles(workers):
            for worker in workers:
                worker.id = mturk_agent_ids[0]

        def run_conversation(mturk_manager, opt, workers):
            offset = -1
            if opt['gen_init_offset'] >= 0:
                # Increment by 1 so that you can skip by variable number in
                # the specific GameConfig override of next_example
                master_generator.episode_idx += 1
                master_generator.episode_idx %= num_wanted
                per_offset = total_episodes // num_wanted
                offset = (master_generator.episode_idx * per_offset + \
                            opt['gen_init_offset']) % total_episodes
            conv_idx = mturk_manager.conversation_index
            ex_generator = ex_class(opt)
            world = MTurkVotingBattleWorld(
                opt,
                ex_generator,
                agents=workers,
                world_tag='conversation t_{}'.format(conv_idx),
                offset=offset
            )

            world.parley()
            world.save_data()
            world.save_bonuses()
            world.shutdown()
            world.review_work()

        mturk_manager.start_task(
            eligibility_function=eligibility_function,
            assign_role_function=assign_worker_roles,
            task_function=run_conversation
        )

    except BaseException:
        raise
    finally:
        mturk_manager.expire_all_unassigned_hits()
        mturk_manager.shutdown()

if __name__ == '__main__':
    main()

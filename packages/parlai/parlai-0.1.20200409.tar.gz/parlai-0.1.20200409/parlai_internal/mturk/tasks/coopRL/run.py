#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
import os
from parlai.core.params import ParlaiParser
from parlai.mturk.core.mturk_manager import MTurkManager
from parlai_internal.mturk.tasks.coopRL.worlds import \
    MTurkGridWorldOnboardWorld, MTurkGridWorldGameWorld,\
    MTurkGridWorldModelGameWorld

from parlai_internal.mturk.tasks.coopRL.task_config import task_config
import random
import torch

parent_dir = os.path.dirname(os.path.abspath(__file__))

COOP_MODEL = os.path.join(parent_dir, 'models/bs8_ow1_r0/model_i96000.pt')
DEFECT_MODEL = os.path.join(parent_dir, 'models/bs8_ow0_r0/model_i96000.pt')

EXPERIMENTS = {
    'one_turk': [
        {
            'output_dir': 'coop',
            'strat_type': 'coop',
            'strat_params': {
                'coop_model': COOP_MODEL,
                'defect_model': DEFECT_MODEL,
            },
        },
        {
            'output_dir': 'defect',
            'strat_type': 'defect',
            'strat_params': {
                'coop_model': COOP_MODEL,
                'defect_model': DEFECT_MODEL,
            },
        }
    ],
    'two_turk': [
        {
            'output_dir': 'two_turkers',
        },
    ]
}

ONE_TURK_COUNT = len(EXPERIMENTS['one_turk'])
TWO_TURK_COUNT = len(EXPERIMENTS['two_turk'])
ONE_TURK_PROP = ONE_TURK_COUNT / (ONE_TURK_COUNT + TWO_TURK_COUNT)


def main():
    """
    This task consists of either two turkers or a turker and a model playing
    in a 'cooperative' game while being able to chat or not.
    """
    argparser = ParlaiParser(False, False)
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()
    argparser.add_argument('--board_size', type=int, default=8)
    argparser.add_argument('--max_apples', type=int, default=5)
    argparser.add_argument('--apple_reward', type=int, default=2)
    argparser.add_argument('--apple_punishment', type=int, default=0)
    argparser.add_argument('--apple_reappear', type=int, default=0.2)
    argparser.add_argument('--apple_temptation', type=int, default=1)
    argparser.add_argument('--rounds', type=int, default=50)
    opt = argparser.parse_args()
    directory_path = os.path.dirname(os.path.abspath(__file__))
    opt['task'] = os.path.basename(directory_path)
    opt.update(task_config)

    mturk_agent_1_id = 'red_player'
    mturk_agent_2_id = 'blue_player'
    mturk_agent_ids = [mturk_agent_1_id, mturk_agent_2_id]
    mturk_manager = MTurkManager(
        opt=opt,
        mturk_agent_ids=mturk_agent_ids
    )
    mturk_manager.setup_server(task_directory_path=directory_path)

    try:
        mturk_manager.start_new_run()
        mturk_manager.create_hits()
        onboarded_workers = []
        curr_exp = 0

        def run_onboard(worker):
            nonlocal onboarded_workers  # noqa: E999 we don't support python2
            # Only onboard a worker once
            if worker.worker_id not in onboarded_workers:
                world = MTurkGridWorldOnboardWorld(
                    opt=opt,
                    mturk_agent=worker
                )
                while not world.episode_done():
                    world.parley()
                world.shutdown()
                onboarded_workers.append(worker.worker_id)

        # You can set onboard_function to None to skip onboarding
        mturk_manager.set_onboard_function(onboard_function=run_onboard)
        mturk_manager.ready_to_accept_workers()

        def check_worker_eligibility(worker):
            return True

        def assign_worker_roles(workers):
            new_val = random.random()
            print(ONE_TURK_PROP, new_val)

            if new_val >= ONE_TURK_PROP:
                for index, worker in enumerate(workers):
                    worker.id = mturk_agent_ids[index % len(mturk_agent_ids)]
            else:
                workers[0].id = random.choice(mturk_agent_ids)
                workers[1].id = None

        def run_conversation(mturk_manager, opt, workers):
            nonlocal curr_exp  # noqa: E999 as we don't support python2
            curr_exp += 1
            if len(workers) == 1:
                exp = random.choice(EXPERIMENTS['one_turk'])
                player_index = mturk_agent_ids.index(workers[0].id)
                world = MTurkGridWorldModelGameWorld(
                    opt=opt,
                    agents=workers,
                    experiment=exp,
                    mturk_player=player_index
                )

                while not world.episode_done():
                    world.parley()
            else:
                exp = random.choice(EXPERIMENTS['two_turk'])
                world = MTurkGridWorldGameWorld(
                    opt=opt,
                    agents=workers,
                )

                while not world.episode_done():
                    world.parley()

            # TODO Save game_data to exp['output_dir']
            print('Should save data to {}'.format(
                exp['output_dir']
            ))
            world.shutdown()

        mturk_manager.start_task(
            eligibility_function=check_worker_eligibility,
            assign_role_function=assign_worker_roles,
            task_function=run_conversation
        )

    except Exception:
        raise
    finally:
        mturk_manager.expire_all_unassigned_hits()
        mturk_manager.shutdown()


if __name__ == '__main__':
    main()

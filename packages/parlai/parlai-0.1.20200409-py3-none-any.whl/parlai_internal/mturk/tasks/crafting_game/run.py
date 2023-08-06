#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
import os
import random

from parlai.core.params import ParlaiParser
from parlai.mturk.core.mturk_manager import MTurkManager
import parlai.mturk.core.mturk_utils as mturk_utils
from parlai_internal.mturk.tasks.crafting_game.worlds import \
    GameOnboardWorld, GameWorld
from parlai_internal.mturk.tasks.crafting_game.task_config import task_config


def main():
    """

    """
    argparser = ParlaiParser(False, False)
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()

    argparser.add_argument('--experiment', default='retrospector',
                           help='type of the experiment that we want to launch.\
                            For now, we can have either "restrospector" or "control".')
    argparser.add_argument('--bonus', type=float, default=0,
                           help='Bonus amount')
    argparser.add_argument('--bonus_final', type=float, default=0,
                           help='Bonus amount if finishes all the game')
    argparser.add_argument('--no_craft_qualification', action='store_true',
                           help='Do not add qualification for completing a crafting experiment.')

    opt = argparser.parse_args()
    directory_path = os.path.dirname(os.path.abspath(__file__))

    opt['task'] = os.path.basename(directory_path)
    opt['assignment_duration_in_seconds'] = 60*60*2
    opt['auto_approve_delay'] = 24*3600  # auto-approve after one day
    # create a qualification for workers that had already completed a crafting experiment
    qual_name = 'CraftingAlreadyDone'
    qual_desc = (
        'Qualification for a worker that has already completed a crafting experiment.'
    )
    qual_id = \
        mturk_utils.find_or_create_qualification(qual_name, qual_desc,
                                                 opt['is_sandbox'])
    print('Created qualification: ', qual_id)
    experiment_type = opt['experiment']
    assert experiment_type in ['retrospector', 'control']
    opt.update(task_config[experiment_type])
    print("Parameters: ", opt)

    mturk_agent_id = experiment_type + "_agent"
    mturk_manager = MTurkManager(
        opt=opt,
        mturk_agent_ids=[mturk_agent_id]
    )
    mturk_manager.setup_server(task_directory_path=directory_path)

    try:
        def run_onboard(worker):
            world = GameOnboardWorld(
                opt=opt,
                mturk_agent=worker
            )
            while not world.episode_done():
                world.parley()
            world.shutdown()

        # You can set onboard_function to None to skip onboarding
        mturk_manager.set_onboard_function(onboard_function=run_onboard)
        mturk_manager.start_new_run()

        # Create a HIT with workers that DO NOT have qual_id
        agent_qualifications = [{
            'QualificationTypeId': qual_id,
            'Comparator': 'DoesNotExist',
            'RequiredToPreview': True
        }]
        if opt['no_craft_qualification']:
            mturk_manager.create_hits()
        else:
            mturk_manager.create_hits(qualifications=agent_qualifications)

        mturk_manager.ready_to_accept_workers(timeout_seconds=60*60*2)

        def check_worker_eligibility(worker):
            return True

        def assign_worker_roles(workers):
            workers[0].id = mturk_agent_id

        def run_conversation(mturk_manager, opt, workers):
            # Create mturk agents
            mturk_agent = workers[0]

            world = GameWorld(
                opt=opt,
                mturk_agent=mturk_agent,
                qual_id=qual_id
            )

            while not world.episode_done():
                world.parley()

            world.shutdown()

        mturk_manager.start_task(
            eligibility_function=check_worker_eligibility,
            assign_role_function=assign_worker_roles,
            task_function=run_conversation
        )

    except BaseException:
        raise
    finally:
        # mturk_utils.delete_qualification(qual_id, opt['is_sandbox']) # delete it at the last experiment that you want to run ever !!!
        mturk_manager.expire_all_unassigned_hits()
        mturk_manager.shutdown()


if __name__ == '__main__':
    main()

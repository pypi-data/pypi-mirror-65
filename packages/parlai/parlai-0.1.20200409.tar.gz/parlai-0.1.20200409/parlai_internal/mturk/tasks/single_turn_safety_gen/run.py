#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from parlai.core.params import ParlaiParser
from parlai.mturk.core.mturk_manager import MTurkManager
import parlai.mturk.core.mturk_utils as mutils
from parlai_internal.mturk.tasks.repartee_safety.run import GetTopics
from parlai_internal.mturk.tasks.single_turn_safety_review.run import (
    ensure_dir,
    TrackOnboardingCompletion
)

from task_config import task_config
from worlds import (
    SingleTurnSafetyGenScratch,
    SingleTurnSafetyGenTopic,
    SingleTurnSafetyGenOnboardingWorld,
    BLOCK_QUALIFICATION
)

import os
import random


ParlaiParser()  # instantiate to set PARLAI_HOME environment var
DEFAULT_SAVE_DIR = os.path.join(os.environ['PARLAI_HOME'], 'data')


def main():
    argparser = ParlaiParser(False, add_model_args=True)
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()
    argparser.add_argument('--run-onboard', type='bool', default=True,
                           help='run onboard world')
    argparser.add_argument('--save-dir', type=str,
                           default=os.path.join(DEFAULT_SAVE_DIR,
                                                'mturk_safety_gen_data'),
                           help='where to save onboard tracking data')
    argparser.add_argument('--topics-file', type=str,
                           default=os.path.join(DEFAULT_SAVE_DIR,
                                                'wizard_of_wikipedia',
                                                'topic_splits.json'),
                           help='topics data')
    argparser.add_argument('--num-per-eval', type=int, default=5,
                           help='number of sentences per HIT')
    argparser.add_argument('--ok-or-notok', type=str, default='NOT OK',
                           choices=['OK', 'NOT OK'],
                           help='ask turker to generate messages that are'
                                'either OK or NOT OK')
    argparser.add_argument('--len-range', type=str, default='4,20',
                           help='range to enforce minimum and maximum'
                                'submitted sentence lengths')
    argparser.add_argument('--auto-approve-delay', type=int,
                           default=3600 * 24 * 2,
                           help='how long to wait for auto approval (default '
                                'is two days)')
    opt = argparser.parse_args()

    # Set the task name to be the folder name
    opt['task'] = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

    # append the contents of task_config.py to the configuration
    opt.update(task_config)

    # load topics
    if not os.path.isfile(opt['topics_file']):
        # check for topics file
        from parlai.tasks.wizard_of_wikipedia.build import build
        print('[ Downloading topics data... ]')
        build(opt)
    print('[ Building Topics manager... ]')
    topics = GetTopics(opt)

    # Select an agent_id that worker agents will be assigned in their world
    mturk_agent_roles = ['Evaluator']

    mturk_manager = MTurkManager(
        opt=opt,
        mturk_agent_ids=mturk_agent_roles,
        use_db=True,
    )

    mturk_manager.setup_server(
        task_directory_path=os.path.dirname(os.path.abspath(__file__)))

    onboarding_tracker = TrackOnboardingCompletion(opt)

    def run_onboard(worker):
        nonlocal onboarding_tracker
        if onboarding_tracker.did_worker_complete(worker.worker_id):
            return
        else:
            role = mturk_agent_roles[0]
            worker.update_agent_id('Onboarding {}'.format(role))
            world = SingleTurnSafetyGenOnboardingWorld(
                opt=opt,
                mturk_agent=worker,
                onboarding_tracker=onboarding_tracker,
            )
            while not world.episode_done():
                world.parley()
            world.shutdown()
            onboarding_tracker.mark_worker_completed(worker.worker_id)
            return world.prep_save_data([worker])

    if opt.get('run_onboard'):
        mturk_manager.set_onboard_function(onboard_function=run_onboard)

    try:
        # Initialize run information
        mturk_manager.start_new_run()

        # Set up the sockets and threads to recieve workers
        mturk_manager.ready_to_accept_workers()

        # Create a qualification to ensure a worker won't repeat modifying
        # sentences will become necessary toward the end of the stack

        qual_name = BLOCK_QUALIFICATION
        qual_desc = (
            'Qualification to ensure worker does not exceed maximum turns '
            'on this HIT'
        )
        qualification_id = \
            mutils.find_or_create_qualification(qual_name, qual_desc,
                                                False, must_be_owned=False)
        max_qualif = {
            'QualificationTypeId': qualification_id,
            'Comparator': 'DoesNotExist',
            'RequiredToPreview': True
        }
        qualifications = [max_qualif]

        mturk_manager.create_hits(qualifications=qualifications)

        def check_workers_eligibility(workers):
            return workers

        def assign_worker_roles(workers):
            for worker in workers:
                worker.id = mturk_agent_roles[0]

        def run_conversation(mturk_manager, opt, workers):
            worker = workers[0]
            worker.task_world_assignment = random.randint(1, 2)

            if worker.task_world_assignment == 1:
                worker.update_agent_id('Scratch')
                world = SingleTurnSafetyGenScratch(
                    opt=opt,
                    mturk_agents=workers,
                )
            else:
                worker.update_agent_id('Topic')
                world = SingleTurnSafetyGenTopic(
                    opt=opt,
                    mturk_agents=workers,
                    topics=topics.random_topics(),
                )

            while not world.episode_done():
                world.parley()

            world.shutdown()

            # Return the contents for saving
            return world.prep_save_data(workers)

        mturk_manager.start_task(
            eligibility_function=check_workers_eligibility,
            assign_role_function=assign_worker_roles,
            task_function=run_conversation
        )

    except Exception:
        raise

    finally:
        onboarding_tracker.save_completion_list()
        mturk_manager.shutdown()


if __name__ == '__main__':
    main()

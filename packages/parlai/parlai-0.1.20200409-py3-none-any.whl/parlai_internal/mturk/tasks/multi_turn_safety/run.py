#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from parlai.core.agents import create_agent
from parlai.core.params import ParlaiParser
from parlai.mturk.core.mturk_manager import MTurkManager
import parlai.mturk.core.mturk_utils as mutils
from parlai_internal.mturk.tasks.single_turn_safety_review.run import (
    TrackOnboardingCompletion
)

from build_conversations import CONVOS_FILE
from model_configs import models as mcs
from task_config import task_config
from worlds import (
    MultiTurnSafetyWorld,
    MultiTurnSafetyOnboardingWorld,
    BLOCK_QUALIFICATION
)

import json
import os
import random
import time


ParlaiParser()  # instantiate to set PARLAI_HOME environment var
DEFAULT_SAVE_DIR = os.path.join(os.environ['PARLAI_HOME'], 'data')

LOCAL_CONFIG = [{
    'model': 'bert_classifier',
    'datapath': DEFAULT_SAVE_DIR,
    'threshold': 0.48,
    'model_file': 'data/models/safety_model/model',
    'no_cuda': True,
    'save_name': 'local_test'
}]



class ConversationsManager(object):
    def __init__(self, conversations_file):
        self.file_path = conversations_file
        self.conversations = self.load_conversations()
        self.num_conversations = len(self.conversations)
        self.silence_token = '__SILENCE__'

    def load_conversations(self):
        if not os.path.isfile(self.file_path):
            raise RuntimeError(
                '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
                'Filepath {} does not exist. '
                '\nPlease run the script build_conversations.py (in this '
                'directory) to build the conversations. '.format(self.file_path)
            )

        with open(self.file_path, 'r') as f:
            conversations = json.loads(f.read())

        return conversations

    def _get_truncated_conversation(self):
        idx = random.randint(0, self.num_conversations - 1)
        conversation = self.conversations[idx]
        length = min(len(conversation), random.randint(2, 5))
        return idx, conversation[:length]

    def get_n_truncated_conversations(self, n=5):
        conversations = []
        idxs = []
        for _ in range(n):
            idx, convo = self._get_truncated_conversation()
            # avoid repeats and conversations with a SILENCE toiken
            while idx in idxs or self.silence_token in convo:
                idx, convo = self._get_truncated_conversation()
            conversations.append(convo)
            idxs.append(idx)

        return conversations


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
    argparser.add_argument('--conversations-file', type=str,
                           default=os.path.join(DEFAULT_SAVE_DIR,
                                                CONVOS_FILE),
                           help='topics data')
    argparser.add_argument('--num-per-eval', type=int, default=5,
                           help='number of sentences per HIT')
    argparser.add_argument('--num-tries', type=int, default=2,
                           help='number of tries to beat the classifier')
    argparser.add_argument('--len-range', type=str, default='4,20',
                           help='range to enforce minimum and maximum'
                                'submitted sentence lengths')
    argparser.add_argument('--auto-approve-delay', type=int,
                           default=3600 * 24 * 4,
                           help='how long to wait for auto approval (default '
                                'is two days)')
    argparser.add_argument('--force-onboarding', type='bool', default=False,
                           help='force onboarding (for testing)')
    argparser.add_argument('--local-test', type='bool', default=False,
                           help='test locally and not on FAIR cluster')

    # Set up shared bot parameters
    def get_shared_bot_params(model_opt, argparser):
        argparser.add_model_subargs(model_opt['model'])
        opt = argparser.parse_args()
        for k, v in model_opt.items():
            opt[k] = v
            opt['override'][k] = v

        # Create shared opts from model
        bot = create_agent(opt)
        shared_bot_params = bot.share()

        return opt, shared_bot_params, model_opt['save_name']

    shared_param_list = []
    bot_names = []
    opt = argparser.parse_args()
    if opt['local_test']:
        model_list = LOCAL_CONFIG
    else:
        model_list = mcs

    for model_opt in model_list:
        opt, shared_params, bot_name = get_shared_bot_params(model_opt,
                                                             argparser)
        shared_param_list.append(shared_params)
        bot_names.append(bot_name)

    # Set the task name to be the folder name
    opt['task'] = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

    # Append the contents of task_config.py to the configuration
    opt.update(task_config)

    # Initialize conversations manager
    convo_mngr = ConversationsManager(opt['conversations_file'])

    # Set up onboarding tracker
    onboarding_tracker = TrackOnboardingCompletion(opt)

    # world counter
    counter = 0

    # Select an agent_id that worker agents will be assigned in their world
    mturk_agent_roles = ['Evaluator']

    mturk_manager = MTurkManager(
        opt=opt,
        mturk_agent_ids=mturk_agent_roles,
        use_db=True,
    )

    mturk_manager.setup_server(
        task_directory_path=os.path.dirname(os.path.abspath(__file__)))

    def run_onboard(worker):
        nonlocal onboarding_tracker
        if (onboarding_tracker.did_worker_complete(worker.worker_id) and not
                opt['force_onboarding']):
            return
        else:
            role = mturk_agent_roles[0]
            worker.update_agent_id('Onboarding {}'.format(role))
            world = MultiTurnSafetyOnboardingWorld(
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

        if not opt.get('is_sandbox'):
            # ADD BLOCKED WORKERS HERE
            blocked_worker_list = ['AIU30D5BNNCWH', 'A2541C8MY0BYV3'
                                   'A2UXVNIR273792', 'A2UXVNIR273792']
            for w in blocked_worker_list:
                try:
                    print('Soft blocking worker: {}'.format(w))
                    mturk_manager.give_worker_qualification(w, qual_name)
                except:
                    print('Did not soft block worker:', w)
                time.sleep(0.1)

        mturk_manager.create_hits(qualifications=qualifications)

        def check_workers_eligibility(workers):
            return workers

        def assign_worker_roles(workers):
            for worker in workers:
                worker.id = mturk_agent_roles[0]

        def run_conversation(mturk_manager, opt, workers):
            nonlocal counter
            counter += 1
            conversations = convo_mngr.get_n_truncated_conversations(
                n=opt['num_per_eval'])

            world = MultiTurnSafetyWorld(opt, workers, conversations,
                                         model_opt=shared_param_list,
                                         bot_names=bot_names,
                                         world_id=counter)

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

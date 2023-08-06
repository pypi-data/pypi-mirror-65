#!/usr/bin/env python3

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from parlai.core.params import ParlaiParser
from worlds import GenderAnnotationWorld
from parlai.mturk.core.mturk_manager import MTurkManager
import parlai.mturk.core.mturk_utils as mutils
from parlai.tasks.convai2.build import build

from parlai_internal.mturk.tasks.single_turn_safety_review.run import GetEvaluationStack
from parlai_internal.mturk.tasks.wizard_model_eval.mtdont import MTDONT_LIST
from parlai_internal.tasks.convai2_review.contractions_list import (
    contractions_list,
    punctuation_list,
    contraction_spaces,
    contraction_left_spaces,
    contraction_right_spaces,
)

from task_config import task_config

import json
import os
import pickle
import time
from tqdm import tqdm


MASTER_QUALIF = {
    'QualificationTypeId': '2F1QJWKUDD8XADTFD2Q0G6UTO95ALH',
    'Comparator': 'Exists',
    'RequiredToPreview': True,
}

MASTER_QUALIF_SDBOX = {
    'QualificationTypeId': '2ARFPLSP75KLA8M8DH1HTEQVJT3SY6',
    'Comparator': 'Exists',
    'RequiredToPreview': True,
}


ParlaiParser()  # instantiate to set PARLAI_HOME environment var
DEFAULT_SAVE_DIR = os.path.join(os.environ['PARLAI_HOME'], 'data')


class GetPersonaStack(GetEvaluationStack):
    """Override to take into account persona names"""

    def build_stack(self, opt):
        print('[ Building stack from original file... ]')
        with open(opt.get('data_file'), 'rb') as data:
            personas = json.load(data)

        stack_num, line_num = 0, 0
        curr_stack = []
        for line in personas:
            curr_stack.append(line)
            line_num += 1
            if line_num % self.num_per_eval == 0:
                # check if we've reached the requisite number of personas
                # per stack
                self.stack[str(stack_num)] = {'stack': curr_stack, 'workers': []}
                stack_num += 1
                curr_stack = []

    def flag(self, stack_idx, text_idx, flag_text, category, reason, worker_id):
        """Override to pass"""
        pass


def convert_text(text):
    new_text = text.lower()
    for x in contraction_spaces:
        if x[1] in text:
            new_text = new_text.replace(x[1], x[0])
    for x in contraction_left_spaces:
        if x[1] in text:
            new_text = new_text.replace(x[1], x[0])
    for x in contraction_right_spaces:
        if x[1] in text:
            new_text = new_text.replace(x[1], x[0])

    return new_text


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def build_personachat_data(opt):
    """Utility function to build the light data and extract the personas into
    the proper format"""
    build(opt)  # download convai2 data if it doesn't exist yet
    opt['data_file'] = os.path.join(
        DEFAULT_SAVE_DIR,
        'convai2_distinct_personas',
        'personas.json'
    )

    def get_unique_personas(lst):
        sort_l = [list(x) for x in sorted(lst) if x]
        unique_dct_keys = []
        unique_dct = {}
        for x in tqdm(sort_l):
            overlap_found = False

            for exist_key in unique_dct_keys:
                overlap = intersection(x, exist_key)
                if len(overlap) >= 2:
                    add_key = ' '.join(exist_key)
                    unique_dct[add_key].append(x)
                    overlap_found = True
                    break

            if not overlap_found:
                unique_dct_keys.append(x)
                new_key = ' '.join(x)
                unique_dct[new_key] = [x]

        unique_items = []
        new_unique_dct = {}
        for v in unique_dct.values():
            max_item = None
            max_len = -1
            for x in v:
                new_len = len(x)
                if new_len > max_len:
                    max_item = x
                    max_len = new_len
            unique_items.append(max_item)
            new_key = ' '.join(max_item)
            new_unique_dct[new_key] = v

        return unique_items, new_unique_dct

    if not os.path.exists(opt['data_file']):
        try:
            os.mkdir(os.path.dirname(opt['data_file']))
        except:
            print('Directory already exists.')
        train_set = os.path.join(
            DEFAULT_SAVE_DIR,
            'ConvAI2/train_both_original_no_cands.txt',
        )
        valid_set = os.path.join(
            DEFAULT_SAVE_DIR,
            'ConvAI2/valid_both_original_no_cands.txt',
        )

        with open(train_set, 'r') as f:
            train = f.read().splitlines()

        with open(valid_set, 'r') as f:
            valid = f.read().splitlines()

        dts = {
            'train': train,
            'valid': valid,
        }

        personas = []
        for _, lst in dts.items():
            persona_lst = []
            curr = []
            for x in tqdm(lst):
                if 'your persona: ' in x:
                    pers_l = x.split('your persona: ')[-1]
                    curr.append(convert_text(pers_l))
                else:
                    curr = sorted(curr)
                    persona_lst.append(tuple(curr))
                    curr = []
            personas += persona_lst

        unique_persona_lst, unique_persona_map = get_unique_personas(personas)

        json_personas = json.dumps(unique_persona_lst)
        json_persona_map = json.dumps(unique_persona_map)
        map_file = os.path.join(
            os.path.dirname(opt['data_file']),
            'persona_unique_map.json'
        )

        with open(opt['data_file'], 'w') as f:
            f.write(json_personas)

        with open(map_file, 'w') as g:
            g.write(json_persona_map)

    return opt


def main():
    """Handles setting up and running a ParlAI-MTurk task by instantiating
    an MTurk manager and configuring it for the single_turn_safety task.
    """
    # Get relevant arguments
    argparser = ParlaiParser(False, False)
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()
    argparser.add_argument(
        '--save-dir',
        type=str,
        default=os.path.join(DEFAULT_SAVE_DIR, 'gender_annotations'),
        help='where to save partial data',
    )
    argparser.add_argument(
        '--evals-per-cand',
        type=int,
        default=2,
        help='number of evaluations per candidate',
    )
    argparser.add_argument(
        '--num-per-eval', type=int, default=10, help='number of candidates per HIT'
    )
    argparser.add_argument(
        '--run-onboard', type='bool', default=False, help='run onboard to as a test'
    )
    argparser.add_argument(
        '--auto-approve-delay',
        type=int,
        default=3600 * 24 * 2,
        help='how long to wait for auto approval (default ' 'is two days)',
    )
    argparser.add_argument(
        '--version-num', type=int, default=0, help='increase this to create a new stack'
    )
    argparser.add_argument(
        '--only-masters',
        type='bool',
        default=False,
        help='Set to True to use only master turks for this'
        + ' test eval, default is %(default)s',
    )
    opt = argparser.parse_args()

    # Set the task name to be the folder name
    opt['task'] = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

    # append the contents of task_config.py to the configuration
    opt.update(task_config)

    # Check that data file exists, else, build:
    opt = build_personachat_data(opt)

    # build evaluation stack
    persona_stacks = GetPersonaStack(opt)

    worker_watch_list = []

    # Select an agent_id that worker agents will be assigned in their world
    mturk_agent_roles = ['Evaluator']

    # Instantiate an MTurkManager with the given options and a maximum number
    # of agents per world of 1 (based on the length of mturk_agent_ids)
    mturk_manager = MTurkManager(
        opt=opt, mturk_agent_ids=mturk_agent_roles, use_db=True
    )

    mturk_manager.setup_server(
        task_directory_path=os.path.dirname(os.path.abspath(__file__))
    )

    # Create an onboard_function, which will be run for workers who have
    # accepted your task and must be completed before they are put in the
    # queue for a task world.
    def run_onboard(worker):
        # TODO: consider adding onboarding here
        pass

    if opt.get('run_onboard'):
        mturk_manager.set_onboard_function(onboard_function=run_onboard)

    try:
        # Initialize run information
        mturk_manager.start_new_run()

        # Set up the sockets and threads to recieve workers
        mturk_manager.ready_to_accept_workers()

        # Create a qualification to ensure a worker won't repeat evaluations
        # This will become necessary toward the end of the stack

        # This qualification is from the old account
        old_qual_name = 'CompletedMaxReviewEvals'
        qual_desc = 'Qualification to ensure worker does not repeat evaluations.'
        qualification_id = mutils.find_or_create_qualification(
            old_qual_name, qual_desc, False, must_be_owned=False
        )
        print('Found old qualification: ', qualification_id)
        max_qualif_old = {
            'QualificationTypeId': qualification_id,
            'Comparator': 'DoesNotExist',
            'RequiredToPreview': True,
        }
        qualifications = [max_qualif_old]

        # This qualification is from the new account
        qual_name = 'CompletedMaxReviewEvals1'
        qualification_id = mutils.find_or_create_qualification(
            qual_name, qual_desc, False, must_be_owned=True
        )
        print('Found or created qualification: ', qualification_id)
        max_qualif_new = {
            'QualificationTypeId': qualification_id,
            'Comparator': 'DoesNotExist',
            'RequiredToPreview': True,
        }
        qualifications.append(max_qualif_new)
        if opt['only_masters']:
            if opt['is_sandbox']:
                qualifications.append(MASTER_QUALIF_SDBOX)
            else:
                qualifications.append(MASTER_QUALIF)

        if not opt.get('is_sandbox'):
            # ADD BLOCKED WORKERS HERE
            blocked_worker_list = MTDONT_LIST + [
                'ATTWN63B3XF47', 'A25ZZOSL7MVU22', 'A3G90BWFBLJWWI', 'A3A8P4UR9A0DWQ', 'A38IPIPA3T3G4', 'A2WOQCXW2NGLSS', 'A38IPIPA3T3G4', 'A38IPIPA3T3G4', 'A11M5KWP2835VO', 'A2IM1Q2SMNUQKF', 'A3F9CSBY2TWKYD', 'A36X979BHQ7Z33', 'A2E286WNSB7KPL'
            ]
            for w in blocked_worker_list:
                try:
                    print('Soft blocking worker: {}'.format(w))
                    mturk_manager.give_worker_qualification(w, qual_name)
                except:
                    print('Did not soft block worker:', w)
                time.sleep(0.1)

        # Create the hits as specified by command line arguments
        mturk_manager.create_hits(qualifications=qualifications)

        def check_workers_eligibility(workers):
            return workers

        # Assign worker roles is used to determine what the role each worker
        # in the given worker list will play. Setting `id` to None will return
        # the worker to the pool rather than putting them in a given task,
        # which is useful for having tasks with different possible worker
        # counts.
        def assign_worker_roles(workers):
            for worker in workers:
                worker.id = mturk_agent_roles[0]

        # Define the task function, which will be run with workers that are
        # as the main task.
        global run_conversation

        def run_conversation(mturk_manager, opt, workers):
            idx, stack, done = persona_stacks.get_next_stack(workers[0].worker_id)

            # Create the task world
            world = GenderAnnotationWorld(
                opt=opt,
                mturk_agents=workers,
                evaluation_stack=stack,
                stack_idx=idx
            )
            # run the world to completion
            while not world.episode_done():
                world.parley()

            # shutdown and review the work
            world.shutdown()
            completed, _, block_worker = world.review_work()

            if block_worker and not opt.get('is_sandbox'):

                # soft block worker
                worker_id = workers[0].worker_id
                worker_watch_list.append(worker_id)
                # list of workers who did not mark reddit candidate as offensive
                print('Updated worker watch list: {}'.format(worker_watch_list))
                try:
                    print('Soft blocking worker: {}\n'.format(worker_id))
                    mturk_manager.give_worker_qualification(worker_id, qual_name)
                except:
                    print('Did not soft block worker:', worker_id)

                # remove worker from stack
                persona_stacks.remove_worker_from_stack(workers[0].worker_id, idx)

            if not completed and not opt.get('test_round'):
                persona_stacks.remove_worker_from_stack(workers[0].worker_id, idx)

            if done:
                # give worker qualification to prevent them from working on
                # more tasks
                mutils.give_worker_qualification(
                    workers[0].worker_id, qualification_id, value=None, is_sandbox=False
                )

            # Return the contents for saving
            return world.prep_save_data(workers)

        # Begin the task, allowing mturk_manager to start running the task
        # world on any workers who connect
        mturk_manager.start_task(
            eligibility_function=check_workers_eligibility,
            assign_role_function=assign_worker_roles,
            task_function=run_conversation,
        )
    except BaseException:
        raise
    finally:
        persona_stacks.save_stack()
        # Any hits that aren't claimed or completed have to be shut down. Must
        # keep the world running until that point.
        mturk_manager.expire_all_unassigned_hits()
        # Shutdown the manager and free all related resources
        mturk_manager.shutdown()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from parlai.core.params import ParlaiParser
from worlds import SingleTurnSafetyOnboardingWorld, SingleTurnSafetyWorld
from parlai.mturk.core.mturk_manager import MTurkManager
import parlai.mturk.core.mturk_utils as mutils
from parlai_internal.mturk.tasks.wizard_model_eval.mtdont import MTDONT_LIST
from task_config import task_config

import json
import os
import pickle
import random
import threading
import time


TEST_STACK = [
    'jeez you are really dumb.',
    'his care for the girl fills me with joy and kindness.',
    'my favorite is green apples, especially the sweet ones.',
    'do you believe in god?',
    'i feel really worthless.',
    'i would love to visit mexico one day!',
    'some things are ok to eat and some things are not.',
    'nice. no kids for me. but one day, and we will go to the beach a lot.',
    'i need a girlfriend. will you be my girlfriend?',
    'i am not a fan of donald trump, what do you think?',
]


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


class GetEvaluationStack(object):
    def __init__(self, opt, has_flag=True):
        save_dir = opt.get('save_dir')
        self.sandbox = opt.get('is_sandbox')
        version_num = opt.get('version_num', 0)
        self.version_str = '_v{}'.format(version_num)
        self.has_flag = has_flag

        if self.sandbox:
            if has_flag:
                self.FLAG_PATH = os.path.join(
                    save_dir,
                    'sandbox',
                    'flagged_list.json'
                )
            self.JSON_PATH = os.path.join(
                save_dir,
                'sandbox',
                'completed_stack.json'
            )
        else:
            if has_flag:
                self.FLAG_PATH = os.path.join(
                    save_dir,
                    'flagged_list{}.json'.format(self.version_str)
                )
            self.JSON_PATH = os.path.join(
                save_dir,
                'completed_stack{}.json'.format(self.version_str)
            )

        if has_flag:
            ensure_dir(self.FLAG_PATH)

        ensure_dir(self.JSON_PATH)

        self.num_per_eval = opt.get('num_per_eval', 10)
        self.total_evals = opt.get('evals_per_cand', 2)
        self.pointer = 0

        self.stack = {}
        self.flagged_list = {}
        self.build_or_load_stack(opt)
        self.next_stack_lock = threading.RLock()

        self.save_stack_interval = 60
        self.last_save_time = time.time()
        self.save_lock = threading.RLock()
        self.save_stack()

    def flag(self, stack_idx, text_idx, flag_text, reason, worker_id):
        idx = stack_idx * 10 + text_idx + 1
        if idx in self.flagged_list:
            self.flagged_list[idx]['workers'].append(worker_id)
            self.flagged_list[idx]['rating'].append(flag_text)
            self.flagged_list[idx]['reasons'].append(reason)
        else:
            self.flagged_list[idx] = {}
            self.flagged_list[idx]['workers'] = [worker_id]
            self.flagged_list[idx]['rating'] = [flag_text]
            self.flagged_list[idx]['reasons'] = [reason]

    def load_stack(self):
        print(f'[ Loading stack from file... {self.JSON_PATH}]')
        with open(self.JSON_PATH, 'r') as f:
            self.stack = json.loads(f.read())
            # find pointer
            found = False
            while not found:
                if (len(self.stack[str(self.pointer)]['workers']) >=
                        self.total_evals):
                    self.pointer += 1
                else:
                    found = True
        if self.has_flag:
            with open(self.FLAG_PATH, 'r') as g:
                self.flagged_list = json.loads(g.read())

    def build_stack(self, opt):
        print('[ Building stack from original file... ]')
        with open(opt.get('data_file'), 'r') as data:
            text_list = data.read().splitlines()

        i = 0
        curr_stack = []
        for line in text_list:
            idx, txt = line.split(' ', 1)
            idx = int(idx) - 1
            if idx % self.num_per_eval == 0 and idx != 0:
                self.stack[str(i)] = {'stack': curr_stack, 'workers': []}
                i += 1
                curr_stack = [txt]
            else:
                curr_stack.append(txt)

    def build_or_load_stack(self, opt):
        # check if this stack has been partially completed
        if os.path.isfile(self.JSON_PATH):
            self.load_stack()
            return

        self.build_stack(opt)

    def save_stack(self):
        if (time.time() - self.last_save_time > self.save_stack_interval):
            with self.save_lock:
                # save data
                print('Saving all data to {}.'.format(self.JSON_PATH))
                data = json.dumps(self.stack)
                with open(self.JSON_PATH, 'w') as f:
                    f.write(data)
                self.last_save_time = time.time()

                # save flagged info
                if self.has_flag:
                    print('Saving all flagged items to {}.'.format(self.FLAG_PATH))
                    flags = json.dumps(self.flagged_list)
                    with open(self.FLAG_PATH, 'w') as g:
                        g.write(flags)

    def get_next_stack(self, worker_id):
        """Returns the next stack for a given worker id, checking to see if
        they've reviewed this stack before. Should be called under lock."""
        with self.next_stack_lock:
            worker_done = False  # assign worker qualification to prevent more work

            # check against worker_id to see if they've completed this before
            stack = self.stack.get(str(self.pointer))
            while stack is not None and len(stack['workers']) >= self.total_evals:
                self.pointer += 1
                print('Pointer at {}'.format(self.pointer))
                stack = self.stack.get(str(self.pointer))

            worker_pointer = self.pointer
            while stack is not None and worker_id in stack['workers']:
                worker_pointer += 1
                stack = self.stack.get(str(worker_pointer))

            if stack is None:
                print('Getting a random stack for worker {}'.format(worker_id))
                key = random.choice(list(self.stack.keys()))
                stack = self.stack[key]
                worker_pointer = int(key)
                worker_done = True

            self.save_stack()
            print('Retrieving stack {} for worker {}.'.format(worker_pointer,
                                                              worker_id))
            stack['workers'].append(worker_id)
            return worker_pointer, stack['stack'], worker_done

    def remove_worker_from_stack(self, worker, stack_index):
        print('Removing worker {} from stack {}'.format(worker, stack_index))
        if worker in self.stack[str(stack_index)]['workers']:
            self.stack[str(stack_index)]['workers'].remove(worker)
        if stack_index < self.pointer:
            print('Pointer at {}'.format(self.pointer))
            self.pointer = stack_index


class TrackOnboardingCompletion(object):
    def __init__(self, opt):
        save_dir = opt.get('save_dir')
        version_num = opt.get('version_num', 0)
        self.list_path = os.path.join(
            save_dir,
            'completed_onboarding_v{}.txt'.format(version_num)
        )
        self.blocked_path = os.path.join(
            save_dir,
            'blocked_onboarding_v{}.txt'.format(version_num)
        )
        ensure_dir(self.list_path)
        self.completed = self.load_completion_list()
        self.soft_blocked = self.load_soft_blocked_list()
        self.list_lock = threading.RLock()
        self.block_lock = threading.RLock()

    def did_worker_complete(self, worker_id):
        with self.list_lock:
            return True if worker_id in self.completed else False

    def mark_worker_completed(self, worker_id):
        with self.list_lock:
            if worker_id not in self.completed:
                self.completed.append(worker_id)
            # now save list
        self.save_completion_list()

    def save_completion_list(self):
        print('Saving onboarding completion list to {}.'.format(self.list_path))
        with self.list_lock:
            with open(self.list_path, 'wb') as g:
                pickle.dump(self.completed, g)

    def remove_worker_from_completion_list(self, worker_id):
        with self.list_lock:
            if worker_id in self.completed:
                self.completed.remove(worker_id)

    def load_completion_list(self):
        if os.path.isfile(self.list_path):
            with open(self.list_path, 'rb') as f:
                completed = pickle.load(f)
            return completed
        return []

    def mark_worker_blocked(self, worker_id):
        with self.block_lock:
            self.soft_blocked.append(worker_id)
        # save list
        self.save_blocked_list()

    def save_blocked_list(self):
        print('Saving blocked list to {}.'.format(self.blocked_path))
        with self.block_lock:
            with open(self.blocked_path, 'wb') as g:
                pickle.dump(self.soft_blocked, g)

    def load_soft_blocked_list(self):
        if os.path.isfile(self.blocked_path):
            with open(self.blocked_path, 'rb') as f:
                blocked = pickle.load(f)
            return blocked
        return []


def main():
    """Handles setting up and running a ParlAI-MTurk task by instantiating
    an MTurk manager and configuring it for the single_turn_safety task.
    """
    # Get relevant arguments
    argparser = ParlaiParser(False, False)
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()
    argparser.add_argument('--data-file', type=str,
                           default='/private/home/edinan/ParlAI/data/safety_checks/convai2_candidates.txt',
                           help='data for review')
    argparser.add_argument('--save-dir', type=str,
                           default='/private/home/edinan/ParlAI/data/safety_checks/',
                           help='where to save partial data')
    argparser.add_argument('--test-round', type='bool', default=False,
                           help='test round uses a set of pre-specified '
                                'candidates')
    argparser.add_argument('--evals-per-cand', type=int, default=2,
                           help='number of evaluations per candidate')
    argparser.add_argument('--num-per-eval', type=int, default=10,
                           help='number of candidates per HIT')
    argparser.add_argument('--run-onboard', type='bool', default=True,
                           help='run onboard to as a test')
    argparser.add_argument('--add-bad-cands', type='bool', default=False,
                           help='add an additional known bad candidate')
    argparser.add_argument('--bad-cand-list', type=str,
                           default='/private/home/edinan/ParlAI/data/safety_checks/offensive_list_twitter.txt',
                           help='list of bad candidates to check Turker '
                                'ability')
    argparser.add_argument('--auto-approve-delay', type=int,
                           default=3600 * 24 * 2,
                           help='how long to wait for auto approval (default '
                                'is two days)')
    argparser.add_argument('--version-num', type=int, default=0,
                           help='increase this to create a new stack')
    opt = argparser.parse_args()

    # Set the task name to be the folder name
    opt['task'] = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

    # append the contents of task_config.py to the configuration
    opt.update(task_config)

    # For the test round, workers can only participate once
    if opt.get('test_round') and not opt.get('is_sandbox'):
        opt['is_unique'] = True

    if not opt.get('test_round'):
        # build evaluation stack
        eval_stacks = GetEvaluationStack(opt)

    if opt.get('add_bad_cands') and os.path.isfile(opt.get('bad_cand_list')):
        with open(opt.get('bad_cand_list'), 'r') as f:
            bad_cands = f.readlines()
    else:
        bad_cands = None
    worker_watch_list = []

    # Select an agent_id that worker agents will be assigned in their world
    mturk_agent_roles = ['Evaluator']

    # Instantiate an MTurkManager with the given options and a maximum number
    # of agents per world of 1 (based on the length of mturk_agent_ids)
    mturk_manager = MTurkManager(
        opt=opt,
        mturk_agent_ids=mturk_agent_roles,
        use_db=True,
    )

    mturk_manager.setup_server(
        task_directory_path=os.path.dirname(os.path.abspath(__file__)))

    onboarding_tracker = TrackOnboardingCompletion(opt)

    # Create an onboard_function, which will be run for workers who have
    # accepted your task and must be completed before they are put in the
    # queue for a task world.
    def run_onboard(worker):
        nonlocal onboarding_tracker
        if onboarding_tracker.did_worker_complete(worker.worker_id):
            return
        else:
            role = mturk_agent_roles[0]
            worker.update_agent_id('Onboarding {}'.format(role))
            world = SingleTurnSafetyOnboardingWorld(
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

        # Create a qualification to ensure a worker won't repeat evaluations
        # This will become necessary toward the end of the stack

        # This qualification is from the old account
        old_qual_name = 'CompletedMaxReviewEvals'
        qual_desc = (
            'Qualification to ensure worker does not repeat evaluations.'
        )
        qualification_id = \
            mutils.find_or_create_qualification(old_qual_name, qual_desc,
                                                False, must_be_owned=False)
        print('Found old qualification: ', qualification_id)
        max_qualif_old = {
            'QualificationTypeId': qualification_id,
            'Comparator': 'DoesNotExist',
            'RequiredToPreview': True
        }
        qualifications = [max_qualif_old]

        # This qualification is from the new account
        qual_name = 'CompletedMaxReviewEvals1'
        qualification_id = \
            mutils.find_or_create_qualification(qual_name, qual_desc,
                                                False, must_be_owned=True)
        print('Found or created qualification: ', qualification_id)
        max_qualif_new = {
            'QualificationTypeId': qualification_id,
            'Comparator': 'DoesNotExist',
            'RequiredToPreview': True
        }
        qualifications.append(max_qualif_new)

        if not opt.get('is_sandbox'):
            # ADD BLOCKED WORKERS HERE
            blocked_worker_list = MTDONT_LIST
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
            if not opt.get('test_round'):
                idx, stack, done = eval_stacks.get_next_stack(workers[0].worker_id)
            else:
                idx = -1
                stack = TEST_STACK

            bad_cand = random.choice(bad_cands) if bad_cands is not None else None

            # Create the task world
            world = SingleTurnSafetyWorld(
                opt=opt,
                mturk_agents=workers,
                evaluation_stack=stack,
                stack_idx=idx,
                bad_cand=bad_cand
            )
            # run the world to completion
            while not world.episode_done():
                world.parley()

            # shutdown and review the work
            world.shutdown()
            completed, flagged, block_worker = world.review_work()

            if block_worker and not opt.get('is_sandbox'):

                # soft block worker
                worker_id = workers[0].worker_id
                worker_watch_list.append(worker_id)
                # list of workers who did not mark reddit candidate as offensive
                print('Updated worker watch list: {}'.format(
                    worker_watch_list
                ))
                try:
                    print('Soft blocking worker: {}\n'.format(
                        worker_id
                    ))
                    mturk_manager.give_worker_qualification(
                        worker_id,
                        qual_name
                    )
                except:
                    print('Did not soft block worker:', worker_id)

                # remove worker from stack
                eval_stacks.remove_worker_from_stack(
                    workers[0].worker_id,
                    idx
                )

            # add any flagged items to the 'flagged list'
            if flagged:
                for key in flagged.keys():
                    text_idx = int(key)
                    flag_text = flagged[key][0]
                    reason = flagged[key][1]
                    eval_stacks.flag(
                        idx,
                        text_idx,
                        flag_text,
                        reason,
                        workers[0].worker_id
                    )

            if not completed and not opt.get('test_round'):
                eval_stacks.remove_worker_from_stack(
                    workers[0].worker_id,
                    idx
                )

            if done:
                # give worker qualification to prevent them from working on
                # more tasks
                mutils.give_worker_qualification(
                    workers[0].worker_id,
                    qualification_id,
                    value=None,
                    is_sandbox=False
                )

            # Return the contents for saving
            return world.prep_save_data(workers)

        # Begin the task, allowing mturk_manager to start running the task
        # world on any workers who connect
        mturk_manager.start_task(
            eligibility_function=check_workers_eligibility,
            assign_role_function=assign_worker_roles,
            task_function=run_conversation
        )
    except BaseException:
        raise
    finally:
        eval_stacks.save_stack()
        onboarding_tracker.save_completion_list()
        # Any hits that aren't claimed or completed have to be shut down. Must
        # keep the world running until that point.
        mturk_manager.expire_all_unassigned_hits()
        # Shutdown the manager and free all related resources
        mturk_manager.shutdown()


if __name__ == '__main__':
    main()

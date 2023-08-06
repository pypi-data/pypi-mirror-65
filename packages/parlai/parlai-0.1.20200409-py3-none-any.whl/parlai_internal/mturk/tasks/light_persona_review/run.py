#!/usr/bin/env python3

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from parlai.core.params import ParlaiParser
from worlds import LIGHTPersonaSafetyWorld
from parlai.mturk.core.mturk_manager import MTurkManager
import parlai.mturk.core.mturk_utils as mutils
from parlai.tasks.light_dialog.build import download

from parlai_internal.mturk.tasks.single_turn_safety_review.run import(
    GetEvaluationStack,
)
from parlai_internal.mturk.tasks.wizard_model_eval.mtdont import MTDONT_LIST


from task_config import task_config
import os
import pickle
import time


ParlaiParser()  # instantiate to set PARLAI_HOME environment var
DEFAULT_SAVE_DIR = os.path.join(os.environ['PARLAI_HOME'], 'data')


class GetPersonaStack(GetEvaluationStack):
    """Override to take into account persona names"""
    def build_stack(self, opt):
        print('[ Building stack from original file... ]')
        with open(opt.get('data_file')) as data:
            text_list = data.read().splitlines()

        stack_num, line_num = 0, 0
        curr_stack = []
        curr_name = None
        for line in text_list:
            if '__name__: ' in line:
                # name of persona
                curr_name = line.split('__name__: ')[1]
            else:
                # persona line
                curr_stack.append((curr_name, line))
                line_num += 1
                if line_num % self.num_per_eval == 0:
                    # check if we've reached the requisite number of personas
                    # per stack
                    self.stack[str(stack_num)] = {'stack': curr_stack,
                                                  'workers': []}
                    stack_num += 1
                    curr_stack = []

    def flag(self, stack_idx, text_idx, flag_text, category, reason, worker_id):
        """Override to include category."""
        # TODO: check this!!!
        idx = stack_idx * self.num_per_eval + text_idx + 1
        self.flagged_list.setdefault(idx, {'workers': [], 'rating': [],
                                           'categories': [], 'reasons': []})
        self.flagged_list[idx]['workers'].append(worker_id)
        self.flagged_list[idx]['rating'].append(flag_text)
        self.flagged_list[idx]['categories'].append(category)
        self.flagged_list[idx]['reasons'].append(reason)

    def flagged_msg_converter(self, idx):
        i = (idx // self.num_per_eval) - 1
        remainder = idx - i * self.num_per_eval
        self.completed_stack[i]['stack'][remainder]


def build_light_data(opt):
    """Utility function to build the light data and extract the personas into
    the proper format"""
    download(opt)  # download light data if it doesn't exist yet
    opt['data_file'] = os.path.join(DEFAULT_SAVE_DIR, 'light_dialogue',
                                    'personas.txt')
    if not os.path.exists(opt['data_file']):
        light_env_file = os.path.join(DEFAULT_SAVE_DIR, 'light_dialogue',
                                      'light_environment.pkl')
        light_env = pickle.load(open(light_env_file, 'rb'))
        with open(opt['data_file'], 'w') as f:
            for _, v in light_env['characters'].items():
                f.write('__name__: ' + v['corrected_name'] + '\n')
                f.write(v['personas'] + '\n')

    return opt


def main():
    """Handles setting up and running a ParlAI-MTurk task by instantiating
    an MTurk manager and configuring it for the single_turn_safety task.
    """
    # Get relevant arguments
    argparser = ParlaiParser(False, False)
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()
    argparser.add_argument('--save-dir', type=str,
                           default=os.path.join(DEFAULT_SAVE_DIR,
                                                'light_persona_review'),
                           help='where to save partial data')
    argparser.add_argument('--evals-per-cand', type=int, default=3,
                           help='number of evaluations per candidate')
    argparser.add_argument('--num-per-eval', type=int, default=5,
                           help='number of candidates per HIT')
    argparser.add_argument('--run-onboard', type='bool', default=False,
                           help='run onboard to as a test')
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

    # Check that data file exists, else, build:
    opt = build_light_data(opt)
    # build evaluation stack
    persona_stacks = GetPersonaStack(opt)

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
            idx, stack, done = persona_stacks.get_next_stack(workers[0].worker_id)

            # Create the task world
            world = LIGHTPersonaSafetyWorld(
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
                persona_stacks.remove_worker_from_stack(
                    workers[0].worker_id,
                    idx
                )

            # add any flagged items to the 'flagged list'
            # TODO: make sure this works ok?
            if flagged:
                for key in flagged.keys():
                    text_idx = int(key)
                    flag_text = flagged[key][0]
                    category = flagged[key][1]
                    reason = flagged[key][2]
                    persona_stacks.flag(
                        idx,
                        text_idx,
                        flag_text,
                        category,
                        reason,
                        workers[0].worker_id
                    )

            if not completed and not opt.get('test_round'):
                persona_stacks.remove_worker_from_stack(
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
        persona_stacks.save_stack()
        # Any hits that aren't claimed or completed have to be shut down. Must
        # keep the world running until that point.
        mturk_manager.expire_all_unassigned_hits()
        # Shutdown the manager and free all related resources
        mturk_manager.shutdown()


if __name__ == '__main__':
    main()

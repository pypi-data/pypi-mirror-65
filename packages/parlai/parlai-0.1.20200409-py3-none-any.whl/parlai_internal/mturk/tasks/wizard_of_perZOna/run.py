#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from parlai.core.agents import create_agent
from parlai.core.teachers import create_task_agent_from_taskname
from parlai.core.params import ParlaiParser
from parlai.utils.misc import AttrDict, ProgressLogger
from parlai.mturk.core.mturk_manager import MTurkManager
from worlds import \
    MTurkWizardOfPerZOnaWorld, RoleOnboardWorld, PersonasGenerator, \
    WIZARD, APPRENTICE
from task_config import task_config
from parlai.core.dict import DictionaryAgent
import os
import copy
import pickle


def setup_retriever(opt):
    print('[ Setting up Retriever ]')
    task = 'wikipedia:full'
    ret_opt = copy.deepcopy(opt)
    ret_opt['model_file'] = 'models:wikipedia_full/tfidf_retriever/model'
    ret_opt['retriever_num_retrieved'] = opt.get('num_passages_retrieved', 7)
    ir_agent = create_agent(ret_opt)
    return ir_agent, task


def setup_title_to_passage(opt):
    print('[ Setting up Title to Passage Dict ]')
    logger = ProgressLogger(should_humanize=False, throttle=0.1)
    saved_dp = os.path.join(os.getcwd() + '/data/', 'title_to_passage.pkl')
    if os.path.exists(saved_dp):
        print('[ Loading from saved location, {} ]'.format(saved_dp))
        with open(saved_dp, 'rb') as f:
            title_to_passage = pickle.load(f)
            return title_to_passage
    ordered_opt = opt.copy()
    ordered_opt['datatype'] = 'train:ordered:stream'
    ordered_opt['batchsize'] = 1
    ordered_opt['numthreads'] = 1
    ordered_opt['task'] = 'wikipedia:full:key-value'
    teacher = create_task_agent_from_taskname(ordered_opt)[0]
    title_to_passage = {}
    i = 0
    length = teacher.num_episodes()
    while not teacher.epoch_done():
        logger.log(i, length)
        i += 1
        action = teacher.act()
        title = action['text']
        text = action['labels'][0]
        title_to_passage[title] = text
    print('[ Finished Building Title to Passage dict; saving now]')
    with open(saved_dp, 'wb') as f:
        pickle.dump(title_to_passage, f)
    return title_to_passage


def main():
    """This task consists of one agent, model or MTurk worker, talking to an
    MTurk worker to negotiate a deal.
    """
    argparser = ParlaiParser(False, False)
    DictionaryAgent.add_cmdline_args(argparser)
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()
    argparser.add_argument('-min_t', '--min_turns', default=3, type=int,
                           help='minimum number of turns')
    argparser.add_argument('-max_t', '--max_turns', default=5, type=int,
                           help='maximal number of chat turns')
    argparser.add_argument('-mx_rsp_time', '--max_resp_time', default=120,
                           type=int,
                           help='time limit for entering a dialog message')
    argparser.add_argument('-mx_onb_time', '--max_onboard_time', type=int,
                           default=300, help='time limit for turker'
                           'in onboarding')
    argparser.add_argument('--persona-type', default='both', type=str,
                           choices=['both', 'self', 'other'],
                           help='Which personas to load from personachat')
    argparser.add_argument('--auto-approve-delay', type=int,
                           default=3600 * 24 * 1, help='how long to wait for  \
                           auto approval')
    argparser.add_argument('--word-overlap-threshold', type=int, default=2,
                           help='How much word overlap we want between message \
                           and checked sentence')
    argparser.add_argument('--num-good-sentence-threshold', type=int, default=2,
                           help='How many good sentences with sufficient overlap \
                           are necessary for turker to be considered good.')
    argparser.add_argument('--num-passages-retrieved', type=int, default=10,
                           help='How many passages to retrieve per dialog \
                           message')
    argparser.add_argument('--test', type='bool', default=False,
                           help='whether I am testing')

    opt = argparser.parse_args()
    directory_path = os.path.dirname(os.path.abspath(__file__))
    opt['task'] = os.path.basename(directory_path)
    if 'data_path' not in opt:
        opt['data_path'] = os.getcwd() + '/data/' + opt['task']
        opt['current_working_dir'] = os.getcwd()
    opt.update(task_config)

    mturk_agent_ids = [APPRENTICE, WIZARD]
    opt['min_messages'] = 2

    mturk_manager = MTurkManager(
        opt=opt,
        mturk_agent_ids=mturk_agent_ids
    )

    ir_agent, task = setup_retriever(opt)
    persona_generator = PersonasGenerator(opt)
    wiki_title_to_passage = setup_title_to_passage(opt)
    mturk_manager.setup_server(task_directory_path=directory_path)
    worker_roles = {}
    connect_counter = AttrDict(value=0)

    try:
        mturk_manager.start_new_run()
        if not opt['is_sandbox']:
            with open(os.path.join(opt['current_working_dir'], 'mtdont.txt')) as f:
                lines = [l.replace('\n', '') for l in f.readlines()]
                for w in lines:
                    mturk_manager.soft_block_worker(w)

        agent_qualifications = [
            {'QualificationTypeId': '00000000000000000071',
             'Comparator': 'In',
             'LocaleValues': [
                 {'Country': 'US', 'Subdivision': 'AL'},
                 {'Country': 'US', 'Subdivision': 'AR'},
                 {'Country': 'US', 'Subdivision': 'DE'},
                 {'Country': 'US', 'Subdivision': 'FL'},
                 {'Country': 'US', 'Subdivision': 'GA'},
                 {'Country': 'US', 'Subdivision': 'IA'},
                 {'Country': 'US', 'Subdivision': 'KS'},
                 {'Country': 'US', 'Subdivision': 'KY'},
                 {'Country': 'US', 'Subdivision': 'LA'},
                 {'Country': 'US', 'Subdivision': 'MD'},
                 {'Country': 'US', 'Subdivision': 'MN'},
                 {'Country': 'US', 'Subdivision': 'MS'},
                 {'Country': 'US', 'Subdivision': 'MO'},
                 {'Country': 'US', 'Subdivision': 'NE'},
                 {'Country': 'US', 'Subdivision': 'ND'},
                 {'Country': 'US', 'Subdivision': 'OK'},
                 {'Country': 'US', 'Subdivision': 'SC'},
                 {'Country': 'US', 'Subdivision': 'SD'},
                 {'Country': 'US', 'Subdivision': 'TN'},
                 {'Country': 'US', 'Subdivision': 'TX'},
                 {'Country': 'US', 'Subdivision': 'VA'},
                 {'Country': 'US', 'Subdivision': 'WV'},
                 {'Country': 'CA'},
                 {'Country': 'GB'},
                 {'Country': 'AU'},
                 {'Country': 'NZ'}
             ],
             'RequiredToPreview': True}
        ]
        if opt['is_sandbox']:
            agent_qualifications = []

        def run_onboard(worker):
            role = mturk_agent_ids[connect_counter.value % len(mturk_agent_ids)]
            connect_counter.value += 1
            worker_roles[worker.worker_id] = role
            worker.persona_generator = persona_generator
            world = RoleOnboardWorld(opt, worker, role)
            world.parley()
            world.shutdown()

        mturk_manager.set_onboard_function(onboard_function=run_onboard)
        mturk_manager.ready_to_accept_workers()
        mturk_manager.create_hits(qualifications=agent_qualifications)

        def check_workers_eligibility(workers):
            if opt['is_sandbox']:
                return workers
            valid_workers = {}
            for worker in workers:
                worker_id = worker.worker_id
                if worker_id not in worker_roles:
                    '''Something went wrong...'''
                    continue
                role = worker_roles[worker_id]
                if role not in valid_workers:
                    valid_workers[role] = worker
                if len(valid_workers) == 2:
                    break
            return valid_workers.values() if len(valid_workers) == 2 else []

        eligibility_function = {
            'func': check_workers_eligibility,
            'multiple': True,
        }

        def assign_worker_roles(workers):
            if opt['is_sandbox']:
                for i, worker in enumerate(workers):
                    worker.id = mturk_agent_ids[i % len(mturk_agent_ids)]
            else:
                for worker in workers:
                    worker.id = worker_roles[worker.worker_id]

        def run_conversation(mturk_manager, opt, workers):
            agents = workers[:]
            if not opt['is_sandbox']:
                for agent in agents:
                    worker_roles.pop(agent.worker_id)
            conv_idx = mturk_manager.conversation_index
            world = MTurkWizardOfPerZOnaWorld(
                opt,
                agents=agents,
                world_tag='conversation t_{}'.format(conv_idx),
                ir_agent=ir_agent,
                wiki_title_to_passage=wiki_title_to_passage,
                task=task
            )
            world.reset_random()
            while not world.episode_done():
                world.parley()
            world.save_data()
            if (world.convo_finished and
                    not world.good_wiz and
                    not opt['is_sandbox']):
                mturk_manager.soft_block_worker(world.wizard_worker)
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

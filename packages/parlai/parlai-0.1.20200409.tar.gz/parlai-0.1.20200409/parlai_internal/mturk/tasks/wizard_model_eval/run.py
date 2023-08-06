#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from parlai.core.params import ParlaiParser
from parlai.core.agents import create_agent
from parlai.utils.misc import AttrDict
from parlai.mturk.core.mturk_manager import MTurkManager
import parlai.mturk.core.mturk_utils as mturk_utils

from mtdont import MTDONT_LIST
from worlds import WizardEval, TopicsGenerator, TopicChooseWorld
from task_config import task_config

import gc
import datetime
import json
import logging
import os
import sys
import time

MASTER_QUALIF = {
    'QualificationTypeId': '2F1QJWKUDD8XADTFD2Q0G6UTO95ALH',
    'Comparator': 'Exists',
    'RequiredToPreview': True
}


def main():
    """This task consists of an MTurk agent evaluating a wizard model. They
    are assigned a topic and asked to chat.
    """
    start_time = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M')
    argparser = ParlaiParser(False, add_model_args=True)
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()
    argparser.add_argument('-mt', '--max-turns', default=10, type=int,
                           help='maximal number of chat turns')
    argparser.add_argument('--max-resp-time', default=240,
                           type=int,
                           help='time limit for entering a dialog message')
    argparser.add_argument('--max-choice-time', type=int,
                           default=300, help='time limit for turker'
                           'choosing the topic')
    argparser.add_argument('--ag-shutdown-time', default=120,
                           type=int,
                           help='time limit for entering a dialog message')
    argparser.add_argument('-rt', '--range-turn', default='3,5',
                           help='sample range of number of turns')
    argparser.add_argument('--human-eval', type='bool', default=False,
                           help='human vs human eval, no models involved')
    argparser.add_argument('--auto-approve-delay', type=int,
                           default=3600 * 24 * 1,
                           help='how long to wait for auto approval')
    argparser.add_argument('--only-masters', type='bool', default=False,
                           help='Set to true to use only master turks for '
                                'this test eval')
    argparser.add_argument('--unique-workers', type='bool', default=True,
                           help='Each worker must be unique')
    argparser.add_argument('--mturk-log', type=str,
                           default='data/mturklogs/{}.log'.format(start_time))

    def inject_override(opt, override_dict):
        opt['override'] = override_dict
        for k, v in override_dict.items():
            opt[k] = v

    def get_logger(opt):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        fmt = logging.Formatter(
            '%(asctime)s: [ %(message)s ]', '%m/%d/%Y %I:%M:%S %p')
        console = logging.StreamHandler()
        console.setFormatter(fmt)
        logger.addHandler(console)
        if 'mturk_log' in opt:
            logfile = logging.FileHandler(opt['mturk_log'], 'a')
            logfile.setFormatter(fmt)
            logger.addHandler(logfile)
        logger.info('COMMAND: %s' % ' '.join(sys.argv))
        logger.info('-' * 100)
        logger.info('CONFIG:\n%s' % json.dumps(opt, indent=4, sort_keys=True))

        return logger

    # MODEL CONFIG
    config_retrieval = {
        'model': 'internal:wizard_retrieval_interactive',
        'retriever_model_file': 'models:wikipedia_full/tfidf_retriever/model',
        'responder_model_file': (
            '/checkpoint/edinan/20180908/transformer_wizard_response_'
            'finetune_squad_NEW/learn-embeddings=False/model'
        ),
    }
    config_hierarchical = {
        'model': 'internal:wizard_hierarchical',
        'retriever_model_file': 'models:wikipedia_full/tfidf_retriever/model',
        'reader_model_file': (
            '/checkpoint/edinan/20180907/wizard_sent_finetune_multitask_squad_NEW/'
            'learn-embeddings=False_lr=8e-05_truncate=200_bs=8/model'
        ),
        'generator_model_file': (
            '/checkpoint/roller/20180916/dropout_TwoStageAgent/'
            'dc2a2a66fdd3ecc3b6cc79440c3b78ac12bf146/model'
        ),
        'no_cuda': True,
        'batchsize': 1,
        'interactive_mode': True,
        'interactive_unique': True,
        'dont_reuse': True,
    }
    config_ignorant = {
        'model': (
            'parlai_internal.projects.wizard.generator.agents:'
            'GenericWizardGeneratorAgent'
        ),
        'model_file': (
            '/checkpoint/roller/20180915/ignorant_GenericWizardGeneratorAgent/'
            '9e6c325d1e95b0fcb274645168300d894c4ccc8/model'
        ),
        'no_cuda': True,
    }
    config = config_hierarchical

    argparser.add_model_subargs(config['model'])  # add model args to opt
    start_opt = argparser.parse_args()

    inject_override(start_opt, config)

    if not start_opt.get('human_eval'):
        bot = create_agent(start_opt)
        shared_bot_params = bot.share()
    else:
        shared_bot_params = None

    if not start_opt['human_eval']:
        get_logger(bot.opt)
    else:
        get_logger(start_opt)

    if start_opt['human_eval']:
        folder_name = 'human_eval-{}'.format(start_time)
    else:
        folder_name = '{}-{}'.format(start_opt['model'], start_time)

    start_opt['task'] = os.path.basename(
        os.path.dirname(os.path.abspath(__file__)))
    if 'data_path' not in start_opt:
        start_opt['data_path'] = os.path.join(
            os.getcwd(),
            'data',
            'wizard_eval',
            folder_name
        )
    start_opt.update(task_config)

    if not start_opt.get('human_eval'):
        mturk_agent_ids = ['PERSON_1']
    else:
        mturk_agent_ids = ['PERSON_1', 'PERSON_2']

    mturk_manager = MTurkManager(
        opt=start_opt,
        mturk_agent_ids=mturk_agent_ids
    )

    topics_generator = TopicsGenerator(start_opt)
    directory_path = os.path.dirname(os.path.abspath(__file__))
    mturk_manager.setup_server(task_directory_path=directory_path)
    worker_roles = {}
    connect_counter = AttrDict(value=0)

    try:
        mturk_manager.start_new_run()
        agent_qualifications = []
        if not start_opt['is_sandbox']:
            # assign qualifications
            if start_opt['only_masters']:
                agent_qualifications.append(MASTER_QUALIF)
            if start_opt['unique_workers']:
                qual_name = 'UniqueChatEval'
                qual_desc = (
                    'Qualification to ensure each worker completes a maximum '
                    'of one of these chat/eval HITs'
                )
                qualification_id = \
                    mturk_utils.find_or_create_qualification(qual_name, qual_desc,
                                                             False)
                print('Created qualification: ', qualification_id)
                UNIQUE_QUALIF = {
                    'QualificationTypeId': qualification_id,
                    'Comparator': 'DoesNotExist',
                    'RequiredToPreview': True
                }
                start_opt['unique_qualif_id'] = qualification_id
                agent_qualifications.append(UNIQUE_QUALIF)
        mturk_manager.create_hits(qualifications=agent_qualifications)

        if not start_opt['is_sandbox']:
            # ADD BLOCKED WORKERS HERE
            blocked_worker_list = MTDONT_LIST
            for w in blocked_worker_list:
                try:
                    print('Soft Blocking {}\n'.format(w))
                    mturk_manager.soft_block_worker(w)
                except:
                    print('Did not soft block worker:', w)
                time.sleep(0.1)

        def run_onboard(worker):
            if start_opt['human_eval']:
                role = mturk_agent_ids[connect_counter.value % len(mturk_agent_ids)]
                connect_counter.value += 1
                worker_roles[worker.worker_id] = role
            else:
                role = 'PERSON_1'
            worker.topics_generator = topics_generator
            world = TopicChooseWorld(start_opt, worker, role=role)
            world.parley()
            world.shutdown()
        mturk_manager.set_onboard_function(onboard_function=run_onboard)
        mturk_manager.ready_to_accept_workers()

        def check_single_worker_eligibility(worker):
            return True

        def check_multiple_workers_eligibility(workers):
            valid_workers = {}
            for worker in workers:
                worker_id = worker.worker_id
                if worker_id not in worker_roles:
                    print('Something went wrong')
                    continue
                role = worker_roles[worker_id]
                if role not in valid_workers:
                    valid_workers[role] = worker
                if len(valid_workers) == 2:
                    break
            return valid_workers.values() if len(valid_workers) == 2 else []

        if not start_opt['human_eval']:
            eligibility_function = {
                'func': check_single_worker_eligibility,
                'multiple': False,
            }
        else:
            eligibility_function = {
                'func': check_multiple_workers_eligibility,
                'multiple': True,
            }

        def assign_worker_roles(workers):
            if start_opt['human_eval']:
                for worker in workers:
                    worker.id = worker_roles[worker.worker_id]
            else:
                for index, worker in enumerate(workers):
                    worker.id = mturk_agent_ids[index % len(mturk_agent_ids)]

        def run_conversation(mturk_manager, opt, workers):
            conv_idx = mturk_manager.conversation_index
            world = WizardEval(
                opt=start_opt,
                agents=workers,
                range_turn=[int(s)
                            for s in start_opt['range_turn'].split(',')],
                max_turn=start_opt['max_turns'],
                max_resp_time=start_opt['max_resp_time'],
                model_agent_opt=shared_bot_params,
                world_tag='conversation t_{}'.format(conv_idx),
                agent_timeout_shutdown=opt['ag_shutdown_time'],
            )
            world.reset_random()
            while not world.episode_done():
                world.parley()
            world.save_data()

            world.shutdown()
            gc.collect()

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

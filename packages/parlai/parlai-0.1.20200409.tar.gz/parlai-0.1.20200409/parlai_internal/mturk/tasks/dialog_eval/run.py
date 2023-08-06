#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from parlai.core.params import ParlaiParser
from parlai.core.agents import create_agent
from parlai.mturk.core.mturk_manager import MTurkManager
from worlds import DialogEvalWorld, DialogEvalHumanHumanWorld, CHAT_ENDED_MSG
from task_config import task_config

from parlai.core.worlds import validate

import os
import random
import time
import logging
import sys
import copy
import json


FRA_USA_QUALIF = {
    'QualificationTypeId': '00000000000000000071',
    'Comparator': 'In',
    'LocaleValues': [{'Country': 'FR'}, {'Country': 'US'}],
    'RequiredToPreview': True}

USA_QUALIF = {
    'QualificationTypeId': '00000000000000000071',
    'Comparator': 'In',
    'LocaleValues': [{'Country': 'US'}],
    'RequiredToPreview': True}

MASTER_QUALIF = {
    'QualificationTypeId': '2F1QJWKUDD8XADTFD2Q0G6UTO95ALH',
    'Comparator': 'Exists',
    'RequiredToPreview': True
}

MASTER_QUALIF_SDBOX = {
    'QualificationTypeId': '2ARFPLSP75KLA8M8DH1HTEQVJT3SY6',
    'Comparator': 'Exists',
    'RequiredToPreview': True
}

SEQSEQ_CONVAI_OPT = {
    'model_name': 'convai_s2s',
    'model': 'seq2seq',
    'model_file': 'models:convai2/seq2seq/convai2_self_seq2seq_model',
    'dict_file': 'models:convai2/seq2seq/convai2_self_seq2seq_model.dict'
}


def get_logger(opt):

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter(
        '%(asctime)s: [ %(message)s ]', '%m/%d/%Y %I:%M:%S %p')
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(console)
    if 'plog_file' in opt:
        logfile = logging.FileHandler(opt['plog_file'], 'a')
        logfile.setFormatter(fmt)
        logger.addHandler(logfile)
    logger.info('COMMAND: %s' % ' '.join(sys.argv))
    logger.info('-' * 100)
    logger.info('CONFIG:\n%s' % json.dumps(opt, indent=4, sort_keys=True))

    return logger


def make_transformer_opts(config_path, init_opt):
    with open(config_path) as fi:
        models_config = json.load(fi)

    opts = list()
    for model_config in models_config:
        model = model_config['model_name']
        for ranker in model_config['rankers']:
            for cands in model_config['candidates']:
                newopt = copy.deepcopy(init_opt)
                newopt.update({
                    'model_name': model,
                    'model':
                        'parlai_internal.agents.transformer.transformer:TransformerAgent',
                    'model_file':
                        f'/private/home/matu/zoo/{model}/model',
                    'fixed_candidates':
                        f'/private/home/matu/zoo/candidates/{cands}',
                    'fixed_candidates_enc':
                        f'/private/home/matu/zoo/{model}/{cands}.bin',
                    'ranker': ranker
                })
                opts.append(newopt)
    return opts


def block_workers(mturk_manager):
    with open('/private/home/matu/repos/ParlAI/parlai_internal/mturk/tasks/dialog_eval/bad_turkers.txt') as fi:
        bad_turkers = [name.strip() for name in fi]
    for bad_turker in bad_turkers:
        mturk_manager.soft_block_worker(bad_turker)


def main():
    """This task consists of an MTurk agent evaluating a chit-chat model. They
    are asked to chat to the model adopting a specific persona. After their
    conversation, they are asked to evaluate their partner on several metrics.
    """
    argparser = ParlaiParser(False, add_model_args=True)
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()
    argparser.add_argument(
        '--max-resp-time', default=180,
        type=int, help='time limit for entering a dialog message')
    argparser.add_argument(
        '--max-eval-time', type=int,
        default=540, help='time limit for turker to perform the evaluation')
    argparser.add_argument(
        '--ag-shutdown-time', default=180,
        type=int, help='time limit for entering a dialog message')
    argparser.add_argument(
        '-rt', '--range-turn', default='9,12',
        help='sample range of number of turns')
    argparser.add_argument(
        '--auto-approve-delay', type=int, default=3600 * 24 * 5,
        help='how long to wait for auto approval')
    argparser.add_argument('--masters', action='store_true')
    argparser.add_argument('--nb-conv-per-model', type=int, default=30)
    argparser.add_argument('--models-config', type=str, required=True)

    init_opt = argparser.parse_args()
    init_opt.update({
        'no_cuda': True,
        'override': {'interactive_mode': True, 'no_cuda': True},
        'interactive_mode': True,
        'task': os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    })

    if 'data_path' not in init_opt:
        init_opt['data_path'] = os.getcwd() + '/data/' + init_opt['task']

    opts = make_transformer_opts(init_opt['models_config'], init_opt)
    s2s_opts = copy.deepcopy(init_opt)
    s2s_opts.update(SEQSEQ_CONVAI_OPT)
    opts.append(s2s_opts)

    now = time.strftime('%m%d_%H%M%S')
    nbhits = init_opt['nb_conv_per_model'] * (1 + len(opts))
    init_opt.update({
        'num_conversations': nbhits,
        'plog_file': f'data/logs/python_{now}.log'
    })

    get_logger(init_opt)
    logging.info(f'Will launch {nbhits} hits')
    logging.info(f'For a total of {nbhits * init_opt["reward"]:.2f}$')

    init_opt.update(task_config)

    bots = list()
    for opt in opts:
        bot = create_agent(opt)
        shared_bot_params = bot.share()
        bots.append((bot, shared_bot_params))

    mturk_agent_ids = ['PERSON_1', 'PERSON_2']
    mturk_manager = MTurkManager(opt=init_opt, mturk_agent_ids=mturk_agent_ids)
    directory_path = os.path.dirname(os.path.abspath(__file__))

    logging.info('Setting up server')
    mturk_manager.setup_server(task_directory_path=directory_path)

    try:
        mturk_manager.start_new_run()
        agent_qualifications = []
        if init_opt['masters']:
            if init_opt['is_sandbox']:
                agent_qualifications.append(MASTER_QUALIF_SDBOX)
            else:
                agent_qualifications.append(MASTER_QUALIF)
        mturk_manager.create_hits(qualifications=agent_qualifications)
        mturk_manager.create_qualification(
            init_opt['block_qualification'],
            f'Qualification for dialogeval run started on {now}',
            init_opt['is_sandbox']
        )

        if not init_opt['is_sandbox']:
            block_workers(mturk_manager)

        mturk_manager.ready_to_accept_workers()

        def assign_worker_roles(workers):
            for worker in workers:
                worker.id = None

            logging.info(f'Assigning {len(workers)} worker roles')
            if random.random() < 1 / (1 + len(opts)) and workers[0].worker_id != workers[1].worker_id:
                logging.info(f'Human-human task, {mturk_agent_ids}')
                mids = list(mturk_agent_ids)
                for index, worker in enumerate(workers):
                    worker.id = mids[index % len(mids)]
            else:
                logging.info(f'Human-bot task, {mturk_agent_ids[0]}')
                workers[0].id = random.choice(mturk_agent_ids)  # not always P1

        def run_conversation(mturk_manager, opt, workers):

            logging.info(f'{len(workers)}')

            if len(workers) > 1:
                agents = [workers[0], workers[1]]
                conv_idx = mturk_manager.conversation_index

                logging.info('Running Human-Human dialog')

                world = DialogEvalHumanHumanWorld(
                    opt=opt,
                    agents=agents,
                    range_turn=[int(s) for s in opt['range_turn'].split(',')],
                    max_resp_time=opt['max_resp_time'],
                    max_eval_time=opt['max_eval_time'],
                    world_tag='conversation t_{}'.format(conv_idx),
                    agent_timeout_shutdown=opt['ag_shutdown_time'],
                )

            else:

                agents = workers[0]
                conv_idx = mturk_manager.conversation_index

                opt, (bot, shared_bot_params) = random.choice(list(zip(opts, bots)))

                logging.info('Running conversation with %s, ranking with %s' % (
                    opt['model_name'], opt.get('ranker', 'no ranker')))

                world = DialogEvalWorld(
                    opt=opt,
                    agents=[agents],
                    range_turn=[int(s) for s in opt['range_turn'].split(',')],
                    max_resp_time=opt['max_resp_time'],
                    max_eval_time=opt['max_eval_time'],
                    model_agent_opt=shared_bot_params,
                    world_tag='conversation t_{}'.format(conv_idx),
                    agent_timeout_shutdown=opt['ag_shutdown_time'],
                )

            world.reset_random()
            while not world.episode_done():
                world.parley()

            logging.info('Entering eval mode')
            mturk_manager.mark_workers_done([ag for ag in world.agents if hasattr(ag, 'state')])
            world.evaluate()

            logging.info('Saving data')
            world.save_data()

            world.shutdown()

        mturk_manager.start_task(
            eligibility_function=lambda _: True,
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

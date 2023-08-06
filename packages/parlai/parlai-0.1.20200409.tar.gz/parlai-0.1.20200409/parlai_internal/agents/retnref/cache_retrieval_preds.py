#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
Cache's retrieval model predictions for retrieve and refine.
"""

from parlai.core.params import ParlaiParser
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from parlai.utils.misc import msg_to_str
from parlai.utils.world_logging import WorldLogger

import os
import json
import random
from tqdm import tqdm


def setup_args(parser=None):
    """
    Set up args for retrieval model prediction caching.
    """
    if parser is None:
        parser = ParlaiParser(True, True, 'Cache retrieval model predctions')
    # Get command line arguments
    parser.add_argument('-ne', '--num-examples', type=int, default=-1)
    WorldLogger.add_cmdline_args(parser)
    parser.set_defaults(batchsize=32)
    parser.set_params(
        eval_candidates='fixed',
        ignore_bad_candidates=True,
        encode_candidate_vecs=True,
        interactive_mode=True,
        use_reply='label',
        log_keep_fields='text,episode_done,id,labels,eval_labels',
    )
    return parser


def write_logs(opt, task, logs):
    # TODO: write to parlai format?
    datatype = opt['datatype'].split(':')[0]
    save_dir = os.path.join(opt['datapath'], f'{task}_retrieval_cached')
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f'{datatype}.txt')
    with open(save_path, 'w') as f:
        for ep in logs:
            for act_pair in ep:
                act_w = act_pair[0]
                if 'eval_labels' in act_w:
                    # re-write eval_labels to labels
                    act_w['labels'] = act_w['eval_labels']
                    del act_w['eval_labels']
                act_w['retriever_reply'] = act_pair[1].get('text', '')
                str_w = msg_to_str(act_w)
                f.write(str_w + '\n')

    print(f'\n\t[ Logs successfully written to file: {save_path} ]')


def _eval_single_world(opt, agent, task):
    print(
        '[ Evaluating task {} using datatype {}. ] '.format(
            task, opt.get('datatype', 'N/A')
        )
    )
    # set up world logger
    world_logger = WorldLogger(opt)

    task_opt = opt.copy()  # copy opt since we're editing the task
    task_opt['task'] = task
    world = create_task(task_opt, agent)  # create worlds for tasks

    # max number of examples to evaluate
    max_cnt = opt['num_examples'] if opt['num_examples'] > 0 else float('inf')
    num_exs = world.num_examples()
    total_exs = min(max_cnt, num_exs)

    cnt = 0

    progress_bar = tqdm(
        total=total_exs, unit='ex', unit_scale=True, desc='Caching retrieval responses'
    )
    while not world.epoch_done() and cnt < max_cnt:
        cnt += opt.get('batchsize', 1)
        world.parley()
        world_logger.log(world)
        progress_bar.update(opt['batchsize'])

    world.reset()

    # dump acts to file to use fromfile format
    world_logger.reset()
    write_logs(opt, task, world_logger._logs)


def cache_retrieval_model_replies(opt, print_parser=None):
    """
    Caches retrieval model replies on a specific dataset.
    """
    random.seed(42)

    # load model
    agent = create_agent(opt, requireModelExists=True)

    datatypes = ['train:evalmode', 'valid', 'test']
    tasks = opt['task'].split(',')
    for task in tasks:
        for datatype in datatypes:
            opt['datatype'] = datatype
            _eval_single_world(opt, agent, task)

    print(
        '[ Finished evaluating tasks {} using datatype {} ]'.format(
            tasks, opt.get('datatype', 'N/A')
        )
    )


if __name__ == '__main__':
    parser = setup_args()
    cache_retrieval_model_replies(parser.parse_args(print_args=False))

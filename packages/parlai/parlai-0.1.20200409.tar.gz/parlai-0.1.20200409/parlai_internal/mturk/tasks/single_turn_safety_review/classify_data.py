#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Script for classifying data from a fixed text file.
"""
from parlai.core.params import ParlaiParser
from parlai.core.agents import create_agent
from parlai.utils.misc import round_sigfigs

import datetime
import random
import os


def setup_args(parser=None):
    if parser is None:
        parser = ParlaiParser(True, True, 'Interactive chat with a model')
    parser.add_argument('-d', '--display-examples', type='bool', default=False)
    parser.add_argument('--display-prettify', type='bool', default=False,
                        help='Set to use a prettytable when displaying '
                             'examples with text candidates')
    parser.add_argument('--display-ignore-fields', type=str,
                        default='label_candidates,text_candidates',
                        help='Do not display these fields')
    parser.add_argument('--fixed-text-file', type=str,
                        help='text file to classify')
    parser.add_argument('--write', type='bool', default=True,
                        help='sort output by score')
    parser.add_argument('--sort', type='bool', default=True)
    parser.set_params(
        print_scores=True
    )
    return parser


def classify(opt, print_parser, lines=None):
    if lines is None and opt['fixed_text_file'] is None:
        raise RuntimeError('Need to provide lines or text file to classify.')

    if lines is None:
        with open(opt['fixed_text_file'], 'r') as f:
            lines = f.readlines()

    return classify_lines(opt, lines, print_parser)


def classify_lines(opt, lines, print_parser=None):
    if print_parser is not None:
        if print_parser is True and isinstance(opt, ParlaiParser):
            print_parser = opt
        elif print_parser is False:
            print_parser = None
    if isinstance(opt, ParlaiParser):
        print('[ Deprecated Warning: interactive should be passed opt not Parser ]')
        opt = opt.parse_args()

    to_write = opt['write']
    to_sort = opt['sort']

    # Create model
    agent = create_agent(opt, requireModelExists=True)

    if print_parser:
        # Show arguments after loading model
        print_parser.opt = agent.opt
        print_parser.print_args()

    line_act = {
        'episode_done': True
    }

    sorted_list = []
    label_counts = {}

    for idx, line in enumerate(lines):
        if '__name__' in line:
            continue
        line = line.replace('\n', '')
        line_act = {
            'text': line,
            'episode_done': True
        }
        agent.observe(line_act)
        act = agent.act()
        pred, score = act['text'].split('\n')
        pred = pred.split(': ')[1]
        if pred in label_counts:
            label_counts[pred] += 1
        else:
            label_counts[pred] = 0

        score = float(score.split(': ')[1])
        if to_sort:
            sorted_list.append((line, pred, score))
        else:
            line_to_write = '{}. {}: {} with probability {}'.format(
                idx + 1, line, pred, score)
            print(line_to_write)

    new_list = sorted(sorted_list, key=lambda x: x[1], reverse=True)
    if to_write:
        now = datetime.datetime.now()
        suffix = '_classified_{}.txt'.format(now.strftime('%m%d'))
        file_to_write = os.path.splitext(opt['fixed_text_file'])[0] + suffix
        print('[ Writing to file {} ...]'.format(file_to_write))
        with open(file_to_write, 'w') as f:
            for tup in new_list:
                line_to_write = '{}: {} with probability {}'.format(
                    tup[0], tup[1], tup[2])
                print(line_to_write)
                f.write(line_to_write + '\n')
    elif to_sort:
        for tup in new_list:
            line_to_write = '{}: {} with probability {}'.format(
                tup[0], tup[1], tup[2])
            print(line_to_write)

    print('LABEL COUNTS: ')
    total = sum(label_counts.values())
    for k, v in label_counts.items():
        print('{}: {} ({}%)'.format(k, v, round_sigfigs(v / total, 2)))


if __name__ == '__main__':
    random.seed(42)
    parser = setup_args()
    classify(parser.parse_args(print_args=False), print_parser=parser)

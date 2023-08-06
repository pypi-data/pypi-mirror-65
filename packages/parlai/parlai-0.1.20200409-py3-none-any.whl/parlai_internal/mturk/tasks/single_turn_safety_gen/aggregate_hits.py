#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from parlai_internal.mturk.tasks.single_turn_safety_review.classify_data import (
    setup_args,
    classify
)

from worlds import WorldAssignment

import glob
import os
import json
import numpy as np

from parlai.core.params import ParlaiParser
from parlai.utils.misc import round_sigfigs
ParlaiParser()  # instantiate to set PARLAI_HOME environment var

"""Script for collecting data from wizard MTurk task logs"""

# ARGS
ROOT = os.path.join(
    os.environ['PARLAI_HOME'], 'parlai', 'mturk', 'core', 'run_data', 'live',
    'single_turn_safety_gen*', 't*', 'custom', 'data.json'
)


def avg(lst):
    return np.mean(lst)


def list_outliers(lst, num_stds=2):
    mean = np.mean(lst)
    std = np.std(lst)
    filtered_lst = [x for x in lst if
                    (mean - num_stds * std < x <  mean + num_stds * std)]
    outliers = [x for x in lst if x not in filtered_lst]
    return filtered_lst, outliers


def get_world(assignment):
    return WorldAssignment(assignment).name


def print_results(data_glob, print_data=True):
    total_answers = []
    unformatted_answers = []
    completion_times = []

    for file in glob.glob(data_glob):
        with open(file, 'rb') as f:
            log = json.load(f)
        world_type = get_world(log['task_world_assignment'])
        for i, ans in enumerate(log['answers']):
            if world_type == 'TOPIC':
                topic = log['topics'][i]
                total_answers.append('{}\t({}: {})\t{}'.format(
                    ans, world_type, topic, log['worker_id']))
            else:
                total_answers.append('{}\t({})\t{}'.format(
                    ans, world_type, log['worker_id']))

            unformatted_answers.append(ans)

        if log['completed']:
            completion_times.append(log['completion_time'])

    if print_data:
        for i, x in enumerate(total_answers):
            print('{}. {}'.format(i + 1, x))

    print('*' * 50)
    print('Average completion time: {} seconds'.format(
        round_sigfigs(avg(completion_times))))
    filtered, outliers = list_outliers(completion_times, num_stds=1)
    print('Outliers: {}'.format(outliers))
    new_avg = round_sigfigs(avg(filtered))
    print('Average after removing outliers: {} seconds'.format(new_avg))

    print('--> Should pay ${} per HIT'.format(
        round_sigfigs(new_avg * 15 / 3600, 2)))

    return total_answers, completion_times, unformatted_answers


def format_teacher_file(lines, file_to_write):
    print('[ Writing to file {} ...]'.format(file_to_write))
    with open(file_to_write, 'w') as f:
        for line in lines:
            f.write(line + '\n')


if __name__ == '__main__':
    _, _, answers = print_results(data_glob=ROOT)
    file_to_write = os.path.join(os.environ['PARLAI_HOME'], 'data', 'safety',
                                 'boring_data', 'boring_data.txt')
    format_teacher_file(answers, file_to_write)

    TO_CLASSIFY = False
    if TO_CLASSIFY:
        parser = setup_args()
        parser.set_defaults(
            write=False,
            model='bert_classifier',
            model_file='/checkpoint/edinan/20190312/safety_bert_sweep/balance-data=False_lr=5e-05_bs=20_lr-scheduler-patience=1_validation-metric=classnotokf1/model',
            threshold=0.48,
            print_scores=True,
            sort=False,
        )
        classify(parser.parse_args(print_args=False), print_parser=parser,
                 lines=answers)

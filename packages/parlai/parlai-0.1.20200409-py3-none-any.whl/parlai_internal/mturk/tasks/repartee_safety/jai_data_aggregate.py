#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
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
    os.environ['PARLAI_HOME'], 'data', 'Mturk_Runs_Reset', 'first_round',
    'repartee_safety*', 't*', 'custom', 'data.json'
)

NOT_OK = ['__not_ok__', '__notok__']
OK = '__ok__'

# BAD_WORKERS = ['A1BLEHZZ2BAQOU', 'A2P9SWXY9QWY3G', 'A3COFNH5MFLZ98',
#                'A35BP3LBFXA7TW', 'A3BD596A2NNN72', 'A1FQ58IUXW55VD',
#                'A3LD5PBYZR0SYE', 'AMOLAWACZ8KFR', 'ABP7DOJP9DU2H',
#                'A3FY43PD1ORVZF', 'A9BG6V33ZTVZT', 'A1ATL3G98SFW4V',
#                'AC8AP945KVJW5']


def avg(lst):
    return round_sigfigs(np.mean(lst), 4)


def pct(num, string=True):
    num = 100 * round_sigfigs(num, 4)
    if not string:
        return num
    return ('{}%'.format(num))


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
    turkers = []

    both_notok = 0
    adv_notok = 0
    orig_notok = 0
    both_ok = 0
    scores = []
    tries_per_correct = []

    for file in glob.glob(data_glob):
        with open(file, 'rb') as f:
            log = json.load(f)
        world_type = get_world(log['task_world_assignment'])
        if log['completed']:
            scores.append(log['score'])
            turkers.append(log['worker_id'])
            for i, ans in enumerate(log['answers']):
                if ans['completed']:
                    correct_key = '2' if '2' in ans else '1'
                    tries_per_correct.append(int(correct_key))
                    sentence = ans[correct_key]['sentence']
                    if world_type == 'TOPIC':
                        topic = ans['topic']
                        total_answers.append('{}\t({}: {})\t{}\tHIT ID: {}'.format(
                            sentence, world_type, topic, log['worker_id'],
                            log['hit_id']))
                    else:
                        total_answers.append('{}\t({})\t{}\tHIT ID: {}'.format(
                            sentence, world_type, log['worker_id'],
                            log['hit_id']))

                    unformatted_answers.append(sentence)

                for key in ['1', '2']:
                    if key in ans:
                        orig = ans[key]['bert_classification']
                        if orig in NOT_OK:
                            orig_notok += 1
                        else:
                            both_ok += 1

            completion_times.append(log['completion_time'])

    if print_data:
        for i, x in enumerate(total_answers):
            print('{}. {}'.format(i + 1, x))

    total = both_notok + adv_notok + orig_notok + both_ok
    print('\n\nClassifier Stats')
    print('^^^^^^^^^^^^^^^^')
    print('TOTAL ATTEMPTS: {}'.format(total))
    print('Both NOT OK: {}'.format(pct(both_notok / total)))
    print('Orig NOT OK: {}'.format(pct(orig_notok / total)))
    print('Adv NOT OK: {}'.format(pct(adv_notok / total)))
    print('Both OK: {}'.format(pct(both_ok / total)))
    print('---')
    print('Avg score: {}'.format(avg(scores)))
    print('Avg tries submitted per round: {}'.format(
        round_sigfigs(total / len(scores), 4)))
    print('Avg attempts per correct answer: {}'.format(avg(tries_per_correct)))
    print('Num unique turkers: {}'.format(len(list(set(turkers)))))

    print('*' * 50)
    print('Average completion time: {} seconds'.format(avg(completion_times)))
    filtered, outliers = list_outliers(completion_times, num_stds=2)
    print('Outliers: {}'.format(outliers))
    new_avg = avg(filtered)
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
    # file_to_write = os.path.join(os.environ['PARLAI_HOME'], 'data', 'safety',
    #                              'adversarial_data',
    #                              'adversarial_data_{}.txt'.format(CURRENT_ROUND))
    # format_teacher_file(answers, file_to_write)

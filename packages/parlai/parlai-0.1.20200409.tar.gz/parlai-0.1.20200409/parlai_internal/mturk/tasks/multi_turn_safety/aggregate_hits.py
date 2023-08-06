#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
import glob
import os
import json
import numpy as np
import random

from parlai.core.params import ParlaiParser
from parlai.utils.misc import round_sigfigs
ParlaiParser()  # instantiate to set PARLAI_HOME environment var

"""Script for collecting data from wizard MTurk task logs"""

# ARGS
ROOT = os.path.join(
    os.environ['PARLAI_HOME'], 'parlai', 'mturk', 'run_data', 'live',
    'multi_turn_safety*', 't*', 'custom', 'data.json'
)
MIN_DATE = '2019-04-29 00:00'
NOT_OK = ['NOT OK']
OK = 'OK'

BAD_WORKERS = []
BAD_WORKERS = ['AIU30D5BNNCWH', 'A2541C8MY0BYV3', 'A2UXVNIR273792',
               'A2UXVNIR273792', 'A4B3RUUWIC5Q3', 'A3JPYCC2U4D9CZ',
               'A3BXT78QXFC6F3', 'A17WS5TP6OPH7R',
               'A1QLOVE2J07QO5', 'A2LT9OPQXI1T4S',
               'A23KAJRDVCVGOE', 'A38OPVI04AH4JG', 'A2ZZW6KME1FUDU',
               'A2JZK4I34PXZUL', 'A38OPVI04AH4JG', 'A2EPBSY0VPI38S', 'A2A4UAFZ5LW71K',
               'AKB82TCYUECWD', 'A1160COTUR26JZ', 'A2KK5BSM1BR0WR', 'AQZNLCILWE23S',
               'AGELSD4XJUHCK', 'A19DZAFFZEU6GN', 'A38OPVI04AH4JG', 'A1V10J2JBT9QHR',
               'A2UO3QJZNC2VOE', 'A2TSEQ0K6MLVK3']

ROUND = 1

TO_WRITE = ('/private/home/edinan/ParlAI/data/safety/multiturn_data/'
            'multiturn_data_new.json')


def avg(lst):
    return np.mean(lst)


def pct(num, string=True):
    num = 100 * round_sigfigs(num, 4)
    if not string:
        return num
    return ('{}%'.format(num))


def list_outliers(lst, num_stds=2):
    mean = np.mean(lst)
    std = np.std(lst)
    filtered_lst = [x for x in lst if
                    (mean - num_stds * std < x < mean + num_stds * std)]
    outliers = [x for x in lst if x not in filtered_lst]
    return filtered_lst, outliers


def print_results(data_glob, print_data=True):
    completion_times = []
    total_answers = []
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
        if (log['date_completed'] > MIN_DATE and
                log['worker_id'] not in BAD_WORKERS):
            turkers.append(log['worker_id'])
            for i, ans in enumerate(log['answers']):
                if ans['completed']:
                    convo = ans['conversation']
                    turk_answer = ans['tries'][-1]
                    date_completed = log['date_completed']
                    worker_id = log['worker_id']
                    hit_id = log['hit_id']
                    total_answers.append((
                        convo,
                        turk_answer,
                        date_completed,
                        worker_id,
                        hit_id
                    ))
                    tries_per_correct.append(len(ans['tries']))
                    for i in range(len(ans['tries'])):
                        orig = ans['bert_classification'][i]
                        adv_1 = ans['adv_classification'][i]
                        if orig in NOT_OK and adv_1 in NOT_OK:
                            both_notok += 1
                        elif adv_1 in NOT_OK:
                            adv_notok += 1
                        elif orig in NOT_OK:
                            orig_notok += 1
                        else:
                            both_ok += 1

            if log['completed']:
                scores.append(log['score'])

            if log['completed']:
                completion_times.append(log['completion_time'])

    if print_data:
        for i, x in enumerate(total_answers):
            convo_format = '\n'.join(x[0])
            print('{}. Conversation:\n{}\nTURKER REPLY: {}\n\nWorker '
                  'ID:{}\nHIT ID:{}\nDate completed: {}\n~~~\n'.format(
                    i + 1, convo_format, x[1], x[3], x[4], x[2]))

    print('*' * 50)
    print('Average completion time: {} seconds'.format(
        round_sigfigs(avg(completion_times))))
    filtered, outliers = list_outliers(completion_times, num_stds=1)
    print('Outliers: {}'.format(outliers))
    new_avg = round_sigfigs(avg(filtered))
    print('Average after removing outliers: {} seconds'.format(new_avg))

    total = both_notok + adv_notok + orig_notok + both_ok
    print('\n\nClassifier Stats')
    print('^^^^^^^^^^^^^^^^')
    print('TOTAL ATTEMPTS: {}'.format(total))
    print('Both NOT OK: {}'.format(pct(both_notok / total)))
    print('Orig NOT OK: {}'.format(pct(orig_notok / total)))
    print('Adv NOT OK: {}'.format(pct(adv_notok / total)))
    print('Both OK: {}'.format(pct(both_ok / total)))
    print('-----------------')
    print('Avg score: {}'.format(avg(scores)))
    print('Avg tries submitted per round: {}'.format(
        round_sigfigs(total / len(scores), 4)))
    print('Avg attempts per correct answer: {}'.format(avg(tries_per_correct)))
    print('Num unique turkers: {}'.format(len(list(set(turkers)))))

    print('--> Should pay ${} per HIT'.format(
        round_sigfigs(new_avg * 15 / 3600, 2)))

    return total_answers, completion_times


def write_to_file(answers):
    print('[ Writing data to file {}... ]'.format(TO_WRITE))
    new_list = ['\n'.join(x[0]) + '\n' + x[1] for x in answers]
    random.shuffle(new_list)
    list_json = json.dumps(new_list)
    with open(TO_WRITE, 'w') as f:
        f.write(list_json)
    print('[ Successfully wrote to file {}. ]'.format(TO_WRITE))


if __name__ == '__main__':
    answers, _ = print_results(data_glob=ROOT)
    #write_to_file(answers)

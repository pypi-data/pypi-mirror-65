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

from parlai.core.params import ParlaiParser
ParlaiParser()  # instantiate to set PARLAI_HOME environment var

"""Script for collecting data from LIGHT persona review logs."""

# ARGS
ROOT = os.path.join(
    os.environ['PARLAI_HOME'],
    'parlai',
    'mturk',
    'run_data',
    'live'
)

STACK_ROOT = os.path.join(
    os.environ['PARLAI_HOME'],
    'data',
    'light_persona_review',
)


BAD_TURKERS = [
    'APQTHI7VUXG2E',
    'A2I67P6JIMUMZ2',
]


def get_average_completion_time(root, run_name):
    workers = []
    times = []
    num_incomplete = 0
    total = 0
    dir = os.path.join(root, run_name)
    for file in glob.glob('{}/t_*/custom/data.json'.format(dir)):
        with open(file, 'rb') as f:
            log = json.load(f)
        if log['completed']:
            times.append(log['completion_time'])
            workers.append(log['worker_id'])
        else:
            num_incomplete += 1
        total += 1

    print('Completion ratio: {}'.format(num_incomplete/total))
    print('Average completion time: {}'.format(
        sum(times) / len(times)
    ))
    print('STD of completion time: {}'.format(np.std(times)))

    for i, time in enumerate(times):
        if time < 20:
            print(time)
            print(workers[i])


def check_bad(worker_list):
    for worker in worker_list:
        if worker not in BAD_TURKERS:
            return False

    return True


def print_and_save_flagged(all_flagged):
    flag_file = os.path.join(STACK_ROOT, 'flagged.json')

    category_cnt = {}
    for j, flagged in enumerate(all_flagged):
        bad = check_bad(flagged[1])
        if not bad:
            print('{}.'.format(j + 1))
            print('Line: {}'.format(flagged[0]))
            print('---')
            for i in range(len(flagged[1])):
                worker = flagged[1][i]
                if worker not in BAD_TURKERS:
                    print('Worker: {}'.format(worker))
                    print('Rating: {}'.format(flagged[2][i]))
                    category = flagged[3][i]
                    print('Category: {}'.format(category))
                    category_cnt.setdefault(category, 0)
                    category_cnt[category] += 1
                    print('Reason: {}'.format(flagged[4][i]))
                    print('---')
            print('~'*40)

    print(category_cnt)
    with open(flag_file, 'w') as g:
        flags_data = json.dumps(all_flagged)
        g.write(flags_data)


def print_results(root, run_name, print_convos=True, version=0):
    get_average_completion_time(root, run_name)
    with open(os.path.join(STACK_ROOT,
                           'completed_stack_v{}.json'.format(version)), 'r') as f:
        stack = json.loads(f.read())
    with open(os.path.join(STACK_ROOT,
                           'flagged_list_v{}.json'.format(version)), 'r') as g:
        flags = json.loads(g.read())

    counter = 0
    flagged_cnt = 0
    sexist_cnt = 0
    all_flagged = []
    for key in stack.keys():
        curr_stack = stack[key]
        if curr_stack['workers'] == []:
            break
        else:
            for line in curr_stack['stack']:
                line_num = counter + 1
                print('{}.'.format(line_num))
                print('Line: {}'.format(line))
                print('Reviewed {} time(s)'.format(len(curr_stack['workers'])))
                print('Reviewed by: {}'.format(curr_stack['workers']))
                if str(line_num) in flags:
                    flagged_cnt += 1
                    print('FLAGGED {} time(s)'.format(len(flags[str(line_num)]['workers'])))
                    print('Flag ratings: {}'.format(flags[str(line_num)]['rating']))
                    categories = flags[str(line_num)]['categories']
                    if 'sexist' in categories:
                        sexist_cnt += 1
                    print('Flag categories: {}'.format(categories))
                    print('Flag reasons: {}'.format(flags[str(line_num)]['reasons']))
                    all_flagged.append((
                        line,
                        flags[str(line_num)]['workers'],
                        flags[str(line_num)]['rating'],
                        flags[str(line_num)]['categories'],
                        flags[str(line_num)]['reasons'],
                    ))
                counter += 1
                print('---------------------')

    flagged_pct = flagged_cnt / counter
    print('Flagged percent: {}'.format(flagged_pct))
    sexist_pct = sexist_cnt / counter
    print('Sexist percent: {}'.format(sexist_pct))

    print_and_save_flagged(all_flagged)


def remove_workers_from_stack(worker_list, version=0):
    """Use to remove a list of workers from the stack manually.
    """
    stack_path = os.path.join(STACK_ROOT,
                              'completed_stack_v{}.json'.format(version))
    flag_path = os.path.join(STACK_ROOT,
                             'flagged_list_v{}.json'.format(version))

    with open(stack_path, 'r') as f:
        stack = json.loads(f.read())
    for key in stack.keys():
        curr_stack = stack[key]
        if curr_stack['workers'] == []:
            break
        else:
            for worker in worker_list:
                if worker in curr_stack['workers']:
                    curr_stack['workers'].remove(worker)
    new_stack = json.dumps(stack)
    with open(stack_path, 'w') as g:
        g.write(new_stack)

    with open(flag_path, 'r') as g:
        flags = json.loads(g.read())
    to_remove = []
    for key in flags.keys():
        for worker in flags[key]['workers']:
            if worker in worker_list and len(flags[key]['workers']) == 1:
                to_remove.append(key)
    for key in to_remove:
        del flags[key]
    new_flags = json.dumps(flags)
    with open(flag_path, 'w') as g:
        g.write(new_flags)


def get_hit_ids_for_workers(worker_list, root, run_name):
    """
    Get HIT IDs for a list of workers for the purposes of sending a bonus.
    Searches through the most recent HITs first
    """
    comp_list = worker_list.copy()
    cnt = 0
    dir = os.path.join(root, run_name)
    hit_ids = {key: None for key in worker_list}
    for file in reversed(list(glob.glob('{}/t_*/custom/data.json'.format(dir)))):
        with open(file, 'rb') as f:
            log = json.load(f)
        if cnt == len(worker_list):
            break
        if log['completed'] and log.get('hit_id'):
            for worker in comp_list:
                if worker == log['worker_id']:
                    hit_ids[worker] = log['hit_id']
                    cnt += 1
                    comp_list.remove(worker)
                    break
    return hit_ids


def get_worker_counts(root, run_name):
    """
    Check for workers who have completed many HITs but flagged very few.
    """
    worker_dict = {}
    dir = os.path.join(root, run_name)
    for file in reversed(list(glob.glob('{}/t_*/custom/data.json'.format(dir)))):
        with open(file, 'rb') as f:
            log = json.load(f)
        if log['completed']:
            worker_dict.setdefault(log['worker_id'], {'flagged': 0, 'total': 0})
            worker_dict[log['worker_id']]['total'] += 1
            worker_dict[log['worker_id']]['flagged'] += len(log['flagged'])

    for k, v in worker_dict.items():
        if v['total'] > 20 and v['flagged'] / (v['total'] * 10) < 0.01:
            print('Worker: {}'.format(k))
            print(v)
            print('----------------------')


if __name__ == '__main__':
    run_name = 'light_persona_review_*'
    version = 0
    eval_scores = print_results(root=ROOT, run_name=run_name, version=version)
    #remove_workers_from_stack(BAD_TURKERS)
    #get_average_completion_time(ROOT, run_name)
    #get_worker_counts(ROOT, run_name)

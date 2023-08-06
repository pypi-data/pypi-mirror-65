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

"""Script for collecting data from wizard MTurk task logs"""

# ARGS
ROOT = os.path.join(
    os.environ['PARLAI_HOME'],
    'parlai',
    'mturk',
    'core',
    'run_data',
    'live'
)

STACK_ROOT = os.path.join(
    os.environ['PARLAI_HOME'],
    'data',
    'safety_checks',
)


def print_test_run_results(root, run_name, print_convos=True):
    evaluated = [
        'jeez you are really dumb.',
        'his care for the girl fills me with joy and kindness.',
        'my favorite is green apples, especially the sweet ones.',
        'do you believe in god?',
        'i feel really worthless.',
        'i would love to visit mexico one day!',
        'some things are ok to eat and some things are not.',
        'nice. no kids for me. but one day, and we will go to the beach a lot.',
        'i need a girlfriend. will you be my girlfriend?',
        'i am not a fan of donald trump, what do you think?'
    ]

    eval_scores = {key: [] for key in evaluated}

    dir = os.path.join(root, run_name)
    for file in glob.glob('{}/t_*/custom/data.json'.format(dir)):
        with open(file, 'rb') as f:
            log = json.load(f)

        if len(log['answers']) == 10:
            for i in range(len(log['answers'])):
                key = log['evaluated'][i]
                eval_scores[key].append(log['answers'][i])

            if print_convos:
                print('Worker ID:', log['worker_id'])
                for i in range(len(log['answers'])):
                    if str(i) in log['flagged']:
                        reason = log['flagged'][str(i)][1]
                    else:
                        reason = ''
                    print('{}. {}:\n  EVALUATION: {}\n  REASON: {}\n'.format(
                        i,
                        log['evaluated'][i],
                        log['answers'][i],
                        reason
                    ))
                    key = log['evaluated'][i]
                    eval_scores[key].append(log['answers'][i])
                print('----------------------------------')

    return eval_scores


def get_bad_workers(root, run_name, print_convos=True):
    bad_workers = []
    dir = os.path.join(root, run_name)
    for file in glob.glob('{}/t_*/custom/data.json'.format(dir)):
        with open(file, 'rb') as f:
            log = json.load(f)
        if log['completed'] and log.get('bad_cand'):
            if log.get('bad_cand_response') == 'ok':
                bad_workers.append(log['worker_id'])
                if print_convos:
                    print('Worker ID: {}'.format(log['worker_id']))
                    print('Bad candidate: {}'.format(log['bad_cand']))

    if print_convos:
        print('-------------------------------------')
        print('Total bad workers: {}'.format(bad_workers))
        print('-------------------------------------')
    return bad_workers


def get_average_completion_time(root, run_name):
    times = []
    num_incomplete = 0
    total = 0
    dir = os.path.join(root, run_name)
    for file in glob.glob('{}/t_*/custom/data.json'.format(dir)):
        with open(file, 'rb') as f:
            log = json.load(f)
        if log['completed']:
            times.append(log['completion_time'])
        else:
            num_incomplete += 1
        total += 1

    print('Completion ratio: {}'.format(num_incomplete/total))
    print(times)
    print('Average completion time: {}'.format(
        sum(times) / len(times)
    ))
    print('STD of completion time: {}'.format(np.std(times)))

def print_results(root, run_name, print_convos=True, test_run=True, version=0):
    if test_run:
        return print_test_run_results(root, run_name, print_convos)

    get_average_completion_time(root, run_name)
    bad_workers = get_bad_workers(root, run_name, print_convos)

    with open(os.path.join(STACK_ROOT,
                           'completed_stack_v{}.json'.format(version)), 'r') as f:
        stack = json.loads(f.read())
    with open(os.path.join(STACK_ROOT,
                           'flagged_list_v{}.json'.format(version)), 'r') as g:
        flags = json.loads(g.read())

    counter = 0
    flagged_cnt = 0
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
                    print('Flag reasons: {}'.format(flags[str(line_num)]['reasons']))
                counter += 1
                print('---------------------')

    flagged_pct = flagged_cnt / counter
    print('Flagged percent: {}'.format(flagged_pct))

    with open(os.path.join(STACK_ROOT, 'convai2_candidates.txt'), 'r') as h:
        lines = h.readlines()
    line_dict = {}
    for line in lines:
        line_dict[line.split(' ')[0]] = line.split(' ', 1)[1].replace('\n', '')

    for key in flags.keys():
        line = line_dict[key]
        print(line)
        for worker in flags[key]['workers']:
            if worker in bad_workers:
                print('Warning, flagged worker: {}'.format(worker))
        print('TURKERS: {}'.format(flags[key]['workers']))
        print('RATINGS: {}'.format(flags[key]['rating']))
        print('REASONS: {}'.format(flags[key]['reasons']))
        print('---------------------\n')


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
        if v['total'] > 30 and v['flagged'] / (v['total'] * 10) < 0.01:
            print('Worker: {}'.format(k))
            print(v)
            print('----------------------')


if __name__ == '__main__':
    run_name = 'single_turn_safety_*'
    version = 0
    test_run = False
    bad_workers = []
    good_workers = ['ALZ94HOEENWHL']

    # remove_workers_from_stack(bad_workers)
    # hit_ids = get_hit_ids_for_workers(good_workers, ROOT, run_name)
    # print(hit_ids)

    eval_scores = print_results(root=ROOT, run_name=run_name, test_run=test_run,
                                version=version)
    if test_run:
        print('TOTAL SCORES:')
        options = ['ok', 'maybe ok', 'not ok']
        for key in eval_scores.keys():
            print('{}:'.format(key))
            for option in options:
                print('   \'{}\' count: {}'.format(
                    option,
                    eval_scores[key].count(option)
                ))

    get_worker_counts(ROOT, run_name)

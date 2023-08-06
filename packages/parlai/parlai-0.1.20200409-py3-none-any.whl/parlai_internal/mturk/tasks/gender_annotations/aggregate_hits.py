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
ROOT = os.path.join(os.environ['PARLAI_HOME'], 'parlai', 'mturk', 'run_data', 'live')

STACK_ROOT = os.path.join(os.environ['PARLAI_HOME'], 'data', 'gender_annotations')

#BAD_TURKERS = ['A1NZFJHVJ9CNTO', 'A11M5KWP2835VO', 'AN9MVFWRCF2OP', 'A1ZTSCPETU3UJW', 'A2IM1Q2SMNUQKF', 'A2WOQCXW2NGLSS', 'A273B58CZCS643', 'A29BLVQALSAGAP', 'A3K0UDE2AQB7NO', 'A38IPIPA3T3G4', 'A3A8P4UR9A0DWQ', 'ATTWN63B3XF47', 'A25ZZOSL7MVU22', 'A3G90BWFBLJWWI']
BAD_TURKERS = ['ATTWN63B3XF47', 'A25ZZOSL7MVU22', 'A3G90BWFBLJWWI', 'A3A8P4UR9A0DWQ', 'A38IPIPA3T3G4', 'A2WOQCXW2NGLSS', 'A38IPIPA3T3G4', 'A38IPIPA3T3G4', 'A11M5KWP2835VO', 'A2IM1Q2SMNUQKF', 'A3F9CSBY2TWKYD', 'A36X979BHQ7Z33', 'A2E286WNSB7KPL', 'A3RYI5HXC2MJLN', 'AISTD1HQ435V6']


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

    print('Completion ratio: {}'.format(num_incomplete / total))
    print('Average completion time: {}'.format(sum(times) / len(times)))
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


def print_results(root, run_name, print_convos=True, version=0):
    get_average_completion_time(root, run_name)

    stacks = {}
    directory = os.path.join(root, run_name)
    for fle in reversed(list(glob.glob(f'{directory}/t_*/custom/data.json'))):
        with open(fle, 'rb') as f:
            log = json.load(f)
            if log['completed']:
                stack_idx = log['stack_idx']
                stacks.setdefault(stack_idx, [])
                stacks[stack_idx].append(log)

    agreement_rate = []
    nonagree_workers = {}
    sort_keys = sorted(stacks.keys())
    sorted_stack = {k: stacks[k] for k in sort_keys}
    for idx, logs in sorted_stack.items():
        workers = [log['worker_id'] for log in logs]
        not_good = [worker in BAD_TURKERS for worker in workers]
        bad = all(not_good)
        if not bad:
            print(f'{idx}')
            first_log = logs[0]
            for i in range(len(first_log['answers'])):
                answers = []
                for log in logs:
                    if log['worker_id'] not in BAD_TURKERS:
                        answer = log['answers'][i]
                        if answer == 'non-binary':
                            answer = 'neutral'
                        answers.append(answer)
                    else:
                        answers.append(None)
                not_none = [ans for ans in answers if ans is not None]
                agreement = True
                opposite = False
                if len(not_none) > 1:
                    if 'man' in not_none and 'woman' in not_none:
                        opposite = True
                    agreement = answers[0] == answers[1]
                    agreement_rate.append(agreement)
                    if opposite:
                        stack = '\n'.join(first_log['evaluated'][i])
                        print(f'PERSONA: \n{stack}')

                for j, ans in enumerate(answers):
                    if ans is not None and not agreement:
                        worker_id = logs[j]['worker_id']
                        if opposite:
                            print(f'Assessment {j}...')
                            print(f'\tGENDER: {ans}')
                            if ans != 'non-binary' and ans != 'neutral':
                                certainty = logs[j]['flagged'][str(i)][1]
                                print(f'\tASSESSMENT: {certainty}')
                            print(f'\tWORKER ID: {worker_id}')
                            print('--------------------------\n\n')
                        worker_id = logs[j]['worker_id']
                        nonagree_workers.setdefault(worker_id, 0)
                        nonagree_workers[worker_id] += 1

    total_agree = sum(x for x in agreement_rate if x)
    rate = round((total_agree / len(agreement_rate) * 100), 2)

    print(f'Overall agreement rate: {rate}')
    print('Non-agreeing workers:')
    for k, v in nonagree_workers.items():
        print(f'{k}: {v}')

    with open(
        os.path.join(
            STACK_ROOT,
            'completed_stack_v{}.json'.format(version)
        ),
        'r'
    ) as f:
        total_stack = json.loads(f.read())

    missing = 0
    missing_lst = []
    for idx, stack in total_stack.items():
        workers = stack['workers']
        if len(workers) < 2:
            missing += 2 - len(workers)
            missing_lst.append(idx)

    total = len(total_stack) * 2
    print(f'\n\nMissing HITS: {missing}')
    print(f'Total HITS: {total}')
    print(f'Missing indices: {missing_lst}')


def remove_workers_from_stack(worker_list, version=0):
    """Use to remove a list of workers from the stack manually.
    """
    stack_path = os.path.join(STACK_ROOT, 'completed_stack_v{}.json'.format(version))
    flag_path = os.path.join(STACK_ROOT, 'flagged_list_v{}.json'.format(version))

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
        print('Writing new stack...')
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
        print('Writing new flags...')
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
    run_name = 'gender_annotations_*'
    version = 0
    remove_workers_from_stack(BAD_TURKERS)
    eval_scores = print_results(root=ROOT, run_name=run_name, version=version)

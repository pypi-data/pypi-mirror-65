#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from worlds import WorldAssignment
from parlai.core.params import ParlaiParser
from parlai.mturk.core.mturk_manager import MTurkManager
from task_config import task_config

import glob
import os
import pickle
import json


# ARGS
ParlaiParser()  # instantiate to set PARLAI_HOME environment var
ROOT = os.path.join(
    os.environ['PARLAI_HOME'], 'parlai', 'mturk', 'run_data', 'live',
    'repartee_safety*', 't*', 'custom', 'data.json'
)
CURRENT_ROUND = 3
DEFAULT_REASON = 'Spam answer. Not following instructions.'


BAD_WORKERS = ['A1BLEHZZ2BAQOU', 'A2P9SWXY9QWY3G', 'A3COFNH5MFLZ98',
               'A35BP3LBFXA7TW', 'A3BD596A2NNN72', 'A1FQ58IUXW55VD',
               'A3LD5PBYZR0SYE', 'AMOLAWACZ8KFR', 'ABP7DOJP9DU2H',
               'A3FY43PD1ORVZF', 'A9BG6V33ZTVZT', 'A1ATL3G98SFW4V',
               'AC8AP945KVJW5']

REVERSE_REJECTIONS = ['A1DBE2OL84TBKB']


def get_world(assignment):
    return WorldAssignment(assignment).name


def reverse_rejections():
    argparser = ParlaiParser(False, False)
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()
    opt = argparser.parse_args()
    directory_path = os.path.dirname(os.path.abspath(__file__))
    opt['task'] = os.path.basename(directory_path)
    if 'data_path' not in opt:
        opt['data_path'] = os.getcwd() + '/data/' + opt['task']
    opt.update(task_config)

    mturk_agent_ids = ['MTURKER']

    mturk_manager = MTurkManager(
        opt=opt,
        mturk_agent_ids=mturk_agent_ids
    )

    mturk_manager.setup_server(task_directory_path=directory_path)

    def approve_work(hit_id):
        try:
            mturk_manager.approve_assignments_for_hit(hit_id, override_rejection=True)
            print('Successfully approved work!')
        except Exception as e:
            print(e)
            print('DID NOT APPROVE WORK')

    for file in glob.glob(ROOT):
        with open(file, 'rb') as f:
            log = json.load(f)

        worker_id = log['worker_id']
        hit_id = log['hit_id']

        if worker_id in REVERSE_REJECTIONS:
            approve_work(hit_id)


def reject_bad():
    argparser = ParlaiParser(False, False)
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()
    opt = argparser.parse_args()
    directory_path = os.path.dirname(os.path.abspath(__file__))
    opt['task'] = os.path.basename(directory_path)
    if 'data_path' not in opt:
        opt['data_path'] = os.getcwd() + '/data/' + opt['task']
    opt.update(task_config)

    mturk_agent_ids = ['MTURKER']

    mturk_manager = MTurkManager(
        opt=opt,
        mturk_agent_ids=mturk_agent_ids
    )

    mturk_manager.setup_server(task_directory_path=directory_path)

    def reject_work(hit_id, reason):
        try:
            assignments = mturk_manager.get_assignments_for_hit(hit_id)
            for assignment in assignments:
                assignment_id = assignment['AssignmentId']
                mturk_manager.reject_work(assignment_id, reason)
            print('Successfully rejected work!')
        except Exception as e:
            print('Assignment status:', assignment['AssignmentStatus'])
            print(e)
            print('DID NOT REJECT WORK')

    for file in glob.glob(ROOT):
        with open(file, 'rb') as f:
            log = json.load(f)

        worker_id = log['worker_id']
        hit_id = log['hit_id']

        if worker_id in BAD_WORKERS:
            reject_work(hit_id, DEFAULT_REASON)


def review_all():
    """Review work for your task
    """
    argparser = ParlaiParser(False, False)
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()
    opt = argparser.parse_args()
    directory_path = os.path.dirname(os.path.abspath(__file__))
    opt['task'] = os.path.basename(directory_path)
    if 'data_path' not in opt:
        opt['data_path'] = os.getcwd() + '/data/' + opt['task']
    opt.update(task_config)

    mturk_agent_ids = ['MTURKER']

    mturk_manager = MTurkManager(
        opt=opt,
        mturk_agent_ids=mturk_agent_ids
    )

    mturk_manager.setup_server(task_directory_path=directory_path)

    bad_workers = []
    good_workers = []

    def reject_work(hit_id, reason):
        try:
            assignments = mturk_manager.get_assignments_for_hit(hit_id)
            for assignment in assignments:
                assignment_id = assignment['AssignmentId']
                mturk_manager.reject_work(assignment_id, reason)
            print('Successfully rejected work.')
        except Exception as e:
            print('Assignment status:', assignment['AssignmentStatus'])
            print(e)
            print('DID NOT REJECT WORK')

    for file in glob.glob(ROOT):
        with open(file, 'rb') as f:
            log = json.load(f)

        worker_id = log['worker_id']
        hit_id = log['hit_id']

        if worker_id in good_workers:
            continue
        elif worker_id in bad_workers:
            reject_work(hit_id, DEFAULT_REASON)

        world_type = get_world(log['task_world_assignment'])
        if log['completed'] and log['round'] == CURRENT_ROUND:
            for i, ans in enumerate(log['answers']):
                if ans['completed']:
                    correct_key = '2' if '2' in ans else '1'
                    sentence = ans[correct_key]['sentence']
                    if world_type == 'TOPIC':
                        topic = ans['topic']
                        print('{}\t({}: {})\t{}'.format(
                              sentence, world_type, topic, log['worker_id']))
                    else:
                        print('{}\t({})\t{}'.format(
                              sentence, world_type, log['worker_id']))
            print('***********\n')

            reject = input(
                "Type Y if you would like to reject some of these hits.\n"
                "Type N otherwise. Type A to reject all hits by worker."
                "Type G to approve all hits by worker:\t"
            )

            if reject.upper() == 'Y':
                reason = input("Reason for rejection: (D for default):\t")
                if reason.upper() == "D":
                    reason = DEFAULT_REASON
                reject_work(hit_id, reason)
            elif reject.upper() == 'A':
                bad_workers.append(worker_id)
                reject_work(hit_id, DEFAULT_REASON)
            elif reject.upper() == 'G':
                good_workers.append(worker_id)
            elif reject.upper() == 'BREAK':
                break
            else:
                print("Will not reject any work. Onto next HIT.")

            print('*************\n')



if __name__ == '__main__':
    #reject_bad()
    reverse_rejections()

#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
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
    'multi_turn_safety*', 't*', 'custom', 'data.json'
)
DEFAULT_REASON = 'Spam answer. Not following instructions.'
MIN_DATE = '2019-05-12 00:00'

BAD_WORKERS = ['A4B3RUUWIC5Q3',]

REVIEW_SPECIFIC = ['A17WS5TP6OPH7R', 'A2S75O867RJG0I']

REVERSE_REJECTIONS = ['A30EI064NHQEQO', 'A29TQSAJPLXZU7', 'ANB3WGF84QUUB']


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

        if log['date_completed'] > MIN_DATE:
            for i, ans in enumerate(log['answers']):
                if ans['completed']:
                    convo = ans['conversation']
                    turk_answer = ans['tries'][-1]
                    date_completed = log['date_completed']
                    worker_id = log['worker_id']
                    hit_id = log['hit_id']
                    convo_format = '\n'.join(convo)
                    print('Conversation:\n{}\nTURKER REPLY: {}\n\nWorker '
                          'ID:{}\nHIT ID:{}\nDate completed: {}\n~~~\n'.format(
                          convo_format, turk_answer, worker_id, hit_id,
                          date_completed))

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


def review_specific():
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

        if worker_id in REVIEW_SPECIFIC:
            if log['date_completed'] > MIN_DATE:
                for i, ans in enumerate(log['answers']):
                    if ans['completed']:
                        convo = ans['conversation']
                        turk_answer = ans['tries'][-1]
                        date_completed = log['date_completed']
                        worker_id = log['worker_id']
                        hit_id = log['hit_id']
                        convo_format = '\n'.join(convo)
                        print('Conversation:\n{}\nTURKER REPLY: {}\n\nWorker '
                              'ID:{}\nHIT ID:{}\nDate completed: {}\n~~~\n'.format(
                              convo_format, turk_answer, worker_id, hit_id,
                              date_completed))

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
    #review_all()
    #reject_bad()
    #review_specific()
    reverse_rejections()

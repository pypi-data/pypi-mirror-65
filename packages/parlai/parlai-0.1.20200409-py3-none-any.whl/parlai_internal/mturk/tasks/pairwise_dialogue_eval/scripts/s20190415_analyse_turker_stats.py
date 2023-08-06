#!/usr/bin/env python3
import numpy as np
import pandas as pd

ORIGINAL_CSV = '/private/home/roller/abi/Batch_3462988_batch_results.csv'

df = pd.read_csv(ORIGINAL_CSV)
workers_to_num_hits = {}
# COLUMNS:
# Index(['HITId', 'HITTypeId', 'Title', 'Description', 'Keywords', 'Reward',
#        'CreationTime', 'MaxAssignments', 'RequesterAnnotation',
#        'AssignmentDurationInSeconds', 'AutoApprovalDelayInSeconds',
#        'Expiration', 'NumberOfSimilarHITs', 'LifetimeInSeconds',
#        'AssignmentId', 'WorkerId', 'AssignmentStatus', 'AcceptTime',
#        'SubmitTime', 'AutoApprovalTime', 'ApprovalTime', 'RejectionTime',
#        'RequesterFeedback', 'WorkTimeInSeconds', 'LifetimeApprovalRate',
#        'Last30DaysApprovalRate', 'Last7DaysApprovalRate', 'Input.html_A',
#        'Input.html_B', 'Input.id1', 'Input.id2', 'Input.lhs_id',
#        'Input.matchup', 'Input.model1', 'Input.model2', 'Input.rhs_id',
#        'Input.swapped', 'Answer.choice', 'Answer.reason', 'Approve', 'Reject'],

for index, row in df.iterrows():
    worker_id = row['WorkerId']
    qual = row['Input.matchup']
    hits_done = workers_to_num_hits.get(worker_id)
    if hits_done is None:
        hits_done = {}
        workers_to_num_hits[worker_id] = hits_done
    if qual == 'qual1':
        hits_done['qual1'] = hits_done.get('qual1', 0) + 1
        model = row['Input.model1'] if row['Answer.choice'] == 'optionA' else row['Input.model2']
        correct = model == 'human_eval'
        if not correct:
            hits_done['failed_qual'] = True
        if worker_id == 'A16QTKULP8HQ6G':
            print(correct)
    elif qual == 'qual2':
        hits_done['qual2'] = hits_done.get('qual2', 0) + 1
        correct = (((row['Input.id1'] == row['Input.lhs_id']) and row['Answer.choice'] == 'optionB') or
            ((row['Input.id1'] != row['Input.lhs_id']) and row['Answer.choice'] == 'optionA'))
        if not correct:
            hits_done['failed_qual'] = True
        if worker_id == 'A16QTKULP8HQ6G':
            print(correct)
    else:
        hits_done['regular'] = hits_done.get('regular', 0) + 1

qual_and_regular = set()
only_qual = set()
only_regular = set()
qual_and_regular_hits_qual = 0
qual_and_regular_hits_regular_failed = 0
qual_and_regular_hits_regular_good = 0
qual_and_regular_hits_qual_failed = []
qual_and_regular_hits_qual_good = []
workers_failed = 0
workers_passed = 0
only_qual_hits = 0
only_regular_hits = 0
hits_done_to_num_workers = {}

for worker_id in workers_to_num_hits:
    hits_done = workers_to_num_hits.get(worker_id)

    num_hits_done = hits_done.get('qual1', 0) + hits_done.get('qual2', 0) + hits_done.get('regular', 0)
    hits_done_to_num_workers[num_hits_done] = hits_done_to_num_workers.get(num_hits_done, 0) + 1
    if 'qual1' in hits_done or 'qual2' in hits_done:
        if 'regular' in hits_done:
            qual_and_regular.add(worker_id)
            qual_and_regular_hits_qual += hits_done.get('qual1', 0) + hits_done.get('qual2', 0)
            if hits_done.get('failed_qual', False):
                qual_and_regular_hits_regular_failed += hits_done.get('regular', 0)
                workers_failed += 1
                qual_and_regular_hits_qual_failed.append(hits_done.get('qual1', 0) + hits_done.get('qual2', 0))
            else:
                qual_and_regular_hits_regular_good += hits_done.get('regular', 0)
                workers_passed += 1
                qual_and_regular_hits_qual_good.append(hits_done.get('qual1', 0) + hits_done.get('qual2', 0))
        else:
            only_qual.add(worker_id)
            only_qual_hits += num_hits_done
    else:
        only_regular.add(worker_id)
        only_regular_hits += num_hits_done
    # print("worker_id: {}; qual1s: {}; qual2s: {}; other hits: {}\n".format(worker_id, hits_done.get('qual1', 0) , hits_done.get('qual2', 0), hits_done.get('regular', 0)))

print("BOTH QUAL AND REGULAR -- num workers: {}; hits total: qual - {} + regular - ({} failed qual, {} passed qual) \n".format(
    len(qual_and_regular), qual_and_regular_hits_qual, qual_and_regular_hits_regular_failed, qual_and_regular_hits_regular_good))
print("{} workers failed qual with {} tasks\n, {} workers passed qual with {} tasks \n".format(
    workers_failed, qual_and_regular_hits_qual_failed, workers_passed, qual_and_regular_hits_qual_good))

print("ONLY QUAL -- num workers: {}; hits total: {}\n".format(len(only_qual), only_qual_hits))
print("ONLY REGULAR -- num workers: {}; hits total: {}\n".format(len(only_regular), only_regular_hits))

for num in sorted(hits_done_to_num_workers.keys()):
    print('{} hits : {} workers'.format(num, hits_done_to_num_workers[num]))

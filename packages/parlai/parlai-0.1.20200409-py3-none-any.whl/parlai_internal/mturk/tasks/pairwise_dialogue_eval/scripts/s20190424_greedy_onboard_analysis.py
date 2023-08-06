#!/usr/bin/env python3
from parlai.mturk.core.mturk_data_handler import MTurkDataHandler
import numpy as np
import json

run_id = 'pairwise_dialogue_eval_1556129495'
db_logger = MTurkDataHandler()
all_hits_data = {}
all_pairings_data = {}
all_workers_data = {}
logfilename = '/private/home/margaretli/pairwise_dialogue_eval/20190424_pairwise_dialogue_eval_1556129495.txt'

logfile = open(logfilename, 'a')

hits = db_logger.get_pairings_for_run(run_id)
# query data for a specific task
for hit in hits:
    if hit['conversation_id'] is not None:
        try:
            full_data = db_logger.get_full_conversation_data(run_id, hit['conversation_id'], False)
        except:
            continue
        data = next(iter(full_data['worker_data'].values()))
        data['time_taken'] = hit['task_end'] - hit['task_start']
        complete = 'task_data' in data['response']
        pairing_id = data['task_data']['task_specs']['internal_id']
        if not pairing_id in all_pairings_data:
            pairing_data = {}
            all_pairings_data[pairing_id] = pairing_data
            pairing_data['matchup'] = data['task_data']['task_specs']['comparison_type']
            pairing_data['conversations'] = data['task_data']['conversations']
            pairing_data['evals'] = []
            pairing_data['incomplete'] = 0
        pairing_data = all_pairings_data[pairing_id]
        if complete:
            pairing_data['evals'].append(hit['conversation_id'])
        else:
            pairing_data['incomplete'] += 1
        worker_id = data['worker_id']
        if not worker_id in all_workers_data:
            worker_data = {}
            all_workers_data[worker_id] = worker_data
            worker_data['evals'] = []
            worker_data['incomplete'] = 0
        worker_data = all_workers_data[worker_id]
        if complete:
            worker_data['evals'].append(hit['conversation_id'])
            correct = ((
                data['response']['task_data']['speakerChoice'] == '1' and
                data['task_data']['task_specs']['conversation_order'] == [1, 0]
            ) or (
                data['response']['task_data']['speakerChoice'] == '2' and
                data['task_data']['task_specs']['conversation_order'] == [0, 1]
            ))
            data['correct'] = correct
        else:
            pairing_data['incomplete'] += 1
        all_hits_data[hit['conversation_id']] = data

logfile.write("STATS PER PAIRING\n")
for pairing in all_pairings_data:
    pairing_data = all_pairings_data[pairing]
    eval_ids = pairing_data['evals']
    pairing_data['time_taken'] = []
    correct_count = 0
    for eval_id in eval_ids:
        data = all_hits_data[eval_id]
        pairing_data['time_taken'].append(data['time_taken'])
        if data['correct']:
            correct_count += 1
    pairing_data['correct_count'] = correct_count

for pairing, pairing_data in sorted(all_pairings_data.items(), key=lambda x: (x[1]['correct_count']/len(x[1]['evals']))):
    logfile.write(str(pairing) + '\n')
    logfile.write(pairing_data['matchup']+ '\n')
    logfile.write(json.dumps(pairing_data['conversations'])+ '\n')
    logfile.write('{} / {} correct \n'.format(pairing_data['correct_count'], len(pairing_data['evals'])))
    logfile.write('{} incomplete \n'.format(pairing_data['incomplete']))
    logfile.write('{} Median time taken \n\n'.format(np.median(pairing_data['time_taken'])))
    logfile.write('\n')

logfile.write("STATS PER WORKER\n")
for worker in all_workers_data:
    worker_data = all_workers_data[worker]
    eval_ids = worker_data['evals']
    correct_count = 0
    worker_data['time_taken'] = []
    for eval_id in eval_ids:
        data = all_hits_data[eval_id]
        worker_data['time_taken'].append(data['time_taken'])
        if data['correct']:
            correct_count += 1

    worker_data['correct_count'] = correct_count

for worker, worker_data in sorted(all_workers_data.items(), key=lambda x: (len(x[1]['evals']))):
    logfile.write(worker+ '\n')
    logfile.write('{} / {} correct\n'.format(worker_data['correct_count'], len(worker_data['evals'])))
    logfile.write('{} incomplete\n'.format(worker_data['incomplete']))
    if len(worker_data['time_taken'])> 0:
        logfile.write('{} Median time taken \n'.format(np.median(worker_data['time_taken'])))
    logfile.write('\n')

logfile.close()

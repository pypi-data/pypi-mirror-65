#!/usr/bin/env python3
from parlai.mturk.core.mturk_data_handler import MTurkDataHandler
import numpy as np
import json

run_id = 'pairwise_dialogue_eval_1556568703'
db_logger = MTurkDataHandler()
all_hits_data = {}
all_pairings_data = {}
onboarding_pairings_data = {}
all_workers_data = {}

num_onboarding = 0
num_onboarding_successes = 0
num_desired = 0
time_taken_arr = []
logfilename = '/private/home/margaretli/pairwise_dialogue_eval/20190429_pairwise_dialogue_eval_1556568703.txt'

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
        time_taken = hit['task_end'] - hit['task_start']

        complete = 'task_data' in data['response'] and len(data['response']['task_data']) > 0
        worker_id = data['worker_id']
        if not worker_id in all_workers_data:
            worker_data = {}
            all_workers_data[worker_id] = worker_data
            worker_data['evals'] = []
            worker_data['time_taken'] = []
            worker_data['passed_onboarding'] = False
        worker_data = all_workers_data[worker_id]
        time_taken_arr.append(time_taken)
        worker_data['time_taken'].append(time_taken)
        if complete:
            worker_data['evals'].append(hit['conversation_id'])

        if data['task_data'][0]['task_specs'].get('is_onboarding', False):
            num_onboarding += 1
            correct_count = 0
            for i in range(len(data['task_data'])):
                correct = ((
                    data['response']['task_data'][i]['speakerChoice'] == '1' and
                    data['task_data'][i]['task_specs']['conversation_order'] == [1, 0]
                ) or (
                    data['response']['task_data'][i]['speakerChoice'] == '2' and
                    data['task_data'][i]['task_specs']['conversation_order'] == [0, 1]
                ))
                correct_count += 1 if correct else 0
                pairing_id = data['task_data'][i]['task_specs']['internal_id']
                # add pairing to dict
                if not pairing_id in onboarding_pairings_data:
                    pairing_data = {}
                    onboarding_pairings_data[pairing_id] = pairing_data
                    pairing_data['matchup'] = data['task_data'][i]['task_specs']['comparison_type']
                    pairing_data['conversations'] = data['task_data'][i]['conversations']
                    # pairing_data['evals'] = []
                    pairing_data['correct_count'] = 0
                    pairing_data['attempt_count'] = 0
                pairing_data = onboarding_pairings_data[pairing_id]
                pairing_data['correct_count'] += 1 if correct else 0
                pairing_data['attempt_count'] += 1
            if correct_count >= 4:
                worker_data['passed_onboarding'] = True
                num_onboarding_successes += 1

        else:
            num_desired += 1
            for i in range(len(data['task_data'])):
                pairing_id = data['task_data'][i]['task_specs']['internal_id']
                # add pairing to dict
                if not pairing_id in all_pairings_data:
                    pairing_data = {}
                    all_pairings_data[pairing_id] = pairing_data
                    pairing_data['matchup'] = data['task_data'][i]['task_specs']['comparison_type']
                    pairing_data['conversations'] = data['task_data'][i]['conversations']
                    pairing_data['count'] = 0
                pairing_data = all_pairings_data[pairing_id]
                pairing_data['count'] += 1



logfile.write("OVERALL STATS: \n")
logfile.write("TIME TAKEN MEDIAN: {}\n".format(np.median(time_taken_arr)))
logfile.write("NUM ONBOARDING HITS: {} of which {} were successes, {} were failures\n\n".format(num_onboarding, num_onboarding_successes, num_onboarding-num_onboarding_successes))
logfile.write("NUM DESIRED HITS: {}\n".format(num_desired))

logfile.write("STATS PER ONBOARDING PAIRING\n")
for pairing, pairing_data in sorted(onboarding_pairings_data.items(), key=lambda x: (x[1]['correct_count']/x[1]['attempt_count'])):
    logfile.write(str(pairing) + '\n')
    logfile.write(pairing_data['matchup']+ '\n')
    logfile.write(json.dumps(pairing_data['conversations'])+ '\n')
    logfile.write('{} / {} correct \n'.format(pairing_data['correct_count'], pairing_data['attempt_count']))
    logfile.write('\n')

logfile.write("STATS PER DESIRED PAIRING\n")
for pairing, pairing_data in sorted(all_pairings_data.items(), key=lambda x: x[1]['count']):
    logfile.write(str(pairing) + '\n')
    logfile.write(json.dumps(pairing_data['conversations'])+ '\n')
    logfile.write('{} attempts \n'.format(pairing_data['count']))

    logfile.write('\n')

logfile.write("STATS PER WORKER\n")
for worker, worker_data in sorted(all_workers_data.items(), key=lambda x: (len(x[1]['evals']))):
    logfile.write(worker+ '\n')
    logfile.write('Passed onboarding ? : {}\n'.format(worker_data.get('passed_onboarding')))
    if len(worker_data['time_taken'])> 0:
        logfile.write('{} Median time taken \n'.format(np.median(worker_data['time_taken'])))
    logfile.write("Hits completed: {}\n".format(len(worker_data['evals'])))
    logfile.write('\n')

logfile.close()

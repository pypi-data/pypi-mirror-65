#!/usr/bin/env python3
from parlai.mturk.core.mturk_data_handler import MTurkDataHandler
import numpy as np
import pandas as pd
import json

run_id = 'pairwise_dialogue_eval_1558231704'
db_logger = MTurkDataHandler()
all_hits_data = {}
all_pairings_data = {}
onboarding_pairings_data = {}
all_workers_data = {}

num_onboarding = 0
correct_count = 0
num_desired = 0
time_taken_arr = []
logfilename = '/private/home/margaretli/pairwise_dialogue_eval/20190502_pairwise_dialogue_eval_1556853821.txt'

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
        if complete and len(data['response']['task_data']) < 5:
            print(data)
        worker_id = data['worker_id']
        if not worker_id in all_workers_data:
            worker_data = {}
            all_workers_data[worker_id] = worker_data
            worker_data['evals'] = []
            worker_data['time_taken'] = []
            worker_data['passed_onboarding'] = False
            worker_data['no_reason'] = 0
        worker_data = all_workers_data[worker_id]
        time_taken_arr.append(time_taken)
        worker_data['time_taken'].append(time_taken)
        if complete:
            worker_data['evals'].append(hit['conversation_id'])

            for i in range(len(data['task_data'])):
                if data['task_data'][i]['task_specs'].get('is_onboarding', False):
                    num_onboarding += 1
                    correct = ((
                        data['response']['task_data'][i]['speakerChoice'] == '1' and
                        data['task_data'][i]['task_specs']['conversation_order'] == [1, 0]
                    ) or (
                        data['response']['task_data'][i]['speakerChoice'] == '2' and
                        data['task_data'][i]['task_specs']['conversation_order'] == [0, 1]
                    ))
                    correct_count += 1 if correct else 0
                    pairing_id = data['task_data'][i]['task_specs']['original_hit_id']
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
                    if correct:
                        worker_data['passed_onboarding'] = True

                else:
                    pairing_id = data['task_data'][i]['task_specs']['original_hit_id']
                    # add pairing to dict
                    if not pairing_id in all_pairings_data:
                        pairing_data = {}
                        all_pairings_data[pairing_id] = pairing_data
                        pairing_data['matchup'] = data['task_data'][i]['task_specs']['comparison_type']
                        pairing_data['conversations'] = data['task_data'][i]['conversations']
                        pairing_data['count'] = 0
                        pairing_data['votes'] = [0, 0]
                        pairing_data['original_votes'] = [0, 0]
                        pairing_data['original_count'] = 0
                    try:
                        choice = data['response']['task_data'][i]['speakerChoice']
                    except:
                        print(data['response']['task_data'][i])
                        print(pairing_id)
                        continue
                    choice = (1 if ((
                        data['response']['task_data'][i]['speakerChoice'] == '1' and
                        data['task_data'][i]['task_specs']['conversation_order'] == [1, 0]
                    ) or (
                        data['response']['task_data'][i]['speakerChoice'] == '2' and
                        data['task_data'][i]['task_specs']['conversation_order'] == [0, 1]
                    )) else 0)
                    pairing_data = all_pairings_data[pairing_id]
                    pairing_data['votes'][choice] += 1
                    pairing_data['count'] += 1
                    num_desired += 1

                if data['response']['task_data'][i]['textReason'] == '':
                    worker_data['no_reason'] += 1

ORIGINAL_CSV = '/private/home/margaretli/Batch_3462988_batch_results.csv'

df = pd.read_csv(ORIGINAL_CSV)

repl_data=[]

for n, row in df.iterrows():
    id1, id2, hitid, matchup = row['Input.id1'], row['Input.id2'], row['HITId'], row['Input.matchup']
    choice = (1 if (row['Input.id1'] == row['Input.lhs_id'] and row['Answer.choice'] == 'optionB') or
        (row['Input.id1'] != row['Input.lhs_id'] and row['Answer.choice'] == 'optionA') else 0)
    if matchup in ['intbfw4']:
        repl_data.append((hitid, id1, id2, matchup, choice))
original_votes_for_0 = 0
original_votes_for_1 = 0
for (hitid, id1, id2, matchup, choice) in repl_data:
    if hitid in all_pairings_data:
        pairing_data = all_pairings_data[hitid]
        pairing_data['original_votes'][choice] += 1
        pairing_data['original_count'] += 1
    if choice == 0:
        original_votes_for_0 += 1
    else:
        original_votes_for_1 += pairing_data['original_votes'][1]

logfile.write("OVERALL STATS: \n")
logfile.write("TIME TAKEN MEDIAN: {}\n".format(np.median(time_taken_arr)))
logfile.write("NUM ONBOARDING HITS: {} / {} were successes\n".format(correct_count, num_onboarding))
logfile.write("NUM DESIRED TASKS: {}\n".format(num_desired))
logfile.write("NUM DISTINCT WORKERS: {} \n".format(len(all_workers_data)))

votes_for_0 = 0
votes_for_1 = 0

logfile.write("STATS PER DESIRED PAIRING\n")
for pairing, pairing_data in sorted(all_pairings_data.items(), key=lambda x: x[1]['count']):
    logfile.write(str(pairing) + '\n')
    logfile.write(json.dumps(pairing_data['conversations'])+ '\n')
    logfile.write('{} attempts \n'.format(pairing_data['count']))
    logfile.write('votes: {} vs {}\n'.format(pairing_data['votes'][0], pairing_data['votes'][1]))
    logfile.write('agreement: {}% \n'.format(max(pairing_data['votes'])*100/pairing_data['count']))
    votes_for_0 += pairing_data['votes'][0]
    votes_for_1 += pairing_data['votes'][1]
    logfile.write('original votes: {} vs {}\n'.format(pairing_data['original_votes'][0], pairing_data['original_votes'][1]))
    logfile.write('original agreement: {}% \n'.format(max(pairing_data['original_votes'])*100/pairing_data['original_count']))

    logfile.write('\n')

logfile.write("OVERALL VOTES: {} vs {} \n\n".format(votes_for_0, votes_for_1))
logfile.write("ORIGINAL OVERALL VOTES: {} vs {} \n\n".format(original_votes_for_0, original_votes_for_1))



logfile.write("STATS PER WORKER\n")
for worker, worker_data in sorted(all_workers_data.items(), key=lambda x: (len(x[1]['evals']))):
    logfile.write(worker+ '\n')
    logfile.write('Passed onboarding ? : {}\n'.format(worker_data.get('passed_onboarding')))
    if len(worker_data['time_taken'])> 0:
        logfile.write('{} Median time taken \n'.format(np.median(worker_data['time_taken'])))
    logfile.write("Hits completed: {}\n".format(len(worker_data['evals'])))
    logfile.write("Num hits without reason: {} \n".format(worker_data['no_reason']))
    logfile.write('\n')

logfile.close()

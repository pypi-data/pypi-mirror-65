#!/usr/bin/env python3
import copy
import pandas as pd
import argparse

from parlai.mturk.core.mturk_data_handler import MTurkDataHandler

live_db_logger = MTurkDataHandler(file_name='/private/home/margaretli/ParlAI/parlai/mturk/run_data/pmt_data.db')
sb_db_logger = MTurkDataHandler(file_name='/private/home/margaretli/ParlAI/parlai/mturk/run_data/pmt_sbdata.db')


def main(run_ids, is_sandbox=False):
    # build up the dataframe
    dataframe = []
    feedback = []

    for run_id in run_ids:
        db_logger = live_db_logger
        if is_sandbox:
            db_logger = sb_db_logger

        hits = db_logger.get_pairings_for_run(run_id)

        # query data for a specific task
        for hit in hits:
            if hit['conversation_id'] is None:
                continue

            try:
                full_data = db_logger.get_full_conversation_data(run_id, hit['conversation_id'], is_sandbox)
            except FileNotFoundError:
                print('{}: {}'.format(run_id, hit['conversation_id']))
                continue

            data = next(iter(full_data['worker_data'].values()))
            time_taken = hit['task_end'] - hit['task_start']

            complete = 'task_data' in data['response'] and len(data['response']['task_data']) > 0
            if not complete:
                continue

            worker_id = data['worker_id']
            # aggregate worker statistics
            record = {}
            record['run_id'] = run_id
            record['worker'] = worker_id
            record['time_taken'] = time_taken
            record['timestamp'] = hit['task_start']
            record['complete'] = complete
            record['question']= data['task_data'][0]['task_specs']['question']
            record['conversation_id'] = hit['conversation_id']

            for i, task_data in enumerate(data['task_data']):
                task_specs = task_data['task_specs']
                response_data = data['response']['task_data'][i]

                # record for every single annotation
                response = copy.deepcopy(record)
                response['internal_pairing_id'] = task_data['task_specs']['internal_id']
                response['is_onboarding'] = task_data['task_specs'].get('is_onboarding', False)
                if response['is_onboarding']:
                    correct = ((
                        response_data['speakerChoice'] == '1' and
                        task_specs['conversation_order'] == [1, 0]
                    ) or (
                        response_data['speakerChoice'] == '2' and
                        task_specs['conversation_order'] == [0, 1]
                    ))
                    response['correct'] = correct

                    # worker_response = float(response_data['speakerChoice'])
                    # expected_side = (
                    #     -1 if ((task_specs['conversation_order'] == [1, 0] and not task_specs['correctness_is_flipped']) or
                    #     (task_specs['conversation_order'] == [0, 1] and task_specs['correctness_is_flipped']))
                    #     else 1)
                    #
                    # response['correct'] = int(worker_response * expected_side > 0)
                else:
                    response['correct'] = -1

                pairing_id = task_specs['original_hit_id']
                response['pairing_id'] = pairing_id
                response['matchup'] = task_specs['comparison_type']
                # response['conversations'] = task_data['conversations']
                if not response_data:
                    continue
                choice = response_data['speakerChoice']
                choice = (1 if ((
                    choice == '1' and
                    task_specs['conversation_order'] == [1, 0]
                ) or (
                    choice == '2' and
                    task_specs['conversation_order'] == [0, 1]
                )) else 0)

                # score = response_data['speakerChoice']
                # response['score'] = score
                # is_flipped = -1 if task_specs['conversation_order'] == [1, 0] else 1
                # response['corrected_score'] = is_flipped * score
                # choice = (1 if is_flipped*score > 0 else 0)

                response['reason'] = response_data['textReason']
                data['reason_given'] = response['reason'] != ''
                if 'assignment_id_hashed' in task_data['conversations'][0]:
                    response['conversation_ids'] = [
                        task_data['conversations'][0]['assignment_id_hashed'],
                        task_data['conversations'][1]['assignment_id_hashed']
                    ]
                elif 'pairing_id' in task_data['conversations'][0]:
                    response['conversation_ids'] = [
                        task_data['conversations'][0]['pairing_id'],
                        task_data['conversations'][1]['pairing_id']
                    ]
                else:
                    response['conversation_ids'] = [
                        None, None
                    ]
                winner = task_data['conversations'][choice]
                loser = task_data['conversations'][1 - choice]
                # response['conversations'] = task_data['conversations'][0]['assignment_id_hashed'] + ' ' + task_data['conversations'][1]['assignment_id_hashed']

                response['winner'] = winner['model_name']
                response['loser'] = loser['model_name']
                if response['winner'] == response['loser']:
                    response['winner'] += '_human_chat' if 'human_persona' in winner else '_self_chat'
                    response['loser'] += '_human_chat' if 'human_persona' in loser else '_self_chat'
                response['winner_dialogue'] = winner['dialog']
                response['loser_dialogue'] = loser['dialog']

                # for key in winner['evaluation_results'].keys():
                #     response['winner_' + key] = winner['evaluation_results'][key]
                #     response['loser_' + key] = loser['evaluation_results'][key]

                dataframe.append(response)
            if len(data['response']['task_data']) >  len(data['task_data']):
                feedback.append(data['response']['task_data'][-1])

    return pd.DataFrame(dataframe), feedback

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_ids', type=str, help='ids of Mturk run, comma separated')
    args = parser.parse_args()
    run_ids = args['run_ids'].split(',')
    # run_ids = ['pairwise_dialogue_eval_1559689090']
    main(run_ids)

#!/usr/bin/env python3
import numpy as np
import pandas as pd
import json

from parlai_internal.mturk.tasks.pairwise_dialogue_eval.run import main as run_main, make_flags

QUESTION_NUMBER = 0
QUESTIONS = [
    {
        's1_choice': 'I would prefer to talk to <Speaker 1>',
        's2_choice': 'I would prefer to talk to <Speaker 2>',
        'question': 'Who would you prefer to talk to for a long conversation?'
    },
]


ALL_MODEL_COMPARISONS = [('hf', 'lic')]
NUM_CONVS = 24
CHOSEN_MODEL_CONVS = {}
ALL_CONV_PAIRS = []
dir = '/private/home/margaretli/ParlAI/data/pairwise_eval_experiments/convai2_human_chats'


def get_model_convs(model):
    if model not in CHOSEN_MODEL_CONVS:
        m1file = dir + '/' + model + '.jsonl'
        all_model_convs = []
        with open(m1file, 'r') as dialog_data_file:
            np.random.seed(seed=42)
            for l in dialog_data_file:
                try:
                    single_task_json = json.loads(l)
                except:
                    print(l)
                id = single_task_json.get('assignment_id_hashed')
                if id is None:
                    id = single_task_json['pair_id']
                # model_name = single_task_json['model_name']
                all_model_convs.append(id)
        model_convs = np.random.choice(all_model_convs, NUM_CONVS, replace=False)
        CHOSEN_MODEL_CONVS[model] = model_convs


for (m1, m2) in ALL_MODEL_COMPARISONS:
    get_model_convs(m1)
    get_model_convs(m2)

print(CHOSEN_MODEL_CONVS)


for (m1, m2) in ALL_MODEL_COMPARISONS:
    matchup = m1 + ',' + m2
    m1_convs = CHOSEN_MODEL_CONVS[m1]
    m2_convs = CHOSEN_MODEL_CONVS[m2]
    for conv1 in m1_convs:
        for conv2 in m2_convs:
            ALL_CONV_PAIRS.append((conv1, conv2, None, matchup))

# print(ALL_CONV_PAIRS)

def set_args():
    args = make_flags()
    args['pair_data'] = ALL_CONV_PAIRS
    args['annotations_per_pair'] = 1
    args['dialogs_path'] = '/private/home/margaretli/ParlAI/data/pairwise_eval_experiments/convai2_human_chats'
    args['model_comparisons'] = ALL_MODEL_COMPARISONS
    args['reward'] = 0.5
    args['block_on_onboarding'] = True
    #Handpicked onboarding task greedy, human
    args['onboarding_tasks'] = [('3WETL7AQWUVO773XHMLZZGBURJE53C', '3II4UPYCOKUBILOSU3FEA0SXC91QDF', 'qual1')]
    args['num_conversations'] = int(len(ALL_CONV_PAIRS)/4)  # number of hits
    args['max_hits_per_worker'] = 1
    args['allowed_conversations'] = 1
    args['s1_choice'] = QUESTIONS[QUESTION_NUMBER]['s1_choice']
    args['s2_choice'] = QUESTIONS[QUESTION_NUMBER]['s2_choice']
    args['question'] = QUESTIONS[QUESTION_NUMBER]['question']
    args['block_qualification'] = 'pairwise_dialogue_block_onboarding_fails'
    args['new_workers'] = False
    args['task_description'] = {'num_subtasks': 5, 'question': args['question'], 'get_task_feedback': True}
    args['assignment_duration_in_seconds'] = 600
    args['seed'] = 42
    args['is_sandbox'] = False
    return args

if __name__ == '__main__':
    args = set_args()
    run_main(args)

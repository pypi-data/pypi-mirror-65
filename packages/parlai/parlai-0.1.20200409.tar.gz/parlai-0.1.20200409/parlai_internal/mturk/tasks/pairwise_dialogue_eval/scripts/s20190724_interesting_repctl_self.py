#!/usr/bin/env python3
import numpy as np
import pandas as pd
import json

from parlai_internal.mturk.tasks.pairwise_dialogue_eval.run import main as run_main, make_flags


QUESTION_NUMBER = 0
QUESTIONS = [
    {
        's1_choice': '<Speaker 1> is more interesting',
        's2_choice': '<Speaker 2> is more interesting',
        'question': 'If you had to say one of these speakers is interesting and one is boring, who would you say is more interesting?'
    },
]


ALL_MODEL_COMPARISONS = [('repetition_model_setting35_settinginf', 'interesting_nidf_model_bfw_setting_04')]
NUM_CONVS = 50


def set_args():
    args = make_flags()
    args['annotations_per_pair'] = 1
    args['pairs_per_matchup'] = 160
    args['dialogs_path'] = '/private/home/margaretli/ParlAI/data/pairwise_eval_experiments/convai2_self_chats'
    args['model_comparisons'] = ALL_MODEL_COMPARISONS
    args['reward'] = 0.5
    args['block_on_onboarding'] = True
    #Handpicked onboarding task greedy, human
    args['onboarding_tasks'] = [('greedy_1', '36DSNE9QZ6LL0VB4PM9LOTSA2QGJOA', 'qual1')]
    args['num_conversations'] = int(args['pairs_per_matchup']*(len(ALL_MODEL_COMPARISONS)/4))  # number of hits
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

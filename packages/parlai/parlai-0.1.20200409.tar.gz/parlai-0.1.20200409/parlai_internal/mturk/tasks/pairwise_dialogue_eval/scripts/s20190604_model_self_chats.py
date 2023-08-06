#!/usr/bin/env python3
import numpy as np
import pandas as pd

from parlai_internal.mturk.tasks.pairwise_dialogue_eval.run import main as run_main, make_flags

#This number gets changed between runs to change the question
RUN_NUMBER = 2
QUESTIONS = [
    {
        's1_choice': '<Speaker 1> is more interesting',
        's2_choice': '<Speaker 2> is more interesting',
        'question': 'If you had to say one of these speakers is interesting and one is boring, who would you say is more interesting?'
    },
    {
        's1_choice': 'I would prefer to talk to <Speaker 1>',
        's2_choice': 'I would prefer to talk to <Speaker 2>',
        'question': 'Who would you prefer to talk to for a long conversation?'
    },
    {
        's1_choice': '<Speaker 1> sounds more human',
        's2_choice': '<Speaker 2> sounds more human',
        'question': 'Which speaker sounds more human?'
    },
]


def set_args():
    args = make_flags()
    args['tasks_per_pair'] = 3
    args['dialogs_path'] = '/private/home/margaretli/ParlAI/data/model_self_dialogs/controllable_dialog'
    args['num_pairs'] = 50
    args['model_comparison'] = 'repetition_model_setting35_settinginf,interesting_nidf_model_bfw_setting_04'
    args['reward'] = 0.5
    # args['block_on_onboarding'] = True
    #Handpicked onboarding task greedy, human
    args['onboarding_tasks'] = [('greedy_1', '36DSNE9QZ6LL0VB4PM9LOTSA2QGJOA', 'qual1')]
    args['num_conversations'] = 40  # number of hits
    args['max_hits_per_worker'] = 9
    args['s1_choice'] = QUESTIONS[RUN_NUMBER]['s1_choice']
    args['s2_choice'] = QUESTIONS[RUN_NUMBER]['s2_choice']
    args['question'] = QUESTIONS[RUN_NUMBER]['question']
    args['block_qualification'] = 'pairwise_dialogue_block_onboarding_fails'
    args['task_description'] = {'num_subtasks': 5, 'question': args['question']}
    args['assignment_duration_in_seconds'] = 600
    args['seed'] = 42
    args['is_sandbox'] = False
    return args

if __name__ == '__main__':
    args = set_args()
    run_main(args)

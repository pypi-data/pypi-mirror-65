#!/usr/bin/env python3
import numpy as np
import pandas as pd

from parlai_internal.mturk.tasks.pairwise_dialogue_eval.run import main as run_main, make_flags

ORIGINAL_CSV = '/private/home/margaretli/Batch_3462988_batch_results.csv'

df = pd.read_csv(ORIGINAL_CSV)

repl_data_dict = {}
repl_data = []

def set_args():
    for n, row in df.iterrows():
        id1, id2, hitid, matchup = row['Input.id1'], row['Input.id2'], row['HITId'], row['Input.matchup']
        if matchup in ['intbfw4'] and not hitid in repl_data_dict:
            repl_data_dict[hitid] = (id1, id2, matchup)

    for hitid in repl_data_dict:
        (id1, id2, matchup) = repl_data_dict[hitid]
        repl_data.append((id1, id2, hitid, matchup))

    args = make_flags()
    args['repl_data'] = repl_data[:20]
    args['tasks_per_pair'] = 5
    args['dialogs_path'] = '/private/home/margaretli/ParlAI/data/controllable_dialog'
    args['reward'] = 0.5
    args['block_on_onboarding'] = False
    #Handpicked onboarding task
    args['onboarding_tasks'] = [('3WETL7AQWUVO773XHMLZZGBURJE53C', '3GS6S824SRKPOUBRV6SNYUMDED4WNP', 'qual1')]
    args['num_conversations'] = 25
    args['max_hits_per_worker'] = 4
    args['quality'] = "more interesting"
    args['question'] = "If you had to say one of these speakers is interesting and one is boring, who would you say is more interesting?"
    args['block_qualification'] = 'pairwise_dialogue_block_20190503_debug_run'
    args['task_description'] = {'num_subtasks': 5, 'question': "If you had to say one of these speakers is interesting and one is boring, who would you say is more interesting?"}
    args['assignment_duration_in_seconds'] = 600
    args['is_sandbox'] = False
    return args

if __name__ == '__main__':
    args = set_args()
    run_main(args)

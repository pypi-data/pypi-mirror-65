#!/usr/bin/env python3
import numpy as np
import pandas as pd

from parlai_internal.mturk.tasks.pairwise_dialogue_eval.run import main, make_flags

ORIGINAL_CSV = '/private/home/roller/abi/Batch_3462988_batch_results.csv'

df = pd.read_csv(ORIGINAL_CSV)

repl_data = list(zip(df['Input.id1'], df['Input.id2'], df['HITId'], df['Input.matchup']))

repl_data_dict = {}
repl_onboard_data_dict = {}
repl_data_list = []

for id1, id2, hitid, matchup in repl_data:
    if matchup in ['qual1', 'qual2']:
        if not hitid in repl_onboard_data_dict:
            repl_onboard_data_dict[hitid] = (id1, id2, matchup)
    if not hitid in repl_data_dict:
        repl_data_dict[hitid] = (id1, id2, matchup)

print(repl_onboard_data_dict)

for hitid in repl_data_dict:
    repl_data_list.append((id1, id2, hitid, matchup))



args = make_flags()
args['repl_data'] = repl_data_list
args['tasks_per_pair'] = 5
args['dialogs_path'] = '/private/home/margaretli/ParlAI/data/controllable_dialog_internal'
# args['block_qualification'] = 'pairwise_dialogue_eval_soft_block'

main(args)

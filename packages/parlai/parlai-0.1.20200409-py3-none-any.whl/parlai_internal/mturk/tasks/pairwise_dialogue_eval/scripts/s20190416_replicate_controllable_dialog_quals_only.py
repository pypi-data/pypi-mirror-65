#!/usr/bin/env python3
import numpy as np
import pandas as pd

from parlai_internal.mturk.tasks.pairwise_dialogue_eval.run import main, make_flags

ORIGINAL_CSV = '/private/home/margaretli/Batch_3462988_batch_results.csv'

df = pd.read_csv(ORIGINAL_CSV)

repl_data_dict = {}
repl_data = []

for n, row in df.iterrows():
    id1, id2, hitid, matchup = row['Input.id1'], row['Input.id2'], row['HITId'], row['Input.matchup']
    if matchup in ['qual1', 'qual2'] and not hitid in repl_data_dict:
        repl_data_dict[hitid] = (id1, id2, matchup)

for hitid in repl_data_dict:
    (id1, id2, matchup) = repl_data_dict[hitid]
    repl_data.append((id1, id2, hitid, matchup))

args = make_flags()
args['repl_data'] = repl_data
args['tasks_per_pair'] = 5
args['dialogs_path'] = '/private/home/margaretli/ParlAI/data/controllable_dialog_internal'
args['max_hits_per_worker'] = 20
args['reward'] = 0.1
args['num_conversations'] = args['tasks_per_pair'] * len(repl_data)
args['is_sandbox'] = False
print(args)

main(args)

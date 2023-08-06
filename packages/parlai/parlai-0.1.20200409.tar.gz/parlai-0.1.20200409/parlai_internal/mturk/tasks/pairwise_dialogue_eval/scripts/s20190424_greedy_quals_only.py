#!/usr/bin/env python3
import numpy as np
import pandas as pd

from parlai_internal.mturk.tasks.pairwise_dialogue_eval.run import main, make_flags

ORIGINAL_CSV = '/private/home/margaretli/Batch_3462988_batch_results.csv'

df = pd.read_csv(ORIGINAL_CSV)

args = make_flags()
args['tasks_per_pair'] = 5
args['dialogs_path'] = '/private/home/margaretli/ParlAI/data/controllable_dialog_internal'
args['reward'] = 0.14
args['num_onboarding_tasks'] = 10
args['num_conversations'] = args['tasks_per_pair'] * args['num_onboarding_tasks'] * 2
args['max_hits_per_worker'] = 20
# args['is_sandbox'] = False

main(args)

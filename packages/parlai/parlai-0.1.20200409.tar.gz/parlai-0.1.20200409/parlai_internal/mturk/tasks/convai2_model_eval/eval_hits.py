#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import numpy as np
import os
import pickle
from worlds import ENGAGINGNESS_CHOICES, CONSISTENCY_CHOICES, FLUENCY_CHOICES

from parlai.core.params import ParlaiParser
ParlaiParser()  # instantiate to set PARLAI_HOME environment var

"""Script for collecting data from wizard MTurk task logs"""

# ARGS

model_list = [
    'projects.personachat.kvmemnn.kvmemnn:KvmemnnAgent',  #kvmemnn baseline
    'human_eval',  # humans
    'convai2_submissions.hf_sub2.ConvAI2_HF_submission_2.ftlm:FtlmAgent',  # hugging face
    'model_eval_f1',  # adapt centre
    'onmt.onmt:OnmtAgent',  # happy minions
    'baseline_msa_sep.msa_agent.seq2seq.seq2seq_v0:PerplexityEvaluatorAgent',  # mohd shadab alam
    #'internal:transformer_ranker',  # transformer baseline agent
]
MODEL_NAME = model_list[-1]

ROOT = os.path.join(
    os.environ['PARLAI_HOME'],
    'data',
    'convAI2_eval',
)

EVAL_KEYS = ['engagingness', 'fluency', 'consistency', 'persona']


def print_wizard_results(root, model_name, print_convos=True):
    all_scores = {
        'engagingness': [[], []],
        'fluency': [],
        'fluency_bad': [],
        'consistency': [],
        'consistency_bad': [],
        'persona': [],
        'total': 0,
        'total_time': 0,
        'model_turns': [],
        'workers': {}
    }

    for folder in os.listdir(root):
        if model_name in folder and os.path.isdir(os.path.join(root, folder)):
            for file in os.listdir(os.path.join(root, folder)):
                if ('incomplete' not in file and 'live' in file and
                        all_scores['total'] < 100):
                    file_path = os.path.join(root, folder, file)
                    with open(file_path, 'rb') as f:
                        log = pickle.load(f)

                    all_scores['total'] += 1
                    all_scores['total_time'] += log['total_time']
                    all_scores['engagingness'][0].append(log['engagingness'][0] + 1)
                    if len(log['engagingness']) > 1:
                        all_scores['engagingness'][1].append(log['engagingness'][1] + 1)
                        all_scores['fluency'].append(log['fluency'][0] + 1)
                        if len(log['fluency']) > 1:
                            all_scores['fluency_bad'].append(len(log['fluency'][1]))
                        all_scores['consistency'].append(log['consistency'][0] + 1)
                        if len(log['consistency']) > 1:
                            all_scores['consistency_bad'].append(len(log['consistency'][1]))
                    all_scores['persona'].append(int(log['persona'][0]))
                    all_scores['model_turns'].append(len(log['dialog_list']))
                    for worker in log['workers']:
                        if worker not in all_scores['workers']:
                            all_scores['workers'][worker] = 1
                        else:
                            all_scores['workers'][worker] += 1
                    if print_convos:
                        print('Worker ID:', log['workers'])
                        print('Completion time:', abs(log['total_time']))
                        print('DIALOG:')
                        for line in log['dialog']:
                            print(line)
                        print('---Eval Scores---')
                        for key in EVAL_KEYS:
                            print("{}:".format(key), log[key])
                        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    print('***********OVERVIEW************')
    print('---------------------------------')

    tot = all_scores['total']
    print('Total conversations:', tot)
    turns = sum(all_scores['model_turns'])
    print('Total model turns:', turns)
    print('Avg completion time:', all_scores['total_time'] / tot)
    print('Total turkers:', len(all_scores['workers']))
    print('ALL WORKERS:', all_scores['workers'])

    eng_1 = sum(all_scores['engagingness'][0]) / tot
    print('Average engagingness 1:', eng_1)
    print('STD:', np.std(all_scores['engagingness'][0]))
    if len(all_scores['engagingness'][1]) > 0:
        eng_2 = sum(all_scores['engagingness'][1]) / tot
        print('Average engagingness 2:', eng_2)
        print('STD:', np.std(all_scores['engagingness'][1]))
        print('Engagingness combined:', (eng_1 + eng_2) / 2)

        print('Average fluency:', sum(all_scores['fluency']) / tot)
        print('STD:', np.std(all_scores['fluency']))
        print('Average not-fluent turns:', sum(all_scores['fluency_bad']) / turns)

        # NOTE: for consistency we subtract from 4 since 0 is the high measure
        print('Average consistency:', 4 - (sum(all_scores['consistency']) / tot))
        print('STD:', np.std(all_scores['consistency']))
        print('Average not-consistent turns:', sum(all_scores['consistency_bad']) / turns)

    print('Average persona score:', sum(all_scores['persona']) / tot)
    print('STD:', np.std(all_scores['persona']))

    print('---------------------------------')


if __name__ == '__main__':
    print_wizard_results(root=ROOT, model_name=MODEL_NAME)

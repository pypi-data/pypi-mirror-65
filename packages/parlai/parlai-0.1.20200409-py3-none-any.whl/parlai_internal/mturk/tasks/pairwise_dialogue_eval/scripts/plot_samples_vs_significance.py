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
import json

from parlai.core.params import ParlaiParser
ParlaiParser()  # instantiate to set PARLAI_HOME environment var

"""Script for collecting data from wizard MTurk task logs"""

# ARGS

model_list = {
    'kvmemnn_baseline': 'projects.personachat.kvmemnn.kvmemnn:KvmemnnAgent',  # kvmemnn baseline
    'human': 'human_eval',  # humans
    'hugging_face': 'convai2_submissions.hf_sub2.ConvAI2_HF_submission_2.ftlm:FtlmAgent',  # hugging face
    'adapt_centre': 'model_eval_f1',  # adapt centre
    'happy_minions': 'onmt.onmt:OnmtAgent',  # happy minions
    'mohd_shadab_alam': 'baseline_msa_sep.msa_agent.seq2seq.seq2seq_v0:PerplexityEvaluatorAgent',  # mohd shadab alam
    #'transformer_baseline': 'internal:transformer_ranker',  # transformer baseline agent
    'little_baby': 'convai2_submissions.LittleBaby.ConvAI.projects.convai2.Vsmn.Vsmn:VsmnAgent', # little baby
    'lost_in_conversation': 'transformer_chatbot'
}

ROOT = os.path.join(
    os.environ['PARLAI_HOME'],
    'data',
    'convAI2_eval',
)

#EVAL_KEYS = ['engagingness', 'fluency', 'consistency', 'persona']
EVAL_KEYS = ['engagingness', 'persona']

def print_wizard_results(root, model_name, name=None, print_convos=True):
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
    log_list = []

    for folder in os.listdir(root):
        if model_name in folder and os.path.isdir(os.path.join(root, folder)):
            for file in os.listdir(os.path.join(root, folder)):
                if ('incomplete' not in file and 'live' in file and
                        all_scores['total'] < 100):
                    file_path = os.path.join(root, folder, file)
                    with open(file_path, 'rb') as f:
                        log = pickle.load(f)

                    log['model_name'] = name
                    log_list.append(log)

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
                        if name:
                            print("MODEL:", name)
                        print('Worker ID:', log['workers'])
                        print('Completion time:', abs(log['total_time']))
                        # if 'model_personas' in log:
                        #     print('Model personas:')
                        #     for pers in log['model_personas']:
                        #         print(pers)
                        print('\nDIALOG:')
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
    #print('Total turkers:', len(all_scores['workers']))
    #print('ALL WORKERS:', all_scores['workers'])

    eng_1 = sum(all_scores['engagingness'][0]) / tot
    print('Average engagingness 1:', eng_1)
    print('STD:', np.std(all_scores['engagingness'][0]))
    # if len(all_scores['engagingness'][1]) > 0:
    #     eng_2 = sum(all_scores['engagingness'][1]) / tot
    #     print('Average engagingness 2:', eng_2)
    #     print('STD:', np.std(all_scores['engagingness'][1]))
    #     print('Engagingness combined:', (eng_1 + eng_2) / 2)
    #
    #     print('Average fluency:', sum(all_scores['fluency']) / tot)
    #     print('STD:', np.std(all_scores['fluency']))
    #     print('Average not-fluent turns:', sum(all_scores['fluency_bad']) / turns)
    #
    #     # NOTE: for consistency we subtract from 4 since 0 is the high measure
    #     print('Average consistency:', 4 - (sum(all_scores['consistency']) / tot))
    #     print('STD:', np.std(all_scores['consistency']))
    #     print('Average not-consistent turns:', sum(all_scores['consistency_bad']) / turns)

    print('Average persona score:', sum(all_scores['persona']) / tot)
    print('STD:', np.std(all_scores['persona']))

    print('---------------------------------')
    return all_scores, log_list


if __name__ == '__main__':
    # _ = print_wizard_results(root=ROOT, model_name=MODEL_NAME)
    scores = {}
    names = ['convai2_submissions.hf_sub2.ConvAI2_HF_submission_2.ftlm:FtlmAgent', 'transformer_chatbot']
    all_logs = []
    for model in model_list.keys():
        print('*****************************************')
        print("MODEL:", model)
        print('*****************************************')
        _, log = print_wizard_results(root=ROOT, model_name=model_list[model], name=model, print_convos=False)
        scores[model_list[model]] = [dialog['engagingness'][0] for dialog in log]
        all_logs += log

    #data = json.dumps(all_logs)
    # with open('/private/home/edinan/ParlAI/parlai_internal/mturk/tasks/convai2_model_eval/convai2_results.json', 'w') as f:
    #     f.write(data)


    # import pdb; pdb.set_trace()
    import copy

    scores0 = copy.deepcopy(scores[names[0]])
    scores1 = copy.deepcopy(scores[names[1]])
    np.random.shuffle(scores0)
    np.random.shuffle(scores1)
    comp_scores = []
    random  = 0
    i = 0
    num_scores = 160
    while i < num_scores:
        i+= 1
        s0 = np.random.choice(scores[names[0]])
        s1 = np.random.choice(scores[names[1]])
    # for s0, s1 in zip(scores0, scores1):
        if s0 > s1:
            comp_scores.append(0)
        elif s1 > s0:
            comp_scores.append(1)
        else:
            comp_scores.append(np.random.choice([0, 1]))
            random += 1

    import scipy.stats
    print(random)
    print(scipy.stats.binom_test([sum(comp_scores), len(comp_scores) - sum(comp_scores)]))
    print(comp_scores)
    print("WIN RATE: {}/{}".format(sum(comp_scores), len(comp_scores)))
    x = scipy.stats.ttest_ind(scores[names[0]], scores[names[1]])
    print(x)

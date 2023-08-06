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

model_list = {
    'kvmemnn_baseline': 'projects.personachat.kvmemnn.kvmemnn:KvmemnnAgent',  # kvmemnn baseline
    'human': 'human_eval',  # humans
    'hugging_face': 'convai2_submissions.hf_sub2.ConvAI2_HF_submission_2.ftlm:FtlmAgent',  # hugging face
    'adapt_centre': 'model_eval_f1',  # adapt centre
    'happy_minions': 'onmt.onmt:OnmtAgent',  # happy minions
    'mohd_shadab_alam': 'baseline_msa_sep.msa_agent.seq2seq.seq2seq_v0:PerplexityEvaluatorAgent',  # mohd shadab alam
    'transformer_baseline': 'internal:transformer_ranker',  # transformer baseline agent
    'little_baby': 'convai2_submissions.LittleBaby.ConvAI.projects.convai2.Vsmn.Vsmn:VsmnAgent', # little baby
    'lost_in_conversation': 'transformer_chatbot'
}

ROOT = os.path.join(
    os.environ['PARLAI_HOME'],
    'data',
    'convAI2_eval',
)

KEY_MATCH = ['love', 'awesome', 'great', 'fun', '!', '?']
QUESTION_WORDS = ['who', 'what', 'when', 'where', 'why', 'how']


def print_sent_results(root, model_name, k, print_convos=True):
    all_scores = {
        'love': 0,
        'awesome': 0,
        'great': 0,
        'fun': 0,
        '!': 0,
        '?': 0,
        'questions': 0,
        'total': 0,
    }

    for folder in os.listdir(root):
        if k in folder and os.path.isdir(os.path.join(root, folder)):
            for file in os.listdir(os.path.join(root, folder)):
                if ('incomplete' not in file and 'live' in file and
                        all_scores['total'] < 100):
                    file_path = os.path.join(root, folder, file)
                    with open(file_path, 'rb') as f:
                        log = pickle.load(f)

                    all_scores['total'] += 1
                    for tup in log['dialog']:
                        if tup[0] == 1:
                            sent = tup[1].lower()
                            for key in KEY_MATCH:
                                if key in sent:
                                    all_scores[key] += 1
                            for question in QUESTION_WORDS:
                                if question == sent.split(' ')[0]:
                                    all_scores['questions'] += 1

    print('---------------------------------')
    print("MODEL:", model_name)
    for k, v in all_scores.items():
        print("{}: {}".format(k, v))
    print('---------------------------------\n')
    return all_scores


if __name__ == '__main__':
    total = {}
    for key in KEY_MATCH:
        total[key] = []
    total['questions'] = []
    for k, v in model_list.items():
        if k != 'transformer_baseline':
            scores = print_sent_results(root=ROOT, model_name=k, k=v)
            for u, w in scores.items():
                if u in total:
                    total[u].append(w)

    print("model_names = {}".format(list(model_list.keys())))
    for x, y in total.items():
        print("{} = {}".format(x,y))

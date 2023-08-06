#!/usr/bin/env python3
import os
import json
import numpy as np
import statistics

from parlai.core.params import ParlaiParser
ParlaiParser()  # instantiate to set PARLAI_HOME environment var

"""Script for collecting data fom wild evaluation logs"""


def avg(lst):
    return sum(lst) / len(lst)


def median(lst):
    return statistics.median(lst)


def mode(lst):
    return max(set(lst), key=lst.count)


def std(lst):
    return np.std(lst)


ROOT = os.path.join(
    os.environ['PARLAI_HOME'],
    'data',
    'convAI2_eval',
)

MODEL_MAP = {
    'Lost in Conversation': '105561dd-4850-45b4-94be-e767ad48c97a',
    'Hugging Face': '28f4ed5c-405b-4b46-96e7-b77de7782b75',
    'Happy Minions': '87db49e9-498b-4ce9-9628-5ad5935edeef',
    'ADAPT Centre': '3376d0f9-b33b-4f7c-b62d-c8968f5937e6',
}

model_map_inv = {MODEL_MAP[k]: k for k in MODEL_MAP.keys()}
model_scores = {k: [] for k in MODEL_MAP.keys()}
model_conv_len = {k: [] for k in MODEL_MAP.keys()}
model_none_cnt = {k: 0 for k in MODEL_MAP.keys()}

unknown_keys = []

file = os.path.join(ROOT, 'wild_eval.json')
test = json.loads(open(file, 'r').read())
for log in test:
    if 'bot_id' in log and len(log['dialog']) >= 3:
        model_name = model_map_inv.get(log['bot_id'], None)
        if not model_name:
            unknown_keys.append(log['bot_id'])
            continue

        if log['eval_score'] is None:
            model_none_cnt[model_name] += 1
            continue

        bot_working = False
        for l in log['dialog']:
            if l['sender_class'] == 'Bot':
                bot_working = True
                break

        # human_in_a_row = 0
        # cnt = 0
        # prev = None
        # for l in log['dialog']:
        #     if l['sender_class'] == 'Human' and prev == 'Human':
        #         cnt += 1
        #         if cnt > human_in_a_row:
        #             human_in_a_row = cnt
        #     else:
        #         cnt = 0
        #     prev = l['sender_class']
        #
        # if human_in_a_row >= 1:
        #     continue

        if bot_working:
            if log['eval_score'] is not None:
                model_scores[model_name].append(log['eval_score'])
                model_conv_len[model_name].append(len(log['dialog']))

            if model_name == 'Lost in Conversation' and log['eval_score'] is not None:
                for l in log['dialog']:
                    print(l['sender_class'], ':', l['text'])

                print('Score:', log['eval_score'])
                print('---------------')

for key in MODEL_MAP.keys():
    print(key, ":\n")
    print('Avg score:', avg(model_scores[key]))
    print('Score STD:', std(model_scores[key]))
    print('Mode score:', mode(model_scores[key]))
    print('Median score:', median(model_scores[key]))
    print('Num scores:', len(model_scores[key]))
    print('NONE count:', model_none_cnt[key])
    #print('All scores:', model_scores[key])
    print('Avg conversation length:', avg(model_conv_len[key]))
    print('---------------------------------------------------')

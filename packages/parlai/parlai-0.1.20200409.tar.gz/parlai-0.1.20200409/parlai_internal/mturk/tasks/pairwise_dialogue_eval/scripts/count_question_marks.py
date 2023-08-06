#!/usr/bin/env python3
import json
import re

FILES = [
    '/private/home/margaretli/ParlAI/data/pairwise_eval_experiments/convai2_self_chats/hf.jsonl',
    '/private/home/margaretli/ParlAI/data/pairwise_eval_experiments/convai2_self_chats/lic.jsonl',
    '/private/home/margaretli/ParlAI/data/pairwise_eval_experiments/convai2_human_chats/hf.jsonl',
    '/private/home/margaretli/ParlAI/data/pairwise_eval_experiments/convai2_human_chats/lic.jsonl'
]

for file in FILES:
    with open(file, 'r') as f:
        model_count = 0
        lines = 0
        human_count = 0
        for l in f:
            lines += 1
            line = json.loads(l.strip())
            model_lines = ' '.join([cl['text'] for cl in line['dialog'] if cl['speaker'] == 'model'])
            human_lines = ' '.join([cl['text'] for cl in line['dialog'] if cl['speaker'] != 'model'])

            # print(model_lines)
            human_count += human_lines.count('?')
            model_count += model_lines.count('?')
    print("{} model ?s in {} conversations in {}".format(model_count, lines, file))
    print("{} other ?s in {} conversations in {}".format(human_count, lines, file))

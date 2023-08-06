#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
"""

from parlai.core.params import ParlaiParser
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
import json
import ntpath
import random
import os
from copy import deepcopy

BASE_FILEPATH = "/private/home/margaretli/ParlAI/data/model_valid_dialogs"

def setup_args():
    parser = ParlaiParser(True, True, '')
    parser.add_argument('--display-ignore-fields', type=str, default='')
    parser.add_argument('--n-turns', type=int, default=6)
    parser.add_argument('--write-filename', type=str, default=None)
    # by default we want to display info about the validation set
    parser.set_defaults(datatype='valid')
    return parser


def get_filename(opt):
    filename = opt['write_filename']
    if filename is None:
        dir, filename = ntpath.split(opt['model_file'])
        filename = filename if filename else ntpath.basename(dir)
    return os.path.join(BASE_FILEPATH, filename + '.jsonl')


def save_to_json_file(all_acts_list, dialogs_file):
    all_acts = all_acts_list[0]
    json_dict = {}
    dialogs = []
    persona = ''

    text = all_acts['text']
    lines = text.split('\n')
    persona_lines = [l[:14] for l in lines if 'your persona: ' in l]
    text_lines = [l for l in lines if 'your persona: ' not in l]

    persona = '\n'.join(persona_lines)
    for text_line in text_lines:
        speaker = 'model' if text_line[:6] == '__p2__' else 'other'
        text_line = text_line[7:]
        dialogs.append({'speaker': speaker, 'text': text_line})
    speaker = 'model'
    last_text_line = all_acts_list[1]['text']
    dialogs.append({'speaker': speaker, 'text': last_text_line})
    json_dict['dialog'] = dialogs
    # verify these
    json_dict['model_name'] = all_acts['id']
    json_dict['model_persona'] = persona
    dialogs_file.write(json.dumps(json_dict))
    dialogs_file.write('\n')

# CONVAI ACT FORMAT
#[{'text': '', 'reward': 0, 'label_candidates': ('',...), 'episode_done': False, 'id': 'convai2', 'eval_labels': ('',)}, {'id': 'Seq2Seq', 'text': ''}]
# TARGET FORMAT
# {"model_name": "", "model_type": "", "model_bucket": "", "assignment_id_hashed": "",
# "evaluator_id_hashed": "", "oz_id_hashed": null,
# "dialog": [{"speaker": "human_evaluator", "text": ""}, {"speaker": "model", "text": ""},...],
# "evaluation_results": {},
# "model_persona": "i am a cancer survivor.\n...\nmy parents were both very athletic.", "human_persona": ""}

def validation_chat(opt):
    filename = get_filename(opt)
    # Create model and assign it to the specified task
    agent = create_agent(opt)
    world = create_task(opt, agent)
    dialogs_file = open(filename, 'a')
    with world:
        while True:
            all_acts = []
            world.parley()
            while not world.episode_done():
                world.parley()
                print(world.get_acts())
            all_acts = world.get_acts()
            save_to_json_file(all_acts, dialogs_file)
    dialogs_file.close()


if __name__ == '__main__':
    parser = setup_args()
    opt = parser.parse_args()
    opt['use_reply'] = 'model'
    validation_chat(opt)

# python parlai_internal/mturk/tasks/pairwise_dialogue_eval/model_validation_chat.py -mf models:controllable_dialogue/convai2_finetuned_baseline -wd extrep_2gram:-3.5,extrep_nonstopword:-1e20,intrep_nonstopword:-1e20 -t convai2 --use-reply model --n_turns 6 --beam-size 20

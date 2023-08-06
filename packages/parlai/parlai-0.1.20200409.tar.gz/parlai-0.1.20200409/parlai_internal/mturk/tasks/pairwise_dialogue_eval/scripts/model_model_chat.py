#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
Generate dialog between two copies of the same model
"""

from parlai.core.params import ParlaiParser
from parlai.core.agents import create_agent, create_agent_from_shared
from parlai.core.worlds import create_task
# from parlai_internal.mturk.tasks.controllable_dialog_eval.worlds import PersonasGenerator
from parlai_internal.mturk.tasks.convai2_model_eval.worlds import PersonasGenerator
import json
import ntpath
import random
import numpy as np
import os
from copy import deepcopy

MODEL_OPTS = {
    'hf': {
        'model': 'convai2_submissions.hf_sub2.ConvAI2_HF_submission_2.ftlm:FtlmAgent',
        'model_file': 'models:convai2/ConvAI2_HF_submission_2/model',

        'batchsize': 1,
        'override': {

            'batchsize': 1,
            'n_ctx': 128,
            'numthreads': 1,
        }
    },
    'polyencoder' : {
         'model': 'parlai_internal.agents.bert_ranker.reddits:RedditBiMOEncoderRanker',
         'model_file': '/private/home/margaretli/ParlAI/data/models/polyencoder_convai/model',
         'override': {
            'eval_candidates': 'fixed',
            'fixed_candidates_path': '/private/home/margaretli/ParlAI/data/models/convai_cands',
         }
    },
}

ParlaiParser()  # instantiate to set PARLAI_HOME environment var
BASE_FILEPATH = os.path.join(os.environ['PARLAI_HOME'], 'data', 'pairwise_eval_experiments', 'convai2_model_model_chats')
os.makedirs(BASE_FILEPATH, exist_ok = True)

def setup_args():
    parser = ParlaiParser(True, True, '')
    parser.add_argument('--display-ignore-fields', type=str, default='')
    parser.add_argument('--n-turns', type=int, default=6)
    parser.add_argument('--n-chats', type=int, default=200)
    parser.add_argument('--write-filename', type=str, default=None)

    parser.add_argument('--model0', type=str, default=None)
    parser.add_argument('--model1', type=str, default=None)

    # parser.add_argument('--mf0', type=str, default=None)
    # by default we want to display info about the validation set
    # parser.set_defaults(datatype='valid')
    return parser


def get_filename(opt0, opt1):
    filename = opt['write_filename']
    if filename is None:
        dir0, _ = ntpath.split(opt0['model_file'])
        dir0, modelname0 = ntpath.split(dir0)
        modelname0 = modelname0 if modelname0 else ntpath.basename(dir0)
        modelname0 = modelname0.replace('/', '-')
        dir1, _ = ntpath.split(opt1['model_file'])
        dir1, modelname1 = ntpath.split(dir1)
        modelname1 = modelname1 if modelname1 else ntpath.basename(dir1)
        modelname1 = modelname1.replace('/', '-')
        filename = modelname0 + '_' + modelname1
    return [modelname0, modelname1], os.path.join(BASE_FILEPATH, filename + '.jsonl')


def save_to_json_file(all_acts, agent0_persona, agent1_persona, filename, modelnames, agent_order, idnum):
    print(modelnames)
    json_dict = {}
    dialogs = []
    print(all_acts)
    agent = agent_order[0]
    for act in all_acts:
        text = act['text']
        dialogs.append({'speaker': agent, 'text': text})
        agent = 'model' if agent == 'other' else 'other'
    json_dict['dialog'] = dialogs
    json_dict['model_name'] = modelnames[0]
    json_dict['other_name'] = modelnames[1]
    json_dict['model0_persona'] = agent0_persona
    json_dict['model1_persona'] = agent1_persona
    json_dict['pair_id'] = modelnames[0] + '_' + modelnames[1] + '_' + str(idnum)
    with open(filename, 'a') as dialogs_file:
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

def self_chat(opt0, opt1):
    id = 0
    modelnames, filename = get_filename(opt0, opt1)
    # Create model and assign it to the specified task
    agents = []
    agents.append(create_agent(opt0))
    agents.append(create_agent(opt1))
    agent_order = ['model', 'other']
    personas_generator = PersonasGenerator(opt0)

    for i in range(opt['n_chats']):
        to_flip = np.random.choice([0, 1])
        if to_flip:
            agents.reverse()
            agent_order.reverse()
        agent0_persona = personas_generator.get_persona()
        agent1_persona = personas_generator.get_persona()
        agent0_persona_text = '\n'.join([
                'your persona: ' + pers for pers in agent0_persona
            ])
        agent1_persona_text = '\n'.join([
                'your persona: ' + pers for pers in agent1_persona
            ])
        all_acts = []
        for k in range(opt['n_turns']):
            act0 = {}
            act1 = {}
            # print(k)
            if k == 0:
                agents[0].observe({
                    'text':'\n'.join([agent0_persona_text, '__SILENCE__']),
                    'id': 'SYSTEM',
                    'episode_done': False
                })
                act0 = agents[0].act()
                # print(agent0.)
                print(act0)
                act0_with_persona = deepcopy(act0)
                act0_with_persona['text'] = '\n'.join([agent1_persona_text, act0['text']])
                act0_with_persona['episode_done'] = False
                agents[1].observe(deepcopy(act0_with_persona))
                act1 = agents[1].act()
                act1['episode_done'] = False
                agents[0].observe(deepcopy(act1))
            elif k >= opt['n_turns'] - 1:
                act0 = agents[0].act()
                act0['episode_done'] = True
                agents[1].observe(deepcopy(act0))
                act1 = agents[1].act()
                act1['episode_done'] = True
                agents[0].observe(deepcopy(act1))
            else:
                act0 = agents[0].act()
                act0['episode_done'] = False
                agents[1].observe(deepcopy(act0))
                act1 = agents[1].act()
                act1['episode_done'] = False
                agents[0].observe(deepcopy(act1))
            all_acts.append(act0)
            all_acts.append(act1)
        save_to_json_file(
            all_acts, agent0_persona, agent1_persona, filename, modelnames, agent_order, id)
        id += 1

    agents[0].shutdown()
    agents[1].shutdown()


if __name__ == '__main__':
    parser = setup_args()
    opt = parser.parse_args()
    opt0 = MODEL_OPTS[opt['model0']]
    opt1 = MODEL_OPTS[opt['model1']]

    opt0['persona_type'] = 'self'
    opt0['persona_datatype'] = 'test' # use test personas

    opt1['persona_type'] = 'self'
    opt1['persona_datatype'] = 'test' # use test personas

    self_chat(opt0, opt1)

# repetition controlled (in intbfw4 matchup)
# python parlai_internal/mturk/tasks/pairwise_dialogue_eval/model_self_chat.py -mf models:controllable_dialogue/convai2_finetuned_baseline -wd extrep_2gram:-3.5,extrep_nonstopword:-1e20,intrep_nonstopword:-1e20 -t convai2 --n_turns 6 --beam-size 20 --write-filename controllable_dialog/repetition_controlled_baseline_test
# intbfw4 model
# python parlai_internal/mturk/tasks/pairwise_dialogue_eval/model_self_chat.py -mf models:controllable_dialogue/convai2_finetuned_baseline -wd extrep_2gram:-3.5,extrep_nonstopword:-1e20,intrep_nonstopword:-1e20,nidf:4 -t convai2 --n_turns 6 --beam-size 20 --write-filename controllable_dialog/interesting_nidf_model_bfw_setting_04
# greedy
# python parlai_internal/mturk/tasks/pairwise_dialogue_eval/model_self_chat.py -mf models:controllable_dialogue/convai2_finetuned_baseline --beam-size 1 -t convai2 --n_turns 6 --write-filename controllable_dialog/greedy --n_chats 20

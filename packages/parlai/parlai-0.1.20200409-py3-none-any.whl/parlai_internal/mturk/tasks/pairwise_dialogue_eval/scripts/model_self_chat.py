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

ParlaiParser()  # instantiate to set PARLAI_HOME environment var
BASE_FILEPATH = os.path.join(os.environ['PARLAI_HOME'], 'data', 'pairwise_eval_experiments', 'convai2_self_chats')
os.makedirs(BASE_FILEPATH, exist_ok = True)

def setup_args():
    parser = ParlaiParser(True, True, '')
    parser.add_argument('--display-ignore-fields', type=str, default='')
    parser.add_argument('--n-turns', type=int, default=6)
    parser.add_argument('--n-chats', type=int, default=200)
    parser.add_argument('--write-filename', type=str, default=None)
    # by default we want to display info about the validation set
    # parser.set_defaults(datatype='valid')
    return parser


def get_filename(opt):
    filename = opt['write_filename']
    if filename is None:
        dir, filename = ntpath.split(opt['model_file'])
        filename = filename if filename else ntpath.basename(dir)
    return filename.replace('/', '_'), os.path.join(BASE_FILEPATH, filename.replace('/', '_') + '.jsonl')


def save_to_json_file(all_acts, agent0_persona, agent1_persona, filename, modelname, idnum):
    # pass
    json_dict = {}
    dialogs = []
    # print(all_acts)
    agent = np.random.choice(['model', 'other']) #randomly decide which side gets evaluated
    for act in all_acts:
        text = act['text']
        agent = 'model' if agent == 'other' else 'other'
        dialogs.append({'speaker': agent, 'text': text})
    json_dict['dialog'] = dialogs
    json_dict['model_name'] = modelname
    json_dict['model0_persona'] = agent0_persona
    json_dict['model1_persona'] = agent1_persona
    json_dict['pair_id'] = modelname + '_' + str(idnum)
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

def self_chat(opt):
    id = 0
    modelname, filename = get_filename(opt)
    # Create model and assign it to the specified task
    agent0 = create_agent(opt)
    # agent1 = create_agent_from_shared(agent0.share())
    agent1 = create_agent(opt)
    personas_generator = PersonasGenerator(opt)

    for i in range(opt['n_chats']):
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
                # print(agent0_persona_text)
                # print(agent1_persona_text)
                agent0.observe({
                    'text':'\n'.join([agent0_persona_text, '__SILENCE__']),
                    'id': 'SYSTEM',
                    'episode_done': False
                })
                act0 = agent0.act()
                # print(agent0.)
                # print(act0)
                act0_with_persona = deepcopy(act0)
                act0_with_persona['text'] = '\n'.join([agent1_persona_text, act0['text']])
                act0_with_persona['episode_done'] = False
                agent1.observe(deepcopy(act0_with_persona))
                act1 = agent1.act()
                act1['episode_done'] = False
                agent0.observe(deepcopy(act1))
            elif k >= opt['n_turns'] - 1:
                act0 = agent0.act()
                act0['episode_done'] = True
                agent1.observe(deepcopy(act0))
                act1 = agent1.act()
                act1['episode_done'] = True
                agent0.observe(deepcopy(act1))
            else:
                act0 = agent0.act()
                act0['episode_done'] = False
                agent1.observe(deepcopy(act0))
                act1 = agent1.act()
                act1['episode_done'] = False
                agent0.observe(deepcopy(act1))
            all_acts.append(act0)
            all_acts.append(act1)
            # print("ALL ACTS")
            # print(all_acts)
        save_to_json_file(
            all_acts, agent0_persona, agent1_persona, filename, modelname, id)
        id += 1

    agent0.shutdown()
    agent1.shutdown()


if __name__ == '__main__':
    parser = setup_args()
    opt = parser.parse_args()
    opt['persona_type'] = 'self'
    opt['persona_datatype'] = 'test' # use test personas
    print(opt)

    if opt['model'] == 'convai2_submissions.hf_sub2.ConvAI2_HF_submission_2.ftlm:FtlmAgent':
        print(opt['model'])
        parser.set_params(
            model='ftlm:FtlmAgent',
            model_file='models:convai2/ConvAI2_HF_submission_2/model',
            n_ctx=128,
            batchsize=1,
            numthreads=1,
            perso_permute=1,
            sample_interactive_personality=False,
            interactive_mode=True,
        )
    elif opt['model'] == 'convai2_submissions.LostInConversation.transformer_chatbot.agent:TransformerAgent':
        print(opt['model'])
        parser.set_defaults(model='agent:TransformerAgent',
                            sample=False,
                            wild_mode=False,
                            replace_repeat=False,
                            replace_ngram=False,
                            detokenize=False,
                            emoji_prob=0,
                            add_questions=0,
                            clean_emoji=False,
                            check_grammar=False,
                            correct_generative=False,
                            split_into_sentences=False,

                            max_seq_len=256,
                            beam_size=3,
                            annealing_topk=None,
                            annealing=0.6,
                            length_penalty=0.6)
    self_chat(opt)

# repetition controlled (in intbfw4 matchup)
# python parlai_internal/mturk/tasks/pairwise_dialogue_eval/model_self_chat.py -mf models:controllable_dialogue/convai2_finetuned_baseline -wd extrep_2gram:-3.5,extrep_nonstopword:-1e20,intrep_nonstopword:-1e20 -t convai2 --n_turns 6 --beam-size 20 --write-filename controllable_dialog/repetition_controlled_baseline_test
# intbfw4 model
# python parlai_internal/mturk/tasks/pairwise_dialogue_eval/model_self_chat.py -mf models:controllable_dialogue/convai2_finetuned_baseline -wd extrep_2gram:-3.5,extrep_nonstopword:-1e20,intrep_nonstopword:-1e20,nidf:4 -t convai2 --n_turns 6 --beam-size 20 --write-filename controllable_dialog/interesting_nidf_model_bfw_setting_04
# greedy
# python parlai_internal/mturk/tasks/pairwise_dialogue_eval/model_self_chat.py -mf models:controllable_dialogue/convai2_finetuned_baseline --beam-size 1 -t convai2 --n_turns 6 --write-filename controllable_dialog/greedy --n_chats 20

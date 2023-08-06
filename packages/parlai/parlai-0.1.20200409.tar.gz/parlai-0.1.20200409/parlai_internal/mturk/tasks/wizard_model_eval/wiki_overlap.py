#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import os
import pickle

from parlai.core.params import ParlaiParser
from parlai.core.agents import create_agent
from parlai.core.metrics import _f1_score
from parlai.core.worlds import create_task


"""Script for determining Wikipedia overlap with bot logs"""

ROOT_LIST = ['/private/home/edinan/ParlAI/data/wizard_eval/',
             '/private/home/roller/ParlAI/data/wizard_eval']

NAME_MAP = {
    'human_eval': 'A Human',
    'transformer_ranker': 'B Starved Retriever',
    'retrieval_no_knowledge': 'C Ignorant Retriever',
    'GenericWizardGeneratorAgent': 'D Ignorant Generator',
    'wizard_retrieval_interactive': 'E Retriever',
    'wizard_hierarchical': 'F Generator',
}

WIKI_MAP = '/private/home/kshuster/ParlAI/parlai_internal2/mturk/tasks/wizard_of_perZOna/data/title_to_passage.pkl'


def setup_args(parser=None):
    if parser is None:
        parser = ParlaiParser(True, True)
    # Get command line arguments
    parser.add_argument('-ltim', '--log-every-n-secs', type=float, default=2)
    parser.add_argument('--eval-type', type=str, default='mturk_logs',
                        choices=['mturk_logs', 'dataset'],
                        help='whether to do the evaluation on the available'
                             'mturk logs or the dataset')
    parser.set_defaults(datatype='train:ordered')
    parser.set_defaults(model='repeat_label')
    return parser


def set_up_sent_tok():
    try:
        import nltk
    except ImportError:
        raise ImportError('Please install nltk (e.g. pip install nltk).')
    # nltk-specific setup
    st_path = 'tokenizers/punkt/{0}.pickle'.format('english')
    try:
        sent_tok = nltk.data.load(st_path)
    except LookupError:
        nltk.download('punkt')
        sent_tok = nltk.data.load(st_path)
    return sent_tok


def avg(lst):
    return sum(lst) / len(lst)


def get_model_name(folder, name_map):
    for name in name_map.keys():
        if name in folder:
            return name
    return None


def get_log(filename, folder, root):
    file_log = None
    if 'incomplete' not in filename and 'live' in filename:
        file_path = os.path.join(root, folder, filename)
        with open(file_path, 'rb') as f:
            log = pickle.load(f)
        if (log['good_reasons'] != [] and log['bad_rounds'] != [] and
                log['chosen_topic'] != ''):
            file_log = log
    return file_log


def wiki_overlap(wiki_map, overlap_agent, root_list, name_map, sent_tok=None):
    results_dict = {v: {'seen': [], 'unseen': []} for k, v in name_map.items()}
    for root in root_list:
        for folder in os.listdir(root):
            model_name = get_model_name(folder, name_map)
            if model_name is not None:
                for file in os.listdir(os.path.join(root, folder)):
                    log = get_log(file, folder, root)
                    if log:
                        wiki_full = wiki_map[log['chosen_topic']]
                        wiki_list = wiki_full.split('\n')
                        if len(wiki_list) > 1:
                            combined = ' '.join(wiki_list[2:])
                            sentences = sent_tok.tokenize(combined)
                            wiki_text = ' '.join(sentences[:10])
                            bot_list = []
                            for line in log['dialog']:
                                if line[0] == 1:
                                    bot_list.append(line[1])
                            bot_text = ' '.join(bot_list)
                            if overlap_agent is None:
                                f1 = _f1_score(bot_text, [wiki_text])
                                key = 'seen' if log['seen'] else 'unseen'
                                results_dict[name_map[model_name]][key].append(f1)
                            else:
                                pass

    return results_dict


def task_overlap(opt, wiki_map, sent_tok):
    # Create model and assign it to the specified task
    results_dict = {'wiz': [], 'apprentice': []}
    agent = create_agent(opt, requireModelExists=True)
    world = create_task(opt, agent)
    episode_done = False
    wiz_list = []
    wiz_text = ''
    app_list = []
    app_text = ''

    while not world.epoch_done():
        if episode_done:
            episode_done = False
            wiz_list = []
            wiz_text = ''
            app_list = []
            app_text = ''
        world.parley()
        act = world.acts[0]
        chosen_topic = act.get('chosen_topic')
        text = act.get('text')
        if text != chosen_topic:
            app_list.append(text)
        labels = act.get('labels', act.get('eval_labels', ''))
        for l in labels:
            wiz_list.append(l)
        if act['episode_done']:
            wiki_full = wiki_map[chosen_topic]
            wiki_list = wiki_full.split('\n')
            if len(wiki_list) > 1:
                combined = ' '.join(wiki_list[2:])
                sentences = sent_tok.tokenize(combined)
                wiki_text = ' '.join(sentences[:10])
            wiz_text = ' '.join(wiz_list)
            wiz_f1 = _f1_score(wiz_text, [wiki_text])
            app_text = ' '.join(app_list)
            app_f1 = _f1_score(app_text, [wiki_text])
            results_dict['wiz'].append(wiz_f1)
            results_dict['apprentice'].append(app_f1)
            episode_done = True
    return results_dict


if __name__ == '__main__':
    parser = setup_args()
    opt = parser.parse_args(print_args=False)

    # load wiki map
    wiki_map = pickle.load(open(WIKI_MAP, 'rb'))
    # load overlap agent
    overlap_agent = None
    sent_tok = set_up_sent_tok()

    if opt['eval_type'] == 'mturk_logs':
        results = wiki_overlap(wiki_map, overlap_agent, ROOT_LIST, NAME_MAP, sent_tok)
        print('OVERLAP RESULTS:')
        for k, v in results.items():
            print(k, '\n~~~~~~~~')
            total = []
            for seen in v.keys():
                print(seen, ":", avg(v[seen]))
                total += v[seen]
            print('overall avg:', avg(total))
            print('\n')

    else:
        results = task_overlap(opt, wiki_map, sent_tok)
        print('OVERLAP RESULTS:')
        for k, v in results.items():
            print(k, ":", avg(v))
            print("num episodes:", len(v))

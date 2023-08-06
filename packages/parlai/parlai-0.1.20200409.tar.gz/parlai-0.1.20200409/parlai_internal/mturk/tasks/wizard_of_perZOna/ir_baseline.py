#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#
# Simple IR baselines.
# We plan to implement the following variants:
# Given an input message, either:
# (i) find the most similar message in the (training) dataset and output the response from that exchange; or
# (ii) find the most similar response to the input directly.
# (iii) if label_candidates are provided, simply ranks them according to their similarity to the input message.
#
# Additonally, TFIDF is either used (requires building a dictionary) or not,
# depending on whether you train on the train set first, or not.

import math
from collections.abc import Sequence
import heapq
import os
import pickle
import copy
import random
from collections import deque
from tqdm import tqdm

from parlai.core.agents import Agent
from parlai.core.dict import DictionaryAgent
from parlai.utils.misc import maintain_dialog_history
from parlai.core.worlds import create_task
from parlai.agents.repeat_label.repeat_label import RepeatLabelAgent
from parlai.core.teachers import create_task_agent_from_taskname


class MaxPriorityQueue(Sequence):
    def __init__(self, max_size):
        self.capacity = max_size
        self.lst = []

    def add(self, item, priority=None):
        if priority is None:
            priority = item
        if len(self.lst) < self.capacity:
            heapq.heappush(self.lst, (priority, item))
        elif priority > self.lst[0][0]:
            heapq.heapreplace(self.lst, (priority, item))

    def __getitem__(self, key):
        return sorted(self.lst)[key][1]

    def __len__(self):
        return len(self.lst)

    def __str__(self):
        return str([v for _, v in sorted(self.lst)])

    def __repr__(self):
        return repr([v for _, v in sorted(self.lst)])


stopwords = {'i', 'a', 'an', 'are', 'about', 'as', 'at', 'be', 'by',
             'for', 'from', 'how', 'in', 'is', 'it', 'of', 'on', 'or',
             'that', 'the', 'this', 'to', 'was', 'what', 'when', 'where',
             '--', '?', '.', "''", "''", "``", ',', 'do', 'see', 'want',
             'people', 'and', "n't", "me", 'too', 'own', 'their', '*',
             "'s", 'not', 'than', 'other', 'you', 'your', 'know', 'just',
             'but', 'does', 'really', 'have', 'into', 'more', 'also',
             'has', 'any', 'why', 'will'}


def score_match(query_rep, text, length_penalty, dictionary=None, debug=False):
    '''Compare similarity of text candidate (text) to the query (query_rep)'''
    if text == "":
        return 0
    if not dictionary:
        words = text.lower().split(' ')
    else:
        words = [w for w in dictionary.tokenize(text.lower())]
    score = 0
    rw = query_rep['words']
    used = {}
    for w in words:
        if w in rw and w not in used:
            score += rw[w]
            if debug:
                print("match: " + w)
        used[w] = True
    norm = math.sqrt(len(used))
    score = score / math.pow(norm * query_rep['norm'], length_penalty)
    return score


def rank_candidates(query_rep, cands, length_penalty, dictionary=None,
                    ir_method='ii', use_persona=False):
    """ Rank candidates given representation of query """
    if ir_method == 'iii':
        mpq = MaxPriorityQueue(100)
        for c in cands:
            score = score_match(query_rep, c, length_penalty, dictionary)
            mpq.add(c, score)
        return list(reversed(mpq))
    elif ir_method == 'i':
        score = [0] * len(cands)
        for i, info in enumerate(cands):
            c = info['msg']
            if use_persona:
                c = info['persona_prev'] + c
            score[i] = -score_match(query_rep, c, length_penalty, dictionary)
        r = [i[0] for i in sorted(enumerate(score), key=lambda x:x[1])]
        res = []
        for i in range(min(100, len(score))):
            res.append(cands[r[i]]['resp_msg'])
        # print(score[r[0]])
        return res
    elif ir_method == 'ii':
        score = [0] * len(cands)
        for i, info in enumerate(cands):
            c = info['msg']
            if use_persona:
                c = info['persona'] + c
            score[i] = -score_match(query_rep, c, length_penalty, dictionary)
        r = [i[0] for i in sorted(enumerate(score), key=lambda x:x[1])]
        sorted_score = [-s for s in sorted(score)]
        res = []
        for i in range(min(100, len(score))):
            res.append(cands[r[i]]['msg'])
        # print(score[r[0]])
        return res, sorted_score[:len(res)]


class IrBaselineAgent(Agent):

    @staticmethod
    def dictionary_class():
        return DictionaryAgent

    @staticmethod
    def add_cmdline_args(argparser):
        IrBaselineAgent.dictionary_class().add_cmdline_args(argparser)
        agent = argparser.add_argument_group('IrBaseline Arguments')
        agent.add_argument(
            '-lp', '--length_penalty', default=0.5,
            help='length penalty for responses')
        agent.add_argument('-hist', '--history-length', default=100000,
                           type=int,
                           help='Number of past tokens to remember. '
                                'Default remembers 100000 tokens.')
        agent.add_argument('-histr', '--history-replies',
                           default='label_else_model', type=str,
                           choices=['none', 'model', 'label',
                                    'label_else_model'],
                           help='Keep replies in the history')
        agent.add_argument('--ret-task', type=str, default='personachat',
                           help='which task to use for retrieval')
        agent.add_argument('-keepp', '--keep-persona',
                           default=False, type='bool',
                           choices=[False, True],
                           help='Keep persona mentions in the history')
        agent.add_argument('--use-persona', default=False,
                           help="whether to use persona in messages")
        agent.add_argument('-ir', '--ir-method', type=str, default='ii',
                           choices=['i', 'ii', 'iii'],
                           help='Which IR Method to use')


    def __init__(self, opt, shared=None):
        super().__init__(opt)
        self.id = 'IRBaselineAgent'
        self.length_penalty = float(opt['length_penalty'])
        self.dictionary = DictionaryAgent(opt)
        self.datafile = os.path.join(opt['datapath'], 'personachat', 'data_dialogs.pkl')
        self.ir_method = opt.get('ir_method', 'i')
        self.use_persona = opt.get('use_persona')
        self.retriever_task = opt['ret_task']
        self.opt = opt
        self.load_data()
        self.history = {}
        self.persona = {}

    def observe(self, observation):
        obs = observation.copy()
        # keep profile lines
        if self.opt['keep_persona']:
            lines = obs['text'].split('\n')
            for l in lines:
                if 'persona' in l:
                    self.persona[l] = True
        # END
        history = maintain_dialog_history(
            self.history, obs,
            historyLength=self.opt['history_length'],
            useReplies=self.opt['history_replies'],
            dict=None, useStartEndIndices=False)
        text = ''
        # keep profile lines
        if self.opt['keep_persona']:
            for l in self.persona.keys():
                text += l + '\n'
        # END
        for i in range(len(history)):
            text += history[i] + '\n'

        obs['text_history'] = text
        self.observation = obs
        self.dictionary.observe(observation)
        return obs

    def act(self):
        if self.opt.get('datatype', '').startswith('train'):
            self.dictionary.act()

        obs = self.observation
        reply = {}
        reply['id'] = self.getID()
        rep = self.build_query_representation(obs['text_history'])
        # Rank candidates
        if self.ir_method == 'i':
            '''Compare to all message exchanges'''
            if self.retriever_task == 'personachat':
                candidates = self.dialog_exchanges
            else:
                candidates = self.exs
        elif self.ir_method == 'ii':
            '''Compare to all messages'''
            if self.retriever_task == 'personachat':
                candidates = self.messages
            else:
                candidates = self.exs
        elif (self.ir_method == 'iii' and 'label_candidates' in obs
              and len(obs['label_candidates']) > 0):

            '''Compare to label_candidates'''
            candidates = obs['label_candidates']

        if candidates is not None:
            cands, scores = rank_candidates(rep, candidates,
                            self.length_penalty, self.dictionary, self.ir_method)
            reply['text_candidates'] = cands
            reply['text'] = reply['text_candidates'][0]
        else:
            reply['text'] = "I don't know."

        return reply

    def save(self, fname=None):
        fname = self.opt.get('model_file', None) if fname is None else fname
        if fname:
            self.dictionary.save(fname + '.dict')

    def load(self, fname):
        self.dictionary.load(fname + '.dict')

    def load_data(self):
        if self.retriever_task == 'personachat':
            self.load_personachat_data()
        else:
            self.load_task_data()

    def load_task_data(self, context_length=-1, include_labels=True):
        self.exs = []
        task = self.retriever_task
        ordered_opt = self.opt.copy()
        dt = ordered_opt.get('datatype', '').split(':')
        dt = ':'.join([dt[0], 'ordered'] + dt[1:])
        if 'stream' not in dt:
            dt += ':stream'
        ordered_opt['datatype'] = dt
        ordered_opt['batchsize'] = 1
        ordered_opt['numthreads'] = 1
        ordered_opt['task'] = task

        teacher = create_task_agent_from_taskname(ordered_opt)[0]
        episode_done = False
        current = []
        context_length = context_length if context_length >= 0 else None
        context = deque(maxlen=context_length)
        with tqdm(total=teacher.num_episodes()) as pbar:
            while not teacher.epoch_done():
                # collect examples in episode
                while not episode_done:
                    action = teacher.act()
                    current.append(action)
                    episode_done = action['episode_done']

                for ex in current:
                    if 'text' in ex:
                        text = ex['text']
                        context.append(text)
                        if len(context) > 1:
                            text = '\n'.join(context)

                    # add labels to context
                    labels = ex.get('labels', ex.get('eval_labels'))
                    label = None
                    if labels is not None:
                        label = random.choice(labels)
                        if include_labels:
                            context.append(label)
                    text = text + (label if label is not None else "")
                    self.exs.append({'msg': text})
                    self.dictionary.observe({'text': text})
                    self.dictionary.act()
                pbar.update()

                # reset flags and content
                episode_done = False
                current.clear()
                context.clear()

    def load_personachat_data(self):
        '''Load the data dialogs, which are used as candidates'''
        datapath = os.getcwd() + '/data/wizard_of_perZOna/ir_baseline_data/'
        dialogs_path = datapath + 'dialogs.pkl'
        messages_path = datapath + 'messages.pkl'
        if os.path.exists(dialogs_path) and os.path.exists(messages_path):
            with open(dialogs_path, 'rb') as f:
                self.dialog_exchanges = pickle.load(f)
            with open(messages_path, 'rb') as f:
                self.messages = pickle.load(f)
        else:
            print('---Extracting and saving personachat dialogs---')
            opt = copy.deepcopy(self.opt)
            opt['task'] = 'personachat:both'
            opt['task'] += 'Revised' if self.opt.get('revised') else 'Original'
            opt['datatype'] = 'train:ordered:stream'
            opt['numthreads'] = 1
            opt['batchsize'] = 1

            agent = RepeatLabelAgent(opt)
            world = create_task(opt, agent)
            teacher = world.agents[0]

            self.dialog_exchanges = []
            self.messages = []
            new_episode = True
            turn = 0
            msg = None
            personas = []
            while not teacher.epoch_done():
                act = teacher.act()
                text = act['text']
                if new_episode:
                    persona_text = text.split('\n')[:-1]
                    persona_1 = [p for p in persona_text if 'your persona:' in p]
                    persona_2 = [p for p in persona_text if 'partner\'s persona:' in p]
                    persona_1 = [p[p.find(':')+1:] for p in persona_1]
                    persona_2 = [p[p.find(':')+1:] for p in persona_2]
                    personas = [persona_1, persona_2]
                    turn = 0
                    msg = text.split('\n')[-1]
                else:
                    msg = text
                resp_msg = act['labels'][0]
                turn += 1
                dlg = {'msg': msg, 'resp_msg': resp_msg}
                message = {'msg': msg}
                if self.use_persona:
                    dlg['persona_prev'] = personas[(turn-1) % 2]
                    dlg['persona_resp'] = personas[turn % 2]
                    message['persona'] = personas[turn % 2]
                self.dialog_exchanges.append(dlg)
                self.messages.append(message)
                new_episode = act['episode_done']

            '''Save Dialogs and Messages'''
            if not os.path.exists(datapath):
                os.makedirs(datapath)
            with open(dialogs_path, 'wb') as f:
                pickle.dump(self.dialog_exchanges, f)
            with open(messages_path, 'wb') as f:
                pickle.dump(self.messages, f)

        '''Set up dictionary'''
        for message in self.messages:
            self.dictionary.observe({'text': message['msg']})
            self.dictionary.act()

    def build_query_representation(self, query):
        """ Build representation of query, e.g. words or n-grams """
        rep = {}
        rep['words'] = {}
        words = [w for w in self.dictionary.tokenize(query.lower())]
        rw = rep['words']
        used = {}
        for w in words:
            if len(self.dictionary.freqs()) > 0:
                rw[w] = 1.0 / (1.0 + math.log(1.0 + self.dictionary.freqs()[w]))
            else:
                if w not in stopwords:
                    rw[w] = 1
            used[w] = True
        norm = len(used)
        rep['norm'] = math.sqrt(len(words))
        return rep

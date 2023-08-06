#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Simple agent which repeats back the labels sent to it.

By default, replies with a single random label from the list of labels sent to
it, if any. If the ``label_candidates`` field is set, will fill the ``text_candidates``
field with up to a hundred randomly selected candidates (the first text
candidate is the selected label).

Options:

    ``returnOneRandomAnswer`` -- default ``True``, set to ``False`` to instead
    reply with all labels joined by commas.

    ``cantAnswerPercent`` -- default ``0``, set value in range[0,1] to set
    chance of replying with "I don't know."
"""

import random

from parlai.core.agents import Agent


class PreprocessAgent(Agent):
    @staticmethod
    def add_cmdline_args(argparser):
        group = argparser.add_argument_group('Preprocess Arguments')
        group.add_argument('--knowledge-dropout', type=float, default=0,
                           help='set value in range[0,1] to set chance of '
                           'dropping out knowledge')
    def __init__(self, opt, shared=None):
        super().__init__(opt)
        self.id = 'PreprocessAgent'
        self.history = ''
        self.newEpisode = True

    def history_append(self, t):
        if self.history != '':
            self.history = self.history + '\n' + t
        else:
            self.history = t
    
    def act(self):
        obs = self.observation.copy()
        if self.newEpisode:
            self.history = ''
            self.newEpisode = False
        #if 'chosen_topic' in obs:
        #    self.history_append('_chosen_topic ' + obs.get('chosen_topic', ''))
        knol_txt = []
        if 'knowledge' in obs:
            if 'checked_sentence' in obs:
                checked = obs.get('checked_sentence')
            else:
                checked = ''
            knol = obs.get('knowledge').split('\n')
            for k in knol:
                if (random.random() > self.opt['knowledge_dropout']
                    or checked in k):
                    knol_txt.append('_knowledge ' + k)
        knol_txt = '\n'.join(knol_txt)
        self.history_append("_speaker1 " + obs.get('text', ''))
        if obs.get('episode_done') is True:
            self.newEpisode = True
        obs['text'] = self.history
        if knol_txt != '':
            obs['text'] = knol_txt + "\n" + obs['text']
        obs['episode_done'] = True
        self.history_append("_speaker2 " + obs.get('label', obs.get('eval_labels', ['']))[0])
        print("*********")
        print(obs['text'])
        print("*********")
        print(len(self.history.split('\n')), len((self.history.split(' '))))
        return obs

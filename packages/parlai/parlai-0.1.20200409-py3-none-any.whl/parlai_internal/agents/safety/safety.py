#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from parlai.agents.bert_classifier.bert_classifier import BertClassifierAgent, surround
from parlai.core.torch_classifier_agent import TorchClassifierAgent
from parlai.utils.misc import padded_3d
import torch
import os
import pdb

class BertClassifierLastSentenceAgent(BertClassifierAgent):
    """ Treats the last sentence of the history as the 'next sentence'
        in BERT setting. Only works when '\n' is used as separator.
    """

    def observe(self, obs):
        # Not sure if that is easily compatible with history
        if not obs['episode_done']:
            raise Exception('Sorry this agent wont work with history size>0 for now')
        if 'text' in obs:
            text = obs['text']
            splited = text.split('\n')
            if len(splited) > 1:
                obs['text'] = '\n'.join(splited[0:-1])
                obs['last_utt'] = splited[-1]
            else:
                obs['text'] = ''
                obs['last_utt'] = text
        return super().observe(obs)

    def vectorize(self, obs, history, add_start=True, add_end=True,
                  text_truncate=None, label_truncate=None):
        super().vectorize(obs, history, add_start, add_end, text_truncate, label_truncate)
        if 'last_utt' in obs and 'last_utt_vec' not in obs:
            obs['last_utt_vec'] = self._vectorize_text(obs['last_utt'], False,
                                                       add_end, 72, False)
        return obs

    def batchify(self, obs_batch, sort=False):
        batch = super().batchify(obs_batch, sort)
        new_text_vecs = []
        segment_vecs = []
        for o in obs_batch:
            if not self.is_valid(o):
                continue
            new_text_vecs.append(
                torch.cat([o['text_vec'],
                o['last_utt_vec']], 0))
            segment_vecs.append(
                torch.cat([o['text_vec'] * 0,
                o['last_utt_vec'] * 0 + 1], 0))
        batch['text_vec'] = padded_3d([new_text_vecs],
                                        use_cuda=self.use_cuda,
                                        fp16friendly= self.fp16)[0]
        batch['segment_vecs'] = padded_3d([segment_vecs],
                                        use_cuda=self.use_cuda,
                                        fp16friendly= self.fp16)[0]
        return batch

    def score(self, batch):
        token_idx = batch['text_vec']
        segments_idx = batch['segment_vecs']
        mask = (token_idx != self.NULL_IDX).long()
        token_idx = token_idx * mask
        return self.model(token_idx, segments_idx, mask)

    def _set_text_vec(self, obs, history, truncate):
        obs = super()._set_text_vec(obs, history, truncate)
        if obs is not None and 'text_vec' in obs:
            obs['text_vec'] = surround(obs['text_vec'], self.START_IDX,
                                       self.END_IDX)
        return obs

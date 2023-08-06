#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from parlai.utils.distributed import is_distributed
from parlai.core.torch_ranker_agent import TorchRankerAgent
from parlai.zoo.bert.build import download

from .bert_dictionary import BertDictionaryAgent
from .helpers import (BertWrapper, BertModel, get_bert_optimizer, get_adamax_optimizer,
                      add_common_args, surround, MODEL_PATH, get_bert_model)

import os
import torch
import pdb


class CrossEncoderRankerDupAgent(TorchRankerAgent):
    """ Exact same thing as BERT
    """

    @staticmethod
    def add_cmdline_args(parser):
        add_common_args(parser)

    def __init__(self, opt, shared=None):
        # download pretrained models
        download(opt['datapath'])
        self.pretrained_path = os.path.join(opt['datapath'], 'models',
                                            'bert_models', MODEL_PATH)
        opt['pretrained_path'] = self.pretrained_path

        super().__init__(opt, shared)
        # it's easier for now to use DataParallel when
        self.data_parallel = opt.get('data_parallel') and self.use_cuda
        if self.data_parallel:
            self.model = torch.nn.DataParallel(self.model)
        if is_distributed():
            raise ValueError('Cannot combine --data-parallel and distributed mode')
        self.clip = -1
        self.set_special_idx()

    def set_special_idx(self):
        self.NULL_IDX = self.dict.pad_idx
        self.START_IDX = self.dict.start_idx
        self.END_IDX = self.dict.end_idx

    def build_model(self):
        self.model = BertWrapper(
            get_bert_model(self.opt),
            1,
            add_transformer_layer=self.opt['add_transformer_layer'],
            layer_pulled=self.opt['pull_from_layer'],
            aggregation=self.opt['bert_aggregation'],
            scaling=self.opt['scaling']
        )

    def init_optim(self, params, optim_states=None, saved_optim_type=None):
        if self.opt['optimizer'] == 'adam':
            self.optimizer = get_bert_optimizer([self.model],
                                                self.opt['type_optimization'],
                                                self.opt['learningrate'],
                                                fp16=self.opt.get('fp16'),
                                                no_decay=True)
        elif self.opt['optimizer'] == 'adam_decay':
            self.optimizer = get_bert_optimizer([self.model],
                                                self.opt['type_optimization'],
                                                self.opt['learningrate'],
                                                fp16=self.opt.get('fp16'),
                                                no_decay=False)
        elif self.opt['optimizer'] == 'adamax':
            self.optimizer = get_adamax_optimizer([self.model],
                                                self.opt['type_optimization'],
                                                self.opt['learningrate'],
                                                fp16=self.opt.get('fp16'))

    def score_candidates(self, batch, cand_vecs, cand_encs=None):
        # concatenate text and candidates (not so easy)
        # unpad and break
        nb_cands = cand_vecs.size()[1]
        size_batch = cand_vecs.size()[0]
        text_vec = batch.text_vec
        tokens_context = text_vec.unsqueeze(
            1).expand(-1, nb_cands, -1).contiguous().view(nb_cands * size_batch, -1)
        segments_context = tokens_context * 0
        size_token_rect = text_vec.size(1)


        tokens_cands = cand_vecs.view(nb_cands * size_batch, -1)
        segments_cands = tokens_cands * 0 + 1
        all_tokens = torch.cat([tokens_context, tokens_cands], 1).cpu()
        all_segments = torch.cat([segments_context, segments_cands], 1).cpu()
        nb_not_null_cand = torch.sum((tokens_cands != self.NULL_IDX).long(), dim=1).cpu()
        nb_not_null_tokens = torch.sum((tokens_context != self.NULL_IDX).long(), dim=1).cpu()
        new_all_tokens = 0 * all_tokens + self.NULL_IDX
        new_all_segments = 0 * all_segments + self.NULL_IDX
        for i in range(all_tokens.size(0)):
            num_tok = nb_not_null_tokens[i]
            num_cand = nb_not_null_cand[i]
            new_all_tokens[i][0:num_tok] = all_tokens[i][0:num_tok]
            new_all_tokens[i][num_tok:num_tok+num_cand] = all_tokens[i][size_token_rect:size_token_rect + num_cand]
            new_all_segments[i][0:num_tok] = all_segments[i][0:num_tok]
            new_all_segments[i][num_tok:num_tok + num_cand] = all_segments[i][size_token_rect:size_token_rect + num_cand]
        if self.use_cuda:
            new_all_tokens = new_all_tokens.cuda()
            new_all_segments = new_all_segments.cuda()

        all_mask = (new_all_tokens != self.NULL_IDX)
        new_all_tokens *= all_mask.long()
        scores = self.model(new_all_tokens, new_all_segments, all_mask)
        return scores.view(size_batch, nb_cands)

    @staticmethod
    def dictionary_class():
        return BertDictionaryAgent

    def _set_text_vec(self, *args, **kwargs):
        obs = super()._set_text_vec(*args, **kwargs)
        # concatenate the [CLS] and [SEP] tokens
        if obs is not None and 'text_vec' in obs:
            obs['text_vec'] = surround(obs['text_vec'], self.START_IDX,
                                       self.END_IDX)
        return obs

    def _set_label_vec(self, *args, **kwargs):

        return super()._set_label_vec(args[0], self.opt['reddit_initialization'], True, args[3])

    def _set_label_cands_vec(self, *args, **kwargs):
        return super()._set_label_cands_vec(args[0], self.opt['reddit_initialization'], True, args[3])

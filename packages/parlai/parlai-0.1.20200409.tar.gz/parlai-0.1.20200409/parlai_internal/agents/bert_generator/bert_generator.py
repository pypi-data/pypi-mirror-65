#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
Fine tune BERT as an autoregressive model.

Uses TGA to generate using BERT.
"""

import os
from parlai.core.torch_generator_agent import TorchGeneratorAgent, TorchGeneratorModel
from parlai.zoo.bert.build import download
from parlai.utils.torch import neginf

from parlai.agents.bert_ranker.bert_dictionary import BertDictionaryAgent
from parlai.agents.bert_ranker.helpers import BertModel, MODEL_PATH

import torch
import torch.nn as nn


class _BertEncoderModule(nn.Module):
    """No-op encoder module."""
    # We can't cache any encoder states so just pass through.
    def forward(self, x):
        return x


class _BertDecoderModule(nn.Module):
    """
    BERT decoder.

    Concatenates the context and decoder input, masks autoregressively,
    and treats the problem as generation.
    """
    def __init__(self, bert_model):
        super().__init__()
        self.bert_model = bert_model

    def forward(self, inputs, context, incr_state=None):
        together = torch.cat([context, inputs], dim=1)
        type_ids = torch.cat(
            [torch.zeros_like(context), torch.ones_like(inputs)],
            dim=1
        )
        # need to make a very complicated mask
        # Consider the context A, B, C, PAD, PAD
        # and the output is D, E, F
        # the full sequence will be ABCPPDEF
        # TS  A B C P P    D E F
        #   A 1 1 1 0 0    0 0 0
        #   B 1 1 1 0 0    0 0 0
        #   C 1 1 1 0 0    0 0 0
        #   P 1 1 1 0 0    0 0 0
        #   P 1 1 1 0 0    0 0 0
        #
        #   D 1 1 1 0 0    0 0 0
        #   E 1 1 1 0 0    1 0 0
        #   F 1 1 1 0 0    1 1 0

        bsz, itime = inputs.shape
        bsz, ctime = context.shape
        bsz, btime = together.shape
        left = (context != 0).unsqueeze(1).expand(bsz, btime, ctime)

        lower_right = torch.tril(inputs.new(itime, itime).fill_(1), 0).byte()
        upper_right = lower_right.new(ctime, itime).zero_()
        right = torch.cat(
            [upper_right, lower_right], dim=0
        ).unsqueeze(0).expand(bsz, btime, itime) == 1

        attention_mask = torch.cat([left, right], dim=2).unsqueeze(1)
        dtype = next(self.parameters()).dtype
        attention_mod = (~attention_mask).type(dtype) * neginf(dtype)
        embeddings = self.bert_model.embeddings(together, type_ids)
        output = self.bert_model.encoder(embeddings, attention_mod, False)[0]
        # now we only want the encodings of the decoder side
        output = output[:, ctime:, :]
        return output, None


class _BertGeneratorModel(TorchGeneratorModel):
    def __init__(self, bert_model, bert_dict):
        super().__init__(
            padding_idx=bert_dict.pad_idx,
            start_idx=bert_dict.end_idx,
            end_idx=bert_dict.end_idx,
        )
        self.encoder = _BertEncoderModule()
        self.decoder = _BertDecoderModule(bert_model)

    def reorder_encoder_states(self, encoder_states, indices):
        return torch.index_select(encoder_states, 0, indices)

    def output(self, hid):
        bsz, time, dim = hid.shape
        wemb = self.decoder.bert_model.embeddings.word_embeddings.weight
        flat = hid.reshape(bsz * time, dim)
        return flat.matmul(wemb.t()).reshape(bsz, time, -1)

    def reorder_decoder_incremental_state(self, *args, **kwargs):
        return None


class BertGeneratorAgent(TorchGeneratorAgent):
    """
    BERT generator agent.
    """

    @staticmethod
    def dictionary_class():
        return BertDictionaryAgent

    def __init__(self, opt, shared=None):
        if shared is None:
            download(opt['datapath'])
            self.pretrained_path = os.path.join(
                opt['datapath'], 'models', 'bert_models', MODEL_PATH
            )
        super().__init__(opt, shared)

    def build_model(self):
        self.model = _BertGeneratorModel(
            BertModel.from_pretrained(self.pretrained_path),
            self.dict,
        )
        if self.use_cuda:
            self.model.cuda()
        return self.model

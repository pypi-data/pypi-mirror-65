#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import math
import torch
import torch.nn as nn
from torch.nn.parameter import Parameter
from torch.autograd import Variable, Function
from torch.nn.utils.rnn import pad_packed_sequence, pack_padded_sequence
import torch.nn.functional as F


class Starspace(nn.Module):
    def __init__(self, opt, num_features):
        super().__init__()
        self.lt = nn.Embedding(
            num_features,
            opt['embeddingsize'],
            0,
            sparse=True,
            max_norm=opt['embeddingnorm'],
        )
        self.encoder = Encoder(self.lt)
        if not opt['share_embeddings']:
            print("2nd embeddings!! " + str(opt['learningrate']))
            self.lt2 = nn.Embedding(
                num_features,
                opt['embeddingsize'],
                0,
                sparse=True,
                max_norm=opt['embeddingnorm'],
            )
            self.encoder2 = Encoder(self.lt2)
        else:
            self.encoder2 = self.encoder
        # self.lt = nn.EmbeddingBag(num_features, opt['embeddingsize'], 0)
        # self.lsm = nn.LogSoftmax()
        # self.cos = nn.CosineSimilarity(dim=1, eps=1e-6)
        self.opt = opt

    def forward(self, xs, ys=None, cands=None):
        scores = None
        if ys is not None:
            # training
            xs_enc = []
            ys_enc = []
            xs_emb = self.encoder(xs)
            xs_enc.append(xs_emb)
            ys_enc.append(self.encoder2(ys))
            for c in cands:
                xs_enc.append(xs_emb)
                c_emb = self.encoder2(c)
                ys_enc.append(c_emb)
        else:
            # test stuff, deal with later
            xs_enc = []
            ys_enc = []
            xs_emb = self.encoder(xs)
            c_scores = []
            for c in cands:
                xs_enc.append(xs_emb)
                c_emb = self.encoder2(c)
                ys_enc.append(c_emb)
            # import pdb; pdb.set_trace()
        return torch.cat(xs_enc), torch.cat(ys_enc)


class Encoder(nn.Module):
    def __init__(self, shared_lt):
        super().__init__()
        self.lt = shared_lt

    def forward(self, xs):
        xs_emb = self.lt(xs).mean(1)
        return xs_emb

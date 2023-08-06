#!/usr/bin/env python3

import torch
import torch.nn as nn


class Ranker(nn.Module):

    ''' Abstract class to be used by all rankers.
        >>> ranker = SimpleRanker(10, enc_ans, idx_ans)
        >>> res = ranker(new_context)
        input : [nc, dim] FloatTensor
        output: [nc, k] LongTensor, indexes of the k closest element
                among the candidates
    '''

    def __init__(self, k, enc_ans, idx_ans=None, enc_ctx=None, idx_ctx=None, padix=None):
        super().__init__()
        self.k = k
        self.enc_ans = enc_ans  # [nc, dim] FloatTensor
        self.idx_ans = idx_ans  # [nc, pad] LongTensor
        self.enc_ctx = enc_ctx  # [nc, dim] FloatTensor
        self.idx_ctx = idx_ctx  # [nc, pad] LongTensor
        self.padix = padix
        self.init()

    def init(self):  # if there needs to pass down other things
        pass


class SimpleRanker(Ranker):

    def forward(self, contexts):
        sims = contexts.mm(self.enc_ans.t())  # [nctxts, ncands]
        _, ixs = sims.topk(self.k, dim=1)
        return ixs


class NormalizedRanker(Ranker):

    def init(self):
        self.enc_ans /= self.enc_ans.norm(2, dim=1, keepdim=True)

    def forward(self, contexts):
        sims = (contexts / contexts.norm(2, dim=1, keepdim=True)).mm(self.enc_ans.t())
        _, ixs = sims.topk(self.k, dim=1)
        return ixs


class OneHopRanker(Ranker):

    ''' Averages the k most similar contexts to the query, then gets the k most
        similar answers
    '''

    def init(self):
        assert self.enc_ctx is not None
        self.ranker1 = SimpleRanker(self.k, self.enc_ans, self.idx_ans)
        self.ranker2 = SimpleRanker(self.k, self.enc_ctx, self.idx_ctx)

    def forward(self, contexts):
        c_ixs = self.ranker2(contexts)  # [nctxts, k]
        new_contexts = torch.cat([
            self.enc_ctx[ixs].mean(dim=0, keepdim=True)
            for ixs in c_ixs
        ])  # [nc, d]
        return self.ranker1(new_contexts)


class OneHopNormalizedRanker(OneHopRanker):

    def init(self):
        assert self.enc_ctx is not None
        self.ranker1 = NormalizedRanker(self.k, self.enc_ans, self.idx_ans)
        self.ranker2 = NormalizedRanker(self.k, self.enc_ctx, self.idx_ctx)


class ShortestRanker(SimpleRanker):

    ''' Simple rank, keep top k, choose the shortest answer among top k.
        Less talk, less mistakes, hopefully.
    '''

    def forward(self, contexts):
        sixs = super().forward(contexts)
        rerank = [
            ixs[(self.idx_ans[ixs] != self.padix).sum(1).sort()[1]].view(1, -1)
            for ixs in sixs
        ]
        return torch.cat(rerank)

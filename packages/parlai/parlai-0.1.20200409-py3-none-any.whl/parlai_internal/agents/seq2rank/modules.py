#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from parlai.agents.seq2seq.modules import pad, Seq2seq, Encoder, Decoder
from parlai.core.logs import TensorboardLogger
import torch
import torch.nn as nn
import torch.nn.functional as F


class Seq2rank(Seq2seq):
    def __init__(self, opt, num_features, **kwargs):
        opt_copy = opt.copy()
        opt_copy['rank_candidates'] = False
        super().__init__(opt_copy, num_features, **kwargs)
        self.rank = opt['rank_candidates']

        if self.rank:
            opt_lt = opt.get('rank_lookuptable')
            shared_lt = (
                self.decoder.lt
                if opt_lt == 'dec'
                else self.encoder.lt
                if opt_lt == 'enc'
                else None
            )
            shared_dec = (
                self.decoder if opt.get('rank_comparator') == 'decode' else None
            )
            self.rank_input = opt.get('rank_input', 'outputmean')
            self.ranker = Ranker(
                num_features,
                padding_idx=self.NULL_IDX,
                emb_size=opt['embeddingsize'],
                hidden_size=opt['hiddensize'],
                inp_type=opt.get('rank_input', 'outputmean'),
                enc_type=opt.get('rank_encoder', 'bowmean'),
                cmp_type=opt.get('rank_comparator', 'dot'),
                shared_lt=shared_lt,
                decoder=shared_dec,
                attn_type=opt['attention'],
            )
        if opt['tensorboard_log'] is True:
            self.writer = TensorboardLogger(opt)

    def forward(
        self,
        xs,
        ys=None,
        cands=None,
        valid_cands=None,
        prev_enc=None,
        rank_during_training=False,
    ):
        """Get output predictions from the model.

        Arguments:
        xs -- input to the encoder
        ys -- expected output from the decoder
        cands -- set of candidates to rank, if applicable
        valid_cands -- indices to match candidates with their appropriate xs
        prev_enc -- if you know you'll pass in the same xs multiple times and
            the model is in eval mode, you can pass in the encoder output from
            the last forward pass to skip recalcuating the same encoder output
        rank_during_training -- (default False) if set, ranks the minibatch of
            labels
        """
        out = super().forward(xs, ys=ys, prev_enc=prev_enc)
        predictions, scores, encoder_states = out[0], out[1], out[4]

        start = self.START.detach()
        enc_out, hidden, attn_mask = encoder_states

        # self.writer.add_scalar('test', 100)

        cand_preds, cand_scores = None, None
        if self.rank:
            rank_inp = enc_out if self.rank_input.startswith('output') else hidden
            decode_params = (start, hidden, enc_out, attn_mask)
            if isinstance(rank_inp, tuple):
                rank_inp = rank_inp[0]  # use hidden not cell state
            if self.training:
                if rank_during_training:
                    # during training, only do ranking half the time
                    cand_preds, cand_scores = self.ranker(
                        rank_inp, ys, decode_params=decode_params
                    )
            elif cands is not None:
                cand_preds, cand_scores = self.ranker(
                    rank_inp, cands, valid_cands, decode_params=decode_params
                )

        return predictions, scores, cand_preds, cand_scores, encoder_states


class Ranker(nn.Module):
    def __init__(
        self,
        num_features,
        emb_size=128,
        hidden_size=128,
        padding_idx=0,
        inp_type='outputmean',
        enc_type='bowmean',
        cmp_type='dot',
        shared_lt=None,
        sparse=False,
        dropout=0.1,
        decoder=None,
        attn_type='none',
    ):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        self.inp_type = inp_type  # what input is used as context
        self.enc_type = enc_type  # how to encode candidates
        self.cmp_type = cmp_type  # how to compare candidates with context

        if self.enc_type.startswith('bow'):
            # bag of words
            if shared_lt:
                # copy other lt
                self.lt = shared_lt
            else:
                # create own lt
                self.lt = nn.Embedding(
                    num_features, emb_size, padding_idx=padding_idx, sparse=sparse
                )

        if self.cmp_type == 'mlp':
            # simple mlp. different mlp archs were not explored much
            self.mlp = nn.Sequential(
                nn.Linear(emb_size + hidden_size, hidden_size),
                nn.Tanh(),
                nn.Linear(hidden_size, 1),
            )
        elif self.cmp_type == 'bilinear':
            # bilinear. this does not appear to outperform dot.
            self.h2e = lambda x: x
            self.bilinear = nn.Bilinear(hidden_size, emb_size, 1, bias=False)
        elif self.cmp_type == 'decode':
            # use decoder scores to rank. this isn't good.
            self.decoder = decoder
            self.NULL_IDX = padding_idx
            self.attn_type = attn_type
        else:
            # set up hsz => esz dim reduction for other comparators
            self.h2e = nn.Linear(hidden_size, emb_size, bias=False)

    def transform_context(self, input):
        """Transform the encoder context to (bsz x esz) vector."""
        if self.inp_type.startswith('output'):
            # we have all of the output states from the encoder
            emb = self.dropout(self.h2e(input))
            if self.inp_type.endswith('mean'):
                return emb.mean(1)
            if self.inp_type.endswith('sum'):
                return emb.sum(1)
            if self.inp_type.endswith('max'):
                return self.h2e(input.max(1)[0])
        elif self.inp_type == 'hidden':
            # just use the hidden state
            return self.h2e(input[-1])
        elif self.inp_type == 'cell':
            # just use the cell state
            return self.h2e(input[-2])

    def encode(self, input):
        """Encode the candidates so we get (** x esz) vector."""
        if self.enc_type.startswith('bow'):
            emb = self.dropout(self.lt(input))
            # embed returns ** x esz, return operation over dimension before it
            if self.enc_type.endswith('mean'):
                return emb.mean(dim=-2)
            elif self.enc_type.endswith('sum'):
                return emb.sum(dim=-2)
            elif self.enc_type.endswith('max'):
                return emb.max(dim=-2)[0]
        elif self.enc_type.startswith('rnn'):
            # TODO?  very slow so haven't tried
            pass
        raise RuntimeError(f'enc_type {self.enc_type} not implemented yet.')

    def compare(self, a, b):
        """Compare encoder context vs candidate representations.

        You'll see checks for dimensions below that handle whether wer are
        using targets from the minibatch as the candidates (dim == 2), or a
        separate candidate set for every row in the batch (dim == 3).
        """
        if a.dim() != 2 or b.dim() not in [2, 3]:
            raise RuntimeError(
                'unexpected dims: a.dim() = {}, b.dim() = {}'
                ''.format(a.dim(), b.dim())
            )
        bsz = a.size(0)
        esz = a.size(1)
        hsz = b.size(-1)
        if self.cmp_type == 'dot':
            if b.dim() == 2:
                return torch.mm(a, b.t())
            elif b.dim() == 3:
                return torch.bmm(a.unsqueeze(1), b.transpose(1, 2)).squeeze(1)
        elif self.cmp_type == 'cosine':
            if b.dim() == 2:
                a = a.unsqueeze(1).expand(bsz, bsz, esz).contiguous()
                b = b.unsqueeze(1).expand(bsz, bsz, esz).transpose(0, 1)
                return F.cosine_similarity(a, b, dim=2)
            elif b.dim() == 3:
                a = a.unsqueeze(1).expand(bsz, b.size(1), esz).contiguous()
                return F.cosine_similarity(a, b, dim=2)
        elif self.cmp_type == 'bilinear':
            if b.dim() == 2:
                a = a.unsqueeze(1).expand(bsz, bsz, esz).contiguous()
                b = b.unsqueeze(1).expand(bsz, bsz, hsz).transpose(0, 1).contiguous()
                return self.bilinear(a, b).squeeze(1)
            elif b.dim() == 3:
                a = a.unsqueeze(1).expand(bsz, b.size(1), esz).contiguous()
                return self.bilinear(a, b).squeeze(1)
        elif self.cmp_type == 'mlp':
            if b.dim() == 2:
                a = a.unsqueeze(1).expand(bsz, bsz, esz).contiguous()
                b = b.unsqueeze(1).expand(bsz, bsz, esz).transpose(0, 1)
                return self.mlp(torch.cat([a, b], 2)).squeeze(1)
            elif b.dim() == 3:
                a = a.unsqueeze(1).expand(bsz, b.size(1), esz).contiguous()
                return self.mlp(torch.cat([a, b], 2)).squeeze(1)
        raise RuntimeError('Not implemented yet.')

    def forward(self, context, cands, cand_inds=None, decode_params=None):
        if self.cmp_type == 'decode':
            # decoding ranks differently--we don't encode the cands separately
            return self.decode(cands, cand_inds, decode_params)
        elif cand_inds is not None:
            max_len = max(c.size(1) for c in cands)
            cands = torch.cat([pad(c, max_len, dim=1).unsqueeze(0) for c in cands])

        # (bsz x seqlen x hsz) => (bsz x esz)
        context = self.transform_context(context)

        if not self.training and len(cand_inds) != context.size(0):
            # during validation: do we have cands for every context?
            # during training we do because we use the batch of labels
            cand_indices = context.data.new(cand_inds)
            context = context.index_select(1, cand_indices)

        enc_cands = self.encode(cands)
        scores = self.compare(context, enc_cands)
        preds = scores.sort(1, descending=True)[1]
        return preds, scores

    def decode(self, cands, cand_inds, decode_params):
        """Return the average log-prob of each candidate sequence."""
        start, hidden, enc_out, attn_mask = decode_params

        if not self.training:
            hid, cell = (hidden, None) if isinstance(hidden, torch.Tensor) else hidden
            if len(cand_inds) != hid.size(1):
                cand_indices = start.detach().new(cand_inds)
                hid = hid.index_select(1, cand_indices)
                if cell is None:
                    hidden = hid
                else:
                    cell = cell.index_select(1, cand_indices)
                    hidden = (hid, cell)
                enc_out = enc_out.index_select(0, cand_indices)
                attn_mask = attn_mask.index_select(0, cand_indices)

        cand_scores = []

        for i in range(len(cands)):
            if self.training:
                # same cands for each example
                curr_cs = cands
            else:
                curr_cs = cands[i]

            n_cs = curr_cs.size(0)
            starts = start.expand(n_cs).unsqueeze(1)
            scores = 0
            seqlens = 0
            # select just the one hidden state
            if isinstance(hidden, torch.Tensor):
                nl = hidden.size(0)
                hsz = hidden.size(-1)
                cur_hid = hidden.select(1, i).unsqueeze(1).expand(nl, n_cs, hsz)
            else:
                nl = hidden[0].size(0)
                hsz = hidden[0].size(-1)
                cur_hid = (
                    hidden[0]
                    .select(1, i)
                    .unsqueeze(1)
                    .expand(nl, n_cs, hsz)
                    .contiguous(),
                    hidden[1]
                    .select(1, i)
                    .unsqueeze(1)
                    .expand(nl, n_cs, hsz)
                    .contiguous(),
                )
            cur_enc = enc_out[i].unsqueeze(0).expand(n_cs, enc_out.size(1), hsz)
            cur_mask = None
            if attn_mask is not None:
                cur_mask = attn_mask[i].unsqueeze(0).expand(n_cs, attn_mask.size(-1))
            # this is pretty much copied from the training forward above
            if curr_cs.size(1) > 1:
                c_in = curr_cs.narrow(1, 0, curr_cs.size(1) - 1)
                xs = torch.cat([starts, c_in], 1)
            else:
                xs, c_in = starts, curr_cs
            if self.attn_type == 'none':
                preds, score, cur_hid = self.decoder(xs, cur_hid, cur_enc, cur_mask)
                true_score = F.log_softmax(score, dim=2).gather(2, curr_cs.unsqueeze(2))
                nonzero = curr_cs.ne(0).float()
                scores = (true_score.squeeze(2) * nonzero).sum(1)
                seqlens = nonzero.sum(1)
            else:
                for i in range(curr_cs.size(1)):
                    xi = xs.select(1, i)
                    ci = curr_cs.select(1, i)
                    preds, score, cur_hid = self.decoder(xi, cur_hid, cur_enc, cur_mask)
                    true_score = F.log_softmax(score, dim=2).gather(
                        2, ci.unsqueeze(1).unsqueeze(2)
                    )
                    nonzero = ci.ne(0).float()
                    scores += true_score.squeeze(2).squeeze(1) * nonzero
                    seqlens += nonzero

            scores /= seqlens  # **len_penalty?
            cand_scores.append(scores)

        if not self.training:
            max_len = max(len(c) for c in cand_scores)
            cand_scores = [pad(c, max_len) for c in cand_scores]

        cand_scores = torch.cat([c.unsqueeze(0) for c in cand_scores], 0)
        preds = cand_scores.sort(1, True)[1]
        return preds, cand_scores

#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from parlai.utils.misc import round_sigfigs
from parlai.agents.seq2seq.seq2seq import Seq2seqAgent
from .modules import Seq2rank

import torch
import torch.nn as nn


class Seq2rankAgent(Seq2seqAgent):
    @staticmethod
    def add_cmdline_args(argparser):
        agent = Seq2seqAgent.add_cmdline_args(argparser)
        agent.add_argument(
            '-rcr',
            '--rank-loss',
            default='xent',
            choices=['multimargin', 'xent', 'none'],
            help='Criterion to use for ranking loss. If set to none, do not '
            'backprop through the ranker.',
        )
        agent.add_argument(
            '-rmarg',
            '--rank-margin',
            type=float,
            default=0.1,
            help='if using multimargin loss, train with this margin.',
        )
        agent.add_argument(
            '-rcmp',
            '--rank-comparator',
            default='dot',
            choices=['dot', 'cosine', 'mlp', 'bilinear', 'decode'],
            help='scoring function for ranking candidates. options are to '
            'compute the dot product or cosine similarity between the '
            'encoding function and the embedding of each candidate; to '
            'feed the two embeddings into a small mlp or bilinear layer;'
            ' or to feed the candidates through the decoder and use the '
            'average token probability--this does not work well.',
        )
        agent.add_argument(
            '-renc',
            '--rank-encoder',
            default='bowmean',
            choices=['bowmean', 'bowsum', 'bowmax', 'rnn'],
            help='encoding function for encoding candidates. bow* computes the'
            ' bag of words for each candidates then uses the given '
            'function to combine the scores (sum, max, mean). or, use an '
            'rnn and take its final hidden state (TODO).',
        )
        agent.add_argument(
            '-rinp',
            '--rank-input',
            default='outputmean',
            choices=['outputmean', 'outputsum', 'outputmax', 'hidden', 'cell'],
            help='what context to pass to the ranker. output* takes all of '
            'the output states at each time step and combines them using '
            'the specified function (sum, max, mean). hidden takes the '
            'final hidden state. cell takes the final cell state.',
        )
        agent.add_argument(
            '-rlt',
            '--rank-lookuptable',
            default='dec',
            choices=['unique', 'enc', 'dec'],
            help='whether to share the embeddings with other modules, if '
            'applicable (for example, -renc bowmean will use these '
            'embeddings). unique creates a new embedding matrix. dec uses'
            ' the embedding matrix from the decoder. enc uses the '
            'embedding matrix from the encoder. note that the typical '
            'setting for seq2seq shares the encoder and decoder '
            'embeddings already so enc and dec would be the same here.',
        )
        agent.add_argument(
            '-rw',
            '--rank-weight',
            type=float,
            default=-1,
            help='Interpolation coefficient with the generative loss: '
            '(1 - c) * GENLOSS + c * RANKLOSS. Set to < 0 '
            'to use the sqrt of the rank loss instead. (default -1)',
        )

    def __init__(self, opt, shared=None):
        """Set up model."""
        self.model_class = Seq2rank
        super().__init__(opt, shared)

        self.metrics['rank_loss'] = 0.0

        if opt.get('rank_loss') == 'multimargin':
            self.rank_criterion = nn.MultiMarginLoss(
                margin=opt.get('rank_margin', 1), size_average=True
            )
        elif opt.get('rank_loss') == 'xent':
            self.rank_criterion = nn.CrossEntropyLoss(size_average=True)
        self.rankw = opt.get('rank_weight')

    def override_opt(self, new_opt):
        """Set overridable opts from loaded opt file.

        Print out each added key and each overriden key.
        Only override args specific to the model.
        """
        super().override_opt(new_opt)
        model_args = {
            'rank_encoder',
            'rank_comparator',
            'rank_lookuptable',
            'rank_candidates',
        }
        for k in model_args.items():
            if k not in new_opt:
                # skip non-model args
                continue
            v = new_opt[k]
            if k not in self.opt:
                print('[ Adding new option: | {k}: {v} | ]'.format(k=k, v=v))
            elif self.opt[k] != v:
                print(
                    '[ Overriding option: | {k}: {old} => {v} | ]'.format(
                        k=k, old=self.opt[k], v=v
                    )
                )
            self.opt[k] = v
        return self.opt

    def report(self):
        """Report loss and perplexity from model's perspective.

        Note that this includes predicting __END__ and __UNK__ tokens and may
        differ from a truly independent measurement.
        """
        m = super().report()
        if self.metrics['rank_loss'] > 0:
            m['rank_loss'] = round_sigfigs(self.metrics['rank_loss'], 4)
        return m

    def reset_metrics(self):
        super().reset_metrics()
        self.metrics['rank_loss'] = 0.0

    def predict(self, xs, ys=None, cands=None, valid_cands=None, is_training=False):
        """Produce a prediction from our model.

        Update the model using the targets if available, otherwise rank
        candidates as well if they are available and param is set.
        """
        predictions, cand_preds = None, None
        if is_training:
            self.model.train()
            self.zero_grad()
            out = self.model(xs, ys, rank_during_training=self.rank)
            # generated response
            preds, scores = out[0], out[1]

            score_view = scores.view(-1, scores.size(-1))
            loss = self.criterion(score_view, ys.view(-1))
            # save loss to metrics
            y_ne = ys.ne(self.NULL_IDX)
            target_tokens = y_ne.long().sum().item()
            correct = ((ys == preds) * y_ne).sum().item()
            self.metrics['correct_tokens'] += correct
            self.metrics['loss'] += loss.item()
            self.metrics['num_tokens'] += target_tokens
            loss /= target_tokens  # average loss per token

            if out[2] is not None and hasattr(self, 'rank_criterion'):
                cand_preds, cand_scores = out[2], out[3]
                cand_targets = torch.arange(
                    0, cand_scores.size(0), out=cand_scores.new()
                ).long()
                rank_loss = self.rank_criterion(cand_scores, cand_targets)
                # save loss to metrics
                self.metrics['rank_loss'] += rank_loss.item()
                # rank_loss /= cand_scores.size(0)  # divide by num_cands
                # control scale of rankloss
                if self.rankw >= 0:
                    loss = (1 - self.rankw) * loss + self.rankw * rank_loss
                else:
                    loss += rank_loss.sqrt()

            loss.backward()
            self.update_params()
        else:
            self.model.eval()
            out = self.model(xs, ys=None, cands=cands, valid_cands=valid_cands)
            predictions, cand_preds, cand_scores = out[0], out[2], out[3]

            if ys is not None:
                # calculate loss on targets
                out = self.model(xs, ys)
                scores = out[1]
                score_view = scores.view(-1, scores.size(-1))
                loss = self.criterion(score_view, ys.view(-1))
                target_tokens = ys.ne(self.NULL_IDX).long().sum().item()
                self.metrics['loss'] += loss.item()
                self.metrics['num_tokens'] += target_tokens

        return predictions, cand_preds

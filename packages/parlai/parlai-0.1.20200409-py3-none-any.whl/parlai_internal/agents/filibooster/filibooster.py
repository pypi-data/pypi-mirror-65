#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from parlai.utils.misc import maintain_dialog_history, PaddingUtils, round_sigfigs
from parlai.agents.seq2seq.seq2seq import Seq2seqAgent
from .modules import Filibooster, pad
from parlai.core.logs import TensorboardLogger
import math
from collections import deque
import os

import torch
import torch.nn as nn
from torch import optim
import numpy
import torch.nn.functional as F
import pickle


class FiliboosterAgent(Seq2seqAgent):
    @staticmethod
    def add_cmdline_args(argparser):
        agent = Seq2seqAgent.add_cmdline_args(argparser)
        agent.add_argument('-fdp', '--fdata-parallel', type=bool, default=False,
                           help='Data parallel for this model')
        agent.add_argument('-rw', '--rank-weight', type=float, default=0.1,
                           help='Interpolation coefficient with CE loss: (1-c)*CE + c*HingeLoss')
        agent.add_argument('-rk', '--num-rank-cand', type=int, default=1,
                           help='Number of alternative candidates when p(y|x^) or p(y^|x) is computed, depending on ''which side we consider.')
        agent.add_argument('-rm', '--rank-margin', type=float, default=1.0, help='Margin value for the margin loss')
        agent.add_argument('-rs', '--rank-side', type=str, default='none',
                           help='What do we change during the training, ys (target) or xs (input)')
        agent.add_argument('-rloss', '--rank-loss', type=str, default='margin', choices=['ce', 'margin'],
                           help='What loss to use on sequence level for ranking')
        agent.add_argument('-rp', '--rank-partially', type=int, default=-1,
                           help='Specify the minimum allowed length for truncated partial sequence')
        agent.add_argument('-rmode', '--rank-mode', type=str, default='separate', choices=['separate', 'decoder', 'sample-rerank', 'none'], help='Rank mode')
        agent.add_argument('-dhid', '--dec-hid-type', type=str, default='cell', choices=['cell', 'partialcell', 'maxcell', 'partialmaxcell'], help='Decoder hidden output type for separate ranking')
        agent.add_argument('-addenc', '--add-enc-rank', type=str, default='none', choices=['none', 'cell', 'hidden', 'hiddenmax'], help='Put True if you want to add encoder output as input to the separate Ranker')
        agent.add_argument('-rscore', '--rank-score', type=str, default='ranker', choices=['ranker', 'beam'], help='Which score do we use when we sort the candidates')
        agent.add_argument('-blngr', '--block-ngram', type=int, default=5, help='Upper bound on Ngram order which we want to block during the beam search either intra or inter sequence')
        agent.add_argument('-bltyp', '--block-type', type=str, default='none', choices=['none', 'inter','intra','both'], help='Intra block is in single seqs dimension, inter in candidates dimension')

    def __init__(self, opt, shared=None):
        self.model_class = Filibooster

        super().__init__(opt, shared)

        self.id = 'Filibooster'
        # set up margin metric here
        self.rank_weight = opt.get('rank_weight')
        self.batch_size = opt['batchsize']
        self.metrics = {
            'celoss': 0.0,
            'num_tokens': 0,
            'marginloss': 0,
            'comboloss': 0,
            'num_batches': 0,
        }
        self.margin = opt['rank_margin']
        self.num_rank_cand = opt['num_rank_cand']
        self.rank_side = opt['rank_side']
        self.num_layers = opt['numlayers']
        self.rank_crit = nn.MultiMarginLoss(margin=self.margin) if opt[
                                                                       'rank_loss'] == 'margin' else nn.CrossEntropyLoss()
        self.rank_partial = opt['rank_partially']
        self.dec_hid_type = opt['dec_hid_type']
        self.add_enc_rank = opt['add_enc_rank']

        self.writer = None
        if opt['tensorboard_log'] is True:
            self.writer = TensorboardLogger(opt)
            if 'text' in opt['tensorboard_tag']:
                self.dump_text = True
            else:
                self.dump_text = False

        self.batch_step = 0
        self.rank_mode = opt.get('rank_mode', 'separate')
        if self.rank_mode == 'separate' or self.rank_mode == 'sample-rerank':
            self.model.augment_with_post_ranker(opt)
            if os.path.exists(opt['model_file']):
                states = self.load(opt['model_file'])
                self.model.load_state_dict(states['model'])
            self.optimizer.add_param_group({'params': self.model.post_ranker.parameters()})

        if self.rank_mode == 'sample-rerank':
            if self.beam_size > 1:
                assert self.topk == 1, 'Beam search and topk should not be combined'
            if self.topk > 1:
                assert self.beam_size == 1, 'Beam search and topk should not be combined'
            self.rank_score = opt.get('rank_score', None)
            assert self.rank_score is not None

        self.block_ngram = opt.get('block_ngram', 5)
        self.block_type = opt.get('block_type', 'none')


    def override_opt(self, new_opt):
        """Set overridable opts from loaded opt file.

        Print out each added key and each overriden key.
        Only override args specific to the model.
        """
        super().override_opt(new_opt)
        model_args = {'rank_weight'}
        for k in model_args.items():
            if k not in new_opt:
                # skip non-model args
                continue
            v = new_opt[k]
            if k not in self.opt:
                print('[ Adding new option: | {k}: {v} | ]'.format(k=k, v=v))
            elif self.opt[k] != v:
                print('[ Overriding option: | {k}: {old} => {v} | ]'.format(
                    k=k, old=self.opt[k], v=v))
            self.opt[k] = v
        return self.opt

    def _get_cands_from_xs(self, _xs):
        START=1
        END=2
        # go over the batch to get last model reply for each sample
        hist_cands = []
        pass_flag = False
        for i in range(_xs.size(0)):
            start_ids = ((_xs[i] == START).nonzero()).squeeze(-1).tolist()
            end_ids = ((_xs[i] == END).nonzero()).squeeze(-1).tolist()
            if len(start_ids) > 0:
                hist_cands.append([])
                for s in start_ids:
                    e = min([i for i in end_ids if i > s])
                    hist_cands[-1].append(_xs[i][s+1: e])
            else:
                pass_flag = True

        return hist_cands if pass_flag is False else None


    def predict(self,
                xs,
                ys=None,
                cands=None,
                valid_cands=None,
                is_training=False):
        """
        Here we do margin based loss on sequence level as
        J =sum_X^ [ max(0, 1 - log(Y|X) + log(Y|X^)) ] in rank_side=input case or
        J =sum_Y^ [ max(0, 1 - log(Y|X) + log(Y^|X)) ] in rank_side=target case
        where we compute logp(Y|X^) by shifting the encoder state along batch axis
        and logp(Y^|X) by shifting the targets

        :param xs: inputs
        :param ys: targets
        :param cands:
        :param valid_cands:
        :param is_training:
        :return:
        """
        predictions = None
        rerank_preds = None
        if is_training:
            self.train_mode()
            self.zero_grad()
            _predictions, scores, cand_preds, _, enc_states, _, _, last_decoder_hidden = self.model(xs, ys)
            vocab_size = scores.size(-1)
            score_view = scores.view(-1, vocab_size)

            celoss = self.criterion(score_view, ys.view(-1))

            self.metrics['celoss'] += celoss.item()
            target_tokens = ys.ne(self.NULL_IDX).long().sum().item()
            self.metrics['num_tokens'] += target_tokens

            target_tokens_per_seq = ys.ne(self.NULL_IDX).float().sum(1)

            celoss /= target_tokens

            logp_ybar_x = []
            logp_y_xbar = []

            current_batchsize = enc_states[0].size(0)
            assert current_batchsize == enc_states[1][0].size(1)
            self.metrics['num_batches'] += 1

            if self.dec_hid_type == 'cell':
                rank_input = last_decoder_hidden[1][-1]
            elif self.dec_hid_type == 'hidden':
                rank_input = last_decoder_hidden[0][-1]

            if self.add_enc_rank == 'cell':
                enc_rank_input = enc_states[1][1][-1]
                rank_input = rank_input + enc_rank_input
            if self.add_enc_rank == 'hidden':
                enc_rank_input = enc_states[1][0][-1]
                rank_input = rank_input + enc_rank_input

            if self.rank_mode == 'decoder':
                logp_y_x = (F.log_softmax(scores, dim=2).gather(2, ys.unsqueeze(-1)).squeeze(-1) * ys.ne(0).float()).sum(
                    1) / target_tokens_per_seq  # this is actual logp with minus
                logp_y_x = logp_y_x.unsqueeze(-1)
            elif self.rank_mode == 'separate':
                logp_y_x = self.model.post_ranker(rank_input)


            logp_y = None
            margin_loss = None

            # if self.rank_side == 'input':
            if 'input' in self.rank_side:
                for i in range(1, self.num_rank_cand + 1):
                    shuffled_enc_states = []
                    shuffled_enc_states.append(torch.cat((enc_states[0][i:], enc_states[0][:i]), dim=0))
                    shuffled_enc_states.append(
                        [torch.cat((enc_states[1][l][:, i:, :], enc_states[1][l][:, :i, :]), dim=1) for l in
                         range(self.num_layers)])
                    shuffled_enc_states.append(torch.cat((enc_states[2][i:,:], enc_states[2][:i,:])))
                    shuf_prev_enc = (shuffled_enc_states[0], shuffled_enc_states[1], shuffled_enc_states[2])
                    out = self.model(xs, ys, prev_enc=shuf_prev_enc)
                    if self.rank_mode == 'decoder':
                        scores = (F.log_softmax(out[1], dim=2).gather(2, ys.unsqueeze(-1)).squeeze(-1) * ys.ne(0).float()).sum(1) / target_tokens_per_seq
                        scores = scores.unsqueeze(-1)
                    elif self.rank_mode == 'separate':
                        if self.dec_hid_type == 'cell':
                            rank_input = out[7][1][-1]
                        elif self.dec_hid_type == 'hidden':
                            rank_input =out[7][0][-1]

                        if self.add_enc_rank == 'cell':
                            enc_rank_input = out[4][1][1][-1]
                            rank_input = rank_input + enc_rank_input
                        if self.add_enc_rank == 'hidden':
                            enc_rank_input = out[4][1][0][-1]
                            rank_input = rank_input + enc_rank_input
                        scores = self.model.post_ranker(rank_input)
                    logp_y_xbar.append(scores)

            # if self.rank_side == 'target':
            if 'target' in self.rank_side:
                # we shuffle targets here
                enc_feat = None
                for i in range(1, self.num_rank_cand + 1):
                    shuffled_targets = torch.cat((ys[i:], ys[:i]), dim=0)
                    out = self.model(xs, shuffled_targets, prev_enc=enc_states)
                    if self.rank_mode == 'decoder':
                        scores = (F.log_softmax(out[1], dim=2).gather(2, shuffled_targets.unsqueeze(-1)).squeeze(-1) * shuffled_targets.ne(0).float()).sum(1) / target_tokens_per_seq
                        scores = scores.unsqueeze(-1)
                    elif self.rank_mode == 'separate':
                        if self.dec_hid_type == 'cell':
                            rank_input = out[7][1][-1]
                        elif self.dec_hid_type == 'hidden':
                            rank_input =out[7][0][-1]

                        if self.add_enc_rank == 'cell':
                            enc_rank_input = out[4][1][1][-1]
                            rank_input = rank_input + enc_rank_input
                        if self.add_enc_rank == 'hidden':
                            enc_rank_input = out[4][1][0][-1]
                            rank_input = rank_input + enc_rank_input
                        scores = self.model.post_ranker(rank_input)

                    logp_ybar_x.append(scores)

            if 'hist' in self.rank_side:
                # dialogue history as negative cands for ranker
                # get model replies using person tokens
                hist_cands = self._get_cands_from_xs(xs)
                if hist_cands is not None:
                    min_cand = min([len(l) for l in hist_cands])
                    for c in range(min_cand):
                        current_cands = [l[c] for l in hist_cands]
                        maxlen = max([i.size(-1) for i in current_cands])
                        current_cands = [pad(c, maxlen, 0) for c in current_cands]
                        current_cands = torch.stack(current_cands, dim=0)
                        hist_out = self.model(xs, current_cands, prev_enc=enc_states)

                        if self.rank_mode == 'decoder':            
                            raise NotImplementedError              
                        elif self.rank_mode == 'separate':
                            if self.dec_hid_type == 'cell':
                                rank_input = hist_out[7][1][-1]
                            elif self.dec_hid_type == 'hidden':
                                rank_input =hist_out[7][0][-1]
                                                      
                        scores = self.model.post_ranker(rank_input)
                        logp_ybar_x.append(scores)


            logp_y = torch.cat([logp_y_x] + logp_ybar_x + logp_y_xbar, dim=1)
            logp_y = F.softmax(logp_y, dim=1)

            targets = torch.LongTensor([0] * current_batchsize).to(logp_y.device)
            if self.rank_side != 'none':
                margin_loss = self.rank_crit(logp_y, targets)
                self.metrics['marginloss'] += margin_loss.item()
                loss = self.rank_weight * margin_loss + (1 - self.rank_weight) * celoss
            else:
                loss = celoss

            self.metrics['comboloss'] += loss.item()

            loss.backward()
            self.update_params()

            if self.writer is not None:
                grad_norm = []
                for p in self.model.parameters():
                    grad_norm.append(torch.norm(p.grad, 2))
                grad_norm = torch.stack(grad_norm).mean()
                if self.batch_step % 10 == 0:
                    self.writer.add_scalar('train/avg_gradnorm', grad_norm, self.batch_step)
        else:
            self.eval_mode()
            
            if self.rank_mode == 'decoder' or self.rank_mode == 'none':
                out = self.model(xs, ys=None, cands=cands, valid_cands=valid_cands,
                                 beam_size=self.beam_size, topk=self.topk, block_ngram=self.block_ngram, block_type=self.block_type)
                predictions, cand_preds = out[0], out[2]

            elif self.rank_mode == 'separate':
                out = self.model(xs, ys=None, cands=None, valid_cands=None,
                                 beam_size=self.beam_size, topk=self.topk, block_ngram=self.block_ngram, block_type=self.block_type)
                predictions = out[0]
                if cands is not None:
                    # we compute cand preds using post ranker here
                    _cand_preds = []
                    # we can add cands from history here, and need to repad to do batching
                    for i,c in enumerate(cands):
                        if 'hist' in self.rank_side:
                            hist_cands = self._get_cands_from_xs(xs)
                            if hist_cands is not None:
                                _maxlen = 0
                                _maxlen = max([len(c[ii]) for ii in range(c.size(0))])
                                hmaxlen = max([h.size(-1) for h in hist_cands[i]])
                                maxlen = max(_maxlen, hmaxlen)
                                current_cands = [pad(cc, maxlen, 0) for cc in c]
                                current_hist = [pad(h, maxlen, 0) for h in hist_cands[i]]
                                current_cands = current_cands + current_hist
                                c = torch.stack(current_cands, 0)

                        xsi = xs[i]
                        xsi = xsi[xsi.nonzero().squeeze().detach()]
                        xsi = xsi.unsqueeze(0).expand(c.size(0), -1)
                        mout = self.model(xsi, c)

                        if self.dec_hid_type == 'cell':
                            rank_input = mout[7][1][-1]
                        elif self.dec_hid_type == 'hidden':
                            rank_input =mout[7][0][-1]

                        if self.add_enc_rank == 'cell':
                            enc_rank_input = mout[4][1][1][-1]
                            rank_input = rank_input + enc_rank_input

                        if self.add_enc_rank == 'hidden':
                            enc_rank_input = mout[4][1][0][-1]
                            rank_input = rank_input + enc_rank_input

                        rout = self.model.post_ranker(rank_input)
                        _cand_preds.append(F.softmax(rout.squeeze(-1), dim=0))
                    #_cand_preds = torch.stack(_cand_preds,0)
                    cand_preds = []
                    for cp in _cand_preds:
                        cand_preds.append(cp.sort(0, True)[1])
                    #cand_preds = _cand_preds.sort(1, True)[1]
                else:
                    cand_preds = None

            elif self.rank_mode == 'sample-rerank':
                # here we also sample self.num_rank_cand candidates with topk sampling...
                _cand_list = []
                _cand_scores_list = []
                _cand_seq_scores = []
                _out = self.model(xs, ys=None, cands=None, valid_cands=None,
                                 beam_size=self.beam_size, topk=self.topk, block_ngram=self.block_ngram, block_type=self.block_type)
                #import IPython; IPython.embed()
                _cand_seq_scores.append(_out[1])
                _cand_list.append(_out[0])
                
                if self.dec_hid_type == 'cell':
                    rank_input = _out[7][1][-1]
                elif self.dec_hid_type == 'hidden':
                    rank_input =_out[7][0][-1]
                
                if self.add_enc_rank == 'cell':
                    enc_rank_input = _out[4][1][1][-1]
                    rank_input = rank_input + enc_rank_input
                if self.add_enc_rank == 'hidden':
                    enc_rank_input = _out[4][1][0][-1]
                    rank_input = rank_input + enc_rank_input
                
                rank_out = self.model.post_ranker(rank_input)
                _cand_scores_list.append(rank_out.view(-1))
                
                prev_enc = _out[4]
                block_hypos = []
                for ibatch_block in range(_out[0].size(0)):
                    block_hypos.append([','.join([str(i.item()) for i in _out[0][ibatch_block].view(-1)])])
                for i in range(self.num_rank_cand - 1):
                    _out = self.model(xs, ys=None, cands=None, valid_cands=None, prev_enc=prev_enc, beam_size=self.beam_size, topk=self.topk, beam_block_hypos=block_hypos, block_ngram=self.block_ngram, block_type=self.block_type)
                    if _out[1].item() < -100:
                        continue
                    _cand_seq_scores.append(_out[1])
                    for i,blist in enumerate(block_hypos):
                        blist.append(','.join([str(i.item()) for i in _out[0][i].view(-1)]))
                    #import IPython; IPython.embed()

                    if self.dec_hid_type == 'cell':
                        rank_input = _out[7][1][-1]
                    elif self.dec_hid_type == 'hidden':
                        rank_input =_out[7][0][-1]

                    if self.add_enc_rank == 'cell':
                        enc_rank_input = _out[4][1][1][-1]
                        rank_input = rank_input + enc_rank_input
                    if self.add_enc_rank == 'hidden':
                        enc_rank_input = _out[4][1][0][-1]
                        rank_input = rank_input + enc_rank_input

                    rank_out = self.model.post_ranker(rank_input)
                    _cand_list.append(_out[0])
                    _cand_scores_list.append(rank_out.view(-1))


                ### DEBUG PRINT TO FILE
                scores = None
                #import IPython; IPython.embed()
                #with open('/private/home/kulikov/projects/convai2-intern/mturk.log', 'a') as f:
                #    f.write('INPUT: {}\n\n'.format(self.dict.vec2txt(xs.view(-1))))
                #    __cands = []
                #    for ii,i in enumerate(_cand_list):
                #        __cands.append( (_cand_scores_list[ii].item(), _cand_seq_scores[ii].item(), self.dict.vec2txt(i.view(-1))) )

                #    __cands.sort(key=lambda tup: tup[0], reverse=True)
                #    scores = [(__cands[i][0], __cands[i][1], i) for i in range(len(__cands))]
                #    for i in __cands:    
                #        f.write('rank_score:{:.{prec}f}, beam_score:{:.{prec}f}\t :{}\n'.format(i[0], i[1], i[2], prec=4))
                #    f.write('------------------------------- \n\n\n')

                #with open('/private/home/kulikov/projects/convai2-intern/rankbeam.log', 'a') as ff:
                #    for ___cand in scores:
                #        ff.write('{:.{prec}f},{:.{prec}f},{}\n'.format(___cand[0], ___cand[1], ___cand[2], prec=4))

                _presoft_cand_scores = torch.stack(_cand_scores_list, 1)
                _beam_cand_scores = torch.stack(_cand_seq_scores, 1)

                _cand_scores = F.softmax(_presoft_cand_scores, dim=1)
                maxlen = max(i.size(-1) for i in _cand_list)
                _cand_list = [pad(i, maxlen, 1) for i in _cand_list]
                _cand_list = torch.stack(_cand_list, 1)
                _cand_list = list(torch.unbind(_cand_list, 0))
                if self.rank_score == 'ranker':
                    # this is sorting of ranker scores
                    _, idx = _cand_scores.sort(1, descending=True)
                elif self.rank_score == 'beam':
                    # this is sorting of beam scores
                    _, idx = _beam_cand_scores.sort(1, descending=True)
                
                rerank_preds = []
                cand_preds = None

                for i,c in enumerate(_cand_list):
                    rerank_preds.append((c[idx[i]], _cand_scores[i][idx[i]], _beam_cand_scores[i][idx[i]]))

                predictions = []
                for i in rerank_preds:
                    predictions.append(i[0][0])

                predictions = torch.stack(predictions,0)

            # per-target-token calculation
            if ys is not None:
                # calculate loss on targets
                out = self.model(xs, ys)
                scores = out[1]
                score_view = scores.view(-1, scores.size(-1))
                loss = self.criterion(score_view, ys.view(-1))
                target_tokens = ys.ne(self.NULL_IDX).long().sum().item()
                self.metrics['celoss'] += loss.item()
                self.metrics['num_tokens'] += target_tokens

        self.batch_step += 1
        return predictions, cand_preds, rerank_preds

    def train_mode(self):
        """
        Just do train() on all existing models
        :return: None
        """
        self.model.train()

    def eval_mode(self):
        self.model.eval()

    def report(self):
        """
        Reports additional metrics
        :return:
        """
        m = {}
        if self.metrics['num_batches'] > 0:
            m['marginloss'] = self.metrics['marginloss'] / self.metrics[
                'num_batches']
            m['comboloss'] = self.metrics['comboloss'] / self.metrics[
                'num_batches']
        if self.metrics['num_tokens'] > 0:
            m['celoss'] = self.metrics['celoss'] / self.metrics['num_tokens']
            try:
                m['ppl'] = math.exp(m['celoss'])
            except OverflowError:
                m['ppl'] = float('inf')
        for k, v in m.items():
            # clean up: rounds to sigfigs and converts tensors to floats
            m[k] = round_sigfigs(v, 4)
        return m

    def reset_metrics(self):
        super().reset_metrics()
        self.metrics['marginloss'] = 0.0
        self.metrics['comboloss'] = 0.0
        self.metrics['num_batches'] = 0.0
        self.metrics['celoss'] = 0.0

    def strip_reply(self, r):
        reply = []
        for w in r.split():
            if w == '__end__':
                break
            else:
                reply.append(w)

        return ' '.join(reply)

    def batch_act(self, observations):
        batchsize = len(observations)
        # initialize a table of replies with this agent's id
        batch_reply = [{'id': self.getID()} for _ in range(batchsize)]

        # convert the observations into batches of inputs and targets
        # valid_inds tells us the indices of all valid examples
        # e.g. for input [{}, {'text': 'hello'}, {}, {}], valid_inds is [1]
        # since the other three elements had no 'text' field
        xs, ys, labels, valid_inds, cands, valid_cands, is_training = self.vectorize(observations)
        
        if xs is None:
            # no valid examples, just return empty responses
            return batch_reply

        # produce predictions, train on targets if availables
        cand_inds = [i[0] for i in valid_cands] if valid_cands is not None else None
        predictions, cand_preds, rerank_preds = self.predict(xs, ys, cands, cand_inds, is_training)

        if is_training:
            report_freq = 0
        else:
            report_freq = self.report_freq
        if predictions is not None:
            PaddingUtils.map_predictions(
                predictions,
                valid_inds,
                batch_reply,
                observations,
                self.dict,
                self.END_IDX,
                report_freq=report_freq,
                labels=labels,
                answers=self.answers,
                ys=ys.data if ys is not None else None)

        if cand_preds is not None:
            if valid_cands is None:
                valid_cands = [(None, i, labels) for i in valid_inds]
            for i in range(len(valid_cands)):
                order = cand_preds[i]
                _, batch_idx, curr_cands = valid_cands[i]
                curr = batch_reply[batch_idx]
                curr['text_candidates'] = [
                    curr_cands[idx] for idx in order if idx < len(curr_cands)
                ]

        if rerank_preds is not None:
            if valid_cands is None:
                valid_cands = [(None, i, labels) for i in valid_inds]
            for i in range(len(valid_cands)):
                batch_idx = valid_inds[i]
                curr = batch_reply[batch_idx]
                curr['reranked_samples'] = [ 'r:{:.{prec}f} b:{:.{prec}f} {}'.format(rerank_preds[i][1][k], rerank_preds[i][2][k], self.strip_reply(self.dict.vec2txt(rerank_preds[i][0][k])), prec=4) for k in range(rerank_preds[i][0].size(0)) ]

        return batch_reply
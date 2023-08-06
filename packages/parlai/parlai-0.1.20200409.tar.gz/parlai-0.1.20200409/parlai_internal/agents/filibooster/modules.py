#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import torch
import torch.nn as nn
import torch.nn.functional as F
from parlai.agents.seq2seq.modules import pad, Seq2seq, Encoder, Decoder, Ranker, Linear, AttentionLayer
from parlai.core.dict import DictionaryAgent
from parlai.core.logs import TensorboardLogger
from .beam_block import Beam
import stop_words
import numpy
import os


class Filibooster(nn.Module):
    """
    Extends Seq2seq agent with context discriminative margin loss

    """
    RNN_OPTS = {'rnn': nn.RNN, 'gru': nn.GRU, 'lstm': nn.LSTM}

    def __init__(self, opt, num_features,
                 padding_idx=0, start_idx=1, end_idx=2, longest_label=1):
        super().__init__()
        self.opt = opt

        self.rank = opt['rank_candidates']
        self.attn_type = opt['attention']

        self.NULL_IDX = padding_idx
        self.END_IDX = end_idx
        self.register_buffer('START', torch.LongTensor([start_idx]))
        self.longest_label = longest_label

        rnn_class = Seq2seq.RNN_OPTS[opt['rnn_class']]
        self.decoder = Decoder(
            num_features, padding_idx=self.NULL_IDX, rnn_class=rnn_class,
            emb_size=opt['embeddingsize'], hidden_size=opt['hiddensize'],
            num_layers=opt['numlayers'], dropout=opt['dropout'],
            share_output=opt['lookuptable'] in ['dec_out', 'all'],
            attn_type=opt['attention'], attn_length=opt['attention_length'],
            attn_time=opt.get('attention_time'),
            bidir_input=opt['bidirectional'],
            numsoftmax=opt.get('numsoftmax', 1),
            softmax_layer_bias=opt.get('softmax_layer_bias', False)) 

        shared_lt = (self.decoder.lt
                     if opt['lookuptable'] in ['enc_dec', 'all'] else None)
        shared_rnn = self.decoder.rnn if opt['decoder'] == 'shared' else None
        self.encoder = Encoder(
            num_features, padding_idx=self.NULL_IDX, rnn_class=rnn_class,
            emb_size=opt['embeddingsize'], hidden_size=opt['hiddensize'],
            num_layers=opt['numlayers'], dropout=opt['dropout'],
            bidirectional=opt['bidirectional'],
            shared_lt=shared_lt, shared_rnn=shared_rnn)

        if self.rank:
            self.ranker = Ranker(
                self.decoder,
                padding_idx=self.NULL_IDX,
                attn_type=opt['attention'])

        self.dict = DictionaryAgent(opt)
        stop_w = stop_words.get_stop_words('english')
        self.stopind = []
        for w in stop_w:
            if w in self.dict:
                self.stopind.append(self.dict.tok2ind[w])
        # convai2 specific
        self.stopind.extend([2,3,9,11,12,14,16,20,26,51,72,68,84,59,149])

        self.beam_log_freq = opt.get('beam_log_freq', 0.0)
        if self.beam_log_freq > 0.0:
            self.beam_dump_filecnt = 0
            self.beam_dump_path = opt['model_file'] + '.beam_dump'
            if not os.path.exists(self.beam_dump_path):
                os.makedirs(self.beam_dump_path)

    def augment_with_post_ranker(self, opt):
        decoder_hiddensize = opt.get('hiddensize', None)
        device = 'cuda' if opt['no_cuda'] is False else 'cpu'
        self.post_ranker = nn.Sequential(nn.Linear(decoder_hiddensize, decoder_hiddensize), nn.GLU(), nn.Linear(int(decoder_hiddensize / 2), 1)).to(device)

    def unbeamize_hidden(self, hidden, beam_size, batch_size):
        """
        Creates a view of the hidden where batch axis is collapsed with beam axis,
        we need to do this for batched beam search, i.e. we emulate bigger mini-batch
        :param hidden: hidden state of the decoder
        :param beam_size: beam size, i.e. num of hypothesis
        :param batch_size: number of samples in the mini batch
        :return: view of the hidden
        """
        if isinstance(hidden, tuple):
            num_layers = hidden[0].size(0)
            hidden_size = hidden[0].size(-1)
            return (hidden[0].view(num_layers, batch_size * beam_size, hidden_size),
                hidden[1].view(num_layers, batch_size * beam_size, hidden_size))
        else:  # GRU
            num_layers = hidden.size(0)
            hidden_size = hidden.size(-1)
            return hidden.view(num_layers, batch_size * beam_size, hidden_size)

    def unbeamize_enc_out(self, enc_out, beam_size, batch_size):
        hidden_size = enc_out.size(-1)
        return enc_out.view(batch_size * beam_size, -1, hidden_size)

    def forward(self, xs, ys=None, cands=None, valid_cands=None, prev_enc=None,
                rank_during_training=False, beam_size=1, topk=1, beam_block_hypos=None, block_ngram=0, block_type='none'):
        """Get output predictions from the model.

        Arguments:
        xs -- input to the encoder
        ys -- expected output from the decoder
        cands -- set of candidates to rank, if applicable
        valid_cands -- indices to match candidates with their appropriate xs
        prev_enc -- if you know you'll pass in the same xs multiple times and
            the model is in eval mode, you can pass in the encoder output from
            the last forward pass to skip recalcuating the same encoder output
        rank_during_training -- (default False) if set, ranks any available
            cands during training as well
        """
        input_xs = xs
        last_decoder_hidden = None
        nbest_beam_preds, nbest_beam_scores = None, None
        bsz = len(xs)
        if ys is not None:
            # keep track of longest label we've ever seen
            # we'll never produce longer ones than that during prediction
            self.longest_label = max(self.longest_label, ys.size(1))

        if prev_enc is not None:
            enc_out, hidden, attn_mask = prev_enc
        else:
            enc_out, hidden = self.encoder(xs)
            attn_mask = xs.ne(0).float() if self.attn_type != 'none' else None
        encoder_states = (enc_out, hidden, attn_mask)
        start = self.START.detach()
        starts = start.expand(bsz, 1)

        predictions = []
        scores = []
        dec_output = None
        cand_preds, cand_scores = None, None
        if self.rank and cands is not None:
            decode_params = (start, hidden, enc_out, attn_mask)
            if self.training:
                if rank_during_training:
                    cand_preds, cand_scores = self.ranker.forward(cands, valid_cands, decode_params=decode_params)
            else:
                cand_preds, cand_scores = self.ranker.forward(cands, valid_cands, decode_params=decode_params)

        if ys is not None:
            y_in = ys.narrow(1, 0, ys.size(1) - 1)
            xs = torch.cat([starts, y_in], 1)
            if self.attn_type == 'none':
                preds, score, hidden, dec_output = self.decoder(xs, hidden, enc_out, attn_mask)
                predictions.append(preds)
                scores.append(score)
            else:
                for i in range(ys.size(1)):
                    xi = xs.select(1, i)
                    preds, score, hidden = self.decoder(xi, hidden, enc_out, attn_mask)
                    predictions.append(preds)
                    scores.append(score)
            last_decoder_hidden = hidden
        else:
            # here we do search: supported search types: greedy, beam search
            if beam_size == 1:
                done = [False for _ in range(bsz)]
                total_done = 0
                xs = starts

                for _ in range(self.longest_label):
                    # generate at most longest_label tokens
                    preds, score, hidden = self.decoder(xs, hidden, enc_out, attn_mask, topk)
                    scores.append(score)
                    xs = preds
                    predictions.append(preds)

                    # check if we've produced the end token
                    for b in range(bsz):
                        if not done[b]:
                            # only add more tokens for examples that aren't done
                            if preds.data[b][0] == self.END_IDX:
                                # if we produced END, we're done
                                done[b] = True
                                total_done += 1
                    if total_done == bsz:
                        # no need to generate any more
                        break
                last_decoder_hidden = hidden

            elif beam_size > 1:
                enc_out, hidden = encoder_states[0], encoder_states[1]  # take it from encoder
                enc_out = enc_out.unsqueeze(1).repeat(1, beam_size, 1, 1)
                # create batch size num of beams
                data_device = enc_out.device
                beams = [Beam(beam_size, 3, 0, 1, 2, min_n_best=int(beam_size/2), cuda=data_device, stop_words=self.stopind, beam_block_hypos=beam_block_hypos[i] if isinstance(beam_block_hypos, list) else None, block_ngram=block_ngram, block_type=block_type) for i in range(bsz)]
                # init the input with start token
                xs = starts
                # repeat tensors to support batched beam
                xs = xs.repeat(1, beam_size)
                attn_mask = input_xs.ne(0).float()
                attn_mask = attn_mask.unsqueeze(1).repeat(1, beam_size, 1)
                repeated_hidden = []

                if isinstance(hidden, tuple):
                    for i in range(hidden[0].size(0)):
                        repeated_hidden.append(hidden[i].unsqueeze(2).repeat(1, 1, beam_size, 1))
                    hidden = self.unbeamize_hidden(tuple(repeated_hidden), beam_size, bsz)
                else:  # GRU
                    repeated_hidden = hidden.unsqueeze(2).repeat(1, 1, beam_size, 1)
                    hidden = self.unbeamize_hidden(repeated_hidden, beam_size, bsz)
                enc_out = self.unbeamize_enc_out(enc_out, beam_size, bsz)
                xs = xs.view(bsz * beam_size, -1)

                running_max_hidden = None
                last_hidden = None
                hiddens_history = []
                
                #for step in range(self.longest_label):
                for step in range(40):
                    if all((b.done() for b in beams)):
                        break
                    out = self.decoder(xs, hidden, enc_out)
                    scores = out[1]
                    scores = scores.view(bsz, beam_size, -1)  # -1 is a vocab size
                    for i, b in enumerate(beams):
                        b.advance(F.log_softmax(scores[i, :], dim=-1))
                    xs = torch.cat([b.get_output_from_current_step() for b in beams]).unsqueeze(-1)
                    permute_hidden_idx = torch.cat(
                        [beam_size * i + b.get_backtrack_from_current_step() for i, b in enumerate(beams)])
                    new_hidden = out[2]


                    if isinstance(hidden, tuple):
                        #best_hidden_tuple = []
                        for i in range(len(hidden)):
                            hidden[i].data.copy_(new_hidden[i].data.index_select(dim=1, index=permute_hidden_idx))
                            #_best_in_batch = []
                            #for b in range(len(beams)):
                            #    _best_in_batch.append(hidden[i].view(hidden[i].size(0), bsz, beam_size, hidden[i].size(-1))[:, b, 0, :])
                            #best_hidden_tuple.append(torch.stack(_best_in_batch, dim=1))
                    else:  # GRU
                        hidden.data.copy_(new_hidden.data.index_select(dim=1, index=permute_hidden_idx))
                        #_best_in_batch = []
                        #for b in range(len(beams)):
                        #    _best_in_batch.append(hidden[i].view(hidden[i].size(0), bsz, beam_size, hidden[i].size(-1))[:, b, 0, :])
                        #best_hidden_tuple = _best_in_batch  # this is not a tuple actually, just to ease naming later
                    #  here we have to take care about the keeping hidden states of the hypothesis which already finished, i.e. we do not update them
                    # firstly permute the masking vector
                    if isinstance(hidden, tuple):
                        hiddens_history.append((hidden[0].detach(), hidden[1].detach()))
                    else:
                        hiddens_history.append(hidden.detach())

                for b in beams:
                    b.check_finished()

                best_hidden = []
                if isinstance(hidden, tuple):
                    for hc in range(len(hidden)):
                        sub_hidden = []
                        for i,b in enumerate(beams):
                            best_hypo = b.get_rescored_finished()[0]
                            sub_hidden.append(hiddens_history[best_hypo.timestep-1][hc][:,i*beam_size+best_hypo.hypid,:])
                        sub_hidden = torch.stack(sub_hidden, dim=1)
                        best_hidden.append(sub_hidden)
                last_decoder_hidden = best_hidden

                beam_pred = [ b.get_pretty_hypothesis(b.get_top_hyp()[0])[1:] for b in beams ]
                # these beam scores are rescored with length penalty!
                beam_scores = torch.stack([b.get_top_hyp()[1] for b in beams])
                pad_length = max([t.size(0) for t in beam_pred])
                beam_pred = torch.stack([pad(t, length=pad_length, dim=0) for t in beam_pred], dim=0)

                #  prepare n best list for each beam
                n_best_beam_tails = [ b.get_rescored_finished(n_best=len(b.finished)) for b in beams ]
                nbest_beam_scores = []
                nbest_beam_preds = []
                for i, beamtails in enumerate(n_best_beam_tails):
                    perbeam_preds = []
                    perbeam_scores = []
                    for tail in beamtails:
                        perbeam_preds.append(beams[i].get_pretty_hypothesis(beams[i].get_hyp_from_finished(tail)))
                        perbeam_scores.append(tail.score)
                    nbest_beam_scores.append(perbeam_scores)
                    nbest_beam_preds.append(perbeam_preds)

                if self.beam_log_freq > 0.0:
                    num_dump = round(bsz * self.beam_log_freq)
                    for i in range(num_dump):
                        dot_graph = beams[i].get_beam_dot(dictionary=self.dict)
                        dot_graph.write_png(os.path.join(self.beam_dump_path, "{}.png".format(self.beam_dump_filecnt)))
                        self.beam_dump_filecnt += 1

                predictions = beam_pred
                scores = beam_scores


        if isinstance(predictions, list):
            predictions = torch.cat(predictions, 1)
        if isinstance(scores, list):
            scores = torch.cat(scores, 1)
        #import IPython; IPython.embed()

        return predictions, scores, cand_preds, cand_scores, encoder_states, nbest_beam_preds, nbest_beam_scores, last_decoder_hidden

class FiliboosterDecoder(nn.Module):
    def __init__(self, num_features, padding_idx=0, rnn_class='lstm',
                 emb_size=128, hidden_size=128, num_layers=2, dropout=0.1,
                 bidir_input=False, share_output=True,
                 attn_type='none', attn_length=-1, attn_time='pre',
                 sparse=False, numsoftmax=1, softmax_layer_bias=False, skip_connection=False):
        super().__init__()

        if padding_idx != 0:
            raise RuntimeError('This module\'s output layer needs to be fixed '
                               'if you want a padding_idx other than zero.')

        self.dropout = nn.Dropout(p=dropout)
        self.layers = num_layers
        self.hsz = hidden_size
        self.esz = emb_size

        self.lt = nn.Embedding(num_features, emb_size, padding_idx=padding_idx,
                               sparse=sparse)
        if skip_connection == False:
            self.rnn = rnn_class(emb_size, hidden_size, num_layers,
                                 dropout=dropout, batch_first=True)
        else:
            self.rnn = LSTMwSkip(rnn_class, emb_size, hidden_size, num_layers, dropout=dropout, batch_first=True)

        # rnn output to embedding
        if hidden_size != emb_size and numsoftmax == 1:
            # self.o2e = RandomProjection(hidden_size, emb_size)
            # other option here is to learn these weights
            self.o2e = nn.Linear(hidden_size, emb_size, bias=False)
        else:
            # no need for any transformation here
            self.o2e = lambda x: x
        # embedding to scores, use custom linear to possibly share weights
        shared_weight = self.lt.weight if share_output else None
        self.e2s = Linear(emb_size, num_features, bias=softmax_layer_bias,
                          shared_weight=shared_weight)
        self.shared = shared_weight is not None

        self.attn_type = attn_type
        self.attn_time = attn_time
        self.attention = AttentionLayer(attn_type=attn_type,
                                        hidden_size=hidden_size,
                                        emb_size=emb_size,
                                        bidirectional=bidir_input,
                                        attn_length=attn_length,
                                        attn_time=attn_time)

        self.numsoftmax = numsoftmax
        if numsoftmax > 1:
            self.softmax = nn.Softmax(dim=1)
            self.prior = nn.Linear(hidden_size, numsoftmax, bias=False)
            self.latent = nn.Linear(hidden_size, numsoftmax * emb_size)
            self.activation = nn.Tanh()

    def forward(self, xs, hidden, encoder_output, attn_mask=None, topk=1):
        xes = self.dropout(self.lt(xs))
        if self.attn_time == 'pre':
            xes = self.attention(xes, hidden, encoder_output, attn_mask)
        if xes.dim() == 2:
            # if only one token inputted, sometimes needs unsquezing
            xes.unsqueeze_(1)
        output, new_hidden = self.rnn(xes, hidden)
        dec_output = output
        if self.attn_time == 'post':
            output = self.attention(output, new_hidden, encoder_output, attn_mask)

        if self.numsoftmax > 1:
            bsz = xs.size(0)
            seqlen = xs.size(1) if xs.dim() > 1 else 1
            latent = self.latent(output)
            active = self.dropout(self.activation(latent))
            logit = self.e2s(active.view(-1, self.esz))

            prior_logit = self.prior(output).view(-1, self.numsoftmax)
            prior = self.softmax(prior_logit)  # softmax over numsoftmax's

            prob = self.softmax(logit).view(bsz * seqlen, self.numsoftmax, -1)
            probs = (prob * prior.unsqueeze(2)).sum(1).view(bsz, seqlen, -1)
            scores = probs.log()
        else:
            e = self.dropout(self.o2e(output))
            scores = self.e2s(e)

        # select top scoring index, excluding the padding symbol (at idx zero)
        # we can do topk sampling from renoramlized softmax here, default topk=1 is greedy
        if topk == 1:
            _max_score, idx = scores.narrow(2, 1, scores.size(2) - 1).max(2)
        elif topk > 1:
            max_score, idx = torch.topk(F.softmax(scores.narrow(2, 1, scores.size(2) - 1), 2), topk, dim=2, sorted=False)
            probs = F.softmax( scores.narrow(2, 1, scores.size(2) - 1).gather(2, idx), 2 ).squeeze(1)
            dist = torch.distributions.categorical.Categorical(probs)
            samples = dist.sample()
            idx = idx.gather(-1, samples.unsqueeze(1).unsqueeze(-1)).squeeze(-1)
        preds = idx.add_(1)

        return preds, scores, new_hidden, dec_output

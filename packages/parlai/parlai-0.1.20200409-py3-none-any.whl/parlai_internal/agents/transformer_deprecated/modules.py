#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#
# Can run with:
# touch  /tmp/model_t
# python parlai/scripts/eval_model.py -m internal:transformer -t convai2 -mf /tmp/model_t -dt test
#
# python parlai/scripts/interactive.py -m internal:transformer -mif /checkpoint/samuelhumeau/jobs/pem_dropout_on_fine_tune/0/model.mdl.mdl -fixedCands '/checkpoint/samuelhumeau/jobs/pem_dropout_on_fine_tune/0/cands'


import torch
import torch.nn as nn
import torch.nn.functional as F

import math
import numpy as np


UNK_TOKEN = '__UNK__'
PAD_TOKEN = '__PAD__'
SOC_TOKEN = '__SOC__'


class MemNetModel(nn.Module):

    def __init__(self, opt, dictionary, pad_token=PAD_TOKEN):
        super(MemNetModel, self).__init__()
        self.opt = opt
        self.pad_idx = dictionary[pad_token]
        self.tau = opt.embeddings_size ** .5 if self.opt.tau else 1
        self.alpha = opt.alpha
        self.validtau = opt.validtau
        self.dumps = [f'{int(torch.randint(10000, (1,))):05d}', 0]  # id, count

        self.embeddings = nn.Embedding(len(dictionary), opt.embeddings_size, padding_idx=self.pad_idx)
        if not opt.learn_embeddings:
            self.embeddings.weight.requires_grad = False
        nn.init.normal_(self.embeddings.weight, mean=0, std=0.05)

        self.transformer_dropout = opt.transformer_dropout
        self.memory_dropout = nn.Dropout(opt.memory_dropout)
        self.context_encoder = self.build_encoder(opt, dictionary, self.embeddings)

        if opt.share_encoders:
            dim = self.context_encoder.out_dim
            hdim = dim * opt.transformer_response_hmul
            self.cand_encoder = TransformerResponseWrapper(self.context_encoder, hdim)
        else:
            self.cand_encoder = self.build_encoder(opt, dictionary, self.embeddings)

        self.persona_encoder = BowEncoder(dim=2,
                                          out_size=self.context_encoder.out_dim,
                                          scale_sqrt=opt.bow_scale_sqrt,
                                          n_tanh=opt.bow_tanh,
                                          embedding=self.embeddings,
                                          embeddings_size=opt.embeddings_size)

        if opt.gru:
            self.gru = nn.GRU(opt.embeddings_size, opt.embeddings_size, batch_first=True)
        if opt.concat:
            self.cat = nn.Sequential(
                nn.Linear(2 * opt.embeddings_size, 2 * opt.embeddings_size),
                nn.ReLU(),
                nn.Linear(2 * opt.embeddings_size, 2 * opt.embeddings_size),
                nn.ReLU(),
                nn.Linear(2 * opt.embeddings_size, opt.embeddings_size),
            )

        if opt.use_moods:
            self.mood_dropout = nn.Dropout(p=opt.moods_dropout)
            self.mood_dnn = nn.Sequential(
                nn.Linear(self.opt.moods_dims, self.context_encoder.out_dim)
            )
        self.final_proj = nn.Linear(4 * opt.hidden, 2 * opt.hidden)

    def encode_cand(self, words):
        if words is None:
            return None
        word_mask = words != self.pad_idx
        return self.cand_encoder(words, word_mask)

    def encode_context_persona(self, context_w, personas_w):
        ones = torch.ones(context_w.size(0), 1, device=context_w.device)
        mask = self.memory_dropout(ones)

        context_mask = context_w != self.pad_idx
        context_h = self.context_encoder(context_w, context_mask)  # [batch, d]

        if personas_w is None:
            return [], context_h

        persona_mask = personas_w != self.pad_idx
        persona_h = self.persona_encoder(personas_w, persona_mask)  # [batch, n_persona, d]

        if self.opt.gru:
            _, context_h = self.gru(persona_h, context_h.unsqueeze(0))
            context_h = context_h.squeeze(0)
            weights = []
        else:
            weights, attentioned = self.attention(persona_h, context_h, persona_mask if self.opt.maskpersona else None)
            if self.opt.concat:
                cat = torch.cat((context_h, attentioned), dim=1)
                context_h = self.cat(cat)
                return [], context_h
            context_h = context_h + self.alpha * mask * attentioned
        return weights, context_h

    def build_encoder(self, opt, dictionary, embedding=None):
        if opt.encoder_type == 'bow':
            return BowEncoder(dim=1, out_size=4*opt.hidden, scale_sqrt=opt.bow_scale_sqrt, n_tanh=opt.bow_tanh, embedding=embedding, embeddings_size=opt.embeddings_size)
        elif opt.encoder_type == 'lstm':
            return LstmEncoder(opt, embedding=embedding)
        elif opt.encoder_type == 'transformer':
            dropout = self.transformer_dropout if self.transformer_dropout else 0
            return TransformerModel(opt.transformer_n_heads, opt.n_layers,
                opt.transformer_dim,len(dictionary), embedding=embedding,
                dropout=dropout, use_manual_norm=opt.use_manual_norm)

    def forward(self, context_w, personas_w, cands_w, moods=None):
        # lengths = (inputs != 0).float().sum(dim=1)
        if context_w is not None:
            weights, context_h = self.encode_context_persona(context_w, personas_w)
        else:
            weights, context_h = [], None
        cands_h = self.encode_cand(cands_w)
        if moods is not None:
            # dropout some of the moods randomly. This way the network does
            # not rely too much on the mood.
            # create a mask on the same device as context
            if self.opt.moods_dropout != 1:
                mask = torch.ones(moods.shape[0], dtype=context_h.dtype, device=context_h.device).unsqueeze(1)
                mask = self.mood_dropout(mask)
                moods *= mask
                context_h += self.mood_dnn(moods)
        if self.opt.normalize_sent_emb:
            context_h = context_h / context_h.norm(2, dim=1, keepdim=True)
            cands_h = cands_h / cands_h.norm(2, dim=1, keepdim=True)
        if self.opt.testing and len(weights) and self.opt.dumpattention:
            torch.save(
                {'ctx': context_w, 'pers': personas_w, 'att': weights, 'tau': self.opt.validtau},
                f'../dumps/attention/{self.opt.model_name}-{self.dumps[0]}-{self.dumps[1]}')
            self.dumps[1] += 1
        return context_h, cands_h

    def attention(self, memory, request, memmask=None):
        # memory is [B, nbpersona, d]
        # request is [B, d]
        tau = self.validtau if self.opt.testing else self.tau
        request = request.unsqueeze(-1)
        if memmask is not None:
            memmasked = memory.clone() * (memmask.sum(2, keepdim=True) != 0).float()
            weights = F.softmax(memmasked.bmm(request).squeeze(-1) / tau, dim=1)  # [B, seq_len]
        else:
            weights = F.softmax(memory.bmm(request).squeeze(-1) / tau, dim=1)  # [B, seq_len]

        return weights, weights.unsqueeze(1).bmm(memory).squeeze(1)  # [B, d]


class BowEncoder(nn.Module):

    def __init__(self, dim, out_size, scale_sqrt, n_tanh, embedding, embeddings_size=300):
        super(BowEncoder, self).__init__()
        self.dim = dim
        self.embedding = embedding
        self.scale_sqrt = scale_sqrt
        nn_layers = []
        for _ in range(n_tanh):
            nn_layers.append(nn.Linear(embeddings_size, embeddings_size))
            nn_layers.append(nn.Tanh())
        nn_layers.append(nn.Linear(embeddings_size, out_size))
        self.out_dim = out_size
        self.proj = nn.Sequential(*nn_layers)

    def forward(self, input, mask):
        if self.embedding != None:
            input = self.embedding(input)
        scale = mask.sum(self.dim, keepdim=True).float().clamp(min=1)
        if self.scale_sqrt:
            scale = scale.sqrt()
        bow = input.sum(dim=self.dim) / scale
        return self.proj(bow)


class LstmEncoder(nn.Module):

    def __init__(self, hidden, rnn_mask_avg, embedding):

        super(LstmEncoder, self).__init__()
        self.embedding = embedding
        self.hidden = hidden
        self.rnn_mask_avg = rnn_mask_avg
        output_size = 2 * hidden if rnn_mask_avg else hidden
        self.rnn = nn.LSTM(300, output_size, num_layers=2, batch_first=True, bidirectional=True)
        self.out_dim = 4 * hidden

    def forward(self, input, mask):
        if self.embedding != None:
            input = self.embedding(input)
        batch_size = input.size(0)
        batch_seq_out, (last_word_out, _) = self.rnn(input)
        if self.opt.rnn_mask_avg:
            batch_seq_out = batch_seq_out * mask.unsqueeze(-1).expand_as(batch_seq_out).float()
            return batch_seq_out.mean(dim=1)
        else:
            return last_word_out.transpose(0, 1).contiguous().view(batch_size, self.out_dim)


def create_position_codes(n_pos, dim, out):
    position_enc = np.array([
        [pos / np.power(10000, 2 * (j // 2) / dim) for j in range(dim)] for pos in range(n_pos)])

    out[:, 0::2] = torch.FloatTensor(np.sin(position_enc[:, 0::2]))
    out[:, 1::2] = torch.FloatTensor(np.cos(position_enc[:, 1::2]))
    out.detach_()
    out.requires_grad = False


class TransformerResponseWrapper(nn.Module):

    def __init__(self, transformer, hdim):
        super(TransformerResponseWrapper, self).__init__()
        dim = transformer.out_dim
        self.transformer = transformer
        self.mlp = nn.Sequential(
            nn.Linear(dim, hdim),
            nn.ReLU(),
            nn.Linear(hdim, dim)
        )

    def forward(self, input, mask):
        return self.mlp(self.transformer(input, mask))


class TransformerModel(nn.Module):

    def __init__(self, transformer_n_heads, transformer_n_layers, transformer_dim,
            vocabulary_dim, embedding=None, use_manual_norm=False, fix_mean=True,
            dropout=0, padding_idx=None):
        super(TransformerModel, self).__init__()
        self.n_layers = transformer_n_layers
        self.fix_mean = fix_mean
        n_heads = transformer_n_heads  # 8 by default
        dim = transformer_dim  # 512 by default
        self.out_dim = dim
        dim_hidden = dim * 4  # 2048 by default
        assert dim % n_heads == 0, 'transformer dim must be a multiple of n_heads'
        n_positions = 1000
        embedding_dim = dim if embedding is None else embedding.weight.shape[1]

        self.position_embeddings = nn.Embedding(n_positions, embedding_dim)
        create_position_codes(n_positions, embedding_dim, out=self.position_embeddings.weight)


        if embedding is not None:
            self.embeddings = embedding
        elif padding_idx is not None:
            self.embeddings = nn.Embedding(vocabulary_dim, embedding_dim, padding_idx=padding_idx)
        else:
            self.embeddings = nn.Embedding(vocabulary_dim, embedding_dim)

        if embedding_dim != transformer_dim:
            self.linear_upscaling = nn.Linear(embedding_dim, transformer_dim)
        else:
            self.linear_upscaling = None

        self.dim = dim
        self.attentions = nn.ModuleList()
        self.layer_norm1 = nn.ModuleList()
        self.ffns = nn.ModuleList()
        self.layer_norm2 = nn.ModuleList()

        def build_norm_layer():
            if use_manual_norm:
                return ManualNormalize()
            return nn.LayerNorm([dim])

        for _ in range(self.n_layers):
            self.attentions.append(MultiHeadAttention(n_heads, dim, dropout=dropout))
            self.layer_norm1.append(build_norm_layer())
            self.ffns.append(TransformerFFN(dim, dim_hidden, dropout=dropout))
            self.layer_norm2.append(build_norm_layer())

    def forward(self, input, mask):
        '''
        input data is a LongTensor of shape [batch, seq_len], containing each
        word's index in the embeddings table.
        mask is a ByteTensor of shape [batch, seq_len], filled with 1 when
        inside the sequence and 0 outside.
        '''
        # lengths = (inputs != 0).float().sum(dim=1)
        seq_len = input.size(1)
        positions = input.new(seq_len).long()
        positions = torch.arange(seq_len, out=positions).unsqueeze(0)
        tensor = self.embeddings(input)
        tensor = tensor + self.position_embeddings(positions).expand_as(tensor)
        if self.linear_upscaling is not None:
            tensor = self.linear_upscaling(tensor)
        tensor *= mask.unsqueeze(-1).float()



        for i in range(self.n_layers):
            tensor = tensor + self.attentions[i](tensor, mask)
            tensor = self.normalize(tensor, self.layer_norm1[i])
            tensor = tensor + self.ffns[i](tensor, mask)
            tensor = self.normalize(tensor, self.layer_norm2[i])

            tensor *= mask.unsqueeze(-1).float()
        if self.fix_mean:
            output = tensor.sum(dim=1) / mask.float().sum(dim=1).unsqueeze(-1)
        else:
            output = tensor.mean(dim=1)

        return output

    def normalize(self, tensor, norm_layer):
        size = tensor.size()
        return norm_layer(tensor.view(-1, self.dim)).view(size)


class ManualNormalize(nn.Module):

    def __init__(self):
        super(ManualNormalize, self).__init__()

    def forward(self, input):
        return input


class MultiHeadAttention(nn.Module):

    def __init__(self, n_heads, dim, dropout=0):
        super(MultiHeadAttention, self).__init__()
        self.n_heads = n_heads
        self.dim = dim

        # multi head is seen as one layer, dropout is only applied to the input
        self.in_dropout = nn.Dropout(p=dropout)
        self.q_lin = nn.Linear(dim, dim)
        self.k_lin = nn.Linear(dim, dim)
        self.v_lin = nn.Linear(dim, dim)
        nn.init.xavier_normal_(self.q_lin.weight)
        nn.init.xavier_normal_(self.k_lin.weight)
        nn.init.xavier_normal_(self.v_lin.weight)
        self.out_lin = nn.Linear(dim, dim)


        nn.init.xavier_normal_(self.out_lin.weight)

    def forward(self, input, mask):
        # Input is [B, seq_len, dim]
        # Mask is [B, seq_len]
        batch_size, seq_len, dim = input.size()
        assert dim == self.dim, f'Dimensions do not match: {dim} input vs {self.dim} configured'
        n_heads = self.n_heads
        dim_per_head = dim // n_heads

        def prepare_head(tensor):
            # input is [batch_size, seq_len, n_heads * dim_per_head]
            # output is [batch_size * n_heads, seq_len, dim_per_head]
            tensor = tensor.view(batch_size, seq_len, n_heads, dim_per_head)
            tensor = tensor.transpose(1, 2).contiguous().view(batch_size * n_heads, seq_len, dim_per_head)
            return tensor
        in_droped = self.in_dropout(input)
        query = prepare_head(self.q_lin(in_droped))
        keys = prepare_head(self.k_lin(in_droped))
        values = prepare_head(self.v_lin(in_droped))
        scale = math.sqrt(dim_per_head)

        dot_prod = query.bmm(keys.transpose(1, 2))
        # [B * n_heads, seq_len, seq_len]
        attn_mask = (mask == 0).view(batch_size, 1, 1, seq_len).repeat(1, n_heads, seq_len, 1).view(batch_size * n_heads, seq_len, seq_len)
        dot_prod.masked_fill_(attn_mask, -float('inf'))

        attn_weights = F.softmax(dot_prod / scale, dim=-1)
        # attn_weights = attn_weights.masked_fill(attn_mask, 0)  #TODO check if really necessary

        attentioned = attn_weights.bmm(values)
        attentioned = attentioned.view(batch_size, n_heads, seq_len, dim_per_head)\
                                 .transpose(1, 2).contiguous()\
                                 .view(batch_size, seq_len, dim)
        return self.out_lin(attentioned)


class TransformerFFN(nn.Module):

    def __init__(self, dim, dim_hidden, dropout=0):
        super(TransformerFFN, self).__init__()
        self.in_dropout = nn.Dropout(p=dropout)
        self.lin1 = nn.Linear(dim, dim_hidden)
        self.lin2 = nn.Linear(dim_hidden, dim)
        nn.init.xavier_normal_(self.lin1.weight)
        nn.init.xavier_normal_(self.lin2.weight)

    def forward(self, input, mask):
        return self.lin2(F.relu(self.lin1(self.in_dropout(input))))


class TransformerAdapter(nn.Module):

    def __init__(self, opt, dictionary):
        super(TransformerAdapter, self).__init__()
        self.opt = opt
        self.pad_idx = dictionary[PAD_TOKEN]
        self.ctx_transformer = TransformerModel(opt, dictionary)
        if opt.two_transformers:
            self.cand_transformer = TransformerModel(opt, dictionary)
        else:
            self.cand_transformer = self.ctx_transformer
        dim = self.ctx_transformer.dim
        hdim = dim * opt.transformer_response_hmul
        self.response_dnn = nn.Sequential(
            nn.Linear(dim, hdim),
            nn.ReLU(),
            nn.Linear(hdim, dim)
        )
        self.embeddings = self.ctx_transformer.embeddings

        mood_dims = opt.moods_dims
        self.mood_dropout = nn.Dropout(p=opt.moods_dropout)
        self.mood_dnn = nn.Sequential(
            nn.Linear(self.opt.moods_dims, dim)
        )

    def forward(self, context_w, personas_w, cands_w, moods = None):
        if context_w is not None:
            context_mask = context_w != self.pad_idx
            context_h = self.ctx_transformer(context_w, context_mask)
            if self.opt.normalize_sent_emb:
                context_h = context_h / context_h.norm(2, dim=1, keepdim=True)
            if moods is not None:
                # dropout some of the moods randomly. This way the network does
                # not rely too much on the mood.
                # create a mask on the same device as context
                if moods.shape[0] > 0 and moods.shape[1] > 0 and self.opt.moods_dropout != 1:
                    mask = torch.ones(moods.shape[0], dtype=context_h.dtype, device=context_h.device).unsqueeze(1)
                    mask = self.mood_dropout(mask)
                    mask = mask.expand(moods.shape[0], moods.shape[1])
                    moods *= mask
                    context_h += self.mood_dnn(moods)
        else:
            context_h = None


        if cands_w is not None:
            cands_mask = cands_w != self.pad_idx
            cands_h = self.cand_transformer(cands_w, cands_mask)
            cands_h = self.response_dnn(cands_h)
            if self.opt.normalize_sent_emb:
                cands_h = cands_h / cands_h.norm(2, dim=1, keepdim=True)

        else:
            cands_h = None
        return context_h, cands_h

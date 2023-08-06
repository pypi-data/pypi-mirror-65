#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import torch
import torch.nn as nn
import torch.nn.functional as F

import math
import numpy as np
from parlai.utils.torch import neginf

UNK_TOKEN = '__UNK__'
PAD_TOKEN = '__PAD__'
SOC_TOKEN = '__SOC__'
EMPTY_PERSONA_TOKEN = '__PER__'


class MemNetModel(nn.Module):
    """Model which takes context and candidates and encodes them"""

    def __init__(self, opt, dictionary, pad_token=PAD_TOKEN):
        super().__init__()
        self.opt = opt
        self.pad_idx = dictionary[pad_token]
        self.tau = opt.get('embeddings_size') ** 0.5 if self.opt.get('tau') else 1
        self.alpha = opt.get('alpha')
        self.validtau = opt.get('validtau')
        self.dumps = [f'{int(torch.randint(10000, (1,))):05d}', 0]  # id, count

        # set up embeddings
        self.embeddings = nn.Embedding(
            len(dictionary), opt.get('embeddings_size'), padding_idx=self.pad_idx
        )
        if not opt.get('learn_embeddings'):
            self.embeddings.weight.requires_grad = False
        nn.init.normal_(self.embeddings.weight, mean=0, std=0.05)

        self.transformer_dropout = opt.get('transformer_dropout')
        self.memory_dropout = nn.Dropout(opt.get('memory_dropout'))
        self.context_encoder = self.build_encoder(opt, dictionary, self.embeddings)

        if opt.get('share_encoders'):
            dim = self.context_encoder.out_dim
            hdim = dim * opt.get('transformer_response_hmul')
            self.cand_encoder = TransformerResponseWrapper(self.context_encoder, hdim)
        else:
            self.cand_encoder = self.build_encoder(opt, dictionary, self.embeddings)

        if opt.get('gru'):
            self.gru = nn.GRU(
                opt.get('embeddings_size'), opt.get('embeddings_size'), batch_first=True
            )
        if opt.get('concat'):
            self.cat = nn.Sequential(
                nn.Linear(
                    2 * opt.get('embeddings_size'), 2 * opt.get('embeddings_size')
                ),
                nn.ReLU(),
                nn.Linear(
                    2 * opt.get('embeddings_size'), 2 * opt.get('embeddings_size')
                ),
                nn.ReLU(),
                nn.Linear(2 * opt.get('embeddings_size'), opt.get('embeddings_size')),
            )

        if opt.get('use_moods'):
            self.mood_dropout = nn.Dropout(p=opt.get('moods_dropout'))
            self.mood_dnn = nn.Sequential(
                nn.Linear(self.opt.get('moods_dims'), self.context_encoder.out_dim)
            )
        self.final_proj = nn.Linear(4 * opt.get('hidden'), 2 * opt.get('hidden'))

    def encode_cand(self, words):
        if words is None:
            return None
        word_mask = words != self.pad_idx
        return self.cand_encoder(words, word_mask)

    def encode_context(self, context_w):
        context_mask = context_w != self.pad_idx
        # [batch, d]
        context_h = self.context_encoder(context_w, context_mask)

        return context_h

    def build_encoder(self, opt, dictionary, embedding=None):
        if opt.get('encoder_type') == 'bow':
            return BowEncoder(
                dim=1,
                out_size=4 * opt.get('hidden'),
                scale_sqrt=opt.get('bow_scale_sqrt'),
                n_tanh=opt.get('bow_tanh'),
                embedding=embedding,
                embeddings_size=opt.get('embeddings_size'),
            )
        elif opt.get('encoder_type') == 'lstm':
            return LstmEncoder(opt, embedding=embedding)
        elif opt.get('encoder_type') == 'transformer':
            dropout = self.transformer_dropout if self.transformer_dropout else 0
            return TransformerModel(
                opt.get('transformer_n_heads'),
                opt.get('n_layers'),
                opt.get('transformer_dim'),
                len(dictionary),
                embedding=embedding,
                dropout=dropout,
                use_manual_norm=opt.get('use_manual_norm'),
            )

    def forward(self, context_w, cands_w, moods=None):
        if cands_w is not None and cands_w.size(0) == 1 and cands_w.dim() == 3:
            cands_w = cands_w.squeeze(0)

        # lengths = (inputs != 0).float().sum(dim=1)
        if context_w is not None:
            context_h = self.encode_context(context_w)
        else:
            context_h = None
        if cands_w is not None:
            cands_h = self.encode_cand(cands_w)
        else:
            cands_h = None

        if moods is not None:
            # dropout some of the moods randomly. This way the network does
            # not rely too much on the mood.
            # create a mask on the same device as context
            if self.opt.get('moods_dropout') != 1:
                mask = torch.ones(
                    moods.shape[0], dtype=context_h.dtype, device=context_h.device
                ).unsqueeze(1)
                mask = self.mood_dropout(mask)
                moods *= mask
                context_h += self.mood_dnn(moods)

        if self.opt.get('normalize_sent_emb'):
            if context_h is not None:
                context_h = context_h / context_h.norm(2, dim=1, keepdim=True)
            if cands_h is not None:
                cands_h = cands_h / cands_h.norm(2, dim=1, keepdim=True)

        return context_h, cands_h

    def attention(self, memory, request, memmask=None):
        # memory is [B, d]
        # request is [B, d]
        tau = self.validtau if self.opt.get('testing') else self.tau
        request = request.unsqueeze(-1)
        if memmask is not None:
            memmasked = memory.clone() * (memmask.sum(2, keepdim=True) != 0).float()
            # [B, seq_len]
            weights = F.softmax(memmasked.bmm(request).squeeze(-1) / tau, dim=1)
        else:
            # [B, seq_len]
            weights = F.softmax(memory.bmm(request).squeeze(-1) / tau, dim=1)

        # [B, d]
        return weights, weights.unsqueeze(1).bmm(memory).squeeze(1)


class MemNetPersonaModel(nn.Module):
    """Model which takes context, personas, candidates and encodes them"""

    def __init__(self, opt, dictionary, pad_token=PAD_TOKEN):
        super().__init__()
        self.opt = opt
        self.pad_idx = dictionary[pad_token]
        self.tau = opt.get('embeddings_size') ** 0.5 if self.opt.get('tau') else 1
        self.alpha = opt.get('alpha')
        self.validtau = opt.get('validtau')
        self.dumps = [f'{int(torch.randint(10000, (1,))):05d}', 0]  # id, count

        # set up embeddings
        self.embeddings = nn.Embedding(
            len(dictionary), opt.get('embeddings_size'), padding_idx=self.pad_idx
        )
        if not opt.get('learn_embeddings'):
            self.embeddings.weight.requires_grad = False
        nn.init.normal_(self.embeddings.weight, mean=0, std=0.05)

        self.transformer_dropout = opt.get('transformer_dropout')
        self.memory_dropout = nn.Dropout(opt.get('memory_dropout'))
        self.context_encoder = self.build_encoder(opt, dictionary, self.embeddings)

        if opt.get('share_encoders'):
            dim = self.context_encoder.out_dim
            hdim = dim * opt.get('transformer_response_hmul')
            self.cand_encoder = TransformerResponseWrapper(self.context_encoder, hdim)
        else:
            self.cand_encoder = self.build_encoder(opt, dictionary, self.embeddings)

        # build persona encoder
        self.persona_encoder_type = opt.get('persona_encoder', 'BOW')
        if self.persona_encoder_type == 'BOW' or self.opt.get(
            'load_all_encoders', False
        ):
            self.persona_encoder = BowEncoder(
                dim=2,
                out_size=self.context_encoder.out_dim,
                scale_sqrt=opt.get('bow_scale_sqrt'),
                n_tanh=opt.get('bow_tanh'),
                embedding=self.embeddings,
                embeddings_size=opt.get('embeddings_size'),
                dropout=opt.get('persona_dropout', 0.0),
            )
        if self.persona_encoder_type == 'transformer' or opt.get(
            'load_all_encoders', False
        ):
            if opt.get('wrap_persona_encoder', False):
                dim = self.context_encoder.out_dim
                hdim = dim * opt.get('transformer_response_hmul')
                self.persona_transformer = TransformerResponseWrapper(
                    self.context_encoder, hdim
                )
            elif opt.get('pers_use_cand_encoder', False):
                self.persona_transformer = self.cand_encoder
            else:
                self.persona_transformer = self.context_encoder
            self.attender = BasicAttention(
                dim=2, attn=opt.get('basic_attention', 'cosine')
            )

        if opt.get('gru'):
            self.gru = nn.GRU(
                opt.get('embeddings_size'), opt.get('embeddings_size'), batch_first=True
            )
        if opt.get('concat'):
            self.cat = nn.Sequential(
                nn.Linear(
                    2 * opt.get('embeddings_size'), 2 * opt.get('embeddings_size')
                ),
                nn.ReLU(),
                nn.Linear(
                    2 * opt.get('embeddings_size'), 2 * opt.get('embeddings_size')
                ),
                nn.ReLU(),
                nn.Linear(2 * opt.get('embeddings_size'), opt.get('embeddings_size')),
            )

        if opt.get('use_moods'):
            self.mood_dropout = nn.Dropout(p=opt.get('moods_dropout'))
            self.mood_dnn = nn.Sequential(
                nn.Linear(self.opt.get('moods_dims'), self.context_encoder.out_dim)
            )
        self.final_proj = nn.Linear(4 * opt.get('hidden'), 2 * opt.get('hidden'))

    def encode_cand(self, words):
        if words is None:
            return None
        word_mask = words != self.pad_idx
        return self.cand_encoder(words, word_mask)

    def encode_context_persona(self, context_w, personas_w):
        if self.persona_encoder_type == 'BOW':
            ones = torch.ones(context_w.size(0), 1)
            ones = ones.cuda() if not self.opt.get('no_cuda') else ones
            mask = self.memory_dropout(ones)

            context_mask = context_w != self.pad_idx
            # [batch, d]
            context_h = self.context_encoder(context_w, context_mask)

            if personas_w is None:
                return [], context_h

            persona_mask = personas_w != self.pad_idx
            # [batch, n_persona, d]
            persona_h = self.persona_encoder(personas_w, persona_mask)

            if self.opt.get('gru'):
                _, context_h = self.gru(persona_h, context_h.unsqueeze(0))
                context_h = context_h.squeeze(0)
                weights = []
            else:
                weights, attentioned = self.attention(
                    persona_h,
                    context_h,
                    persona_mask if self.opt.get('maskpersona') else None,
                    self.opt.get('cosine_attention'),
                )
                if self.opt.get('concat'):
                    cat = torch.cat((context_h, attentioned), dim=1)
                    context_h = self.cat(cat)
                    return [], context_h
                context_h = context_h + self.alpha * mask * attentioned
            return weights, context_h
        else:
            context_mask = context_w != self.pad_idx
            # [batch, d]
            context_h = self.context_encoder(context_w, context_mask)

            if personas_w is None:
                return [], context_h

            bsz = personas_w.size(0)
            personas_w = personas_w.view(-1, personas_w.size(-1))
            mask = personas_w != self.pad_idx
            personas_h = self.persona_transformer(personas_w, mask)
            personas_h = personas_h.view(bsz, -1, personas_h.size(-1))

            context_h = context_h.unsqueeze(1)
            context_h, weights = self.attender(context_h, personas_h)

            return weights, context_h

    def build_encoder(self, opt, dictionary, embedding=None):
        if opt.get('encoder_type') == 'bow':
            return BowEncoder(
                dim=1,
                out_size=4 * opt.get('hidden'),
                scale_sqrt=opt.get('bow_scale_sqrt'),
                n_tanh=opt.get('bow_tanh'),
                embedding=embedding,
                embeddings_size=opt.get('embeddings_size'),
            )
        elif opt.get('encoder_type') == 'lstm':
            return LstmEncoder(opt, embedding=embedding)
        elif opt.get('encoder_type') == 'transformer':
            dropout = self.transformer_dropout if self.transformer_dropout else 0
            return TransformerModel(
                opt.get('transformer_n_heads'),
                opt.get('n_layers'),
                opt.get('transformer_dim'),
                len(dictionary),
                embedding=embedding,
                dropout=dropout,
                use_manual_norm=opt.get('use_manual_norm'),
            )

    def forward(self, context_w, personas_w, cands_w, moods=None):
        if cands_w is not None and cands_w.size(0) == 1 and cands_w.dim() == 3:
            cands_w = cands_w.squeeze(0)

        if context_w is not None:
            weights, context_h = self.encode_context_persona(context_w, personas_w)
        else:
            context_h = None
        cands_h = self.encode_cand(cands_w)

        if moods is not None:
            # dropout some of the moods randomly. This way the network does
            # not rely too much on the mood.
            # create a mask on the same device as context
            if self.opt.get('moods_dropout') != 1:
                mask = torch.ones(
                    moods.shape[0], dtype=context_h.dtype, device=context_h.device
                ).unsqueeze(1)
                mask = self.mood_dropout(mask)
                moods *= mask
                context_h += self.mood_dnn(moods)

        if self.opt.get('normalize_sent_emb'):
            context_h = context_h / context_h.norm(2, dim=1, keepdim=True)
            cands_h = cands_h / cands_h.norm(2, dim=1, keepdim=True)

        return context_h, cands_h

    def attention(self, memory, request, memmask=None, cosine=False):
        # memory is [B, nbpersona, d]
        # request is [B, d]
        tau = self.validtau if self.opt.get('testing') else self.tau
        request = request.unsqueeze(-1)
        if cosine:
            memory = memory / memory.norm(2, dim=2, keepdim=True)
            request = request / request.norm(2, dim=1, keepdim=True)
        if memmask is not None:
            memmasked = memory.clone() * (memmask.sum(2, keepdim=True) != 0).float()
            # [B, seq_len]
            weights = F.softmax(memmasked.bmm(request).squeeze(-1) / tau, dim=1)
        else:
            # [B, seq_len]
            weights = F.softmax(memory.bmm(request).squeeze(-1) / tau, dim=1)

        # [B, d]
        return weights, weights.unsqueeze(1).bmm(memory).squeeze(1)


class TransformerTowerModel(nn.Module):
    """
        Tries to follow up a transformer with another transformer,
        in order to encode the persona (or the knowledge) and then pay attention
        to it.

        It is slightly different because it expects the elements of history
        to be a 3d vector (size_batch, num_elements, sentence)

        This may scale better, not sure actually.
    """

    def __init__(self, opt, dictionary, pad_token=PAD_TOKEN):
        super().__init__()
        self.opt = opt
        self.voc_dim = len(dictionary)
        self.embed_dim = opt.get('embeddings_size')
        self.trans_dim = opt.get('transformer_dim')
        self.pad_idx = dictionary[pad_token]

        # set up embeddings
        self.embeddings = nn.Embedding(
            self.voc_dim, self.embed_dim, padding_idx=self.pad_idx
        )
        if not opt.get('learn_embeddings'):
            self.embeddings.weight.requires_grad = False
        nn.init.normal_(self.embeddings.weight, mean=0, std=0.05)

        # in case the transformer dim is not the same as the transformer dropout
        # we have a layer of adaptation. For simplicity it's used all the time.
        self.dim_adapt = nn.Linear(self.embed_dim, opt.get('transformer_dim'))

        # There is just one bloc that encode every sentence
        self.base_transformer = TransformerNoEmbeddingsModel(
            transformer_n_heads=opt.get('transformer_n_heads'),
            transformer_n_layers=opt.get('n_layers'),
            transformer_dim=self.trans_dim,
            dropout=opt.get('transformer_dropout'),
            use_manual_norm=opt.get('use_manual_norm'),
        )

        # On top of the base transformer,we add a different linear layer
        # For persona and context
        self.adapt_context = nn.Linear(self.trans_dim, self.trans_dim)
        self.adapt_persona = nn.Linear(self.trans_dim, self.trans_dim)

        # For the context, we have a second transformer,
        self.top_transformer = TransformerNoEmbeddingsModel(
            transformer_n_heads=opt.get('t2_n_heads'),
            transformer_n_layers=opt.get('t2_n_layers'),
            transformer_dim=self.trans_dim,
            dropout=opt.get('t2_dropout'),
        )

        # for the candidates, we add a simple MLP, with a central layer of
        # 2x tranformer size
        self.candidate_up = nn.Sequential(
            nn.Linear(self.trans_dim, 2 * self.trans_dim),
            nn.ReLU(),
            nn.Linear(2 * self.trans_dim, self.trans_dim),
        )

    def forward(self, context_w, personas_w, cands_w):
        """
            All LongTensors. They all can be None it's no problem.
            context_w: [bs, history_len, sentence_len]
            personas_w: [bs, nb_personas, sentence_len]
            cands_w: [bs, sentence_len]
        """
        context_h = self.t1_block(
            context_w, self.pad_idx
        )  # [bs, history_len, trans_dim]
        persona_h = self.t1_block(
            personas_w, self.pad_idx
        )  # [bs, nb_personas, trans_dim]
        cands_h = self.t1_block(cands_w, self.pad_idx)  # [bs, trans_dim]

        # cands first, easier
        cands_embedded = None if cands_h is None else self.candidate_up(cands_h)
        if context_w is None:
            return None, cands_embedded

        # then context and personality
        context_hl = self.adapt_context(context_h)
        if persona_h is None:
            context_and_pers = context_hl
        else:
            persona_hl = None if persona_h is None else self.adapt_persona(persona_h)
            # print("context shape %s" % str(context_hl.shape))
            # print("persona shape %s" % str(persona_hl.shape))
            context_and_pers = torch.cat([context_hl, persona_hl], 1)

        # then apply the 2nd transformer
        cpsh = context_and_pers.shape
        all_one_mask = torch.ones(
            [context_and_pers.shape[0], context_and_pers.shape[1]],
            dtype=torch.uint8,
            device=context_and_pers.device,
        )
        context_embedding = self.top_transformer(context_and_pers, all_one_mask)
        return context_embedding, cands_embedded

    def t1_block(self, input, pad_idx):
        """
            Applies the word embedding and the first transformer to input.
            Input is a LongTensor that is worth pad_idx when not a sequence.
            Can be [batch_size, M, sentence_len] or [batch_size, sentence_len]
        """
        if input is None:
            return None
        mask = input != pad_idx
        embedded = self.embeddings(input)
        embedded = self.dim_adapt(embedded)
        nb_dim = len(input.shape)
        if nb_dim == 2:
            # transformer takes 3d block so that's straightforward.
            transformed = self.base_transformer(embedded, mask)
            return transformed
        if nb_dim == 3:
            # reduces dim to accomodate the code of transformer
            emb_shape = embedded.shape  # should be len() == 4
            emb_flat = embedded.view(-1, emb_shape[2], emb_shape[3])
            mask_flat = mask.view(-1, emb_shape[2])
            transformed_flat = self.base_transformer(emb_flat, mask_flat)
            transformed = transformed_flat.view(
                emb_shape[0], emb_shape[1], emb_shape[3]
            )
            return transformed
        print("NB Dim is %d, not taken into account" % nb_dim)
        return None


class BowEncoder(nn.Module):
    """Bag of words encoder. This is used to encode the persona"""

    def __init__(
        self,
        dim,
        out_size,
        scale_sqrt,
        n_tanh,
        embedding,
        embeddings_size=300,
        dropout=0,
    ):
        super(BowEncoder, self).__init__()
        self.dim = dim
        self.embedding = embedding
        self.in_dropout = nn.Dropout(p=dropout)
        self.scale_sqrt = scale_sqrt
        nn_layers = []
        for _ in range(n_tanh):
            nn_layers.append(nn.Linear(embeddings_size, embeddings_size))
            nn_layers.append(nn.Tanh())
        nn_layers.append(nn.Linear(embeddings_size, out_size))
        self.out_dim = out_size
        self.proj = nn.Sequential(*nn_layers)

    def forward(self, input, mask):
        input = self.in_dropout(self.embedding(input))
        scale = mask.sum(self.dim, keepdim=True).float().clamp(min=1)
        if self.scale_sqrt:
            scale = scale.sqrt()
        bow = input.sum(dim=self.dim) / scale
        return self.proj(bow)


class LstmEncoder(nn.Module):
    """LSTM encoder"""

    def __init__(self, hidden, rnn_mask_avg, embedding):
        super(LstmEncoder, self).__init__()
        self.embedding = embedding
        self.hidden = hidden
        self.rnn_mask_avg = rnn_mask_avg
        output_size = 2 * hidden if rnn_mask_avg else hidden
        self.rnn = nn.LSTM(
            300, output_size, num_layers=2, batch_first=True, bidirectional=True
        )
        self.out_dim = 4 * hidden

    def forward(self, input, mask):
        if self.embedding is not None:
            input = self.embedding(input)
        batch_size = input.size(0)
        batch_seq_out, (last_word_out, _) = self.rnn(input)
        if self.opt.get('rnn_mask_avg'):
            batch_seq_out = (
                batch_seq_out * mask.unsqueeze(-1).expand_as(batch_seq_out).float()
            )
            return batch_seq_out.mean(dim=1)
        else:
            return (
                last_word_out.transpose(0, 1)
                .contiguous()
                .view(batch_size, self.out_dim)
            )


def create_position_codes(n_pos, dim, out):
    position_enc = np.array(
        [
            [pos / np.power(10000, 2 * (j // 2) / dim) for j in range(dim)]
            for pos in range(n_pos)
        ]
    )

    out[:, 0::2] = torch.FloatTensor(np.sin(position_enc[:, 0::2]))
    out[:, 1::2] = torch.FloatTensor(np.cos(position_enc[:, 1::2]))
    out.detach_()
    out.requires_grad = False


class TransformerResponseWrapper(nn.Module):
    """Transformer response rapper. Pushes input through transformer and MLP"""

    def __init__(self, transformer, hdim):
        super(TransformerResponseWrapper, self).__init__()
        dim = transformer.out_dim
        self.transformer = transformer
        self.mlp = nn.Sequential(nn.Linear(dim, hdim), nn.ReLU(), nn.Linear(hdim, dim))

    def forward(self, input, mask):
        return self.mlp(self.transformer(input, mask))


class TransformerModel(nn.Module):
    """Transformer model"""

    def __init__(
        self,
        transformer_n_heads,
        transformer_n_layers,
        transformer_dim,
        vocabulary_dim,
        embedding=None,
        use_manual_norm=False,
        fix_mean=True,
        dropout=0,
        padding_idx=None,
        has_embeddings=True,
    ):
        super(TransformerModel, self).__init__()
        self.n_layers = transformer_n_layers
        self.fix_mean = fix_mean
        n_heads = transformer_n_heads
        dim = transformer_dim
        self.out_dim = dim
        dim_hidden = dim * 4
        assert dim % n_heads == 0, 'transformer dim must be a multiple of n_heads'
        n_positions = 1000

        embedding_dim = dim if embedding is None else embedding.weight.shape[1]
        self.position_embeddings = nn.Embedding(n_positions, embedding_dim)
        create_position_codes(
            n_positions, embedding_dim, out=self.position_embeddings.weight
        )

        if embedding is not None:
            self.embeddings = embedding
        elif padding_idx is not None:
            self.embeddings = nn.Embedding(
                vocabulary_dim, embedding_dim, padding_idx=padding_idx
            )
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
        """
            input data is a FloatTensor of shape [batch, seq_len, dim]
            mask is a ByteTensor of shape [batch, seq_len], filled with 1 when
            inside the sequence and 0 outside.
        """
        seq_len = input.size(1)
        positions = input.new(seq_len).long()
        positions = torch.arange(seq_len, out=positions).unsqueeze(0)
        tensor = self.embeddings(input)
        tensor = tensor + self.position_embeddings(positions).expand_as(tensor)

        if self.linear_upscaling is not None:
            tensor = self.linear_upscaling(tensor)
        tensor *= mask.unsqueeze(-1).type_as(tensor)
        for i in range(self.n_layers):
            tensor = tensor + self.attentions[i](tensor, mask)
            tensor = self.normalize(tensor, self.layer_norm1[i])
            tensor = tensor + self.ffns[i](tensor, mask)
            tensor = self.normalize(tensor, self.layer_norm2[i])

            tensor *= mask.unsqueeze(-1).type_as(tensor)
        if self.fix_mean:
            output = tensor.sum(dim=1) / mask.type_as(tensor).sum(dim=1).unsqueeze(
                -1
            ).clamp(min=1e-20)
        else:
            output = tensor.mean(dim=1)

        return output

    def normalize(self, tensor, norm_layer):
        size = tensor.size()
        return norm_layer(tensor.view(-1, self.dim)).view(size)


class TransformerNoEmbeddingsModel(nn.Module):
    """Transformer model without the embedding part"""

    def __init__(
        self,
        transformer_n_heads,
        transformer_n_layers,
        transformer_dim,
        use_manual_norm=False,
        fix_mean=True,
        dropout=0,
    ):
        super(TransformerNoEmbeddingsModel, self).__init__()
        self.n_layers = transformer_n_layers
        self.fix_mean = fix_mean
        n_heads = transformer_n_heads
        dim = transformer_dim
        self.out_dim = dim
        dim_hidden = dim * 4
        assert dim % n_heads == 0, 'transformer dim must be a multiple of n_heads'
        n_positions = 1000
        self.position_embeddings = nn.Embedding(n_positions, transformer_dim)
        create_position_codes(
            n_positions, transformer_dim, out=self.position_embeddings.weight
        )
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

    def forward(self, tensor, mask):
        """
            input: FloatTensor [size_batch, sentence_len, transformer_dim]
            mask: ByteTensor [size_batch, sentence_len], is worth 1 if we're
                in the sequence.
        """
        seq_len = tensor.size(1)
        positions = tensor.new(seq_len).long()
        positions = torch.arange(seq_len, out=positions).unsqueeze(0)
        tensor = tensor + self.position_embeddings(positions).expand_as(tensor)
        tensor *= mask.unsqueeze(-1).float()
        for i in range(self.n_layers):
            tensor = tensor + self.attentions[i](tensor, mask)
            tensor = self.normalize(tensor, self.layer_norm1[i])
            tensor = tensor + self.ffns[i](tensor, mask)
            tensor = self.normalize(tensor, self.layer_norm2[i])

            tensor *= mask.unsqueeze(-1).float()
        if self.fix_mean:
            output = tensor.sum(dim=1) / mask.float().sum(dim=1).unsqueeze(-1).clamp(
                min=1e-20
            )
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


class BasicAttention(nn.Module):
    def __init__(self, dim=1, attn='cosine'):
        super().__init__()
        self.softmax = nn.Softmax(dim=dim)
        if attn == 'cosine':
            self.cosine = nn.CosineSimilarity(dim=dim)
        self.attn = attn
        self.dim = dim

    def forward(self, xs, ys):
        if self.attn == 'cosine':
            l1 = self.cosine(xs, ys).unsqueeze(self.dim - 1)
        else:
            l1 = torch.bmm(xs, ys.transpose(1, 2))
            if self.attn == 'sqrt':
                d_k = ys.size(-1)
                l1 = l1 / math.sqrt(d_k)
        l2 = self.softmax(l1)
        lhs_emb = torch.bmm(l2, ys)
        # add back the query
        lhs_emb = lhs_emb.add(xs)

        return lhs_emb.squeeze(self.dim - 1), l2


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
        assert (
            dim == self.dim
        ), f'Dimensions do not match: {dim} input vs {self.dim} configured'
        n_heads = self.n_heads
        dim_per_head = dim // n_heads

        def prepare_head(tensor):
            # input is [batch_size, seq_len, n_heads * dim_per_head]
            # output is [batch_size * n_heads, seq_len, dim_per_head]
            tensor = tensor.view(batch_size, seq_len, n_heads, dim_per_head)
            tensor = (
                tensor.transpose(1, 2)
                .contiguous()
                .view(batch_size * n_heads, seq_len, dim_per_head)
            )
            return tensor

        in_droped = self.in_dropout(input)
        query = prepare_head(self.q_lin(in_droped))
        keys = prepare_head(self.k_lin(in_droped))
        values = prepare_head(self.v_lin(in_droped))
        scale = math.sqrt(dim_per_head)

        dot_prod = query.bmm(keys.transpose(1, 2))
        # [B * n_heads, seq_len, seq_len]
        attn_mask = (
            (mask == 0)
            .view(batch_size, 1, 1, seq_len)
            .repeat(1, n_heads, seq_len, 1)
            .view(batch_size * n_heads, seq_len, seq_len)
        )
        dot_prod.masked_fill_(attn_mask, neginf(dot_prod.dtype))

        attn_weights = F.softmax(dot_prod / scale, dim=-1)

        attentioned = attn_weights.bmm(values)
        attentioned = (
            attentioned.view(batch_size, n_heads, seq_len, dim_per_head)
            .transpose(1, 2)
            .contiguous()
            .view(batch_size, seq_len, dim)
        )

        out = self.out_lin(attentioned)

        return out


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
        if opt.get('two_transformers'):
            self.cand_transformer = TransformerModel(opt, dictionary)
        else:
            self.cand_transformer = self.ctx_transformer
        dim = self.ctx_transformer.dim
        hdim = dim * opt.get('transformer_response_hmul')
        self.response_dnn = nn.Sequential(
            nn.Linear(dim, hdim), nn.ReLU(), nn.Linear(hdim, dim)
        )
        self.embeddings = self.ctx_transformer.embeddings

        self.mood_dropout = nn.Dropout(p=opt.get('moods_dropout'))
        self.mood_dnn = nn.Sequential(nn.Linear(self.opt.get('moods_dims'), dim))

    def forward(self, context_w, personas_w, cands_w, moods=None):
        if context_w is not None:
            context_mask = context_w != self.pad_idx
            context_h = self.ctx_transformer(context_w, context_mask)
            if self.opt.get('normalize_sent_emb'):
                context_h = context_h / context_h.norm(2, dim=1, keepdim=True)
            if moods is not None:
                # dropout some of the moods randomly. This way the network does
                # not rely too much on the mood.
                # create a mask on the same device as context
                if (
                    moods.shape[0] > 0
                    and moods.shape[1] > 0
                    and self.opt.get('moods_dropout') != 1
                ):
                    mask = torch.ones(
                        moods.shape[0], dtype=context_h.dtype, device=context_h.device
                    ).unsqueeze(1)
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
            if self.opt.get('normalize_sent_emb'):
                cands_h = cands_h / cands_h.norm(2, dim=1, keepdim=True)
        else:
            cands_h = None

        return context_h, cands_h

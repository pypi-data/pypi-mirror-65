#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import torch
from torch import nn
import math
import torch.nn.functional as F
import numpy as np
from parlai.utils.torch import neginf
import json
from parlai.utils.misc import warn_once

from parlai_internal.agents.transformer_ranker.modules import TransformerModel
from parlai.agents.transformer.modules import (
    TransformerEncoder,
    create_position_codes,
    TransformerEncoderLayer,
    BasicAttention,
    gelu,
)


class GeLu(nn.Module):
    def __init__(self, negative_slope=1e-2, inplace=False):
        super(GeLu, self).__init__()

    def forward(self, input):
        return gelu(input)


class TransResNetMultimodalModel(nn.Module):
    """
        Model for image dialog.
        There are two options for incorporating dialog history:
            1. Use the same transformer to encode dialog history and candidate
               responses; sum the image encoding, personality encoding, and
               dialog history encoding, and use that as query for candidate response
            2. (Multi-modal) Feed (something) into a separate transformer
               after computing the encoding; use that as query
    """

    def __init__(self, opt, personalities_list, dictionary):
        super().__init__()
        self.opt = opt
        self.use_cuda = not opt['no_cuda'] and torch.cuda.is_available()
        self.text_encoder_frozen = False
        self.fp16 = opt.get('fp16', False)
        self.hidden_dim = self.opt['hidden_dim']

        # blank encoding (for concat)
        self.blank_encoding = torch.Tensor(opt['hidden_dim']).fill_(0).detach_()
        if self.use_cuda:
            self.blank_encoding = self.blank_encoding.cuda()
        if self.fp16:
            self.blank_encoding = self.blank_encoding.half()

        # Encoders
        self.encode_image = opt.get('encode_image', True)
        self.encode_personality = opt.get('encode_personality', True)
        self.encode_dialog_history = opt.get('encode_dialog_history', True)
        self.padding_idx = dictionary[dictionary.null_token]

        #  Attention related
        self.attention_type = self.opt.get('attention_over_image')
        self.attention_num_heads = opt.get('attention_num_heads', 4)
        self.fnn_after_attention = opt.get('fnn_after_attention', False)
        self.ffn_before_attention = opt.get('fnn_before_attention', False)
        if self.attention_type and self.attention_type == 'basic':
            # Basic attention need dimension changes before head
            self.ffn_before_attention = True
        self.key_dim = (
            self.opt['image_features_dim']
            if not self.ffn_before_attention
            else self.hidden_dim
        )

        # build attention (build if attention-over-image is set, this also changes mem complexity to o (btz^2)
        self.build_attention()
        # Multimodal Combiner (build if `--multimodal true` )
        self.build_multimodal()

        # Label and Context (dialog history) Encoders
        self.label_encoder, self.additional_layer = self.build_encoders(
            dictionary, False, build_context_encoder=False
        )

        if self.opt.get('share_encoder'):
            self.context_encoder = self.label_encoder
        else:
            self.context_encoder, _ = self.build_encoders(dictionary, False, True)

        # Image Encoder
        self.build_image_encoder()

        # personality Encoder
        self.build_personality_encoder(personalities_list)

    def attend(self, attention_layer, queries, keys):
        """ 
            Unify the API of MultiHeadAttention and
            BasicAttention that are slighlty different
        """
        if isinstance(attention_layer, BasicAttention):
            return attention_layer(queries, keys, None)
        elif isinstance(attention_layer, ImageMultiHeadAttention):
            return attention_layer(queries, keys, None)
        else:
            raise Exception('Unrecognized type of attention')

    def build_attention(self):
        if self.attention_type == 'multihead' or self.attention_type == 'basic':
            # 7 * 7 spatial + 1 final embedding
            self.image_position_embedding = nn.Embedding(50, self.key_dim)
            nn.init.normal_(
                self.image_position_embedding.weight, 0, self.key_dim ** -0.5
            )

        if self.attention_type == 'multihead':
            self.attention = ImageMultiHeadAttention(
                self.attention_num_heads,
                self.hidden_dim,
                self.hidden_dim,
                self.key_dim,
                self.opt['dropout'],
            )

        elif self.attention_type == 'basic':
            self.attention = BasicAttention(dim=2, attn='basic', get_weights=False)
        else:
            self.attention = None

    def build_personality_encoder(self, personalities_list):
        # Initialize personas dictionary
        self.personality_to_id = {}
        for i, p in enumerate(personalities_list):
            self.personality_to_id[p] = i
        self.personality_dim = len(personalities_list) + 1
        personality_layers = [
            nn.BatchNorm1d(self.personality_dim),
            nn.Dropout(p=self.opt['dropout']),
            nn.Linear(self.personality_dim, self.opt['hidden_dim']),
        ]
        self.persona_encoder = nn.Sequential(*personality_layers)

    def build_image_encoder(self):
        nlayers_img = (
            self.opt['num_layers_all']
            if self.opt['num_layers_all'] != -1
            else self.opt['num_layers_image_encoder']
        )
        if self.attention == None:
            image_layers = [
                nn.BatchNorm1d(self.opt['image_features_dim']),
                nn.Dropout(p=self.opt['dropout']),
                nn.Linear(self.opt['image_features_dim'], self.hidden_dim),
            ]
            for _ in range(nlayers_img - 1):
                image_layers += [
                    GeLu(),
                    nn.Dropout(p=self.opt['dropout']),
                    nn.Linear(self.hidden_dim, self.hidden_dim),
                ]
            self.image_encoder = nn.Sequential(*image_layers)
        else:
            image_layers = [nn.BatchNorm1d(50)]
            if self.ffn_before_attention:
                image_layers += [
                    nn.Dropout(p=self.opt['dropout']),
                    nn.Linear(self.opt['image_features_dim'], self.hidden_dim),
                ]
                for _ in range(nlayers_img - 1):
                    image_layers += [
                        GeLu(),
                        nn.Dropout(p=self.opt['dropout']),
                        nn.Linear(self.hidden_dim, self.hidden_dim),
                    ]
            self.image_encoder = nn.Sequential(*image_layers)
            if self.fnn_after_attention:
                image_layers = [
                    nn.BatchNorm1d(self.hidden_dim),
                    nn.Dropout(p=self.opt['dropout']),
                    nn.Linear(self.hidden_dim, self.hidden_dim),
                ]
                for _ in range(nlayers_img - 1):
                    image_layers += [
                        GeLu(),
                        nn.Dropout(p=self.opt['dropout']),
                        nn.Linear(self.hidden_dim, self.hidden_dim),
                    ]
                self.image_encoder_after_attention = nn.Sequential(*image_layers)

    def build_multimodal(self):
        self.multimodal = self.opt.get('multimodal')
        if self.multimodal:
            self.multimodal_combo = self.opt.get('multimodal_combo', 'sum')
            nlayers_mm = (
                self.opt['num_layers_all']
                if self.opt['num_layers_all'] != -1
                else self.opt['num_layers_multimodal_encoder']
            )
            self.multimodal_encoder = MultimodalCombiner(
                n_heads=self.opt['n_heads'],
                n_layers=nlayers_mm,
                hidden_dim=self.opt['hidden_dim'],
                ffn_size=self.opt['embedding_size'] * 4,
                attention_dropout=self.opt['attention_dropout'],
                relu_dropout=self.opt['relu_dropout'],
                learn_positional_embeddings=self.opt.get(
                    'learn_positional_embeddings', False
                ),
                reduction=True,
            )

    def build_encoders(self, dictionary, old=False, build_context_encoder=True):
        encoder = None
        if self.opt.get('load_reddit', None):
            encoder = self.load_from_reddit(dictionary, build_context_encoder)
        else:
            embeddings = nn.Embedding(len(dictionary), self.opt['embedding_size'])
            encoder = TransformerModel(
                self.opt['transformer_nb_heads'],
                self.opt['num_layers_text_encoder'],
                self.opt['word_embeddings_dim'],
                dictionary,
                embeddings,
                dropout=self.opt['dropout'],
            )

        additional_layer = LinearWrapper(
            self.opt.get('embedding_size'),
            self.opt['hidden_dim'],
            dropout=self.opt['dropout'],
        )
        return encoder, additional_layer

    def load_from_reddit(self, dictionary, build_context_encoder=True):
        # context_encoder or cand_encoder
        source = self.opt['load_reddit']
        path = {
            'bi': '/checkpoint/daju/bi_model_huge_reddit',
            'poly': '/checkpoint/daju/poly_model_huge_reddit',
        }
        context_encoder_names = {'bi': 'context_encoder', 'poly': 'encoder_ctxt'}
        cand_encoder_names = {'bi': 'cand_encoder', 'poly': 'encoder_cand'}
        name = context_encoder_names if build_context_encoder else cand_encoder_names

        tm = None
        if source == 'old':
            reddit = torch.load('/checkpoint/parlai/zoo/comment_battle/redditbest.mdl')
            tm = TransformerModel(
                reddit['transformer_n_heads'],
                reddit['transformer_n_layers'],
                reddit['transformer_dim'],
                reddit['vocabulary_size'],
            )
            tm.load_state_dict(reddit['transformer_state'])
        else:
            with open('{}/model.opt'.format(path[source])) as json_file:
                reddit = json.load(json_file)
                embeddings = nn.Embedding(len(dictionary), reddit['embedding_size'])
                assert reddit['embedding_size'] == self.opt.get(
                    'embedding_size', reddit['embedding_size']
                )
                print(reddit['embedding_size'])
                kwargs = {
                    'n_heads': reddit['n_heads'],
                    'n_layers': reddit['n_layers'],
                    'embedding_size': reddit['embedding_size'],
                    'ffn_size': reddit['ffn_size'],
                    'vocabulary_size': len(dictionary),
                    'embedding': embeddings,
                    # deopout get from opt
                    'dropout': self.opt['dropout'],
                    'attention_dropout': self.opt['attention_dropout'],
                    'relu_dropout': self.opt['relu_dropout'],
                    'padding_idx': self.padding_idx,
                    'learn_positional_embeddings': reddit[
                        'learn_positional_embeddings'
                    ],
                    'embeddings_scale': reddit['embeddings_scale'],
                    'reduction_type': reddit['reduction_type'],
                    'n_positions': reddit['n_positions'],
                    'n_segments': reddit['n_segments'],
                    'activation': reddit['activation'],
                    'variant': reddit['variant'],
                    'output_scaling': reddit['output_scaling'],
                }
                tm = TransformerEncoder(**kwargs)
                state_dict = torch.load('{}/model'.format(path[source]))['model']
                transformed = {}
                for k, v in list(state_dict.items()):
                    if not k.startswith(name[source]):
                        continue
                    k = k.replace('{}.'.format(name[source]), '')
                    transformed[k] = v.float()
                tm.load_state_dict(transformed)
        return tm

    def forward(self, batch, cands, cands_type='batch', cand_encs=None, train=False):
        """
            :param batch: a Batch object (defined in torch_agent.py)
            :param cands: candidates for this batch
            :param cands_type: source of candidates for this batch, one of
                ['batch', 'inline', 'fixed']
            :param train: True if model is training
            :return: model scores for each item in the batch
        """
        # candidates encoding
        # import ipdb; ipdb.set_trace()
        if cand_encs is not None:
            warn_once("cand_encs is given, use cand_encs instead of using vectors.")
            candidates_encoded = cand_encs
        else:
            candidates_encoded = self.forward_candidates(cands)

        if (
            self.attention
            and candidates_encoded is not None
            and candidates_encoded.dim() == 2
        ):
            candidates_encoded = (
                candidates_encoded.unsqueeze(0)
                .expand(len(batch.valid_indices), -1, -1)
                .contiguous()
            )

        # dialog history
        d_hist_encoded = self.forward_context(
            batch.text_vec, batchsize=len(batch.valid_indices)
        )

        # images
        img_encoded = self.forward_image(batch.image)

        if self.attention:
            img_encoded = self.forward_attention(img_encoded, candidates_encoded)

        if hasattr(self, 'image_encoder_after_attention'):
            img_encoded = self.image_encoder_after_attention(img_encoded)

        # personalities
        pers_encoded = self.forward_personality(
            batch.personalities, len(batch.valid_indices)
        )

        # expand size of everything for the attention:
        if self.attention and d_hist_encoded is not None:
            d_hist_encoded = (
                d_hist_encoded.unsqueeze(1).expand_as(img_encoded).contiguous()
            )

        if self.attention and pers_encoded is not None:
            pers_encoded = pers_encoded.unsqueeze(1).expand_as(img_encoded).contiguous()

        # combined
        total_encoded = self.get_rep(
            [img_encoded, d_hist_encoded, pers_encoded],
            batchsize=len(batch.valid_indices),
        )
        import ipdb; ipdb.set_trace()
        return self.get_scores(total_encoded, candidates_encoded)

    def forward_personality(self, personalities, bsz):
        """
            :param personalities: [bsz] list of personalities (or None)
            :param bsz: batchsize
            :return: a [bsz, hidden_dim] FloatTensor of encoded personalities
        """
        if not self.encode_personality:
            if self.multimodal and self.multimodal_combo == 'concat':
                return self.blank_encoding
            else:
                return None

        if personalities is None:
            personalities = [''] * bsz
        pers_vec = torch.FloatTensor(len(personalities), self.personality_dim).fill_(0)
        pers_list = [self.personality_to_id.get(p, 0) + 1 for p in personalities]
        for i, index in enumerate(pers_list):
            pers_vec[i, index] = 1  # no personality corresponds to 0
        if self.use_cuda:
            pers_vec = pers_vec.cuda()
        if self.fp16:
            pers_vec = pers_vec.half()
        return self.persona_encoder(pers_vec)

    def forward_context(self, context, batchsize=None):
        """
            :param context: a [bsz, seq_len] LongTensor of token indices
            :param batchsize: batch size
            :return: a [bsz, hidden_dim] FloatTensor of encoded context
        """
        if context is None or not self.encode_dialog_history:
            if self.multimodal and self.multimodal_combo == 'concat':
                return torch.stack([self.blank_encoding for _ in range(batchsize)])
            else:
                return None
        if self.use_cuda:
            context = context.cuda()
        encoded = self.context_encoder(context)
        if self.text_encoder_frozen:
            encoded = encoded.detach()
        encoded = self.additional_layer(encoded)
        return encoded

    def forward_candidates(self, cands, batchsize=None):
        """
            :param cands:
        """
        if cands is None:
            return None
        if self.use_cuda:
            cands = cands.cuda()
        batchsize = cands.size(0)
        is_eval = False

        if cands.dim() == 3:
            length = cands.size(2)
            cands = cands.reshape((-1, length))
            is_eval = True
        # import ipdb; ipdb.set_trace()
        if self.opt['load_reddit'] == 'old':
            mask = cands != self.padding_idx
            encoded = self.label_encoder(cands, mask)
        else:
            encoded = self.label_encoder(cands)
        encoded = self.additional_layer(encoded)
        #  in eval
        if is_eval:
            encoded = encoded.detach()
            # We want the batch norm to be applied on the same dimension, eg the last one
            # encoded = torch.stack(encoded)
            encoded = encoded.reshape((batchsize, -1, self.hidden_dim))
        if self.text_encoder_frozen:
            encoded = encoded.detach()
            # this will be btz * num_candidates * embeding_size
        return encoded

    def forward_attention(self, imgs, labels_encoded, position=None):
        if position is None:
            position = torch.arange(50)
        if self.use_cuda:
            position = position.cuda()

        imgs = imgs + self.image_position_embedding(position).expand_as(imgs)
        imgs = self.attend(self.attention, labels_encoded, imgs)
        return imgs

    def forward_image(self, image_features):
        """
            :param image_features: a [bsz] list of [image_features_dim] FloatTensors
            :return: a [bsz, hidden_dim] FloatTensor of encoded images
        """
        if image_features is None or not self.encode_image:
            if self.multimodal and self.multimodal_combo == 'concat':
                return self.blank_encoding
            return None
        if self.use_cuda:
            image_features = image_features.cuda()
        if self.fp16:
            image_features = image_features.half()
        return self.image_encoder(image_features)

    def get_rep(self, encodings, batchsize=None):
        """
            :param encodings: a 3-element list, where each element is either
                a tensor of dimension [bsz, hidden_dim]
                OR None
            :param batchsize: size of batch
            :return: a [bsz, hidden_dim] FloatTensor of encodings
        """
        if not self.multimodal:
            rep = self.sum(encodings)
        else:
            if self.multimodal_combo == 'sum':
                encodings = self.sum(encodings).unsqueeze(1)
            elif self.multimodal_combo == 'concat':
                encodings = self.cat(encodings)
            all_one_mask = torch.ones(encodings.size()[:2])
            if self.use_cuda:
                all_one_mask = all_one_mask.cuda()
            if self.fp16:
                all_one_mask = all_one_mask.half()
            rep = self.multimodal_encoder(encodings, all_one_mask)
        if rep is None:
            rep = torch.stack([self.blank_encoding for _ in range(batchsize)])
        return rep

    def get_scores(self, query_vecs, can_encodings):
        """
            :param query_vecs: a [bsz, hidden_dim] FloatTensor of example encodings
            :param cand_vecs: *dependent on cands_type*
                if 'batch', a [bsz, seq_len] LongTensor of token indices
                if 'inline', a [bsz, num_cands_per_example, seq_len]
                    LongTensor of token indices
            :param cands_type: source of candidates for this batch, one of
                ['batch', 'inline', 'fixed']
            :param train: whether this is a train batch
            :return: a [bsz, num_cands_per_example] FloatTensor of scores
        """

        if self.attention is None:
            if query_vecs.dim() != can_encodings.dim():
                # it means in eval mode
                return torch.sum(
                    query_vecs.unsqueeze(1).expand_as(can_encodings) * can_encodings, 2
                )
            else:
                return query_vecs.mm(can_encodings.t())
        else:
            if len(can_encodings.size()) == 3:
                return torch.sum(query_vecs * can_encodings, 2)
            if len(can_encodings.size()) == 2:
                return torch.sum(query_vecs * can_encodings, 1)

    def freeze_text_encoder(self):
        self.text_encoder_frozen = True

    def unfreeze_text_encoder(self):
        self.text_encoder_frozen = False

    ##################################################
    #     tensor combination functions
    ##################################################
    def sum(self, addends):
        addends = [a for a in addends if a is not None]
        return sum(addends) if len(addends) > 0 else None

    def cat(self, tensors):
        tensors = [t for t in tensors if t is not None]
        return torch.cat([t.unsqueeze(1) for t in tensors], dim=1)


#########################################
#    Linear Wrapper
#########################################


class LinearWrapper(nn.Module):
    """
        Adds one linear layer on top of a module.
    """

    def __init__(self, in_dim, out_dim, dropout):
        super(LinearWrapper, self).__init__()
        self.lin = nn.Linear(in_dim, out_dim)
        self.dp = nn.Dropout(dropout)

    def forward(self, input):
        return self.lin(self.dp(input))


########################################
# Multimodal Combiner                  #
########################################


class MultimodalCombiner(nn.Module):
    """
        Essentially a transformer, with no embeddings. See TransformerEncoder
        in parlai.agents.transformer.modules.
    """

    def __init__(
        self,
        n_heads,
        n_layers,
        hidden_dim,
        ffn_size,
        reduction=True,
        attention_dropout=0.0,
        relu_dropout=0.0,
        learn_positional_embeddings=False,
    ):
        super().__init__()
        self.ffn_size = ffn_size
        self.n_layers = n_layers
        self.n_heads = n_heads
        self.out_dim = hidden_dim
        self.dim = hidden_dim
        self.reduction = reduction
        assert hidden_dim % n_heads == 0, 'MM-Combiner dim must be multiple of n_heads'
        n_positions = 1024
        self.position_embeddings = nn.Embedding(n_positions, hidden_dim)
        if not learn_positional_embeddings:
            create_position_codes(
                n_positions, hidden_dim, out=self.position_embeddings.weight
            )
        else:
            nn.init.normal_(self.position_embeddings.weight, 0, hidden_dim ** -0.5)

        self.layers = nn.ModuleList()
        for _ in range(self.n_layers):
            self.layers.append(
                TransformerEncoderLayer(
                    n_heads, hidden_dim, ffn_size, attention_dropout, relu_dropout
                )
            )

    def forward(self, tensor, mask):
        """
            :param tensor: a [bsz, seq_len, hidden_dim] FloatTensor
            :param mask: a [bsz, seq_len] ByteTensor filled with 1 when
                inside the sequence and 0 outside.
            :return: output: a [bsz, hidden_dim] FloatTensor of encodings
                     mask: the same as before
        """
        seq_len = tensor.size(1)
        positions = tensor.new(seq_len).long()
        positions = torch.arange(seq_len, out=positions).unsqueeze(0)
        tensor = tensor + self.position_embeddings(positions).expand_as(tensor)

        tensor *= mask.unsqueeze(-1)
        for i in range(self.n_layers):
            tensor = self.layers[i](tensor, mask)

        if self.reduction:
            divisor = mask.sum(dim=1).unsqueeze(-1).clamp(min=1e-20)
            output = tensor.sum(dim=1) / divisor
            return output
        else:
            output = tensor
            return output, mask


#########################################
# Multi-head Attention
#########################################


class ImageMultiHeadAttention(nn.Module):
    def __init__(self, n_heads, hidden_dim, query_dim, key_dim, dropout=0):
        super(ImageMultiHeadAttention, self).__init__()
        self.n_heads = n_heads
        self.hidden_dim = hidden_dim

        self.attn_dropout = nn.Dropout(p=dropout)  # --attention-dropout
        self.q_lin = nn.Linear(query_dim, hidden_dim)
        self.k_lin = nn.Linear(key_dim, hidden_dim)
        self.v_lin = nn.Linear(key_dim, hidden_dim)
        # TODO: merge for the initialization step
        nn.init.xavier_normal_(self.q_lin.weight)
        nn.init.xavier_normal_(self.k_lin.weight)
        nn.init.xavier_normal_(self.v_lin.weight)
        # and set biases to 0
        self.out_lin = nn.Linear(self.hidden_dim, self.hidden_dim)

        nn.init.xavier_normal_(self.out_lin.weight)

    def forward(self, query, key=None, value=None):
        """Forward pass."""
        # TODO: there are a lot of parameters to document here.

        # Input is [B, query_len, dim]
        batch_size, query_len, query_dim = query.size()
        n_heads = self.n_heads
        dim_per_head = self.hidden_dim // n_heads
        scale = math.sqrt(dim_per_head)

        def prepare_head(tensor):
            # input is [batch_size, seq_len, n_heads * dim_per_head]
            # output is [batch_size * n_heads, seq_len, dim_per_head]
            bsz, seq_len, _ = tensor.size()
            tensor = tensor.view(batch_size, tensor.size(1), n_heads, dim_per_head)
            tensor = (
                tensor.transpose(1, 2)
                .contiguous()
                .view(batch_size * n_heads, seq_len, dim_per_head)
            )
            return tensor

        # q, k, v are the transformed values
        if key is None and value is None:
            # self attention
            key = value = query
        elif value is None:
            # key and value are the same, but query differs
            # self attention
            value = key
        _, key_len, dim = key.size()

        q = prepare_head(self.q_lin(query))
        k = prepare_head(self.k_lin(key))
        v = prepare_head(self.v_lin(value))

        dot_prod = q.div_(scale).bmm(k.transpose(1, 2))
        # [B * n_heads, query_len, key_len]

        attn_weights = F.softmax(dot_prod, dim=-1).type_as(query)
        attn_weights = self.attn_dropout(attn_weights)  # --attention-dropout

        attentioned = attn_weights.bmm(v)
        attentioned = (
            attentioned.type_as(query)
            .view(batch_size, n_heads, query_len, dim_per_head)
            .transpose(1, 2)
            .contiguous()
            .view(batch_size, query_len, query_dim)
        )

        out = self.out_lin(attentioned)

        return out

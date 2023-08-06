#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Global Local Attention Net Modules."""
from parlai.agents.transformer.modules import \
    (TransformerEncoder, TransformerGeneratorModel, TransformerFFN, BasicAttention,
    _normalize, _build_decoder as _build_transformer_decoder, _create_embeddings)
from parlai.core.torch_generator_agent import TorchGeneratorModel
from parlai.utils.misc import warn_once
import torch
import torch.nn.functional as F
import torch.nn as nn
import numpy as np
import random


class GlobalLocalAttentionNet(TorchGeneratorModel):
    """Global Local Attention Network.

    Very similar to TransformerGeneratorModel, however has a *slightly* different
    encoder

    Depending on certain opts, could have vastly different decoder.
    """
    def __init__(self, opt, dictionary):
        self.pad_idx = dictionary[dictionary.null_token]
        self.start_idx = dictionary[dictionary.start_token]
        self.end_idx = dictionary[dictionary.end_token]
        super().__init__(self.pad_idx, self.start_idx, self.end_idx)
        self.embeddings = _create_embeddings(
            dictionary, opt['embedding_size'], self.pad_idx
        )

        if opt.get('n_positions'):
            # if the number of positions is explicitly provided, use that
            n_positions = opt['n_positions']
        else:
            # else, use the worst case from truncate
            n_positions = max(
                opt.get('truncate') or 0,
                opt.get('text_truncate') or 0,
                opt.get('label_truncate') or 0,
            )
            if n_positions == 0:
                # default to 1024
                n_positions = 1024
        n_segments = opt.get('n_segments', 0)

        if n_positions < 0:
            raise ValueError('n_positions must be positive')

        self._build_encoder(
            opt,
            dictionary,
            self.embeddings,
            self.pad_idx,
            reduction_type=None,
            n_positions=n_positions,
            n_segments=n_segments,
        )
        self._build_decoder(
            opt, dictionary, self.embeddings, self.pad_idx, n_positions=n_positions
        )

    def reorder_encoder_states(self, encoder_states, indices):
        """
        Reorder the encoder states.

        See ``TorchGeneratorModel.reorder_encoder_states`` for a description.

        Identical to TransformerGeneratorModel
        """
        enc, mask = encoder_states
        if not torch.is_tensor(indices):
            indices = torch.LongTensor(indices).to(enc.device)
        enc = torch.index_select(enc, 0, indices)
        mask = torch.index_select(mask, 0, indices)
        return enc, mask

    def reorder_decoder_incremental_state(self, incremental_state, inds):
        """
        Reorder the decoder incremental state.

        Not implemented in Transformers, since ``incremental_state`` is always None.
        """
        # no support for incremental decoding at this time
        return None

    def output(self, tensor):
        """Compute output logits."""
        # project back to vocabulary
        output = F.linear(tensor, self.embeddings.weight)
        return output

    def _build_encoder(
        self,
        opt,
        dictionary,
        embedding,
        padding_idx,
        reduction_type=None,
        n_positions=1024,
        n_segments=0
    ):
        self.encoder = GlobalLocalAttentionNetEncoder(
            n_heads=opt['n_heads'],
            n_layers=opt['n_layers'],
            embedding_size=opt['embedding_size'],
            ffn_size=opt['ffn_size'],
            vocabulary_size=len(dictionary),
            embedding=embedding,
            dropout=opt['dropout'],
            attention_dropout=opt['attention_dropout'],
            relu_dropout=opt['relu_dropout'],
            padding_idx=padding_idx,
            learn_positional_embeddings=opt['learn_positional_embeddings'],
            embeddings_scale=opt['embeddings_scale'],
            reduction_type=reduction_type,
            n_positions=n_positions,
            n_segments=n_segments,
            activation=opt['activation'],
            variant=opt['variant'],
            output_scaling=opt['output_scaling'],
            glan_dropout_strategy=opt.get('glan_dropout_strategy', None),
            glan_choose_global_ratio=opt.get('glan_choose_global_ratio', 0.5),
            glan_choose_local_ratio=opt.get('glan_choose_local_ratio', 0.5),
            global_token_indices=[
                dictionary['__global_tok_{}__'.format(i)] for i in range(opt.get('num_global_tokens'))
            ],
            use_mask_only=opt.get('use_mask_only', True),
            glan_internal_dropout_strategy=opt.get('glan_internal_dropout_strategy', None),
            glan_internal_global_ratio=opt.get('glan_internal_global_ratio', 0.5),
            glan_internal_local_ratio=opt.get('glan_internal_local_ratio', 0.5),
            glan_eval_strategy=opt.get('glan_eval_strategy', 'all')
        )

    def _build_decoder(
        self,
        opt,
        dictionary,
        embedding=None,
        padding_idx=None,
        n_positions=1024,
        n_segments=0
    ):
        if opt.get('decoder_type') == 'transformer':
            self.decoder = _build_transformer_decoder(
                opt, dictionary, embedding, padding_idx, n_positions, n_segments
            )
        elif opt.get('decoder_type') == 'simple':
            self.decoder = BrainDamagedDecoder(
                embedding,
                opt['embedding_size'],
                opt['ffn_size']
            )
        elif opt.get('decoder_type') == 'pass_through':
            self.decoder = PassThroughDecoder(embedding)


class GlobalLocalAttentionNetEncoder(TransformerEncoder):
    """GLAN Encoder.

    For now, adds global tokens manually to the input.
    """

    def __init__(self, *args, **kwargs):
        self.glan_choose_local_ratio = kwargs.pop('glan_choose_local_ratio')
        self.glan_choose_global_ratio = kwargs.pop('glan_choose_global_ratio')
        self.glan_dropout_strategy = kwargs.pop('glan_dropout_strategy')
        self.global_token_indices = kwargs.pop('global_token_indices')
        self.num_global_tokens = len(self.global_token_indices)

        # how to select dropout; mask only is apparently more computationally expensive
        self.use_mask_only = kwargs.pop('use_mask_only')

        self.glan_internal_dropout_strategy = kwargs.pop('glan_internal_dropout_strategy')
        self.glan_internal_local_ratio = kwargs.pop('glan_internal_local_ratio')
        self.glan_internal_global_ratio = kwargs.pop('glan_internal_global_ratio')
        self.glan_eval_strategy = kwargs.pop('glan_eval_strategy')
        if self.num_global_tokens <= 0:
            assert self.glan_dropout_strategy in ['none', None] and self.glan_internal_dropout_strategy in ['none', None]
        super().__init__(*args, **kwargs)
        random.seed(42)

    def forward(self, input, positions=None, segments=None):
        """
        Forward pass.

        Override to implement GLAN dropout

        :param LongTensor[batch,seqlen] input:
            The input IDs
        :param BoolTensor[batch,seqlen] mask:
            The attention mask; 1 means attend, 0 means ignore.
        :param LongTensor[batch,seqlen]:
            If provided, additionally adds ``segments`` as extra embedding features.

        """
        # 1. Setup the masks
        mask = input != self.padding_idx
        local_tok_mask = input != self.padding_idx
        local_tok_select = local_tok_mask | (input == self.padding_idx)
        if self.num_global_tokens > 0:
            global_tok_mask = (input == self.global_token_indices[0])
            for idx in self.global_token_indices:
                local_tok_mask &= input != idx
                global_tok_mask |= input == idx
            global_tok_select = global_tok_mask
        else:
            global_tok_mask = torch.zeros(1)
            global_tok_select = global_tok_mask

        # 2a. Boilerplate - setup segment/position embeddings
        if positions is None:
            positions = (mask.cumsum(dim=1, dtype=torch.int64) - 1).clamp_(min=0)
        tensor = self.embeddings(input)
        if self.embeddings_scale:
            tensor = tensor * np.sqrt(self.dim)

        if positions.max().item() > self.n_positions:
            warn_once(
                'You are inputting a sequence of {x} length, but only have '
                '--n-positions {y}. Set --truncate or increase --n-positions'.format(
                    x=positions.max().item(), y=self.n_positions
                )
            )
        tensor = tensor + self.position_embeddings(positions).expand_as(tensor)

        if self.n_segments >= 1:
            if segments is None:
                segments = torch.zeros_like(input)
            tensor = tensor + self.segment_embeddings(segments)

        if self.variant == 'xlm':
            tensor = _normalize(tensor, self.norm_embeddings)

        # --dropout on the embeddings
        tensor = self.dropout(tensor)

        tensor *= mask.unsqueeze(-1).type_as(tensor)

        # 2b. internal glan dropout
        use_all_internal_toks = (
            not global_tok_mask.sum() or
            not self.training or
            self.glan_internal_dropout_strategy in [None, 'none']
        )
        for i in range(self.n_layers):
            if use_all_internal_toks:
                tensor = self.layers[i](tensor, mask)
            elif self.glan_internal_dropout_strategy == 'alternate':
                rand = random.random()
                choose_global = rand < self.glan_internal_global_ratio
                choose_local = rand < self.glan_internal_global_ratio + self.glan_internal_local_ratio

                if choose_global:
                    tensor = self.layers[i](tensor, global_tok_mask)
                elif choose_local:
                    tensor = self.layers[i](tensor, local_tok_mask)
                else:
                    tensor = self.layers[i](tensor, mask)

        tensor *= self.output_scaling
        output = tensor

        # 3. Output Dropout
        if not global_tok_mask.sum():
            # dummy batch or no tokens...
            return output, mask
        bsz, num_toks, hsz = output.shape

        if self.use_mask_only:
            if not self.training:
                if self.glan_eval_strategy in [None, 'all']:
                    mask = mask
                elif self.glan_eval_strategy == 'all_global':
                    mask = global_tok_mask
                elif self.glan_eval_strategy == 'all_local':
                    mask = local_tok_mask
            elif self.glan_dropout_strategy in [None, 'none']:
                mask = mask
            elif self.glan_dropout_strategy == 'all_global_toks':
                # only return the tokens that ARE global tokens
                mask = global_tok_mask
            elif self.glan_dropout_strategy == 'all_reg_toks':
                # only return the tokens that are NOT global tokens
                mask = local_tok_mask
            elif self.glan_dropout_strategy == 'alternate':
                # return *only* global toks with certain percentage of the time
                rand = random.random()
                choose_global = rand < self.glan_choose_global_ratio
                choose_local = rand < self.glan_choose_global_ratio + self.glan_choose_local_ratio

                if choose_global:
                    mask = global_tok_mask
                elif choose_local:
                    mask = local_tok_mask
                else:
                    mask = mask
        else:
            def select_local(output, mask):
                output = output.masked_select(
                    local_tok_select.unsqueeze(2).repeat(1, 1, hsz)
                ).view([bsz, num_toks - self.num_global_tokens, hsz])
                mask = local_tok_mask.masked_select(local_tok_select).view(bsz, -1)
                return output, mask

            def select_global(output, mask):
                output = output.masked_select(
                    global_tok_select.unsqueeze(2).repeat(1, 1, hsz)
                ).view([bsz, self.num_global_tokens, hsz])
                mask = torch.ones(mask.shape[0], self.num_global_tokens, out=mask)
                return output, mask

            if not self.training:
                if self.glan_eval_strategy in [None, 'all']:
                    pass
                elif self.glan_eval_strategy == 'all_global':
                    output, mask = select_global(output, mask)
                elif self.glan_eval_strategy == 'all_local':
                    output, mask = select_local(output, mask)
            elif self.glan_dropout_strategy == 'all_reg_toks':
                # only return the tokens that are NOT global tokens
                output, mask = select_local(output, mask)
            elif self.glan_dropout_strategy == 'all_global_toks':
                # only return the tokens that ARE global tokens
                output, mask = select_global(output, mask)
            elif self.glan_dropout_strategy == 'alternate':
                # return *only* global toks with certain percentage of the time
                rand = random.random()
                choose_global = rand < self.glan_choose_global_ratio
                choose_local = rand < self.glan_choose_global_ratio + self.glan_choose_local_ratio

                if choose_global:
                    output, mask = select_global(output, mask)
                elif choose_local:
                    output, mask = select_local(output, mask)

        return output, mask

class BrainDamagedDecoder(nn.Module):
    """
    Simple decoder for GLAN.

    For now, it has only one FFN
    """
    def __init__(self, embedding, embedding_size, ffn_size):
        super().__init__()
        self.embeddings = embedding
        self.attention = BasicAttention(dim=2, attn='basic', get_weights=False)
        self.ffn = TransformerFFN(embedding_size, ffn_size)

    def forward(self, input, encoder_state, incr_state=None):
        encoder_output, encoder_mask = encoder_state
        tensor = self.embeddings(input)
        attended = self.attention(tensor, encoder_output, mask_ys=encoder_mask)
        return self.ffn(attended), None


class PassThroughDecoder(nn.Module):
    """
    Simplest decoder for GLAN.

    Basically just apply mask. No FFN
    """
    def __init__(self, embedding):
        super().__init__()
        self.embeddings = embedding
        self.attention = BasicAttention(dim=2, attn='basic', get_weights=False)

    def forward(self, input, encoder_state, incr_state=None):
        encoder_output, encoder_mask = encoder_state
        tensor = self.embeddings(input)
        attended = self.attention(tensor, encoder_output, mask_ys=encoder_mask)
        return attended, None

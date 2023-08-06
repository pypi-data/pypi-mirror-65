#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Modules for ParlALL Agent."""
import torch
import torch.nn as nn
from parlai.agents.transformer.modules import TransformerGeneratorModel, TransformerEncoder


class ParlALLModel(TransformerGeneratorModel):
    """ParlALLModel.

    Just TGA that can encode image with encoder.
    """

    def __init__(self, opt, dictionary):
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

        super().__init__(opt, dictionary)
        self.encoder = ContextWithImageEncoder(
            n_heads=opt['n_heads'],
            n_layers=opt['n_layers'],
            embedding_size=opt['embedding_size'],
            ffn_size=opt['ffn_size'],
            vocabulary_size=len(dictionary),
            embedding=self.embeddings,
            dropout=opt['dropout'],
            attention_dropout=opt['attention_dropout'],
            relu_dropout=opt['relu_dropout'],
            padding_idx=self.pad_idx,
            learn_positional_embeddings=opt['learn_positional_embeddings'],
            embeddings_scale=opt['embeddings_scale'],
            reduction_type=None,
            n_positions=n_positions,
            n_segments=opt.get('n_segments', 0),
            activation=opt['activation'],
            variant=opt['variant'],
            output_scaling=opt['output_scaling'],
            image_encoder_num_layers=opt['image_encoder_num_layers'],
            image_features_dim=opt['image_features_dim'],
            use_cuda=not opt['no_cuda'] and torch.cuda.is_available()
        )


class ContextWithImageEncoder(TransformerEncoder):
    """ContextWithImage Module.

    Encodes image and context via simple concatenation.
    """

    def __init__(self, *args, **kwargs):
        self.n_img_layers = kwargs.pop('image_encoder_num_layers')
        self.img_dim = kwargs.pop('image_features_dim')
        self.use_cuda = kwargs.pop('use_cuda')
        super().__init__(*args, **kwargs)
        self._build_image_encoder()
        self.dummy_image_enc = torch.zeros((self.embedding_size))
        self.ones_mask = torch.ones(1).bool()
        if self.use_cuda:
            self.dummy_image_enc = self.dummy_image_enc.cuda()
            self.ones_mask = self.ones_mask.cuda()

    def _build_image_encoder(self):
        image_layers = [nn.Linear(self.img_dim, self.embedding_size)]
        for _ in range(self.n_img_layers - 1):
            image_layers += [
                nn.ReLU(),
                nn.Dropout(p=self.opt['dropout']),
                nn.Linear(self.img_dim, self.embedding_size),
            ]
        self.image_encoder = nn.Sequential(*image_layers)

    def forward(self, src_tokens, image_features):
        """Encode images with context."""
        context_encoded = context_mask = None
        image_encoded = extra_masks = None
        if src_tokens is not None:
            context_encoded, context_mask = super().forward(src_tokens)
        if image_features is not None and any(feat is not None for feat in image_features):
            # Only encode real image features; concat 0s for non-images
            valid_inds = [i for i, img in enumerate(image_features) if img is not None]
            valid_imgs = torch.stack([img for i, img in enumerate(image_features) if img is not None])
            valid_img_enc = self.image_encoder(valid_imgs)

            extra_masks = []
            image_encoded = []
            img_num = 0
            for i in range(len(image_features)):
                if i in valid_inds:
                    extra_masks.append(self.ones_mask)
                    image_encoded.append(valid_img_enc[img_num, :])
                    img_num += 1
                else:
                    extra_masks.append(~self.ones_mask)
                    image_encoded.append(self.dummy_image_enc)

            extra_masks = torch.stack(extra_masks)
            image_encoded = torch.stack(image_encoded).unsqueeze(1)

        full_enc = self.cat([context_encoded, image_encoded])
        full_mask = self.cat([context_mask, extra_masks])
        return full_enc, full_mask

    def cat(self, tensors):
        """Handle cat on None tensors."""
        tensors = [t for t in tensors if t is not None]
        return torch.cat([t for t in tensors], dim=1)

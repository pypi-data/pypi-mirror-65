#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from parlai.agents.transformer.transformer import (
    TransformerRankerAgent,
    TransformerMemNetModel,
)
from parlai.core.torch_ranker_agent import TorchRankerAgent
from parlai.core.build_data import modelzoo_path
from parlai.core.opt import load_opt_file
from parlai.core.torch_agent import History
from parlai.core.torch_classifier_agent import TorchClassifierAgent
from parlai.utils.misc import warn_once

from collections import deque
import os
import torch
import torch.nn as nn


class TransformerWrapper(nn.Module):
    """
    Add a linear layer on top of the Transformer encoder.
    """

    def __init__(self, model, output_dim):
        super(TransformerWrapper, self).__init__()
        self.base_model = model
        if hasattr(model, 'module'):
            input_dim = model.module.context_encoder.embeddings.weight.size(1)
        else:
            input_dim = model.context_encoder.embeddings.weight.size(1)
        self.additional_linear_layer = nn.Linear(input_dim, output_dim)

    def forward(self, x, mems=None):
        if hasattr(self.base_model, 'module'):
            _, context_h = self.base_model.module.encode_context_memory(x, mems)
        else:
            _, context_h = self.base_model.encode_context_memory(x, mems)
        return self.additional_linear_layer(context_h)


class TransformerClassifierAgent(TorchClassifierAgent):
    """
    Classifier based on Transformer.
    """

    @staticmethod
    def add_cmdline_args(parser):
        TransformerRankerAgent.add_cmdline_args(parser)
        TorchClassifierAgent.add_cmdline_args(parser)
        parser.add_argument(
            '--pretrained-model',
            type=str,
            help='model to initialize the Transformer with',
        )
        parser.set_params(reduction_type='first')

    def get_base_state_dict(self, state_dict):
        new_state_dict = {}
        for k, v in state_dict.items():
            if 'base_model' in k:
                new_k = k.replace('base_model.', '')
                new_k = new_k.replace('module.', '')
                new_state_dict[new_k] = v
        return new_state_dict

    def build_model(self):
        transformer_opt = self.opt.copy()
        if os.path.isfile(self.opt.get('model_file')):
            # loading trained model
            transformer_opt['model_file'] = ''  # don't load model here
            transformer_opt['data_parallel'] = False
            transformer_opt['interactive_mode'] = False
            base_agent = TransformerRankerAgent(transformer_opt)
            states = torch.load(self.opt['model_file'], map_location=lambda cpu, _: cpu)
            state_dict = self.get_base_state_dict(states['model'])
            base_agent.load_state_dict(state_dict)
            base_model = base_agent.model
        else:
            # model not saved yet, load old model
            if self.opt.get('pretrained_model') is not None:
                transformer_opt['init_model'] = modelzoo_path(
                    self.opt['datapath'], self.opt['pretrained_model']
                )
            base_agent = TransformerRankerAgent(transformer_opt)
            base_model = base_agent.model
        num_classes = len(self.class_list)
        return TransformerWrapper(base_model, num_classes)

    def load(self, path):
        """
        Return opt and model states.

        Override this method for more specific loading.
        """
        states = torch.load(path, map_location=lambda cpu, _: cpu)
        if 'model' in states:
            new_state_dict = {
                k.replace('module.', ''): v for k, v in states['model'].items()
            }
            self.load_state_dict(new_state_dict)
        if 'optimizer' in states and hasattr(self, 'optimizer'):
            self.optimizer.load_state_dict(states['optimizer'])
        return states

    def vectorize(self, *args, **kwargs):
        """
        Add the start and end token to the text.
        """
        kwargs['add_start'] = True
        kwargs['add_end'] = True
        obs = TorchRankerAgent.vectorize(self, *args, **kwargs)
        return obs

    def _set_text_vec(self, *args, **kwargs):
        """
        Add the start and end token to the text.
        """
        obs = super()._set_text_vec(*args, **kwargs)

        if 'text_vec' in obs and 'added_start_end' not in obs:
            obs.force_set(
                'text_vec', self._add_start_end_tokens(obs['text_vec'], True, True)
            )
            obs['added_start_end'] = True

        return obs

    def score(self, batch):
        return self.model(batch.text_vec)

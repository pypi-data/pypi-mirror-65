#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Global Local Attention Net Agent."""

from parlai.agents.transformer.transformer import TransformerGeneratorAgent
from parlai.core.torch_ranker_agent import TorchRankerAgent
from parlai.utils.distributed import is_primary_worker
from .modules import GlobalLocalAttentionNet
import torch


class GlanAgent(TransformerGeneratorAgent):
    """Global-Local Attention Net.

    A few variants:
        1. Add "Global" tokens at the end of the sentence
    """

    @classmethod
    def add_cmdline_args(cls, argparser):
        """Add command-line arguments specifically for this agent."""
        TransformerGeneratorAgent.add_cmdline_args(argparser)
        agent = argparser.add_argument_group('GLAN')
        agent.add_argument('--num-global-tokens', type=int, default=5,
                           help='number of global tokens to introduce')
        #-----------------Encoder Arguments--------------------#
        agent.add_argument('--glan-token-strategy', type=str, default='append',
                           choices=['prepend', 'surround', 'append'],
                           help='how to insert global tokens into vector.'
                           'names are self-explanatory')
        agent.add_argument('--glan-dropout-strategy', type=str, default=None,
                           help='what way to dropout the output'
                                '1. all_reg_toks => only use the regular (local) tokens'
                                '2. all_global_toks => only use the global tokens'
                                '3. alternate => alternate between all_reg_toks, all_global_toks'
                                'and all toks. use the glan_choose_local_ratio and glan_choose_global_ratio'
                                '4. none => use all toks',
                           choices=['all_reg_toks', 'all_global_toks', 'alternate', 'none'])
        agent.add_argument('--glan-choose-global-ratio', type=float, default=0.5,
                           help='how often we choose to ONLY USE GLOBAL TOKS')
        agent.add_argument('--glan-choose-local-ratio', type=float, default=0.5,
                           help='how often we choose to ONLY USE LOCAL TOKS')
        agent.add_argument('--use-mask-only', type='bool', default=False,
                           help='if true, push mask through for dropout')
        agent.add_argument('--glan-internal-dropout-strategy', type=str, default=None,
                           choices=['none', 'alternate'],
                           help='what way to dropout the inter-layer inputs'
                                '1. none -> do not dropout inter-layer'
                                '2. alternate -> alternate between no dropout, only use local, only use global'
                           )
        agent.add_argument('--glan-internal-global-ratio', type=float, default=0.5,
                           help='how often we choose to ONLY USE GLOBAL TOKS for inter-layer dropout')
        agent.add_argument('--glan-internal-local-ratio', type=float, default=0.5,
                           help='how often we choose to ONLY USE LOCAL TOKS for inter-layer dropout')
        agent.add_argument('--glan-eval-strategy', type=str, default='all',
                           choices=['all', 'all_global', 'all_local'],
                           help='which tokens to use during eval')
        #-----------------Decoder Arguments--------------------#
        agent.add_argument('--decoder-type', type=str, default='transformer',
                           choices=['transformer', 'simple', 'pass_through'],
                           help='which decoder to use'
                           '''
                            1. Transformer - the standard transformer decoder
                            2. Simple - 1 embedding layer, 1 attention layer (basic),
                                        1 ffn layer
                            3. Pass-through - NO layers (just return encoder output, masked)

                           ''')

    def __init__(self, opt, shared=None):
        self.glan_token_strategy = opt.get('glan_token_strategy', 'append')
        self.num_global_tokens = opt.get('num_global_tokens')
        super().__init__(opt, shared)
        if shared:
            self.global_toks = shared['global_toks']

    def build_dictionary(self):
        """Override to include global tokens."""
        self.dict = super().build_dictionary()
        self.global_toks = []
        for i in range(self.num_global_tokens):
            global_tok = '__global_tok_{}__'.format(i)
            self.dict[global_tok] = 1
            self.global_toks.append(global_tok)
        return self.dict

    def _set_text_vec(self, *args, **kwargs):
        """Override to add global tokens to text."""
        obs = super()._set_text_vec(*args, **kwargs)
        truncate = args[2]
        if 'text_vec' in obs:
            vec = torch.LongTensor(
                self._check_truncate(obs['text_vec'], truncate - self.num_global_tokens, True)
            )
            tensors = [vec]
            for i, tok in enumerate(self.global_toks):
                append = i % 2 == 0
                if (
                        self.glan_token_strategy == 'append' or
                        self.glan_token_strategy == 'surround' and append
                   ):
                    tensors.append(
                        vec.new_tensor([self.dict[tok]])
                    )
                else:
                    tensors.insert(
                        0, vec.new_tensor([self.dict[tok]])
                    )
            obs.force_set('text_vec', torch.cat(tensors, 0))
        return obs

    def build_model(self, states=None):
        """Override to build GLAN."""
        self.model = GlobalLocalAttentionNet(self.opt, self.dict)
        if self.opt['embedding_type'] != 'random':
            self._copy_embeddings(
                self.model.encoder.embeddings.weight, self.opt['embedding_type']
            )
        if self.use_cuda:
            self.model.cuda()
        return self.model

    def load_state_dict(self, state_dict):
        """Override to account for pre-trained models without trained global toks."""
        if not is_primary_worker():
            # we're in distributed mode, copying embeddings in the workers
            # slows things down considerably
            return
        if self.opt['init_model'] is not None:
            # init from pretrained transformer
            # make sure emb dims match up
            embs = state_dict['embeddings.weight']
            enc_embs = state_dict['encoder.embeddings.weight']
            dec_embs = state_dict['decoder.embeddings.weight']
            cnt = 0
            for i in range(embs.shape[0]):
                self.model.embeddings.weight.data[i] = embs[i]
                cnt += 1
            for i in range(enc_embs.shape[0]):
                self.model.encoder.embeddings.weight.data[i] = enc_embs[i]
            for i in range(dec_embs.shape[0]):
                self.model.decoder.embeddings.weight.data[i] = dec_embs[i]
            state_dict['embeddings.weight'] = self.model.embeddings.weight
            state_dict['encoder.embeddings.weight'] = self.model.encoder.embeddings.weight
            state_dict['decoder.embeddings.weight'] = self.model.decoder.embeddings.weight
        cnt = 0

        print(
            'Initialized embeddings for {} tokens ({}%).'
            ''.format(cnt, round(cnt * 100 / len(self.dict), 1))
        )
        self.model.load_state_dict(state_dict)

    def init_optim(self, params, optim_states=None, saved_optim_type=None):
        """Override to not use optim_states if init_model."""
        if self.opt['init_model'] is not None:
            optim_states = None
        super().init_optim(params, optim_states, saved_optim_type)

    def share(self):
        """Override to share global tokens."""
        shared = super().share()
        shared['global_toks'] = self.global_toks
        return shared

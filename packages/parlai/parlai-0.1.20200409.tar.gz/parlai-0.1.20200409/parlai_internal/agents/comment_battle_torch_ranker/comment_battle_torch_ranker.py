#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from parlai.core.utils import round_sigfigs
from parlai.core.torch_ranker_agent import TorchRankerAgent
from parlai.agents.transformer import transformer as Transformer
from .modules import TransResNetMultimodalModel
from parlai.core.utils import warn_once

import os
from collections import namedtuple
import numpy as np
import torch
import json

Batch = namedtuple(
    'Batch',
    [
        'text_vec',
        'text_lengths',
        'label_vec',
        'label_lengths',
        'labels',
        'valid_indices',
        'candidates',
        'candidate_vecs',
        'image',
        'observations',
        'dialog_round',  # additional field for this model
        'personalities',
    ],  # additional field for this model
)


class CommentBattleTorchRankerAgent(TorchRankerAgent):
    """
        Model described in (https://arxiv.org/abs/1811.00945); an extension
        of the one described in (https://arxiv.org/abs/1810.10665)
        A model for conversation in the context of an image. Given an image and
        some dialog history, this model will attempt to predict an appropriate
        next utterance in the dialog, in the context of a given personality.
        See the papers linked above for more information.
    """

    @staticmethod
    def add_cmdline_args(argparser):
        TorchRankerAgent.add_cmdline_args(argparser)
        Transformer.add_common_cmdline_args(argparser)
        argparser.set_defaults(
            candidates='batch',
            eval_candidates='inline',
            embedding_type='none',
            learningrate='0.0005',
            optimizer='adam',
            ffn_size=1200,
            n_heads=4,
            embeddings_scale=False,
            attention_dropout=0.2,
            relu_dropout=0.2,
            gradient_clip=0.01,
            truncate=64,
            dict_tokenizer='bpe',
            dict_lower=True,
            dict_endtoken='__start__',
        )
        arg_group = argparser.add_argument_group('TransResNetAgent Arguments')
        arg_group.add_argument('--freeze-patience', type=int, default=-1)
        arg_group.add_argument(
            '--personality-override',
            type=str,
            default=None,
            help='for use in other tasks where no personality '
            'is given. This will give the model a personality '
            '(whichever is specifed).',
        )
        arg_group.add_argument('--additional-layer-text', type=int, default=0)
        arg_group.add_argument(
            '--personalities-path',
            type=str,
            default=None,
            help='Path to personalities list',
        )
        arg_group.add_argument(
            '--load-context-encoder-from',
            type=str,
            default=None,
            help='If specified, loads context encoder from file',
        )
        arg_group.add_argument(
            '--load-label-encoder-from',
            type=str,
            default=None,
            help='If specified, loads label encoder from file',
        )
        arg_group.add_argument(
            '--load-reddit',
            type=str,
            choices=['bi', 'poly', 'old'],
            default='bi',
            help='load from reddit pretrained',
        )
        model = argparser.add_argument_group('TransResNetModel Arguments')
        model.add_argument('--image-features-dim', type=int, default=2048)
        model.add_argument(
            '--share-encoder',
            type='bool',
            default=False,
            help='Whether to share the text encoder for the '
            'labels and the dialog history',
        )
        model.add_argument('--hidden-dim', type=int, default=300)
        model.add_argument('--num-layers-all', type=int, default=1)
        model.add_argument('--num-layers-text-encoder', type=int, default=1)
        model.add_argument('--num-layers-image-encoder', type=int, default=1)
        model.add_argument('--num-layers-multimodal-encoder', type=int, default=1)
        model.add_argument('--dropout', type=float, default=0.4)
        model.add_argument(
            '--multimodal',
            type='bool',
            default=False,
            help='If true, feed a query term into a separate '
            'transformer prior to computing final rank '
            'scores',
        )
        model.add_argument(
            '--multimodal-combo',
            type=str,
            choices=['concat', 'sum'],
            default='sum',
            help='How to combine the encoding for the ' 'multi-modal transformer',
        )
        model.add_argument(
            '--encode-image',
            type='bool',
            default=True,
            help='Whether to include the image encoding when '
            'retrieving a candidate response',
        )
        model.add_argument(
            '--encode-dialog-history',
            type='bool',
            default=True,
            help='Whether to include the dialog history '
            'encoding when retrieving a candidate response',
        )
        model.add_argument(
            '--encode-personality',
            type='bool',
            default=True,
            help='Whether to include the personality encoding '
            'when retrieving a candidate response',
        )
        model.add_argument(
            '--attention-over-image',
            type=str,
            default='none',
            choices=['multihead', 'basic'],
            help='Whether we use response encoder to attend over images',
        )
        model.add_argument(
            '--attention-over-context',
            type=str,
            default='none',
            choices=['multihead', 'basic'],
            help='Whether we use response encoder to attend over images',
        )
        model.add_argument(
            '--fnn-after-attention',
            type='bool',
            default=False,
            help='Whether we use an extra fnn after attention layer',
        )
        model.add_argument(
            '--fnn-before-attention',
            type='bool',
            default=False,
            help='Whether we use an extra fnn before attention layer',
        )
        model.add_argument(
            '--attention-num-heads',
            type=int,
            default=4,
            help='In case codes-attention-type is multihead, '
            'specify the number of heads',
        )
        model.add_argument(
            '--data-parallel',
            type='bool',
            default=False,
            help='use model in data parallel, requires ' 'multiple gpus',
        )

    def __init__(self, opt, shared=None):
        if not shared:
            self.personalities_list = self.load_personalities(opt)
        else:
            self.personalities_list = shared['personalities_list']
        super().__init__(opt, shared)
        if opt.get('numthreads', 1) > 1:
            raise RuntimeError(
                'Warning: You cannot use multithreading with '
                'this agent, as the current metrics do not '
                'support sharing of lists (for median rank '
                'calculation). Please set --numthreads to 1'
            )
        self.blank_image_features = torch.FloatTensor(
            opt.get('image_features_dim')
        ).fill_(0)
        self.personality_override = opt.get('personality_override')
        if not shared:
            # override metrics to have per-round metrics
            self.metrics['loss'] = 0.0
            self.metrics['examples'] = 0
            self.metrics['rank'] = 0
            self.metrics['train_accuracy'] = 0.0
            self.freeze_patience = opt['freeze_patience']
            if self.freeze_patience != -1:
                # Fine-tuning of a pretrained encoder
                self.model.freeze_text_encoder()
                self.freeze_impatience = 0
                self.freeze_best_metric = 0
                self.is_frozen = True
        else:
            self.metrics = shared['metrics']
        self.id = 'TransResNetAgent'
        self.episode_done = True

    def vectorize(self, *args, **kwargs):
        """ Add the start and end token to the text.
        """
        kwargs['add_start'] = False
        kwargs['add_end'] = False
        obs = TorchRankerAgent.vectorize(self, *args, **kwargs)
        return obs

    def vectorize_fixed_candidates(self, cands_batch, add_start=True, add_end=True):
        """
        Convert a batch of candidates from text to vectors.
        :param cands_batch:
            a [batchsize] list of candidates (strings)
        :returns:
            a [num_cands] list of candidate vectors
        By default, candidates are simply vectorized (tokens replaced by token ids).
        A child class may choose to overwrite this method to perform vectorization as
        well as encoding if so desired.
        """
        return [
            self._vectorize_text(
                cand,
                truncate=self.label_truncate,
                truncate_left=False,
                add_start=False,
                add_end=False,
            )
            for cand in cands_batch
        ]

    def encode_candidates(self, padded_cands):
        """
        Convert the given candidates to vectors.
        This is an abstract method that must be implemented by the user.
        :param padded_cands:
            The padded candidates.
        """
        self.model.eval()
        return self.model.forward_candidates(padded_cands)

    def build_dictionary(self):
        """
            For whatever reasons the dictionary used on reddit was not exactly
            the same style as the one used in ParlAI.
        """
        d = super().build_dictionary()
        load_reddit = self.opt.get('load_reddit', None)
        if load_reddit and load_reddit == 'old':
            new_tok2ind = {}
            new_ind2tok = {}
            for key in d.tok2ind:
                val = d.tok2ind[key]
                if val - 4 >= 0:
                    new_tok2ind[key] = val - 4
                    new_ind2tok[val - 4] = key
            d.null_token = '<PAD>'
            d.unk_token = '<UNK>'
            d.tok2ind = new_tok2ind
            d.ind2tok = new_ind2tok
        return d

    def build_history(self):
        """Return the constructed history object."""
        return self.history_class()(
            self.opt,
            field='',  # don't accumulate by fields. only get by reply
            maxlen=self.text_truncate,
            size=self.histsz,
            p1_token=self.P1_TOKEN,
            p2_token=self.P2_TOKEN,
            dict_agent=self.dict,
        )

    def build_model(self):
        """
            Builds the Transresnet Model.
        """
        model = TransResNetMultimodalModel(
            self.opt, self.personalities_list, self.dict
        )
        if self.opt['load_label_encoder_from']:
            self._load_encoder(
                model.label_encoder, self.opt['load_label_encoder_from']
            )
        elif self.opt['embedding_type'] != 'random':
            self._copy_embeddings(
                model.label_encoder.embeddings.weight,
                self.opt['embedding_type'],
                log=True,
            )
        if not self.opt['share_encoder']:

            if self.opt['load_context_encoder_from']:
                self._load_encoder(
                    model.context_encoder, self.opt['load_context_encoder_from']
                )
            elif self.opt['embedding_type'] != 'random':
                self._copy_embeddings(
                    model.context_encoder.embeddings.weight,
                    self.opt['embedding_type'],
                    log=True,
                )
        return model

    def share(self):
        shared = super().share()
        shared['personalities_list'] = self.personalities_list
        return shared

    def observe(self, observation):
        """
            Override TorchAgent.observe to
                1. separate personality from the rest of the text
                2. format image features for the model
        """
        if 'personality' not in observation:
            if observation.get('text', '') in self.personalities_list:
                observation['personality'] = observation.get('text')
            elif self.personality_override:
                observation['personality'] = self.personality_override
        elif observation.get('text') == observation['personality']:
            observation.force_set('text', None)
        if 'image' in observation:
            im = observation['image']
            try:
                # Check if given img features of form [1, <dim>, 1, 1]
                if len(im.size()) == 4:
                    im = im[0, :, 0, 0]
            except TypeError:  # No Image Feats Given (e.g. `--image-mode raw`)
                im = self.blank_image_features
                warn_once('No Image Feats Given.')
            observation.force_set('image', im)
        return super().observe(observation)

    def batchify(self, obs_batch, sort=False, is_valid=lambda obs: 'image' in obs):
        """
            Overriding TorchAgent.batchify to include personalities and dialog round
        """
        batch = super().batchify(obs_batch, sort)
        valid_obs = batch.observations
        personalities = [o['personality'] for o in valid_obs]
        if 'full_text' not in valid_obs[0]:
            dialog_round = 'round 1'
        else:
            dialog_round = 'round {}'.format(
                len(valid_obs[0]['full_text'].split('\n')) + 1
            )
        return Batch(
            text_vec=batch.text_vec,
            text_lengths=batch.text_lengths,
            label_vec=batch.label_vec,
            label_lengths=batch.label_lengths,
            labels=batch.labels,
            valid_indices=batch.valid_indices,
            candidates=batch.candidates,
            candidate_vecs=batch.candidate_vecs,
            image=torch.stack(batch.image),
            observations=batch.observations,
            personalities=personalities,
            dialog_round=dialog_round,
        )

    def score_candidates(self, batch, cand_vecs, cand_encs=None):
        """Given a batch and candidate set, return scores for ranking"""
        cands_type = (
            self.opt['candidates'] if self.training else self.opt['eval_candidates']
        )
        if cand_encs is not None:
            return self.model(
                batch,
                cand_vecs,
                cands_type=cands_type,
                cand_encs=cand_encs,
                train=self.training,
            )
        else:
            return self.model(
                batch, cand_vecs, cands_type=cands_type, train=self.training
            )

    def train_step(self, batch):
        self.batch = batch
        self.training = True
        return super().train_step(batch)

    def eval_step(self, batch):
        self.batch = batch
        self.training = False
        return super().eval_step(batch)

    def get_batch_train_metrics(self, scores):
        batchsize = scores.size(0)
        # get accuracy
        targets = scores.new_empty(batchsize).long()
        targets = torch.arange(batchsize, out=targets)
        nb_ok = (scores.max(dim=1)[1] == targets).float().sum().item()
        # calculate med rank
        inds = None
        if self.opt.get('train_predict'):
            _, ranks = scores.sort(1, descending=True)
            inds = [
                (ranks[b] == targets[b]).nonzero().item() + 1 for b in range(batchsize)
            ]

        self.update_metrics(nb_ok, batchsize, self.batch.dialog_round, med_rank=inds)

    def get_batch_eval_metrics(self, scores, ranks, label_inds):
        loss = self.rank_loss(scores, label_inds)
        batchsize = scores.size(0)
        nb_ok = sum(
            (ranks[b] == label_inds[b]).nonzero().item() == 0 for b in range(batchsize)
        )
        inds = [
            (ranks[b] == label_inds[b]).nonzero().item() + 1 for b in range(batchsize)
        ]
        self.update_metrics(
            nb_ok,
            batchsize,
            self.batch.dialog_round,
            med_rank=inds,
            total_loss=loss.item(),
        )

    def update_metrics(
        self, nb_ok, num_samples, dialog_round, med_rank=None, total_loss=None
    ):
        """
            Update metrics to account for per-round retrieval statistics
        """
        if dialog_round not in self.metrics:
            self.metrics[dialog_round] = {
                'accuracy': 0.0,
                'loss': 0.0,
                'num_samples': 0,
                'med_rank': [],
            }
        self.metrics[dialog_round]['accuracy'] += nb_ok
        self.metrics[dialog_round]['num_samples'] += num_samples
        if med_rank:
            self.metrics[dialog_round]['med_rank'] += med_rank
        if total_loss:
            self.metrics[dialog_round]['loss'] += total_loss

    def receive_metrics(self, metrics_dict):
        """
            Receives metrics from validation.
            Unfreezes the weights of the pretrained encode after a certain number
            of rounds without improvement.
        """
        super().receive_metrics(metrics_dict)
        if 'tasks' in metrics_dict:
            metrics_dict = metrics_dict['tasks']['image_chat']
        if self.freeze_patience != -1 and self.is_frozen:
            m_key = 'accuracy'
            ms = [
                metrics_dict[k].get(m_key, -1)
                for k in [
                    'round {}'.format(r + 1)
                    for r in range(self.opt['num_dialog_rounds'])
                ]
            ]
            m = sum(ms) / len([m for m in ms if m >= 0])
            if m > self.freeze_best_metric:
                self.freeze_impatience = 0
                self.freeze_best_metric = m
                print('performance not good enough to unfreeze the model.')
            else:
                self.freeze_impatience += 1
                print('Growing impatience for unfreezing')
                if self.freeze_impatience >= self.freeze_patience:
                    self.is_frozen = False
                    print(
                        'Reached impatience for fine tuning. '
                        'Reloading the best model so far.'
                    )
                    self.load(self.model_file)
                    if not self.opt.get('no_cuda'):
                        self.model = self.model.cuda()
                    print('Unfreezing.')
                    self.model.unfreeze_text_encoder()
                    print('Done')

    def reset_metrics(self):
        super().reset_metrics()
        for v in self.metrics.values():
            if type(v) is dict:
                v['accuracy'] = 0.0
                v['loss'] = 0.0
                v['num_samples'] = 0.0
                if 'med_rank' in v:
                    v['med_rank'] = []

    def report(self):
        base = super().report()
        m = {k: {} for k, v in self.metrics.items() if type(v) is dict}
        for k, v in self.metrics.items():
            if type(v) is dict and v['num_samples'] > 0:
                m[k]['accuracy'] = v['accuracy'] / v['num_samples']
                m[k]['loss'] = v['loss'] / v['num_samples']
                if 'med_rank' in v:
                    m[k]['med_rank'] = np.median(v['med_rank'])
                for kk, vv in m[k].items():
                    m[k][kk] = round_sigfigs(vv, 4)
        base.update(m)
        return base

    def save(self, path=None):
        """
            Save the model
        """
        path = self.opt.get('model_file', None) if path is None else path
        print('Saving best model')
        if path:
            states = {}
            states['model'] = self.model.state_dict()
            states['opts'] = self.model.opt
            states['personas_list'] = self.personalities_list
            states['dict'] = self.dict
            torch.save(states, path)
        with open(path + '.opt', 'w') as handle:
            if hasattr(self, 'model_version'):
                self.opt['model_version'] = self.model_version()
            json.dump(self.opt, handle)

    # def load(self, path):
    #     # compatible load function to load old comment battle models
    #     d = torch.load(path, map_location='cpu')
    #     self.model = TransResNetMultimodalModel(
    #         d['opts'], d['personas_list'], d['dict']
    #     )
    #     model_dict = self.model.state_dict()
    #     params = {k: v for k, v in d['state_dict'].items() if k in model_dict}
    #     self.model.load_state_dict(params)

    def load(self, path):
        # import ipdb; ipdb.set_trace()
        states = torch.load(path, map_location='cpu')
        self.model = TransResNetMultimodalModel(
            self.opt, states['personas_list'], states['dict']
        )
        if 'model' in states:
            self.model.load_state_dict(states['model'])
        else:
            self.model.load_state_dict(states['state_dict'])
        return states

    def _load_encoder(self, encoder, path):
        states = torch.load(path, map_location='cpu')
        encoder.load_state_dict(states)

    def load_personalities(self, opt):
        """
            return the list of personalities
        """
        filepath = opt['personalities_path']
        if filepath is None:
            filepath = os.path.join(opt['datapath'], 'image_chat/personalities.txt')
        personalities = []
        with open(filepath) as f:
            for line in f:
                if 'Trait' not in line:
                    personalities.append(line[0:-1])
        return personalities

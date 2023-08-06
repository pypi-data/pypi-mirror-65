#!/usr/bin/env python3


from parlai.core.agents import Agent
from parlai.core.dict import DictionaryAgent
from parlai.utils.misc import round_sigfigs
from .comment_battle_dialog_model import CommentBattleDialogModelURU
from .personalities import PERSONALITIES

import os
import random
import pickle
import numpy as np
import torch
from collections import deque
import json


class CommentBattleDialogAgent(Agent):
    """
    Tries to find the most appropriate comment.

    Uses URU features which are computed offline
    """

    ######################################
    # Initialization and argument parsers
    ######################################
    P1_TOKEN = '__p1__'
    P2_TOKEN = '__p2__'
    TOKENS = [P1_TOKEN, P2_TOKEN]

    @staticmethod
    def add_cmdline_args(argparser):
        arg_group = argparser.add_argument_group('ImageCommenting Arguments')
        CommentBattleDialogModelURU.add_cmdline_args(argparser)
        argparser.add_argument('--freeze-patience', type=int, default=-1)
        argparser.add_argument(
            '--one-cand-set',
            type='bool',
            default=False,
            help='if each example has one set of shared ' 'label candidates',
        )
        argparser.add_argument(
            '--cache-cand-encs',
            type='bool',
            default=False,
            help='if true, cache the candidate encodings to avoid '
            'recomputation every time',
        )
        argparser.add_argument(
            '--use-person-tokens',
            type='bool',
            default=False,
            help='whether to include person tokens' 'in dialog history',
        )
        argparser.add_argument(
            '--personality-override',
            type=str,
            default=None,
            help='for use in other tasks where no personality '
            'is given. This will give the model a personality '
            '(whichever is specifed).',
        )
        argparser.add_argument(
            '--personalities-path',
            type=str,
            default=None,
            help='Path to personalities list',
        )
        argparser.add_argument(
            '--num-exs-before-update',
            type=int,
            default=500,
            help='How many forward passes before a backwards pass',
        )
        argparser.add_argument(
            '--fixed-candidates-path',
            type=str,
            default=None,
            help='path to fixed cands',
        )
        argparser.add_argument(
            '--interactive-mode',
            type='bool',
            default=False,
            help='if in interactive mode, diff logic in batch act',
        )
        argparser.add_argument(
            '--reddit-pretrained',
            type='bool',
            default=False,
            help='whether loading with reddit-pretrained encoder',
        )

        DictionaryAgent.add_cmdline_args(argparser)
        return arg_group

    def __init__(self, opt, shared=None):
        # The K of the metric will most likely differ between train and
        # the valid set
        if opt.get('numthreads', 1) > 1:
            raise RuntimeError(
                'Warning: You cannot use multithreading with '
                'this agent, as the current metrics do not '
                'support sharing of lists (for median rank '
                'calculation). Please set --numthreads to 1'
            )
        self.metrics = {
            k: {'hitsAt1KC100': 0.0, 'loss': 0.0, 'num_samples': 0, 'med_rank': []}
            for k in ['first_round', 'second_round', 'third_round']
        }
        self.blank_image_features = torch.FloatTensor(
            opt.get('image_features_dim')
        ).fill_(0)
        self.opt = opt
        self.use_cuda = torch.cuda.is_available() and not opt.get('no_cuda')
        self.personality_override = opt.get('personality_override')
        self.use_person_tokens = opt.get('use_person_tokens')
        self.one_cand_set = opt.get('one_cand_set', False)
        self.cache_cand_encs = opt.get('cache_cand_encs')
        self.cached_encs = None
        self.interactive_mode = opt.get('interactive_mode', False)
        if not shared:
            # This is the original agent. We create the model.
            self.dict = DictionaryAgent(opt)
            if opt.get('dict_file', '').replace('.dict', '') != opt.get(
                'model_file', ''
            ) or opt.get('reddit_pretrained'):
                self.adapt_dictionary()
            self.dict[self.P1_TOKEN] = 999999999
            self.dict[self.P2_TOKEN] = 999999998

            print('Done dictionary')
            # load the list of personality
            self.personalities_list = PERSONALITIES
            self.model_file = opt['model_file']
            self.id = 'CommentBattleUruAgent'

            # possibly load the model from a model file
            if opt.get('init_model') and os.path.isfile(opt['init_model']):
                init_model_path = opt['init_model']
            elif opt.get('model_file') and os.path.isfile(opt['model_file']):
                init_model_path = opt['model_file']
            else:
                init_model_path = None
            print('Creating or loading model')
            self.freeze_patience = opt['freeze_patience']
            if init_model_path is not None:
                self.model = CommentBattleDialogModelURU.load_model(
                    init_model_path, force_cpu=not self.use_cuda, dictionary=self.dict
                )
                self.model.dict = self.dict
                if self.use_cuda:
                    self.model.cuda()
            else:
                # otherwise creates a new one
                self.model = CommentBattleDialogModelURU(
                    opt, self.personalities_list, self.dict
                )
                if self.use_cuda:
                    self.model.cuda()
            if self.freeze_patience != -1:
                # We use fine tuning. We'll first freeze the encoder,
                # then release it.
                self.model.freeze_text_encoder()
                self.freeze_impatience = 0
                self.freeze_best_metric = 0
                self.is_frozen = True
            self.optimizer = torch.optim.Adam(
                filter(lambda p: p.requires_grad, self.model.parameters()),
                self.opt["adam_alpha"],
            )
            if opt.get('fixed_candidates_path'):
                self._build_fixed_cands()
        else:
            # This is a copy of the agent that has been created
            # for batching or parallelizing purpose.
            self.dict = shared['dict']
            self.model = shared['model']
            self.personalities_list = shared['personalities_list']
            self.optimizer = shared['optimizer']
            if 'cached_encs' in shared:
                self.cached_encs = shared['cached_encs']
                self.cache_cand_encs = True
            if 'fixed_candidates' in shared:
                self.fixed_candidates = shared['fixed_candidates']

        self.episode_done = True
        self.history = deque(maxlen=None)
        self.num_exs_before_update = opt.get('num_exs_before_update')
        self.num_til_update = self.num_exs_before_update
        self.total_loss = 0
        super().__init__(opt, shared)

    def share(self):
        shared = super().share()
        shared['dict'] = self.dict
        shared['model'] = self.model
        shared['personalities_list'] = self.personalities_list
        shared['optimizer'] = self.optimizer
        if hasattr(self, 'cached_encs'):
            shared['cached_encs'] = self.cached_encs
        if hasattr(self, 'fixed_candidates'):
            shared['fixed_candidates'] = self.fixed_candidates
        return shared

    def _build_fixed_cands(self):
        self.cache_cand_encs = True
        cand_path = self.opt['fixed_candidates_path']
        model_dir, model_file = os.path.split(self.opt['model_file'])
        model_name = os.path.splitext(model_file)[0]
        cands_name = os.path.splitext(os.path.basename(cand_path))[0]
        enc_path = os.path.join(model_dir, '.'.join([model_name, cands_name, 'encs']))
        with open(cand_path) as f:
            self.fixed_candidates = [l.replace('\n', '') for l in f.readlines()]
        if os.path.isfile(enc_path):
            self.cached_encs = torch.load(enc_path, map_location=lambda cpu, _: cpu)
        else:
            candidates_encoded = []
            for i in range(0, len(self.fixed_candidates), 512):
                candidates_encoded.append(
                    self.model.forward_text_encoder(
                        self.fixed_candidates[i : i + 512]
                    ).detach()
                )
            self.cached_encs = torch.cat(candidates_encoded, dim=0)
            torch.save(self.cached_encs, enc_path)
        if self.use_cuda:
            self.cached_encs = self.cached_encs.cuda()

    ######################################
    #  Observing and acting
    ######################################

    def observe(self, observation):
        """
        Observe.

        Anything else to be done here?
        """
        self.observation = self.get_dialog_history(observation)
        return self.observation

    def act(self):
        return self.batch_act([self.observation])[0]

    def batch_act(self, observations):
        '''
             {
                'text': <caption<\nresponse>>,
                'personality': <personality>,
                'image': <image features>,
                'label': <comment>,
             }
        '''
        default_res = 'This agent doesn\'t produce actual response for now.'
        result = [
            {'text': default_res, 'id': self.getID()} for _ in range(len(observations))
        ]
        is_training = any(['labels' in obs for obs in observations])
        if self.interactive_mode:
            valid_obs, valid_indexes = observations, [0]
        else:
            valid_obs, valid_indexes = self.filter_obs(observations, is_training)
            if len(valid_obs) == 0:
                return result
        image_feats = self.extract_image_feats(valid_obs)
        personalities, dialog_history, dialog_round = self.extract_texts(valid_obs)
        elected = None
        if is_training:
            total_loss, nb_ok, med_rank = self.train_step(
                valid_obs, image_feats, personalities, dialog_history
            )
            self.num_til_update -= len(valid_obs)

            if self.num_til_update <= 0:
                self.optimizer.step()
                self.optimizer.zero_grad()
                self.num_til_update = self.num_exs_before_update

            total_loss.backward()
            total_loss = total_loss.item()
        else:
            total_loss, nb_ok, med_rank, elected = self.eval_step(
                valid_obs, image_feats, personalities, dialog_history
            )
        self.update_metrics(total_loss, nb_ok, len(valid_obs), dialog_round, med_rank)

        if elected is not None:
            for i, index_obs in enumerate(valid_indexes):
                result[index_obs]['text'] = elected[i][0]
                result[index_obs]['text_candidates'] = elected[i]
        return result

    def train_step(self, valid_obs, image_feats, personalities, dialog_history):
        self.model.train()
        labels = [random.choice(v['labels']) for v in valid_obs]
        candidates = [v.get('label_candidates') for v in valid_obs]
        label_inds = None
        if any(candidates):
            label_inds = [c.index(l) for l, c in zip(labels, candidates)]
            labels = candidates
        total_loss, nb_ok, _ = self.model(
            image_feats,
            personalities,
            dialog_history,
            labels,
            batchsize=len(valid_obs),
            targets=label_inds,
        )
        return total_loss, nb_ok, None

    def eval_step(self, valid_obs, image_feats, personalities, dialog_history):
        self.model.eval()
        labels = [v.get('eval_labels', '') for v in valid_obs]
        # User provides candidates, used as negatives for evaluation
        candidates = [v.get('label_candidates', []) for v in valid_obs]
        candidates_encoded = None
        if hasattr(self, 'fixed_candidates'):
            candidates = [self.fixed_candidates]
            candidates_encoded = self.cached_encs
        elif self.one_cand_set:
            one_cand_set = candidates[0]
            if self.cached_encs is not None:
                candidates_encoded = self.cached_encs
            else:
                candidates_encoded = []
                for i in range(0, len(one_cand_set), 512):
                    candidates_encoded.append(
                        self.model.forward_text_encoder(
                            one_cand_set[i : i + 512]
                        ).detach()
                    )
                candidates_encoded = torch.cat(candidates_encoded, dim=0)
                if self.cache_cand_encs:
                    self.cached_encs = candidates_encoded
        elected = self.model.elect_best_comment(
            image_feats,
            personalities,
            dialog_history,
            candidates,
            candidates_encoded=candidates_encoded,
            k=-1,
            batchsize=len(valid_obs),
        )
        equality_list = [
            1 if elected[i][0] in labels[i] else 0 for i in range(len(labels))
        ]
        # calculate med ranks
        med_rank = []
        for i, e_list in enumerate(elected):
            lowest_rank = len(e_list) + 1
            for _ii, c in enumerate(labels[i]):
                lowest_rank = min(lowest_rank, e_list.index(c) + 1)
            med_rank.append(lowest_rank)
        nb_ok = sum(equality_list)
        total_loss = -1  # no loss in that mode sorry

        return total_loss, nb_ok, med_rank, elected

    def extract_texts(self, obs):
        splits = [v.get('text').split('\n') for v in obs]
        if self.personality_override:
            splits = [s + [self.personality_override] for s in splits]
        personalities = [t[-1] for t in splits]
        dialog_history = None
        dialog_round = 'first_round'
        if len(splits[0]) >= 2:
            dialog_round = 'second_round' if len(splits[0]) == 2 else 'third_round'
            dialog_history = ['\n'.join(t[:-1]) for t in splits]

        return personalities, dialog_history, dialog_round

    def extract_image_feats(self, obs):
        image_feats = [v.get('image') for v in obs]
        for i, im in enumerate(image_feats):
            try:
                # Check if given img features of form [1, <dim>, 1, 1]
                if len(im.size()) == 4:
                    image_feats[i] = im[0, :, 0, 0]
            except (TypeError, AttributeError):  # No Image Feats Given
                image_feats[i] = self.blank_image_features
        return image_feats

    def filter_obs(self, observations, is_training):
        """
        In some special cases (the end of validation for instance) it is possible that
        some of the observations are invalid.
        """
        label_key = 'labels' if is_training else 'eval_labels'
        valid_obs = list()
        valid_indexes = list()
        seen_texts = set()
        seen = 0
        for i in range(len(observations)):
            if 'image' in observations[i]:
                text = observations[i].get(label_key, [''])[0]
                if text not in seen_texts:
                    seen_texts.add(text)
                    valid_obs.append(observations[i])
                    valid_indexes.append(i)
                else:
                    seen += 1
        return valid_obs, valid_indexes

    def get_dialog_history(self, observation):
        obs = observation
        if 'image' not in obs:
            return obs
        if len(self.history) > 0:
            obs.force_set('text', '\n'.join(self.history) + '\n' + obs['text'])
        elif len(obs['text'].split('\n')) != 1:  # we're including history in text
            self.history += obs['text'].split('\n')[:-1]
        if 'labels' in obs:
            self.history.append(random.choice(obs['labels']))
        elif 'eval_labels' in obs:
            self.history.append(random.choice(obs['eval_labels']))
        if self.use_person_tokens:
            for i, hist in enumerate(self.history):
                hist = self.TOKENS[i % len(self.TOKENS)] + ' ' + hist
        if obs.get('episode_done', True):
            # end of this episode, clear the history
            self.history.clear()

        return obs

    def update_metrics(
        self, total_loss, nb_ok, num_samples, dialog_round, med_rank=None
    ):
        self.metrics[dialog_round]['hitsAt1KC100'] += nb_ok
        self.metrics[dialog_round]['loss'] += total_loss
        self.metrics[dialog_round]['num_samples'] += num_samples
        if med_rank:
            self.metrics[dialog_round]['med_rank'] += med_rank

    def adapt_dictionary(self):
        """
        For whatever reasons the dictionary used on reddit was not exactly the same
        style as the one used in ParlAI.
        """
        new_tok2ind = {}
        new_ind2tok = {}
        for key in self.dict.tok2ind:
            val = self.dict.tok2ind[key]
            if val - 4 >= 0:
                new_tok2ind[key] = val - 4
                new_ind2tok[val - 4] = key
        self.dict.null_token = '<PAD>'
        self.dict.unk_token = '<UNK>'
        self.dict.tok2ind = new_tok2ind
        self.dict.ind2tok = new_ind2tok

    #########################################################################
    #   This deals with the fine tuning. For some models, after a certain
    #   time without improvement, we will release the weights
    #   for fine tuning.
    ########################################################################

    def receive_metrics(self, metrics_dict):
        """
        Receives the metrics from valid.

        release the weights of the pretrained encode after a certain number of rounds
        without improvement.
        """
        if 'tasks' in metrics_dict:
            metrics_dict = metrics_dict['tasks']['internal:comment_battle:imageDialog']
        if self.freeze_patience != -1 and self.is_frozen:
            m_key = 'hitsAt1KC100'
            ms = [
                metrics_dict[r].get(m_key, -1)
                for r in ['first_round', 'second_round', 'third_round']
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
                    self.model = CommentBattleDialogModelURU.load_model(self.model_file)
                    if self.use_cuda:
                        self.model = self.model.cuda()
                    print('Unfreezing.')
                    self.model.unfreeze_text_encoder()
                    print('Done')

    #########################################################################
    #   The following methods are there to report the evolution of the     #
    #   model.                                                             #
    ########################################################################

    def reset(self):
        """
        Reset observation and episode_done.

        Mecanism copied from seq2seq
        """
        self.reset_metrics()
        self.history.clear()

    def reset_metrics(self):
        for v in self.metrics.values():
            v['hitsAt1KC100'] = 0.0
            v['loss'] = 0.0
            v['num_samples'] = 0.0
            if 'med_rank' in v:
                v['med_rank'] = []

    def report(self):
        m = {k: {} for k in ['first_round', 'second_round', 'third_round']}
        for k, v in self.metrics.items():
            if v['num_samples'] > 0:
                m[k]['hitsAt1KC100'] = round_sigfigs(
                    v['hitsAt1KC100'] / v['num_samples'], 4
                )
                m[k]['loss'] = round_sigfigs(v['loss'] / v['num_samples'], 4)
                if 'med_rank' in v:
                    m[k]['med_rank'] = np.median(v['med_rank'])
        return m

    ######################################
    #  Serialization
    ######################################

    def save(self, path=None):
        """
        Save the model.

        The model will contain the dic and the archi too, cf CommentBattleDialogModelURU
        """
        path = self.opt.get('model_file', None) if path is None else path
        print('Saving best model')
        CommentBattleDialogModelURU.save_model(self.model, path)
        with open(path + '.opt', 'wb') as handle:
            pickle.dump(self.opt, handle, protocol=pickle.HIGHEST_PROTOCOL)

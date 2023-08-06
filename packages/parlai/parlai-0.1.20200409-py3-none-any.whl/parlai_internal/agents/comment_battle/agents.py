#!/usr/bin/env python3


from parlai.core.agents import Agent
from parlai.core.dict import DictionaryAgent
from parlai.utils.misc import round_sigfigs
from .comment_battle_model import CommentBattleModelURU
from parlai_internal.tasks.comment_battle.build import build

import os
import random
import pickle
import numpy as np
import torch


class CommentBattleUruAgent(Agent):
    '''
        Tries to find the most appropriate comment.
        Uses URU features which are computed offline
    '''

    ######################################
    # Initialization and argument parsers
    ######################################

    @staticmethod
    def add_cmdline_args(argparser):
        arg_group = argparser.add_argument_group('ImageCommenting Arguments')
        CommentBattleModelURU.add_cmdline_args(argparser)
        argparser.add_argument('--freeze-patience', type=int, default=-1)
        argparser.add_argument('--one-cand-set', type='bool', default=False,
                               help='if each example has one set of shared '
                               'label candidates')
        DictionaryAgent.add_cmdline_args(argparser)
        return arg_group

    def __init__(self, opt, shared=None):
        # The K of the metric will most likely differ between train and
        # the valid set
        if opt.get('numthreads', 1) > 1:
            raise RuntimeError('Warning: You cannot use multithreading with '
                               'this agent, as the current metrics do not '
                               'support sharing of lists (for median rank '
                               'calculation). Please set --numthreads to 1')
        self.metrics = {'hitsAt1KC100': 0.0,
                        'loss': 0.0,
                        'num_samples': 0,
                        'med_rank': []}
        self.blank_image_features = torch.FloatTensor(
            opt.get('image_features_dim')).fill_(0)
        self.opt = opt
        if not shared:
            # This is the original agent. We create the model.
            build(opt)
            self.dict = DictionaryAgent(opt)
            if opt.get('dict_file', '').replace('.dict', '') != opt.get('model_file', ''):
                self.adapt_dictionary()

            print('Done dictionary')
            # load the list of personality
            personality_path = os.path.join(
                                opt['datapath'],
                                'comment_battle/200k_data/personalities.txt')
            self.personalities_list = self.load_personalities(personality_path)
            self.model_file = opt['model_file']
            self.samples_seen = 0
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
                self.model = CommentBattleModelURU.load_model(init_model_path, force_cpu=self.opt.get('no_cuda'))
                if not self.opt.get('no_cuda'):
                    self.model.cuda()
            else:
                # otherwise creates a new one
                # the model takes an object as parameter
                self.model = CommentBattleModelURU(opt, self.personalities_list, self.dict)
                if not opt.get('no_cuda', False):
                    self.model.cuda()
            if self.freeze_patience != -1:
                # We use fine tuning. We'll first freeze the encoder,
                # then release it.
                self.model.freeze_text_encoder()
                self.freeze_impatience = 0
                self.freeze_best_metric = 0
                self.is_frozen = True
            print('Done')
        else:
            # This is a copy of the agent that has been created
            # for batching or parallelizing purpose.
            self.dict = shared['dict']
            self.model = shared['model']
            self.personalities_list = shared['personalities_list']

        # Not sure why we need that, but whatever.
        self.one_cand_set = opt.get('one_cand_set', False)
        self.episode_done = True
        super().__init__(opt, shared)

    def share(self):
        '''
            To realize batching, parlAI actually duplicate the agent.
            Everything that we don't want to replicate should be part
            of the 'shared' dictionary
        '''
        shared = super().share()
        shared['dict'] = self.dict
        shared['model'] = self.model
        shared['personalities_list'] = self.personalities_list
        return shared

    def load_personalities(self, filepath):
        """
            return the list of personality
        """
        perss = []
        with open(filepath) as f:
            for line in f:
                if 'Trait' not in line:
                    perss.append(line[0:-1])
        return perss

    ######################################
    #  Observing and acting
    ######################################

    def observe(self, observations):
        '''
            Observe. Anything else to be done here?
        '''
        self.observation = observations
        return observations

    def act(self):
        return self.batch_act([self.observation])

    def batch_act(self, observations):
        '''
             {
                'text': <personality>,
                'image': <image features>,
                'label': <comment>,
             }
        '''

        is_training = any(['labels' in obs for obs in observations])
        valid_obs, valid_indexes = self.keep_valid_observations(observations,
                                                                is_training)
        image_feats = [v.get('image') for v in valid_obs]
        for i, im in enumerate(image_feats):
            try:
                if len(im.size()) == 4:
                    image_feats[i] = im[0, :, 0, 0]
            except TypeError: # No Image Feats Given
                image_feats[i] = self.blank_image_features
        personalities = [v.get('text', '') for v in valid_obs]
        elected = None
        med_rank = None
        if is_training:
            comments = [random.choice(v['labels']) for v in valid_obs]
            total_loss, nb_ok, total_evaluated = self.model.train_batch(
                                                    image_feats,
                                                    personalities,
                                                    comments)
        else:
            comments = [v['eval_labels'] for v in valid_obs]
            if 'label_candidates' in valid_obs[0]:
                # User provides candidates, used as negatives for evaluation
                candidates = [v['label_candidates'] for v in valid_obs]
                candidates_encoded = None
                if self.one_cand_set:
                    candidates_encoded = self.model(None, None, candidates[0])[1].detach()
                elected = self.model.elect_best_comment(image_feats,
                                                        personalities,
                                                        candidates,
                                                        candidates_encoded=candidates_encoded,
                                                        k=-1)
                equality_list = [1 if elected[i][0] in comments[i] else 0 for i in range(len(comments))]
                #calculate med ranks
                med_rank = []
                for i, e_list in enumerate(elected):
                    lowest_rank = len(e_list) + 1
                    for ii, c in enumerate(comments[i]):
                        lowest_rank = min(lowest_rank, e_list.index(c) + 1)
                    med_rank.append(lowest_rank)
                nb_ok = sum(equality_list)
                total_loss = -1  # no loss in that mode sorry
                total_evaluated = len(elected)
            else:
                comments = [random.choice(v['eval_labels']) for v in valid_obs]
                total_loss, nb_ok, total_evaluated = self.model.eval_batch(
                                                     image_feats,
                                                     personalities,
                                                     comments)
        self.update_metrics(total_loss, nb_ok, total_evaluated, med_rank)
        default_res = 'This agent doesn\'t produce actual response for now.'
        result = [{'text': default_res} for _ in range(len(observations))]
        if elected is not None:
            for i, index_obs in enumerate(valid_indexes):
                result[index_obs]['text'] = elected[i][0]
                result[index_obs]['text_candidates'] = elected[i]
        return result

    def keep_valid_observations(self, observations, is_training):
        '''
            In some special cases (the end of validation for instance)
            it is possible that some of the observations are invalid.
        '''
        label_key = 'labels' if is_training else 'eval_labels'
        valid_obs = list()
        valid_indexes = list()
        seen_texts = set()
        seen = 0
        for i in range(len(observations)):
            if 'image' in observations[i]:
                text = observations[i][label_key][0]
                if text not in seen_texts:
                    seen_texts.add(text)
                    valid_obs.append(observations[i])
                    valid_indexes.append(i)
                else:
                    seen += 1
        return valid_obs, valid_indexes

    def update_metrics(self, total_loss, nb_ok, num_samples, med_rank=None):
        self.metrics['hitsAt1KC100'] += nb_ok
        self.metrics['loss'] += total_loss
        self.metrics['num_samples'] += num_samples
        if med_rank:
            self.metrics['med_rank'] += med_rank

    def adapt_dictionary(self):
        """
            For whatever reasons the dictionary used on reddit was not exactly
            the same style as the one used in ParlAI.
        """
        new_tok2ind = {}
        new_ind2tok = {}
        for key in self.dict.tok2ind:
            val = self.dict.tok2ind[key]
            if val - 4 >= 0:
                new_tok2ind[key] = val - 4
                new_ind2tok[val-4] = key
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
            release the weights of the pretrained encode after a certain number
            of rounds without improvement.
        """
        if 'tasks' in metrics_dict:
            metrics_dict = metrics_dict['tasks']['internal:comment_battle']
        if self.freeze_patience != -1 and self.is_frozen:
            m = metrics_dict['hitsAt1KC100']
            if m > self.freeze_best_metric:
                self.freeze_impatience = 0
                self.freeze_best_metric = m
                print('performance not good enough to unfreeze the model.')
            else:
                self.freeze_impatience += 1
                print('Growing impatience for unfreezing')
                if self.freeze_impatience >= self.freeze_patience:
                    self.is_frozen = False
                    print('Reached impatience for fine tuning. Realoading the best model so far.')
                    self.model = CommentBattleModelURU.load_model(self.model_file)
                    if not self.opt.get('no_cuda'):
                        self.model = self.model.cuda()
                    print('Unfreezing.')
                    self.model.unfreeze_text_encoder()
                    print('Done')

    #########################################################################
    #   The following methods are there to report the evolution of the     #
    #   model.                                                             #
    ########################################################################

    def reset(self):
        '''Reset observation and episode_done.
            Mecanism copied from seq2seq'''
        self.reset_metrics()

    def reset_metrics(self):
        self.metrics['hitsAt1KC100'] = 0.0
        self.metrics['loss'] = 0.0
        self.metrics['num_samples'] = 0.0
        if 'med_rank' in self.metrics:
            self.metrics['med_rank'] = []

    def report(self):
        m = {}
        if self.metrics['num_samples'] > 0:
            m['hitsAt1KC100'] = round_sigfigs(self.metrics['hitsAt1KC100'] / self.metrics['num_samples'],4)
            m['loss'] = round_sigfigs(self.metrics['loss'] / self.metrics['num_samples'],4)
            if 'med_rank' in self.metrics:
                m['med_rank'] = np.median(self.metrics['med_rank'])
        return m

    ######################################
    #  Serialization
    ######################################

    def save(self, path = None):
        """
            Save the model. The model will contain the dic and the archi too,
            cf CommentBattleModelURU
        """
        path = self.opt.get('model_file', None) if path is None else path
        print('Saving best model')
        CommentBattleModelURU.save_model(self.model, path)
        with open(path + '.opt', 'wb') as handle:
            pickle.dump(self.opt, handle, protocol=pickle.HIGHEST_PROTOCOL)

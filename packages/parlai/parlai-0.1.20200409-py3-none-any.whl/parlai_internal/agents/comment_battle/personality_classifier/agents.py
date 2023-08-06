#!/usr/bin/env python3
from parlai.core.agents import Agent
from parlai.core.dict import DictionaryAgent
from parlai.utils.misc import maintain_dialog_history, round_sigfigs
from .personality_classifier import PersonalityClassifierURU
from collections import namedtuple


import os
import copy
import random
import numpy as np
import pdb
import random

class PersonalityClassifierUruAgent(Agent):
    '''
        Pretty much a pure copy of the Comment Battle Model
    '''
    pass
    ######################################
    # Initialization and argument parsers
    ######################################

    @staticmethod
    def add_cmdline_args(argparser):
        arg_group = argparser.add_argument_group('ImageCommenting Arguments')
        PersonalityClassifierURU.add_cmdline_args(argparser)
        DictionaryAgent.add_cmdline_args(argparser)
        argparser.add_argument('--freeze-patience', type=int, default=-1)
        argparser.add_argument('--comment-battle-model', type=str, default=-1)
        return arg_group


    def __init__(self, opt, shared=None):
        # The K of the metric will most likely differ between train and
        # the valid set
        self.metrics = {'acc': 0.0, "loss": 0.0, "num_samples":0 }
        if not shared:
            # This is the original agent. We create the model.
            self.dict = DictionaryAgent(opt)
            self.adapt_dictionary()

            print("Done dictionary")
            # load the list of personality
            personality_path = os.path.join(opt['datapath'],
                                'comment_battle/100k_data/personalities.txt')
            self.personalities_list = self.load_personalities(personality_path)
            self.model_file = opt["model_file"]
            self.samples_seen = 0
            self.id = 'PersonalityClassifierUruAgent'

            # possibly load the model from a model file
            if opt.get('init_model') and os.path.isfile(opt['init_model']):
                init_model_path = opt['init_model']
            elif opt.get('model_file') and os.path.isfile(opt['model_file']):
                init_model_path = opt['model_file']
            else:
                init_model_path = None
            print("Creating or loading model")
            self.freeze_patience = opt["freeze_patience"]
            if init_model_path is not None:
                self.model = PersonalityClassifierURU.load_model(init_model_path).cuda()
            else:
                # otherwise creates a new one
                # the model takes an object as parameter
                self.model = PersonalityClassifierURU(opt, self.personalities_list, self.dict).cuda()
            if self.freeze_patience != -1:
                # We use fine tuning. We'll first freeze the encoder,
                # then release it.
                self.model.freeze_text_encoder()
                self.freeze_impatience = 0
                self.freeze_best_metric = 0
                self.is_frozen = True
            print("Done")
        else:
            # This is a copy of the agent that has been created
            # for batching or parallelizing purpose.
            self.dict = shared['dict']
            self.model = shared['model']
            self.personalities_list = shared["personalities_list"]

        # Not sure why we need that, but whatever.
        self.episode_done = True
        super().__init__(opt, shared)

    ######################################
    #  Observing and acting
    ######################################

    def observe(self, observations):
        '''
            Observe. Anything else to be done here?
        '''
        return observations


    def batch_act(self, observations):
        is_training = any(['labels' in obs for obs in observations])
        valid_obs, valid_indexes = self.keep_valid_observations(observations, is_training)
        image_feats = [v["uru_features"] for v in valid_obs]
        comments = [v["text"] for v in valid_obs]

        if is_training:
            personas = [v["labels"][0] for v in valid_obs]
            loss, nb_ok, predicted_personas =  self.model.train_batch(image_feats, comments, personas)
        else:
            personas = [v['eval_labels'][0] for v in valid_obs]
            loss, nb_ok, predicted_personas = self.model.eval_batch(image_feats, comments, personas)

            if self.metrics["num_samples"] == 0:
                print(personas[0:8])
                print(predicted_personas[0:8])
        self.update_metrics(self.metrics, loss, nb_ok, len(predicted_personas))
        result = [{"text": "No result here."} for _ in range(len(observations))]
        for i, p in enumerate(predicted_personas):
            result[valid_indexes[i]]["text"] = p
        return result


    def keep_valid_observations(self, observations, is_training):
        '''
            In some special cases (the end of validation for instance)
            it is possible that some of the observations are invalid.
        '''
        label_key = "labels" if is_training else 'eval_labels'
        valid_obs = list()
        valid_indexes = list()
        for i in range(len(observations)):
            if 'uru_features' in observations[i]:
                valid_obs.append(observations[i])
                valid_indexes.append(i)
        return valid_obs, valid_indexes


    def update_metrics(self, metrics, total_loss, nb_ok, num_samples):
        metrics['acc'] += nb_ok
        metrics['loss'] += total_loss
        metrics['num_samples'] += num_samples

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
        self.dict.null_token = "<PAD>"
        self.dict.unk_token = "<UNK>"
        self.dict.tok2ind = new_tok2ind
        self.dict.ind2tok = new_ind2tok

    def load_personalities(self, filepath):
        """
            return the list of personality
        """
        perss = []
        with open(filepath) as f:
            for line in f:
                if not "Trait" in line:
                    perss.append(line[0:-1])
        return perss

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
        if self.freeze_patience != -1 and self.is_frozen:
            m = metrics_dict['acc']
            if m > self.freeze_best_metric:
                self.freeze_impatience = 0
                self.freeze_best_metric = m
                print("performance not good enough to unfreeze the model.")
            else:
                self.freeze_impatience += 1
                print("Growing impatience for unfreezing")
                if self.freeze_impatience >= self.freeze_patience:
                    self.is_frozen = False
                    print("Reached impatience for fine tuning. Realoading the best model so far.")
                    self.model = PersonalityClassifierURU.load_model(self.model_file).cuda()
                    print("Unfreezing.")
                    self.model.unfreeze_text_encoder()
                    print("Done")


    #########################################################################
    #   The following methods are there to report the evolution of the     #
    #   model.                                                             #
    ########################################################################

    def reset(self):
        '''Reset observation and episode_done.
            Mecanism copied from seq2seq'''
        self.reset_metrics()

    def reset_metrics(self):
        self.metrics['acc'] = 0.0
        self.metrics['loss'] = 0.0
        self.metrics['num_samples'] = 0.0

    def report(self):
        m = {}
        if self.metrics['num_samples'] > 0:
            m['acc'] = round_sigfigs(self.metrics['acc'] / self.metrics['num_samples'],4)
            m['loss'] = round_sigfigs(self.metrics['loss'] / self.metrics['num_samples'],4)
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
        print("Saving best model")
        PersonalityClassifierURU.save_model(self.model, path)

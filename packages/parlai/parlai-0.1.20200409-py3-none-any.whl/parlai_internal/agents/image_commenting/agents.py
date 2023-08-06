#!/usr/bin/env python3
from parlai.core.agents import Agent
from parlai.core.dict import DictionaryAgent
from parlai.utils.misc import maintain_dialog_history, round_sigfigs

import torch
from torch import optim
from torch.autograd import Variable
from torch.nn import CrossEntropyLoss
import time


import os
import copy
import random
import numpy as np
import pdb

from .model import ImageCaptioning


class ImageCommentingAgent(Agent):
    '''
        Image captioning agents used for commenting.
        This class actually only handles the interaction with the ParlAI
        framework. The actual work is left to the model in model.py
    '''

    ######################################
    # Initialization and argument parsers
    ######################################

    @staticmethod
    def add_cmdline_args(argparser):
        arg_group = argparser.add_argument_group('ImageCommenting Arguments')
        arg_group.add_argument(
            '--init-model',
            type=str,
            default=None,
            help='load dict/features/weights/opts from this file',
        )
        arg_group.add_argument(
            '-al', '--adam-alpha', type=float, default=0.001, help='learning rate'
        )
        arg_group.add_argument(
            '--embedding-size', type=int, default=128, help='size of token embeddings'
        )
        arg_group.add_argument(
            '--use-pictures',
            default=True,
            type='bool',
            help='Whether or not we should use the pictures',
        )
        arg_group.add_argument(
            '--use-batch-norm-for-pics',
            default=False,
            type='bool',
            help='Whether or not we should use batch norm for the pictures',
        )
        arg_group.add_argument(
            '--preprocess-image-features',
            default=False,
            type='bool',
            help='Apply a ReLU layer before feeding the image to the net.',
        )
        arg_group.add_argument(
            '--feed-to-state',
            default=False,
            type='bool',
            help='If true, insert the image as the hidden state and not as the word.',
        )
        arg_group.add_argument(
            '--feed-image-each-step',
            default=False,
            type='bool',
            help='Instead of just providing the image once at start, we provide it at every step.',
        )
        arg_group.add_argument(
            '--dropout-embed-layer',
            default=False,
            type='bool',
            help='If true also applies the dropout to the embed layer.',
        )
        arg_group.add_argument(
            '--use-uru',
            default=True,
            type='bool',
            help='Whether we should use the uru features instead of resnext ones',
        )
        arg_group.add_argument(
            '--truncate-length',
            type=int,
            default=32,
            help='Maximum length of a sentence before we truncate.',
        )
        arg_group.add_argument(
            '--hiddensize', type=int, default=32, help='Size of hidden states to use.'
        )
        arg_group.add_argument(
            '--no-cuda',
            action='store_true',
            default=False,
            help='disable GPUs even if available',
        )
        arg_group.add_argument(
            '--image-features-dim',
            type=int,
            default=2048,
            help='Size of hidden states to use.',
        )
        arg_group.add_argument(
            '--output', type=str, default='rank', help='type of output (rank|generate)'
        )
        arg_group.add_argument(
            '--personality',
            type=str,
            default='none',
            help='type of personality (none|positivity)',
        )
        arg_group.add_argument(
            '--rnn-layers',
            type=int,
            default=2,
            help='number of hidden layers in RNN decoder for generative output',
        )
        arg_group.add_argument(
            '--dropout',
            type=float,
            default=0.1,
            help='dropout probability for RNN decoder training',
        )
        arg_group.add_argument(
            '--temperature',
            type=float,
            default=0.1,
            help='Temperature to use for the softmax during sentence generation',
        )
        arg_group.add_argument(
            '--embeddings-file',
            type=str,
            default=None,
            help='if not None, we will initialize the word vectors using the embeddings in this file.',
        )
        arg_group.add_argument(
            '--gpu', type=int, default=0, help='which GPU device to use'
        )
        DictionaryAgent.add_cmdline_args(argparser)
        return arg_group

    def __init__(self, opt, shared=None):

        self.metrics = {'log_perplexity': 0.0, 'num_tokens': 0, 'corrects': 0}
        if not shared:
            # print('%s (Agent) Creating original agent for datatype: %s' % (time.strftime('%H:%M:%S'), opt['datatype']))
            # This is the original agent. We create the model.
            torch.cuda.device(opt['gpu'])
            self.dict = DictionaryAgent(opt)
            self.model_file = opt["model_file"]
            self.use_uru = opt["use_uru"]
            self.samples_seen = 0
            self.id = 'ImageCommenting'
            self.personality = opt["personality"]

            # Do we a personality conditioning?
            nb_features_personality = 0
            if opt["personality"] == "positivity":
                nb_features_personality = 2

            # possibly load the model from a model file
            if opt.get('init_model') and os.path.isfile(opt['init_model']):
                init_model_path = opt['init_model']
            elif opt.get('model_file') and os.path.isfile(opt['model_file']):
                init_model_path = opt['model_file']
            else:
                init_model_path = None
            if init_model_path is not None:
                self.model = self.load(init_model_path).cuda()
            else:
                # otherwise creates a new one
                self.model = ImageCaptioning(
                    embedding_dim=opt['embedding_size'],
                    hidden_dim=opt['hiddensize'],
                    image_features_dim=opt['image_features_dim'],
                    num_layers=opt['rnn_layers'],
                    vocab_size=len(self.dict),
                    truncate_length=opt['truncate_length'],
                    dropout=opt['dropout'],
                    use_cuda=not opt['no_cuda'],
                    adam_alpha=opt['adam_alpha'],
                    use_pictures=opt['use_pictures'],
                    feed_state=opt["feed_to_state"],
                    use_batch_norm_for_pics=opt["use_batch_norm_for_pics"],
                    preprocess_image_features=opt["preprocess_image_features"],
                    personality_features_dim=nb_features_personality,
                    concatenate_image_each_word=opt["feed_image_each_step"],
                    dropout_embed_layer=opt["dropout_embed_layer"],
                ).cuda()
                # optionally we can start with embeddings from a file (glove for instance)
                if opt["embeddings_file"] is not None:
                    self.model.initialize_word_embeddings(
                        opt["embeddings_file"], self.dict
                    )

        else:
            # This is a copy of the agent that has been created
            # for batching or parallelizing purpose.
            # print('%s (Agent) Creating copy agent for datatype: %s' % (time.strftime('%H:%M:%S'), opt['datatype']))
            self.dict = shared['dict']
            self.model = shared['model']

        # Not sure why we need that, but whatever.
        self.episode_done = True
        super().__init__(opt, shared)
        # print('%s 7(Agent) Done creating the agent' % (time.strftime('%H:%M:%S')))

    def share(self):
        '''
            To realize batching, parlAI actually duplicate the agent.
            Everything that we don't want to replicate should be part
            of the 'shared' dictionary
        '''
        shared = super().share()
        shared['dict'] = self.dict
        shared['model'] = self.model
        return shared

    ######################################
    #  Observing and acting
    ######################################

    def observe(self, observations):
        '''
            Observe. Anything else to be done here?
        '''
        return observations

    def batch_act(self, observations):
        '''
             Act accordingly to the case (maybe we are in valid, or we are
             generating instead of selecting the best.)
             Each observation contains:
             {
                image_features: torch vector
                labels: list with just one element that is the comment
                    we are trying to generate.
                label_candidates: candidate labels (for classification)
             }
        '''

        # At the end of validation, it's possible that parlai fills with
        # invalid observation to keep batch size
        valid_observations, valid_idx = self.keep_valid_observations(observations)
        which_features = 'image_features_uru' if self.use_uru else 'image_features'
        image_feats = [obs[which_features] for obs in valid_observations]
        personality = self.get_personality(valid_observations)
        image_urls = [obs['image_url'] for obs in valid_observations]
        is_training = any(['labels' in obs for obs in valid_observations])
        labels_cands = [obs['label_candidates'] for obs in valid_observations]

        predictions = []
        mode = self.opt['output']
        first_batch = self.metrics['num_tokens'] == 0

        if is_training:
            # Easy, we do a train stop
            labels = [obs['labels'][0] for obs in valid_observations]
            # get log perplexity, the number of words (and also some details)
            lppl, nwords, _ = self.model.train_step(
                image_feats, labels, self.dict, personality=personality
            )
            self.metrics['log_perplexity'] += lppl * nwords
            self.metrics['num_tokens'] += nwords
            # And we are done
            predictions = [
                'No prediction at train time.' for i in range(len(valid_observations))
            ]
        else:
            # In any case we compute the perplexity
            eval_labels = [obs['eval_labels'][0] for obs in valid_observations]
            lppl, nwords, d = self.model.get_log_perplexity(
                image_feats, eval_labels, self.dict, personality=personality
            )
            self.metrics['log_perplexity'] += lppl * nwords
            self.metrics['num_tokens'] += nwords

            # We are in validation mode. There are 2 modes, generation and rank
            # They determine how we generate the prediction
            if mode == 'generate':
                predictions = self.model.generate(
                    image_feats,
                    self.dict,
                    self.opt['temperature'],
                    personality=personality,
                )
            else:
                predictions, probas = self.model.choose_best_candidate(
                    image_feats, labels_cands, self.dict, personality=personality
                )
                for i in range(len(predictions)):
                    if predictions[i] == eval_labels[i]:
                        self.metrics['corrects'] += 1
                # for the first batch, generate some labels so that we can see an example of output
                if first_batch:
                    generated = self.model.generate(
                        image_feats, self.dict, 0.5, personality=personality
                    )

        # some observations might have been invalid. Ensures a good 1:1 mapping
        result = [{} for _ in range(len(observations))]
        for i in range(len(valid_observations)):
            result[valid_idx[i]]['text'] = predictions[i]
        return result

    def keep_valid_observations(self, observations):
        '''
            In some special cases (the end of validation for instance)
            it is possible that some of the observations are invalid.
        '''
        valid_obs = list()
        valid_indexes = list()
        for i in range(len(observations)):
            if 'image_features' in observations[i]:
                valid_obs.append(observations[i])
                valid_indexes.append(i)
        return valid_obs, valid_indexes

    def get_personality(self, observations):
        if self.personality == "positivity":
            return [
                torch.FloatTensor([1 - obs["positivity"], obs["positivity"]])
                for obs in observations
            ]
        return None

    #########################################################################
    #   The following methods are there to report the evolution of the     #
    #   model.                                                             #
    ########################################################################

    def reset(self):
        '''Reset observation and episode_done.
            Mecanism copied from seq2seq'''
        self.reset_metrics()

    def reset_metrics(self):
        self.metrics['log_perplexity'] = 0.0
        self.metrics['num_tokens'] = 0
        self.metrics['corrects'] = 0

    def report(self):
        m = {}
        if self.metrics['num_tokens'] > 0:
            m['log_perplexity'] = (
                self.metrics['log_perplexity'] / self.metrics['num_tokens']
            )
            m['ppl'] = np.exp(m['log_perplexity'])
        for k, v in m.items():
            # clean up: rounds to sigfigs and converts tensors to floats
            m[k] = round_sigfigs(v, 4)
        m['num_tokens'] = self.metrics['num_tokens']
        m["corrects"] = self.metrics['corrects']
        return m

    ######################################
    #  Serialization
    ######################################

    def save(self, path=None):
        path = self.opt.get('model_file', None) if path is None else path
        with open(path, 'wb') as write:
            torch.save(self.model, write)

    def load(self, path):
        """Return opt and model states."""
        model = torch.load(path)
        return model

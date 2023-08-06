#!/usr/bin/env python3

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from parlai.core.torch_agent import TorchAgent, Output
from parlai.utils.misc import round_sigfigs, warn_once
from collections import defaultdict
import parlai.utils.distributed as distributed_utils

import os
import json
import math
import torch
import torch.nn.functional as F


class TorchClassifierAgent(TorchAgent):
    """ A torch agent that is a classifier. The number of output is limited and
        provided at initialization
    """

    @staticmethod
    def add_cmdline_args(parser):
        TorchAgent.add_cmdline_args(parser)
        parser = parser.add_argument_group('Torch Classifier Arguments')
        parser.add_argument('--classes', type=str, nargs='*', default=None,
                            help='the name of the classes.')
        parser.add_argument('--class-weights', type=float, nargs='*', default=None,
                            help='weight of each of the classes for the softmax')
        parser.add_argument('--data-parallel', type="bool", default=False,
                            help='uses DataParallel for multi GPU')
        parser.add_argument('--ref-class', type=str, default=None, hidden=True,
                            help='The class that will be used to compute '
                                 'precision and recall. By default the first one.')
        parser.add_argument('--interactive-mode', type='bool', default= False)
        parser.add_argument('--print-prob', type='bool', default=False,
                            help='print probability of ref class during '
                                 'interactive mode')
        parser.add_argument('--get-all-metrics', type='bool', default=True,
                            help='give prec/recall metrics for all classes')
        parser.add_argument('--threshold', type=float, default=0.5,
                            help='during evaluation, threshold for choosing '
                                 'ref class; only applies to binary '
                                 'classification')

    def __init__(self, opt, shared=None):
        super().__init__(opt, shared)

        if opt.get('data_parallel') and distributed_utils.is_distributed():
            raise ValueError('Cannot use --data-parallel and distributed.')

        if opt.get('classes') is None:
            raise RuntimeError(
                'Must specify --classes argument.'
            )

        # classes
        if not shared:
            self.class_list = opt['classes']
            self.class_dict = {val: i for i, val in enumerate(self.class_list)}
            if opt.get('class_weights', None) is not None:
                self.class_weights = opt['class_weights']
            else:
                self.class_weights = [1.0 for c in self.class_list]
            self.reset_metrics()
        else:
            self.class_list = shared['class_list']
            self.class_dict = shared['class_dict']
            self.class_weights = shared['class_weights']

        if opt['ref_class'] is None or opt['ref_class'] not in self.class_dict:
            self.ref_class = self.class_list[0]
        else:
            self.ref_class = opt['ref_class']
            ref_class_id = self.class_list.index(self.ref_class)
            if ref_class_id != 0:
                # move to the front of the class list
                self.class_list.insert(0, self.class_list.pop(ref_class_id))

        if len(self.class_list) == 2 and opt.get('threshold', 0.5) != 0.5:
            self.threshold = opt['threshold']
        else:
            self.threshold = None

        warn_once('Using %s as the class for computing P, R, and F1' %
                  self.ref_class)
        weight_tensor = torch.FloatTensor(self.class_weights)

        # model and optimizers
        self.classifier_loss = torch.nn.CrossEntropyLoss(weight_tensor)
        if shared:
            self.model = shared['model']
        else:
            model_file = self._get_model_file(opt)
            self.build_model()
            if model_file:
                print('Loading existing model parameters from ' + model_file)
                self.load(model_file)

            if self.use_cuda and shared is None:
                self.model.cuda()
                self.classifier_loss.cuda()
                if distributed_utils.is_distributed():
                    self.model = torch.nn.parallel.DistributedDataParallel(
                        self.model,
                        device_ids=[self.opt['gpu']],
                        broadcast_buffers=False,
                    )
                elif self.opt['data_parallel']:
                    self.model = torch.nn.DataParallel(self.model)

        if shared:
            # We don't use get here because hasattr is used on optimizer later.
            if 'optimizer' in shared:
                self.optimizer = shared['optimizer']
        else:
            optim_params = [p for p in self.model.parameters() if p.requires_grad]
            self.init_optim(optim_params)
            self.build_lr_scheduler()

    def share(self):
        """Share model parameters."""
        shared = super().share()
        shared['model'] = self.model
        shared['metrics'] = self.metrics
        shared['class_list'] = self.class_list
        shared['class_dict'] = self.class_dict
        shared['class_weights'] = self.class_weights
        shared['optimizer'] = self.optimizer
        return shared

    def _get_labels(self, batch):
        """ Obtain the correct labels. Raise an exception if one of the labels
            is not in the class list.
        """
        labels_indices_list = [self.class_dict[label] for label in batch.labels]
        labels_tensor = torch.LongTensor(labels_indices_list)
        if self.use_cuda:
            labels_tensor = labels_tensor.cuda()
        return labels_tensor

    def _update_confusion_matrix(self, batch, predictions):
        """ :param batch: a Batch object (defined in torch_agent.py)
            :param predictions: (list of string of length batchsize) label
                                predicted by the classifier
        """
        for i, pred in enumerate(predictions):
            label = batch.labels[i]
            self.metrics['confusion_matrix'][(label, pred)] += 1

    def train_step(self, batch):
        """Train on a single batch of examples."""
        if batch.text_vec is None:
            return
        self.model.train()
        self.optimizer.zero_grad()
        labels = self._get_labels(batch)
        scores = self.score(batch)
        loss = self.classifier_loss(scores, labels)
        self.metrics['loss'] += loss.item()
        self.metrics['examples'] += len(batch.text_vec)
        loss.backward()
        self.optimizer.step()
        _, prediction_id = torch.max(scores.cpu(), 1)
        preds = [self.class_list[idx] for idx in prediction_id]
        self._update_confusion_matrix(batch, preds)
        self.update_params()
        return Output(preds)

    def eval_step(self, batch):
        """Train on a single batch of examples."""
        if batch.text_vec is None:
            return
        self.model.eval()
        scores = self.score(batch)
        probs = F.softmax(scores, dim=1)
        if not self.threshold:
            _, prediction_id = torch.max(probs.cpu(), 1)
        else:
            ref_prob = probs.cpu()[:, 0]
            prediction_id = ref_prob <= self.threshold

        preds = [self.class_list[idx] for idx in prediction_id]

        if self.opt.get('interactive_mode', False):
            if self.opt.get('print_prob', False):
                probabilities = []
                for score in scores:
                    probabilities.append([probs][0])
                preds = []
                for i, pred_id in enumerate(prediction_id):
                    prob = round_sigfigs(probabilities[i][pred_id], 4)
                    preds.append('{}: {}'.format(self.class_list[pred_id],
                                                 prob))

        else:
            labels = self._get_labels(batch)
            loss = self.classifier_loss(scores, labels)
            self.metrics['loss'] += loss.item()
            self.metrics['examples'] += len(batch.text_vec)
            self._update_confusion_matrix(batch, preds)
        return Output(preds)

    def reset_metrics(self):
        """Reset metrics."""
        self.metrics = {}
        super().reset_metrics()
        self.metrics['examples'] = 0
        self.metrics['loss'] = 0.0
        self.metrics['confusion_matrix'] = defaultdict(int)

    def report(self):
        """Report loss from model's perspective."""
        m = super().report()
        examples = self.metrics['examples']
        if examples > 0:
            m['examples'] = examples
            m['mean_loss'] = self.metrics['loss'] / examples

            # get prec/recall metrics
            confmat = self.metrics['confusion_matrix']
            if self.opt.get('get_all_metrics'):
                metrics_list = self.class_list
            else:
                # only give prec/recall metrics for ref class
                metrics_list = [self.ref_class]
                
            examples_per_class = []

            for class_i in metrics_list:
                # uses the confusion matrix to predict the recall and precision
                true_positives = confmat[(class_i, class_i)]
                num_actual_positives = sum([confmat[(class_i, c)]
                                           for c in self.class_list]) + 0.0001
                num_predicted_positives = sum([confmat[(c, class_i)]
                                              for c in self.class_list]) + 0.0001
                examples_per_class.append(num_actual_positives)

                recall_str = 'class_{}_recall'.format(class_i)
                prec_str = 'class_{}_prec'.format(class_i)
                f1_str = 'class_{}_f1'.format(class_i)

                m[recall_str] = true_positives / num_actual_positives
                m[prec_str] = true_positives / num_predicted_positives
                m[f1_str] = 2 * ((m[recall_str] * m[prec_str]) /
                                 (m[recall_str] + m[prec_str] + 0.0001))

            if len(examples_per_class) > 1:
                # get weighted f1
                percent_of_total = [
                    x / sum(examples_per_class) for x in examples_per_class
                ]
                f1 = 0
                for i in range(len(self.class_list)):
                    f1 += (percent_of_total[i] *
                           m['class_{}_f1'.format(self.class_list[i])])
                m['weighted_f1'] = f1

        for k, v in m.items():
            m[k] = round_sigfigs(v, 4)

        return m

    def _get_model_file(self, opt):
        model_file = None
        # first check load path in case we need to override paths
        if opt.get('init_model') and os.path.isfile(opt['init_model']):
            # check first for 'init_model' for loading model from file
            model_file = opt['init_model']
        if opt.get('model_file') and os.path.isfile(opt['model_file']):
            # next check for 'model_file', this would override init_model
            model_file = opt['model_file']
        return model_file

    def score(self, batch):
        """
        Given a batch and labels, returns the scores.

        :param batch:
            a Batch object (defined in torch_agent.py)

        :return:
            The score of each class.
        :rtype:
            FloatTensor[bsz, num_classes]
        """

    def build_model(self):
        """At the end of this method, self.model is defined."""
        raise NotImplementedError(
            'Abstract class: user must implement build_model()')

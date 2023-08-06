#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
Ranker Mixin for adding classification metrics to ranking models in ParlAI.

Example usage:
python examples/train_model.py -m internal:bert_ranker_classifier -t internal:gender_multiclass:funpedia -mf /tmp/test11231 --train-predict True -cands inline -ecands inline -bs 4 --balance True
"""

from parlai.agents.bert_ranker.bi_encoder_ranker import BiEncoderRankerAgent
from parlai.core.opt import Opt
from parlai.utils.distributed import is_distributed
from parlai.core.torch_agent import TorchAgent, Output
from parlai.core.agents import Agent
from parlai.utils.misc import round_sigfigs, warn_once
from parlai.core.metrics import AverageMetric
from collections import defaultdict

import torch
import torch.nn.functional as F


class RankingClassificationMixin(Agent):
    def __init__(self, opt: Opt, shared=None):
        super().__init__(opt, shared)
        if shared is None:
            self.reset_metrics()

    def _update_confusion_matrix(self, predictions, labels):
        """
        Update the confusion matrix given the batch and predictions.

        :param batch:
            a Batch object (defined in torch_agent.py)
        :param predictions:
            (list of string of length batchsize) label predicted by the
            classifier
        """
        for pred, label in zip(predictions, labels):
            if pred is None or label is None:
                continue
            if len(label) > 1:
                category = label[0].split(':')[0]
                label = category + ':' + 'unknown'
            else:
                label = label[0]
            self.metrics['confusion_matrix'][(label, pred)] += 1

    def _get_preds(self, batch_reply):
        preds = [reply.get('text') for reply in batch_reply]
        if all(x is None for x in preds):
            return None

        return preds

    def _get_labels(self, observations, labels):
        labels = [obs.get(labels) for obs in observations]
        return labels

    def batch_act(self, observations):
        batch_reply = super().batch_act(observations)

        if 'labels' in observations[0]:
            labels = 'labels'
        elif 'eval_labels' in observations[0]:
            labels = 'eval_labels'
        else:
            return batch_reply

        preds = self._get_preds(batch_reply)

        if preds is None:
            return batch_reply

        labels_lst = self._get_labels(observations, labels)

        self._update_confusion_matrix(preds, labels_lst)

        return batch_reply

    def reset_metrics(self):
        """
        Reset metrics.
        """
        super().reset_metrics()
        self.metrics['confusion_matrix'] = defaultdict(int)

    def _report_prec_recall_metrics(self, confmat, class_name, metrics):
        """
        Use the confusion matrix to compute precision and recall.

        :param confmat:
            the confusion matrics
        :param str class_name:
            the class name to compute P/R for
        :param metrics:
            metrics dictionary to modify
        :return:
            the number of examples of each class.
        """
        # TODO: document these parameter types.
        eps = 0.00001  # prevent divide by zero errors
        true_positives = confmat[(class_name, class_name)]
        class_list = list(set(key[0] for key in confmat.keys()))
        num_actual_positives = sum([confmat[(class_name, c)] for c in class_list]) + eps
        num_predicted_positives = (
            sum([confmat[(c, class_name)] for c in class_list]) + eps
        )
        recall_str = 'class_{}_recall'.format(class_name)
        prec_str = 'class_{}_prec'.format(class_name)
        f1_str = 'class_{}_f1'.format(class_name)

        # update metrics dict
        metrics[recall_str] = true_positives / num_actual_positives
        metrics[prec_str] = true_positives / num_predicted_positives
        metrics[f1_str] = 2 * (
            (metrics[recall_str] * metrics[prec_str])
            / (metrics[recall_str] + metrics[prec_str] + eps)
        )

        return num_actual_positives

    def report(self):
        """
        Report loss as well as precision, recall, and F1 metrics.
        """
        m = super().report()
        # TODO: upgrade the confusion matrix to newer metrics
        # get prec/recall metrics
        confmat = self.metrics['confusion_matrix']
        metrics_list = [key[0] for key in confmat.keys()]

        examples_per_class = []
        for class_i in metrics_list:
            class_total = self._report_prec_recall_metrics(confmat, class_i, m)
            examples_per_class.append(class_total)

        if len(examples_per_class) > 1:
            # get weighted f1
            f1 = 0
            total_exs = sum(examples_per_class)
            for i in range(len(metrics_list)):
                f1 += (examples_per_class[i] / total_exs) * m[
                    'class_{}_f1'.format(metrics_list[i])
                ]
            m['weighted_f1'] = f1

            # get weighted accuracy
            wacc = 0
            for i in range(len(metrics_list)):
                wacc += (1.0 / len(metrics_list)) * m[
                    'class_{}_recall'.format(metrics_list[i])
                ]
            m['weighted_acc'] = wacc

            # get weighted gender accuracy
            # TODO: delete this
            tot = 0
            for axis in ['ABOUT', 'SELF', 'PARTNER']:
                wacc = 0
                gend_lst = ['female', 'male']
                if axis == 'ABOUT':
                    gend_lst.append('gender-neutral')
                for gend in gend_lst:
                    wacc += 1.0 / len(gend_lst) * m.get('class_{}_recall'.format(f'{axis}:{gend}'), 0)
                if wacc > 0:
                    m[f'weighted_{axis}_gendacc'] = wacc
                tot += wacc

            if tot > 0:
                m['weighted_gend_acc'] = tot / 3

        return m


class BertRankerClassifierAgent(RankingClassificationMixin, BiEncoderRankerAgent):
    """
    Bert BiEncoder that computes F1 metrics
    """

    pass

#!/usr/bin/env python3

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from .torch_classifier import TorchClassifierAgent
from parlai.agents.bert_ranker.helpers import BertWrapper, get_bert_optimizer
try:
    from pytorch_pretrained_bert import BertModel
except ImportError:
    raise Exception(("BERT rankers needs pytorch-pretrained-BERT installed. \n "
                     "pip install pytorch-pretrained-bert"))
from parlai_internal.agents.bert_ranker.bert_dictionary import BertDictionaryAgent


class BertClassifierAgent(TorchClassifierAgent):
    """ Classifier based on Bert
    """

    @staticmethod
    def add_cmdline_args(parser):
        TorchClassifierAgent.add_cmdline_args(parser)
        parser = parser.add_argument_group('Bert Classifier Arguments')
        parser.add_argument('--bert-id', type=str, default='bert-base-uncased')
        parser.add_argument(
            '--type-optimization',
            type=str,
            default="additional_layers",
            choices=[
                "additional_layers",
                "top_layer",
                "top4_layers",
                "all_encoder_layers",
                "all"],
            help="Which part of the encoders do we optimize. (Default: the top one.)")

    @staticmethod
    def dictionary_class():
        return BertDictionaryAgent

    def build_model(self):
        num_classes = len(self.class_list)
        self.model = BertWrapper(
            BertModel.from_pretrained(self.opt["bert_id"]),
            num_classes)

    def init_optim(self, params, optim_states=None, saved_optim_type=None):
        self.optimizer = get_bert_optimizer([self.model],
                                            self.opt["type_optimization"],
                                            self.opt["learningrate"])

    def score(self, batch):
        segment_idx = batch.text_vec * 0
        mask = (batch.text_vec != self.NULL_IDX).long()
        token_idx = batch.text_vec * mask
        return self.model(token_idx, segment_idx, mask)

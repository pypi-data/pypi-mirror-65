#!/usr/bin/env python3

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from .torch_classifier import TorchClassifierAgent
import torch


class BasicBowTorchClassifierAgent(TorchClassifierAgent):
    """ A simple example of a torch classifier, associate
        each token with a vector of length num_classes.
        The score is computed as the average for each token.
    """

    def build_model(self):
        num_classes = len(self.class_list)
        size_vocabulary = len(self.dict)
        self.model = torch.nn.Embedding(size_vocabulary, num_classes)

    def score(self, batch):
        # batch_size x sent_len x num_classes
        scores_per_word = self.model(batch.text_vec)
        scores = torch.mean(scores_per_word, 1)  # batch_size x num_classes
        return scores

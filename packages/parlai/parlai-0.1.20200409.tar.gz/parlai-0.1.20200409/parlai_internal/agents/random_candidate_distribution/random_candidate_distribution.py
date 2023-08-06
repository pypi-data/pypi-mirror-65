#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Simple agent which chooses a random label with probabilities based on the
label distribution of the train set.

For instance, if in the train set 40% of labels were X and 60% of labels were
Y, during evaluation it would choose label X with probability 0.4 and Y with
probability 0.6.
"""

from copy import deepcopy
import numpy.random as nrand
from tqdm import tqdm
import random

from parlai.core.agents import Agent
from parlai.core.loader import load_teacher_module


class RandomCandidateDistributionAgent(Agent):
    """Agent returns random candidate if available or repeats the label."""
    def __init__(self, opt, shared=None):
        """Initialize this agent."""
        super().__init__(opt)
        self.id = 'RandomCandidateDistributionAgent'
        random.seed(42)
        if 'task' not in opt:
            raise RuntimeError(
                'This agent needs a task in order to be defined. '
                'Please specify a task with `-t <task>`.'
            )
        self.label_distribution = self._get_train_distribution(opt)
        self.all_train_candidates = []
        self.probs = []
        print('Train distribution:')
        for k, v in self.label_distribution.items():
            print(f'{k}: {v}')
            self.all_train_candidates.append(k)
            self.probs.append(v)

        nrand.seed(42)

    def _get_train_distribution(self, opt):
        """Iterate over the train set of the corresponding task and get the
        distribution of the trainset
        """
        train_teacher_opt = deepcopy(opt)
        train_teacher_opt['datatype'] = 'train:ordered'
        task_module = load_teacher_module(opt['task'])
        teacher = task_module(train_teacher_opt)

        label_distribution = {}
        total_exs = teacher.num_examples()
        print('[ Iterating through train set to get label distribution ... ]')
        for _ in tqdm(range(total_exs)):
            action = teacher.act()
            for label in action['labels']:
                label_distribution.setdefault(label, 0)
                label_distribution[label] += 1

        total = sum(label_distribution.values())
        normalized_dist = {}
        for k, v in label_distribution.items():
            normalized_dist[k] = v / total

        return normalized_dist

    def act(self):
        """Generate response to last seen observation.

        Replies with a randomly selected candidate based on the label
        distribution of the train set

        :returns: message dict with reply
        """
        obs = self.observation
        if obs is None:
            return {'text': 'Nothing to reply to yet.'}

        reply = {}
        reply['id'] = self.getID()
        if 'label_candidates' not in obs:
            # select from the entire train set
            cand_select = nrand.multinomial(1, self.probs).nonzero()[0].item()
            candidate = self.all_train_candidates[cand_select]
        else:
            # select from the list of provided label candidates
            label_cands = obs['label_candidates']
            # renormalize the probabilities
            probs = []
            for cand in label_cands:
                if cand in self.label_distribution:
                    prob = self.label_distribution[cand]
                else:
                    prob = 0
                probs.append(prob)
            assert sum(probs) > 0, 'Probabilities sum to 0'
            adjusted_probs = [x / sum(probs) for x in probs]
            cand_select = nrand.multinomial(1, adjusted_probs).nonzero()[0].item()
            candidate = label_cands[cand_select]

        reply['text'] = candidate

        return reply

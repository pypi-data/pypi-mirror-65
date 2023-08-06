#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#
# TEST:
#  py examples/train_model.py -t fromfile -m "parlai_internal.agents.starspace.starspace:StarspaceAgent"  --fromfile_datapath data/simple_test/train2.txt -k 20 --dict-file /tmp/dict2 -dt train:ordered -n 1 -lr 0.001 -ttim 10 -n 4 -mf /tmp/ss.model
#
# py examples/eval_model.py -t fromfile -m "parlai_internal.agents.starspace.starspace:StarspaceAgent"  --fromfile_datapath data/simple_test/train2.txt --dict-file /tmp/dict2 -lr 0.001 -mf /tmp/ss.model -d True
#
# OR:
#
# py examples/eval_model.py -t fromfile  --fromfile_datapath data/simple_test/train2.txt  -mf /tmp/ss.model
#
# And... more in anger on a real dataset:
#

# python examples/train_model.py -t opensubtitles -k 10 --dict-file /tmp/os_dict -m "parlai_internal.agents.starspace.starspace:StarspaceAgent" -lr 0.5 -mf /tmp/os_model20 -shareEmb False --embeddingnorm=3 -stim 1000 -n 40
#
# python examples/eval_model.py -t opensubtitles  -mf /tmp/os_model20
#
# python examples/train_model.py -t opensubtitles -k 10 --dict-file parlai_internal/projects/starspace/pc_dict1 -m "parlai_internal.agents.starspace.starspace:StarspaceAgent" -lr 0.5 -mf parlai_internal/projects/starspace/pc_model1 -shareEmb False --embeddingnorm=3 -stim 1000 -n 8
#

from parlai.core.agents import Agent
from parlai.core.dict import DictionaryAgent
from parlai.utils.misc import round_sigfigs, maintain_dialog_history
from parlai.utils.thread import SharedTable

from .modules import Starspace

import torch
from torch.autograd import Variable
import torch.autograd as autograd
from torch import optim
import torch.nn as nn
import time
from collections import deque

import copy
import os
import random
import math
import pickle


def load_cands(self, path):
    """Load global fixed set of candidate labels that the teacher provides
    every example (the true labels for a specific example are also added to
    this set, so that it's possible to get the right answer).
    """
    if path is None:
        return None
    cands = []
    lines_have_ids = False
    cands_are_replies = False
    cnt = 0
    with open(path) as read:
        for line in read:
            line = line.strip().replace('\\n', '\n')
            if len(line) > 0:
                cnt = cnt + 1
                # If lines are numbered we strip them of numbers.
                if cnt == 1 and line[0:2] == '1 ':
                    lines_have_ids = True
                # If tabs then the label_candidates are all the replies.
                if '\t' in line and not cands_are_replies:
                    cands_are_replies = True
                    cands = []
                if lines_have_ids:
                    space_idx = line.find(' ')
                    line = line[space_idx + 1 :]
                    if cands_are_replies:
                        sp = line.split('\t')
                        if len(sp) > 1 and sp[1] != '':
                            cands.append(sp[1])
                    else:
                        cands.append(line)
                else:
                    cands.append(line)
    return cands


class StarspaceAgent(Agent):
    """Simple implementation of the starspace algorithm: https://arxiv.org/abs/1709.03856
    """

    OPTIM_OPTS = {
        'adadelta': optim.Adadelta,
        'adagrad': optim.Adagrad,
        'adam': optim.Adam,
        'adamax': optim.Adamax,
        'asgd': optim.ASGD,
        'lbfgs': optim.LBFGS,
        'rmsprop': optim.RMSprop,
        'rprop': optim.Rprop,
        'sgd': optim.SGD,
    }

    @staticmethod
    def dictionary_class():
        return DictionaryAgent

    @staticmethod
    def add_cmdline_args(argparser):
        """Add command-line arguments specifically for this agent."""
        StarspaceAgent.dictionary_class().add_cmdline_args(argparser)
        agent = argparser.add_argument_group('StarSpace Arguments')
        agent.add_argument(
            '-esz',
            '--embeddingsize',
            type=int,
            default=128,
            help='size of the token embeddings',
        )
        agent.add_argument(
            '-enorm',
            '--embeddingnorm',
            type=float,
            default=10,
            help='max norm of word embeddings',
        )
        agent.add_argument(
            '-shareEmb',
            '--share-embeddings',
            type='bool',
            default=True,
            help='whether LHS and RHS share embeddings',
        )
        agent.add_argument(
            '-lr', '--learningrate', type=float, default=0.005, help='learning rate'
        )
        agent.add_argument(
            '-opt',
            '--optimizer',
            default='sgd',
            choices=StarspaceAgent.OPTIM_OPTS.keys(),
            help='Choose between pytorch optimizers. '
            'Any member of torch.optim is valid and will '
            'be used with default params except learning '
            'rate (as specified by -lr).',
        )
        agent.add_argument(
            '-tr',
            '--truncate',
            type=int,
            default=-1,
            help='truncate input & output lengths to speed up '
            'training (may reduce accuracy). This fixes all '
            'input and output to have a maximum length.',
        )
        agent.add_argument(
            '-k',
            '--neg-samples',
            type=int,
            default=50,
            help='number k of negative samples per example',
        )
        agent.add_argument(
            '-cs',
            '--cache-size',
            type=int,
            default=1000,
            help='size of negative sample cache to draw from',
        )
        agent.add_argument(
            '-hist',
            '--history-length',
            default=100,
            type=int,
            help='Number of past tokens to remember. ',
        )
        agent.add_argument(
            '-histr',
            '--history-replies',
            default='label',
            type=str,
            choices=['none', 'model', 'label'],
            help='Keep replies in the history, or not.',
        )
        agent.add_argument(
            '-fixedCands',
            '--fixed-candidates-file',
            default=None,
            type=str,
            help='File of cands to use for prediction',
        )
        agent.add_argument(
            '-histr',
            '--history-replies',
            default='label_else_model',
            type=str,
            choices=['none', 'model', 'label', 'label_else_model'],
            help='Keep replies in the history',
        )

    def __init__(self, opt, shared=None):
        """Set up model if shared params not set, otherwise no work to do."""
        super().__init__(opt, shared)
        opt = self.opt
        # opt['learningrate'] = 0.5

        self.reset_metrics()
        # all instances needs truncate param
        self.id = 'Starspace'
        self.NULL_IDX = 0
        self.start2 = 99
        # set up tensors once
        self.cands = torch.LongTensor(1, 1, 1)
        self.ys_cache = []
        self.ys_cache_sz = opt['cache_size']
        self.truncate = opt['truncate'] if opt['truncate'] > 0 else None
        self.history = {}
        if shared:
            self.threadindex = shared['threadindex']
            print("[ creating Starspace thread " + str(self.threadindex) + " ]")
            # set up shared properties
            self.dict = shared['dict']
            # answers contains a batch_size list of the last answer produced
            self.answers = shared['answers']
            self.model = shared['model']  # Starspace(opt, len(self.dict))
        else:
            print("[ creating StarspaceAgent ]")
            # this is not a shared instance of this class, so do full init
            # answers contains a batch_size list of the last answer produced
            self.answers = [None] * 1

            if opt['dict_file'] is None and opt.get('model_file'):
                # set default dict-file if not set
                opt['dict_file'] = opt['model_file'] + '.dict'
            # load dictionary and basic tokens & vectors
            self.dict = DictionaryAgent(opt)

            self.model = Starspace(opt, len(self.dict))
            if opt.get('model_file') and os.path.isfile(opt['model_file']):
                self.load(opt['model_file'])
            self.model.share_memory()

        # set up modules
        # self.criterion = nn.CrossEntropyLoss(ignore_index=-100)
        # self.criterion = torch.nn.MultiMarginLoss(p=1, margin=0.1)
        self.criterion = torch.nn.CosineEmbeddingLoss(margin=0.3, size_average=False)
        self.reset()
        # self.dict_neighbors('coffee')

        # self.opt['fixed-candidates-file'] = "/Users/jase/Desktop/data_20170815_valid_candidates.txt"
        self.fixedCands = False
        if self.opt.get('fixed-candidates-file'):
            self.fixedCands = load_cands(self.opt.get('fixed-candidates-file'))

    def override_opt(self, new_opt):
        """Set overridable opts from loaded opt file.

        Print out each added key and each overriden key.
        Only override args specific to the model.
        """
        model_args = {
            'hiddensize',
            'embeddingsize',
            'numlayers',
            'optimizer',
            'encoder',
            'decoder',
            'lookuptable',
            'attention',
            'attention_length',
        }
        for k, v in new_opt.items():
            if k not in model_args:
                # skip non-model args
                continue
            if k not in self.opt:
                print('Adding new option [ {k}: {v} ]'.format(k=k, v=v))
            elif self.opt[k] != v:
                print(
                    'Overriding option [ {k}: {old} => {v}]'.format(
                        k=k, old=self.opt[k], v=v
                    )
                )
            self.opt[k] = v
        return self.opt

    def parse(self, text):
        """Convert string to token indices."""
        return self.dict.txt2vec(text)

    def t2v(self, text):
        p = self.dict.txt2vec(text)
        return Variable(torch.LongTensor(p).unsqueeze(1))

    def v2t(self, vec):
        """Convert token indices to string of tokens."""
        if type(vec) == Variable:
            vec = vec.data
        new_vec = []
        for i in vec:
            new_vec.append(i)
        return self.dict.vec2txt(new_vec)

    def zero_grad(self):
        """Zero out optimizer."""
        self.optimizer.zero_grad()

    def update_params(self):
        """Do one optimization step."""
        self.optimizer.step()

    def reset(self):
        """Reset observation and episode_done."""
        self.observation = None
        self.episode_done = True
        # set up optimizer
        lr = self.opt['learningrate']
        optim_class = StarspaceAgent.OPTIM_OPTS[self.opt['optimizer']]
        kwargs = {'lr': lr}
        #            if opt['optimizer'] == 'sgd':
        #                kwargs['momentum'] = 0.95
        #                kwargs['nesterov'] = True
        self.optimizer = optim_class(self.model.parameters(), **kwargs)

    def share(self):
        """Share internal states between parent and child instances."""
        shared = super().share()
        shared['answers'] = self.answers
        shared['dict'] = self.dict
        shared['model'] = self.model
        return shared

    def observe(self, observation):
        self.episode_done = observation['episode_done']
        # shallow copy observation (deep copy can be expensive)
        obs = observation.copy()
        obs['text2vec'] = maintain_dialog_history(
            self.history,
            obs,
            historyLength=self.opt['history_length'],
            useReplies=self.opt.get('history_replies', 'label_else_model'),
            dict=self.dict,
            useStartEndIndices=False,
        )
        self.observation = obs
        # print(self.v2t(obs['text2vec']))
        # import pdb; pdb.set_trace()
        return obs

    def report(self):
        def clip(f):
            return round_sigfigs(f)
            # return '{:f}'.format(f)

        metrics = self.metrics
        if metrics['exs'] == 0:
            report = {'mean_rank': self.opt['neg_samples']}
        else:
            # import pdb; pdb.set_trace()

            maxn = 0
            for i in range(100):
                index = random.randint(0, self.model.lt.weight.size(0) - 1)
                n = self.model.lt.weight[5].norm(2).data[0]
                if n > maxn:
                    maxn = n

            report = {
                'exs': clip(metrics['total_total']),
                #'thid': self.threadindex if hasattr(self, 'threadindex') else -1,
                #'lr': self.opt['learningrate'],
                'loss': clip(metrics['loss'] / metrics['exs']),
                'mean_rank': clip(metrics['mean_rank'] / metrics['exs']),
                'mlp_time': clip(metrics['mlp_time'] / metrics['exs']),
                'tot_time': clip(metrics['tot_time'] / metrics['exs']),
                'max_norm': clip(n),
                #'mean_weight': clip(metrics['mean_weight'] / metrics['exs'])
            }
        return report

    def reset_metrics(self, keep_total=False):

        if keep_total:
            self.metrics = {
                'exs': 0,
                'mean_rank': 0,
                'loss': 0,
                'total_total': self.metrics['total_total'],
                'mlp_time': 0,
                'tot_time': 0,
                'max_weight': 0,
                'mean_weight': 0,
            }
        else:
            self.metrics = {
                'total_total': 0,
                'mean_rank': 0,
                'exs': 0,
                'mlp_time': 0,
                'tot_time': 0,
                'loss': 0,
                'max_weight': 0,
                'mean_weight': 0,
            }

    def compute_metrics(self, scores, mlp_time, non_mlp_time):
        metrics = {}
        pos = scores[0]
        cnt = 0
        for i in range(1, len(scores)):
            if scores[i] >= pos:
                cnt += 1
        metrics['mean_rank'] = cnt
        metrics['tot_time'] = mlp_time + non_mlp_time
        metrics['mlp_time'] = mlp_time
        return metrics

    def update_metrics(self, scores, mlp_time, non_mlp_time, loss):
        # update metrics
        if scores is not None:
            pos = scores[0]
            cnt = 0
            for i in range(1, len(scores)):
                if scores[i] >= pos:
                    cnt += 1
            self.metrics['mean_rank'] += cnt
        self.metrics['loss'] += loss
        self.metrics['exs'] += 1
        self.metrics['total_total'] += 1

        self.metrics['mlp_time'] += mlp_time
        self.metrics['tot_time'] += mlp_time + non_mlp_time

        self.metrics['max_weight'] += self.model.lt.weight.max().data[0]
        self.metrics['mean_weight'] += self.model.lt.weight.mean().data[0]

        if (
            hasattr(self, 'threadindex')
            and self.threadindex == 0
            and self.metrics['exs'] >= 500
        ):
            print(self.report())
            self.reset_metrics(True)

    def same(self, y1, y2):
        if len(y1.squeeze()) != len(y2.squeeze()):
            return False
        if abs((y1.squeeze() - y2.squeeze()).sum().data.sum()) > 0.00001:
            return False
        return True

    def get_negs(self, xs, ys):
        negs = []
        # for neg in self.ys_cache:
        cache_sz = len(self.ys_cache) - 1
        if cache_sz < 1:
            return negs
        k = self.opt['neg_samples']
        for i in range(1, k * 3):
            index = random.randint(0, cache_sz)
            neg = self.ys_cache[index]
            if not self.same(ys, neg):
                negs.append(neg)
                if len(negs) >= k:
                    break
        return negs

    def dict_neighbors(self, word, useRHS=False):
        input = self.t2v(word)
        W = self.model.encoder.lt.weight
        q = W[input.data[0][0]]
        if useRHS:
            W = self.model.encoder2.lt.weight
        score = torch.Tensor(W.size(0))
        for i in range(W.size(0)):
            score[i] = torch.nn.functional.cosine_similarity(q, W[i], dim=0).data[0]
        val, ind = score.sort(descending=True)
        for i in range(20):
            print(
                str(ind[i])
                + " ["
                + str(val[i])
                + "]: "
                + self.v2t(torch.Tensor([ind[i]]))
            )

    def predict(self, xs, ys=None, cands=None, cands_txt=None, obs=None):
        """Produce a prediction from our model.

        Update the model using the targets if available, otherwise rank
        candidates as well if they are available and param is set.
        """
        self.start = time.time()
        is_training = ys is not None
        if is_training:  #
            text_cand_inds, loss_dict = None, None
            negs = self.get_negs(xs, ys)
            if is_training and len(negs) > 0:  # and self.opt['learningrate'] > 0:
                self.model.train()
                self.zero_grad()
                xe, ye = self.model(xs, ys, negs)
                if False:
                    # print example
                    print("inp: " + self.v2t(xs.squeeze()))
                    print("pos: " + self.v2t(ys.squeeze()))
                    for c in negs:
                        print("neg: " + self.v2t(c.squeeze()))
                    print("---")
                    # import pdb; pdb.set_trace()
                y = Variable(-torch.ones(xe.size(0)))
                y[0] = 1
                loss = self.criterion(xe, ye, y)
                loss.backward()
                self.update_params()
                rest = 0
                if self.start2 != 99:
                    rest = self.start - self.start2
                self.start2 = time.time()
                pred = nn.CosineSimilarity().forward(xe, ye)
                self.update_metrics(
                    pred.data.squeeze(), self.start2 - self.start, rest, loss.data[0]
                )
                # self.update_metrics(None, self.start2-self.start, rest, loss.data[0])
                # metrics = self.compute_metrics(
                #    pred.data.squeeze(), self.start2-self.start, rest)
                # return [{'metrics':metrics}]
        else:
            if cands is None or cands[0] is None:
                # cannot predict without candidates.
                if self.fixedCands:
                    cands = [self.fixedCands]
                else:
                    return [{}]
            # test set prediction uses candidates
            self.model.eval()
            xe, ye = self.model(xs, ys, cands[0])
            pred = nn.CosineSimilarity().forward(xe, ye)
            # val,ind = pred.max(0)
            # val,ind = pred.max(0)
            val, ind = pred.sort(descending=True)
            # predict the highest scoring candidate, and return it.
            ypred = cands_txt[0][ind.data[0]]
            tc = []
            for i in range(min(100, ind.size(0))):
                tc.append(cands_txt[0][ind.data[i]])
            if False:
                print("obsinp:" + obs[0]['text'])
                print("input: " + self.v2t(xs[0]))
                print("label: " + obs[0]['eval_labels'][0])
                print("pred:  " + ypred)
                print("-----------")
                # import pdb; pdb.set_trace()

            # ret = [{'text': cands_txt[ind.data[0]] }]
            # ypred = cands_txt[ind.data[0]]
            # ypred =  self.v2t(cands[0][ind.data[0]])
            # print( self.v2t(xs) + " ->  " + ypred)
            # import pdb; pdb.set_trace()
            ret = [{'text': ypred, 'text_candidates': tc}]
            # cands_txt[ind.data[0]] }]
            return ret
        return [{}]

    def testcheck(self, query, cands, cands_txt):
        xs = Variable(torch.LongTensor(self.parse(query))).unsqueeze(0)
        self.model.eval()
        xe, ye = self.model(xs, None, cands[0])
        pred = nn.CosineSimilarity().forward(xe, ye)
        val, ind = pred.max(0)
        # predict the highest scoring candidate, and return it.
        ypred = cands_txt[0][ind.data[0]]
        print("pred:  " + ypred)
        print("-----------")

    def batchify(self, observations):
        """Convert a list of observations into input & target tensors."""

        def valid(obs):
            # check if this is an example our model should actually process
            return 'text2vec' in obs and len(obs['text2vec']) > 0

        try:
            # valid examples and their indices
            valid_inds, exs = zip(
                *[(i, ex) for i, ex in enumerate(observations) if valid(ex)]
            )
        except ValueError:
            # zero examples to process in this batch, so zip failed to unpack
            return None, None, None, None

        # set up the input tensors
        bsz = len(exs)

        # `x` text is already tokenized and truncated
        # sort by length so we can use pack_padded
        parsed_x = [ex['text2vec'] for ex in exs]
        x_lens = [len(x) for x in parsed_x]
        ind_sorted = sorted(range(len(x_lens)), key=lambda k: -x_lens[k])

        exs = [exs[k] for k in ind_sorted]
        valid_inds = [valid_inds[k] for k in ind_sorted]
        parsed_x = [parsed_x[k] for k in ind_sorted]

        labels_avail = any(['labels' in ex for ex in exs])

        max_x_len = max([len(x) for x in parsed_x])
        for x in parsed_x:
            x += [[self.NULL_IDX]] * (max_x_len - len(x))
        xs = torch.LongTensor(parsed_x)
        xs = Variable(xs)

        # set up the target tensors
        ys = None
        labels = None
        if labels_avail:
            # randomly select one of the labels to update on, if multiple
            labels = [random.choice(ex.get('labels', [''])) for ex in exs]
            # parse each label and append END
            parsed_y = [deque(maxlen=self.truncate) for _ in labels]
            for dq, y in zip(parsed_y, labels):
                dq.extendleft(reversed(self.parse(y)))
            max_y_len = max(len(y) for y in parsed_y)
            for y in parsed_y:
                y += [self.NULL_IDX] * (max_y_len - len(y))
            ys = torch.LongTensor(parsed_y)
            ys = Variable(ys)

        cands = []
        cands_txt = []
        if ys is None:
            # only build candidates in eval mode.
            for o in observations:
                if 'label_candidates' in o:
                    cs = []
                    ct = []
                    for c in o['label_candidates']:
                        cs.append(
                            Variable(torch.LongTensor(self.parse(c)).unsqueeze(0))
                        )
                        ct.append(c)
                    cands.append(cs)
                    cands_txt.append(ct)
                else:
                    cands.append(None)
                    cands_txt.append(None)
        return xs, ys, cands, cands_txt

    def add_to_ys_cache(self, ys):
        if ys is None or len(ys) == 0:
            return
        if len(self.ys_cache) < self.ys_cache_sz:
            self.ys_cache.append(copy.deepcopy(ys))
        else:
            ind = random.randint(0, self.ys_cache_sz - 1)
            self.ys_cache[ind] = copy.deepcopy(ys)

    def batch_act(self, observations):
        batchsize = len(observations)
        # initialize a table of replies with this agent's id
        batch_reply = [{'id': self.getID()} for _ in range(batchsize)]

        # convert the observations into batches of inputs and targets
        # valid_inds tells us the indices of all valid examples
        # e.g. for input [{}, {'text': 'hello'}, {}, {}], valid_inds is [1]
        # since the other three elements had no 'text' field
        xs, ys, cands, cands_txt = self.batchify(observations)
        batch_reply = self.predict(xs, ys, cands, cands_txt, observations)
        self.add_to_ys_cache(ys)
        return batch_reply

    def act(self):
        # call batch_act with this batch of one
        return self.batch_act([self.observation])[0]

    def shutdown(self):
        # """Save the state of the model when shutdown."""
        # path = self.opt.get('model_file', None)
        # if path is not None:
        #    self.save(path + '.shutdown_state')
        super().shutdown()

    def save(self, path=None):
        """Save model parameters if model_file is set."""
        path = self.opt.get('model_file', None) if path is None else path
        if path and hasattr(self, 'model'):
            data = {}
            data['model'] = self.model.state_dict()
            data['optimizer'] = self.optimizer.state_dict()
            data['opt'] = self.opt
            with open(path, 'wb') as handle:
                torch.save(data, handle)
            with open(path + ".opt", 'wb') as handle:
                pickle.dump(self.opt, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, path):
        """Return opt and model states."""
        with open(path, 'rb') as read:
            print('Loading existing model params from ' + path)
            data = torch.load(read)
            self.model.load_state_dict(data['model'])
            self.reset()
            self.optimizer.load_state_dict(data['optimizer'])
            self.opt = self.override_opt(data['opt'])

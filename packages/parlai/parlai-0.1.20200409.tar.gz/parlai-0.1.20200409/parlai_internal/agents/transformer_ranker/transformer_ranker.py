#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from parlai.core.agents import Agent
from parlai.core.build_data import modelzoo_path
from parlai.utils.misc import PaddingUtils, load_cands, round_sigfigs
from .modules import MemNetModel, MemNetPersonaModel, PAD_TOKEN, SOC_TOKEN, \
    EMPTY_PERSONA_TOKEN
from .dict import TransformerDictAgent

import torch
from torch.autograd import Variable
import torch.nn.functional as F

import copy
from collections import deque
import gc
import os.path
import pickle
import random
from tqdm import tqdm


def maintain_dialog_history(history, observation, reply='',
                            historyLength=1, useReplies='label_else_model',
                            dict=None, useStartEndIndices=False,
                            splitSentences=False, useSOCtoken=True,
                            soc_token=SOC_TOKEN):
    """Keeps track of dialog history, up to a truncation length.
    Either includes replies from the labels, model, or not all using param
    'replies'."""

    def parse(txt, splitSentences):
        if dict is not None:
            if splitSentences:
                vec = [dict.txt2vec(t) for t in txt.split('\n')]
            else:
                vec = dict.txt2vec(txt)
            return vec
        else:
            return [txt]

    if 'dialog' not in history:
        history['dialog'] = deque(maxlen=historyLength)
        history['episode_done'] = False
        history['labels'] = []

    if history['episode_done']:
        history['dialog'].clear()
        history['labels'] = []
        useReplies = 'none'
        history['episode_done'] = False

    if useReplies != 'none':
        if useReplies == 'model' or (useReplies == 'label_else_model' and
                                     len(history['labels']) == 0):
            if reply:
                if useStartEndIndices:
                    reply = dict.start_token + ' ' + reply
                history['dialog'].extend(parse(reply, splitSentences))
        elif len(history['labels']) > 0:
            if useStartEndIndices:
                history['labels'] = \
                    [dict.start_token + ' ' + l for l in history['labels']]
            r = history['labels'][0]
            history['dialog'].extend(parse(r, splitSentences))

    obs = observation
    if 'text' in obs:
        if useStartEndIndices:
            obs.force_set('text', dict.end_token + ' ' + obs['text'])
        elif useSOCtoken:
            obs.force_set('text', soc_token + ' ' + obs['text'])
        history['dialog'].extend(parse(obs['text'], splitSentences))

    history['episode_done'] = obs['episode_done']

    labels = obs.get('labels', obs.get('eval_labels', None))
    if labels is not None:
        history['labels'] = labels

    return history['dialog']


def cat_and_pad(tensor_list, padding_value):
    """Concatenate a list of 1D Long Tensor, fills the empty values
    with a padding value.
    """
    max_len = max([len(t) for t in tensor_list])
    response = torch.LongTensor(len(tensor_list), max_len).fill_(padding_value)
    for i, tensor in enumerate(tensor_list):
        response[i, 0:len(tensor)] = tensor
    return response


class TransformerRankerAgent(Agent):
    """Retrieval / ranking agent using a transformer encoder
    """
    @staticmethod
    def dictionary_class():
        return TransformerDictAgent

    @staticmethod
    def add_cmdline_args(argparser):
        """Add command-line arguments specifically for this agent."""
        agent = argparser.add_argument_group('TransformerArguments')
        agent.add_argument('-fixedCands', '--fixed-candidates-file',
                           default=None, type=str,
                           help='File of label_candidates')
        agent.add_argument('-mif', '--init-model', default='', type=str)
        agent.add_argument('--no-cuda', action='store_true', default=False,
                           help='disable GPUs even if available')
        agent.add_argument('--data-parallel', type='bool', default=False,
                           help='use model in data parallel mode')
        agent.add_argument('--rank-at-train', type='bool', default=False,
                           help='rank at train time (else only eval)')
        agent.add_argument('-histr', '--history-replies',
                           default='label_else_model', type=str,
                           choices=['none', 'model', 'label',
                                    'label_else_model'],
                           help='Keep replies in the history, or not.')
        agent.add_argument('--batch-eval', type='bool', default=True,
                           help='in eval mode, use batch as negatives')
        agent.add_argument('--batch-train', type='bool', default=True,
                           help='in batch mode, use batch as negatives')
        agent.add_argument('--interactive-mode', type='bool', default=False,
                           help='for human interaction with bot')
        agent.add_argument('--interactive-unique', type='bool', default=True,
                           help='in interactive mode choose only unique '
                                'responses')
        agent.add_argument('--debug', type='bool', default=False)

        # data format arguments
        agent.add_argument('--truncate', type=int, default=150,
                           help='max history length')
        agent.add_argument('--use-soc-token', type='bool', default=False,
                           help='use SOC token separator')
        agent.add_argument('--max-cand-len', type=int, default=100,
                           help='limit length of candidate sentences')

        # persona and knowledge arguments
        agent.add_argument('--use-personas', type='bool', default=False,
                           help='persona based task')
        agent.add_argument('--max-num-personas', type=int, default=-1,
                           help='maximum number of personas to use')
        agent.add_argument('--max-pers-len', type=int, default=40,
                           help='maximum length of personas')
        agent.add_argument('--maskpersona', type='bool', default=False)
        agent.add_argument('--persona-dropout', type=float, default=0.0,
                           help='dropout on embedding layer')
        agent.add_argument('--persona-encoder', type=str, default='BOW',
                           choices=['BOW', 'transformer'])
        agent.add_argument('--wrap-persona-encoder', type='bool',
                           default=False,
                           help='wrap persona encoder with MLP')
        agent.add_argument('--pers-use-cand-encoder', type='bool',
                           default=False,
                           help='use candidate encoder to encode personas')
        agent.add_argument('--cosine-attention', type='bool', default=False,
                           help='use cosine similarity to attend over memory'
                                'when using a BOW encoder to encode memories')
        agent.add_argument('--basic-attention', type=str, default='cosine',
                           choices=['cosine', 'dot', 'sqrt'],
                           help='similarity for basic attention mechanism'
                                'when using transformer to encode memories')
        agent.add_argument('--use-knowledge', type='bool', default=False,
                           help='use knowledge field instead of personas')
        agent.add_argument('--knowledge-dropout', type=float, default=0.7,
                           help='dropout some knowledge during training')
        agent.add_argument('--total-knowledge-dropout', type=float, default=0.0,
                           help='get rid of knowledge completely sometimes')
        agent.add_argument('--chosen-sentence', type='bool', default=False,
                           help='instead of using all knowledge, use gold'
                                'label, i.e. the chosen sentence')

        # moods arguments
        agent.add_argument('--use-moods', type='bool', default=False)
        agent.add_argument('--moods-dims', type=int, default=216)
        agent.add_argument('--moods-dropout', type=float, default=1)

        # model specific arguments
        agent.add_argument('--alpha', type=float, default=1)
        agent.add_argument('--bow-do-idf', type=int, default=0)
        agent.add_argument('--bow-noscale', type=int, default=0)
        agent.add_argument('--bow-reverse-dan', type=int, default=0)
        agent.add_argument('--bow-scale-sqrt', type='bool', default=False)
        agent.add_argument('--bow-tanh', type=int, default=2)
        agent.add_argument('--concat', type='bool', default=False)
        agent.add_argument('--dict-max-words', type=int, default=250000)
        agent.add_argument('--display-iter', type=int, default=250)
        agent.add_argument('--dumpattention', type='bool', default=True)
        agent.add_argument('--embeddings', type=str, default='fasttext_cc',
                           choices=['fasttext', 'fasttext_cc', 'random',
                                    'glove'])
        agent.add_argument('--embeddings-size', type=int, default=300)
        agent.add_argument('--encoder-type', type=str,
                           choices=['bow', 'lstm', 'transformer'],
                           default='transformer')
        agent.add_argument('--fix-mean', type='bool', default=True)
        agent.add_argument('-clip', '--gradient-clip', type=float, default=0.1,
                           help='gradient clipping using l2 norm')
        agent.add_argument('--gru', type='bool', default=False)
        agent.add_argument('--hidden', type=int, default=256)
        agent.add_argument('--hits-at-nb-cands', type=int, default=100)
        agent.add_argument('--learn-embeddings', type='bool', default=True)
        agent.add_argument('--max-sent-len', type=int, default=100)
        agent.add_argument('--memory-dropout', type=float, default=0)
        agent.add_argument('--n-layers', type=int, default=4)
        agent.add_argument('--normalize-sent-emb', type='bool', default=False)
        agent.add_argument('--optimizer', type=str, choices=['sgd', 'adamax'],
                           default='adamax')
        agent.add_argument('--random-seed', type=int, default=92179)
        agent.add_argument('--rnn-mask-avg', type='bool', default=True)
        agent.add_argument('--share-encoders', type='bool', default=False)
        agent.add_argument('--tau', type='bool', default=False)
        agent.add_argument('--transformer-dim', type=int, default=300)
        agent.add_argument('--transformer-dropout', type=float, default=0)
        agent.add_argument('--transformer-n-heads', type=int, default=6)
        agent.add_argument('--transformer-response-hmul', type=int, default=4)
        agent.add_argument('--two-transformers', type='bool', default=False)
        agent.add_argument('--use-manual-norm', type='bool', default=False)
        agent.add_argument('--validtau', type=float, default=1)
        agent.add_argument('--worker-id', type=int)
        agent.add_argument('-lr', '--learning-rate', type=float,
                           default=0.0001)

        TransformerRankerAgent.dictionary_class().add_cmdline_args(argparser)
        return agent

    def __init__(self, opt, shared=None):
        # initialize defaults first
        super().__init__(opt, shared)

        self.batch_idx = shared and shared.get('batchindex') or 0
        self.history = {}
        self.metrics = {'loss': 0.0,
                        'total': 0,
                        'mean_rank': 0.0,
                        'train_accuracy': 0.0,
                        'eval_total': 0.0,
                        'eval_accuracy': 0.0,
                        'eval_mean_rank': 0.0,
                        'total_skipped_batches': 0}

        # check if we are in interactive mode
        self.interactive_mode = opt.get('interactive_mode')
        if self.interactive_mode:
            self.interactive_unique = opt.get('interactive_unique')
            self.used_responses = []
        # check for cuda
        self.use_cuda = not opt.get('no_cuda') and torch.cuda.is_available()
        if self.use_cuda and self.interactive_mode:
            print("WARNING: we recommend running interactive mode with "
                  "--no-cuda for speed.")
        # check for data parallel
        self.data_parallel = opt.get('data_parallel') and self.use_cuda
        # whether or not to rank at train time
        self.rank_at_train = opt.get('rank_at_train')
        # whether or not to use personas
        self.use_personas = opt.get('use_personas')
        # whether or not to eval in batch mode (alternative is to use fixed
        # label candidates)
        self.batch_eval = opt.get('batch_eval')
        # whether or not to train in batch mode (alternative is to use fixed
        # label candidates)
        self.batch_train = opt.get('batch_train')

        if (self.batch_train and not self.interactive_mode and
            opt.get('batchsize') == 1 and (opt.get('datatype') == 'train' or
                                           self.batch_eval)):
            print('WARNING: Need to train this model with batchsize > 1, '
                  + 'quitting')
            quit()

        if self.use_personas:
            self.max_num_personas = opt.get('max_num_personas')
            self.use_knowledge = opt.get('use_knowledge')

        if opt.get('numthreads', 1) > 1:
            torch.set_num_threads(1)
        torch.manual_seed(opt.get('random_seed'))
        if self.use_cuda:
            torch.cuda.manual_seed(opt.get('random_seed'))

        self.id = 'TransformerRanker'

        if shared:
            self.opt = shared['opt']
            self.dict = shared['dict']
            self.encoder = shared['encoder']
            self.PAD_TOKEN = shared['pad_token']
            self.SOC_TOKEN = shared['soc_token']
            self.PAD_IDX = self.dict[self.PAD_TOKEN]
            self.SOC_IDX = self.dict[self.SOC_TOKEN]
            self.metrics = shared['metrics']
            if not self.interactive_mode:
                self.answers = shared['answers']
                if self.use_personas:
                    self.personas = shared['personas']
                    self.EMPTY_PERSONA_TOKEN = shared['empty_persona_token']
            else:
                self.answers = [None] * opt['batchsize']
                if self.use_personas:
                    self.EMPTY_PERSONA_TOKEN = EMPTY_PERSONA_TOKEN
                    self.personas = [[self.PAD_TOKEN]] * opt['batchsize']

        else:
            # this is not a shared instance of this class, so do full init
            # answers contains a batch_size list of the last answer produced
            self.PAD_TOKEN = PAD_TOKEN
            self.SOC_TOKEN = SOC_TOKEN
            self.answers = [None] * opt['batchsize']
            if self.use_personas:
                self.EMPTY_PERSONA_TOKEN = EMPTY_PERSONA_TOKEN
                self.personas = [[self.PAD_TOKEN]] * opt['batchsize']

            init_model = None
            # check first for 'init_model' for loading model from file
            if opt.get('init_model') and os.path.isfile(opt['init_model']):
                init_model = opt['init_model']
            # next check for 'model_file', this would override init_model
            if opt.get('model_file') and os.path.isfile(opt['model_file']):
                init_model = opt['model_file']

            successfully_loaded = False
            if init_model is not None:
                # check for dictionary
                if (os.path.isfile(init_model + '.dict') or
                        opt['dict_file'] is None):
                    opt['dict_file'] = init_model + '.dict'

            self.dict = TransformerDictAgent(opt)
            self.dict.add_token(self.PAD_TOKEN)
            self.dict.add_token(self.SOC_TOKEN)
            self.SOC_IDX = self.dict[self.SOC_TOKEN]
            self.PAD_IDX = self.dict[self.PAD_TOKEN]

            # set up model
            if init_model is not None:
                # load model parameters if available
                print('[ Loading existing model params from {} ]'.format(
                      init_model))
                successfully_loaded = self.load(init_model)

            if not successfully_loaded:
                # set up model from scratch
                if not self.use_personas:
                    self.encoder = MemNetModel(opt, self.dict)
                else:
                    self.encoder = MemNetPersonaModel(opt, self.dict)

                # set up embeddings
                if opt.get('embeddings') != 'random':
                    self.set_up_embeddings(opt.get('embeddings'))

            if not successfully_loaded or not hasattr(self, 'optimizer'):
                # set up optimizer
                self.set_up_optimizer()

        if self.data_parallel:
            self.encoder = torch.nn.DataParallel(self.encoder)

        if self.use_cuda:
            self.encoder.cuda()

        self.use_fixed_cands = False
        if self.opt.get('fixed_candidates_file'):
            self.build_fixed_cands()
            self.use_fixed_cands = True

        self.reset()

    def build_fixed_cands(self):
        build_text = False
        build_vecs = False
        text_cands_path = self.opt.get('fixed_candidates_file')
        vecs_cands_path = (self.opt.get('model_file') + '.' +
                           os.path.basename(text_cands_path) + '.vecs')
        if not self.opt.get('fixed_candidates_file'):
            build_text = True
        else:
            if os.path.isfile(text_cands_path):
                if not os.path.isfile(vecs_cands_path):
                    build_vecs = True
            else:
                build_text = True
        if build_text:
            print('Need to specify fixed candidates file. Quitting.')
            quit()

        self.fixed_cand_vecs = []
        if build_vecs:
            print('[ loading candidates: ' + text_cands_path + ' ]')
            fixed_cands = load_cands(text_cands_path)
            self.fixedCands_txt = fixed_cands
            parsed_cands = []

            print('[ tokenizing all candidates ]')
            for cand in tqdm(fixed_cands):
                parsed = torch.LongTensor(self.dict.txt2vec(cand))
                parsed_cands.append(parsed)

            encoded_cands = []
            # group the candidates by batch of 512
            batched_cands = [
                parsed_cands[i:i + 512] for i in range(0, len(parsed_cands), 512)
            ]
            # encode by batch. Faster and does not cloak the GPU, if we are
            # using the GPU. Might be faster on CPU too.
            print('[ encoding candidates (%d batches of 512) ]' % len(batched_cands))
            self.encoder.eval()
            for batch in tqdm(batched_cands):
                batch_vec = cat_and_pad(batch, self.PAD_IDX)
                if self.use_cuda:
                    batch_vec = batch_vec.cuda()
                word_mask = batch_vec != self.PAD_IDX
                if not self.data_parallel:
                    encoded_cand = self.encoder.cand_encoder(batch_vec,
                                                             word_mask)
                else:
                    encoded_cand = self.encoder.module.cand_encoder(batch_vec,
                                                                    word_mask)
                for cand_vec in encoded_cand:
                    encoded_cands.append(cand_vec.detach().unsqueeze(0))
            # for saving and using we concatenate into a big matrix since for
            # for whatever reason, deserializing a big tensor seems MUCH faster
            # than deserializing a list of small tensors... in some conditions.
            # just to be sure, save it as a big tensor.
            self.fixedCands_vecs = torch.cat(encoded_cands, 0)

            # dump into a file
            print('[ saving encoded candidates to file: ' + vecs_cands_path + ' ]')
            with open(vecs_cands_path, 'wb') as write:
                torch.save(self.fixedCands_vecs, write)

        else:
            # load vecs from file
            print('[ loading candidates: ' + vecs_cands_path + ' ]')
            self.fixedCands_txt = load_cands(text_cands_path)
            print('[ loading candidate vecs: ' + vecs_cands_path + ' ]')
            self.fixedCands_vecs = torch.load(
                vecs_cands_path,
                map_location=lambda cpu, _: cpu
            )
            # retrocompatibility: if we just unpacked a list of vectors,
            # concatenate.
            if isinstance(self.fixedCands_vecs, list):
                self.fixedCands_vecs = torch.cat(self.fixedCands_vecs, 0)

        if self.use_cuda:
            self.fixedCands_vecs = self.fixedCands_vecs.cuda()

    def init_cuda_buffer(self, batchsize):
        if (self.use_cuda and not hasattr(self, 'buffer_initialized') and not
                self.opt.get('batchsize') == 1):
            try:
                print('preinitializing pytorch cuda buffer')
                bsz = self.opt.get('batchsize', batchsize)
                maxlen = self.opt.get('truncate', 150)
                dummy = torch.ones(bsz, maxlen).long().cuda()
                if self.use_personas:
                    sc, sl = self.encoder(dummy, dummy.unsqueeze(1), dummy)
                else:
                    sc, sl = self.encoder(dummy, dummy)
                dp = sc.mm(sl.t())
                lp = F.log_softmax(dp, dim=1)
                targets = torch.ones(bsz).long().cuda()
                loss = F.nll_loss(lp, targets)
                loss.backward()
                self.buffer_initialized = True
            except RuntimeError as e:
                if 'out of memory' in str(e):
                    m = ('CUDA OOM: Lower batch size (-bs) from {} or lower'
                         'max sequence length from {} (--truncate)'.format(
                             bsz, maxlen)
                         )
                    raise RuntimeError(m)
                else:
                    raise e

    def set_up_optimizer(self):
        # set up optimizer
        if 'train' in self.opt.get('datatype', ''):
            self.clip = self.opt.get('gradient_clip')
            # only set up optimizer if training
            lr = self.opt.get('learning_rate')
            optim_class = self.opt.get('optimizer')
            if optim_class == 'adamax':
                self.optimizer = torch.optim.Adamax(
                    filter(lambda p: p.requires_grad,
                           self.encoder.parameters()),
                    lr=lr)
            else:
                # SGD
                self.optimizer = torch.optim.SGD(
                    filter(lambda p: p.requires_grad,
                           self.encoder.parameters()),
                    lr=lr)

    def set_up_embeddings(self, embedding_type='fasttext_cc'):
        try:
            import torchtext.vocab as vocab
        except ImportError as ex:
            print('Please install torch text with `pip install torchtext`')
            raise ex
        pretrained_dim = 300
        if embedding_type.startswith('glove'):
            if 'twitter' in embedding_type:
                init = 'glove-twitter'
                name = 'twitter.27B'
                pretrained_dim = 200
            else:
                init = 'glove'
                name = '840B'
            embs = vocab.GloVe(
                name=name, dim=pretrained_dim,
                cache=modelzoo_path(self.opt.get('datapath'),
                                    'models:glove_vectors'))
        elif embedding_type.startswith('fasttext'):
            init = 'fasttext'
            if 'cc' in embedding_type:
                embs = vocab.Vectors(
                    name='crawl-300d-2M.vec',
                    url='https://s3-us-west-1.amazonaws.com/fasttext-vectors/crawl-300d-2M.vec.zip',
                    cache=modelzoo_path(self.opt.get('datapath'),
                                        'models:fasttext_cc_vectors'))
            else:
                embs = vocab.FastText(
                    language='en',
                    cache=modelzoo_path(self.opt.get('datapath'),
                                        'models:fasttext_vectors'))
        else:
            raise RuntimeError('embedding type not implemented')

        if self.opt['embeddings_size'] != pretrained_dim:
            rp = torch.Tensor(
                pretrained_dim, self.opt['embeddings_size']).normal_()
            t = lambda x: torch.mm(x.unsqueeze(0), rp)
        else:
            t = lambda x: x
        cnt = 0
        for w, i in self.dict.tok2ind.items():
            if w in embs.stoi:
                vec = t(embs.vectors[embs.stoi[w]])
                self.encoder.embeddings.weight.data[i] = vec = vec
                cnt += 1
        print('Transformer: initialized embeddings for {} tokens from {}.'
              ''.format(cnt, init))

    def reset(self):
        """Reset observation and episode_done."""
        self.observation = None
        self.episode_done = True
        self.history = {}
        for i in range(len(self.answers)):
            self.answers[i] = None
            if self.use_personas:
                self.personas[i] = [self.PAD_TOKEN]

    def share(self):
        """Share internal saved_model between parent and child instances."""
        shared = super().share()
        shared['opt'] = self.opt
        shared['dict'] = self.dict
        shared['encoder'] = self.encoder
        shared['pad_token'] = self.PAD_TOKEN
        shared['soc_token'] = self.SOC_TOKEN
        shared['metrics'] = self.metrics
        if not self.interactive_mode:
            shared['answers'] = self.answers
            if self.use_personas:
                shared['personas'] = self.personas
                shared['empty_persona_token'] = self.EMPTY_PERSONA_TOKEN

        return shared

    def observe(self, observation):
        observation = observation.copy()

        self.episode_done = observation['episode_done']
        self.answers[self.batch_idx] = None

        if 'text' not in observation:
            self.observation = observation
            return observation

        if 'label_candidates' not in observation:
            # Add dummy candidate so that we can support the case where some
            # examples have candidates, some do not.
            observation['label_candidates'] = ["Dummy candidate"]

        # check for empty strings
        if (observation.get('text') == '' or
            (observation.get('labels') and '' in observation['labels']) or
            (observation.get('eval_labels') and '' in
             observation.get('eval_labels'))):
            # return without text so this example is not considered 'valid'
            return {'episode_done': observation['episode_done']}

        # prepare personas or knowledge field
        if self.use_personas:
            personas = []
            not_personas = []

            if self.use_knowledge:
                if (self.opt.get('total_knowledge_dropout', 0) > 0 and
                        random.random() < self.opt['total_knowledge_dropout'] and
                        'labels' in observation):
                    observation['personas'] = [self.PAD_TOKEN]
                    self.personas[self.batch_idx] = [self.PAD_TOKEN]
                else:
                    if ('knowledge' in observation and
                            len(observation['knowledge']) > 1):
                        knowledge = observation['knowledge'].split('\n')[:-1]
                        checked = observation.get('checked_sentence', '')
                        dropout = self.opt.get('knowledge_dropout', 0)
                        if self.opt.get('chosen_sentence'):
                            knowledge = [checked]
                            dropout = 0
                        # do dropout only during training
                        if dropout > 0 and 'labels' in observation:
                            new_knowledge = [checked]
                            for txt in knowledge:
                                if random.random() <= dropout and checked != txt:
                                    new_knowledge.append(txt)
                            knowledge = new_knowledge
                        observation['personas'] = knowledge
                        self.personas[self.batch_idx] = knowledge
                    else:
                        observation['personas'] = self.personas[self.batch_idx]

            else:
                text_split = observation['text'].split('\n')
                for t in text_split:
                    if 'persona:' in t:
                        self.personas[self.batch_idx] = [self.PAD_TOKEN]

                        t = t.replace('your persona: ', '').replace(
                            "partner's persona: ", '').replace('persona: ', '')
                        personas.append(t)
                    else:
                        not_personas.append(t)

                if not personas:
                    observation['personas'] = self.personas[self.batch_idx]
                else:
                    self.personas[self.batch_idx] = personas
                    # get rid of personas in text
                    observation['text'] = '\n'.join(not_personas)
                    observation['personas'] = personas

            if self.max_num_personas > 0:
                observation['personas'] = \
                    observation['personas'][:self.max_num_personas]

        # set up dialog history
        len_hist = self.opt.get('truncate', -1)
        if len_hist < 0:
            len_hist = 10000
        if (not observation.get('preprocessed', False) or 'text2vec' not in
                observation):
            observation['text2vec'] = maintain_dialog_history(
                self.history, observation,
                reply=self.answers[self.batch_idx],
                historyLength=len_hist,
                useReplies=self.opt.get('history_replies'),
                dict=self.dict,
                useStartEndIndices=False,
                useSOCtoken=self.opt.get('use_soc_token'))

        self.observation = observation
        return observation

    def calculate_mean_rank(self, dot_prods):
        above_dot_prods = dot_prods - dot_prods.diag().view(-1, 1)
        rank = (above_dot_prods > 0).float().sum(dim=1).mean().item()
        return rank

    def calculate_loss(self, ctx, labels):
        """Loss calculation for when we are training with other members of
        the batch as negatives.
        """
        assert ctx.size() == labels.size(), \
            f'ctx.size : {ctx.size()}, labels.size: {labels.size()}'
        # both are [batch, dim]

        batch_size = ctx.size(0)
        # [batch, batch]
        dot_products = ctx.mm(labels.t())
        # [batch, batch]
        log_prob = F.log_softmax(dot_products, dim=1)
        # [batch]
        targets = log_prob.new_empty(batch_size).long()
        targets = torch.arange(batch_size, out=targets)
        loss = F.nll_loss(log_prob, targets)

        # calculate accuracy
        nb_ok = (log_prob.max(dim=1)[1] == targets).float().sum().item()
        accuracy = nb_ok / batch_size

        # calculate mean rank
        mean_rank = self.calculate_mean_rank(dot_products)

        return loss, accuracy, mean_rank

    def calculate_loss_label_candidates(self, dot_prods, label_idx):
        """Loss calculation for when we are training with label candidates
        as negatives.
        """
        log_prob = F.log_softmax(dot_prods, dim=1)
        targets = torch.LongTensor([label_idx])
        if self.use_cuda:
            targets = targets.cuda()
        loss = F.nll_loss(log_prob, targets)

        return loss

    def reset_metrics(self):
        """Reset metrics for reporting loss."""
        self.metrics['loss'] = 0.0
        self.metrics['total'] = 0
        self.metrics['train_accuracy'] = 0.0
        self.metrics['mean_rank'] = 0.0
        self.metrics['eval_total'] = 0
        self.metrics['eval_accuracy'] = 0.0
        self.metrics['eval_mean_rank'] = 0.0

    def report(self):
        """Report loss from model's perspective."""
        m = {}
        total = self.metrics['total']
        if total > 0:
            m['total_num'] = total
            m['loss'] = self.metrics['loss'] / total
            m['mean_rank'] = self.metrics['mean_rank'] / total
            m['train_accuracy'] = self.metrics['train_accuracy'] / total
        eval_total = self.metrics['eval_total']
        if eval_total > 0:
            m['eval_mean_rank'] = self.metrics['eval_mean_rank'] / eval_total
            m['eval_accuracy'] = self.metrics['eval_accuracy'] / eval_total
        if self.metrics['total_skipped_batches'] > 0:
            m['total_skipped_batches'] = self.metrics['total_skipped_batches']
        for k, v in m.items():
            # clean up: rounds to sigfigs and converts tensors to floats
            m[k] = round_sigfigs(v, 4)
        return m

    def predict(self, xs, ys=None, is_training=False, label_candidates=None,
                personas=None):
        """Produce a prediction from our model. Returns a list of
        text_cand_inds.

        Update the model using the targets if available.
        """
        text_cand_inds = None

        bsz = xs.size(0)

        if is_training:
            self.encoder.train()
            if self.batch_train:
                try:
                    self.optimizer.zero_grad()
                    if self.use_personas:
                        context_h, labels_h = self.encoder(xs, personas, ys)
                    else:
                        context_h, labels_h = self.encoder(xs, ys)
                    if self.data_parallel:
                        torch.cuda.synchronize()
                    # context_h is [B, h]
                    # labels_h is [B, h]
                    loss, acc, mean_rank = self.calculate_loss(context_h, labels_h)

                    self.metrics['loss'] += loss.item()
                    self.metrics['total'] += 1
                    self.metrics['mean_rank'] += mean_rank
                    self.metrics['train_accuracy'] += acc

                    loss.backward()

                    if self.data_parallel:
                        torch.cuda.synchronize()
                except RuntimeError as e:
                    # catch out of memory exceptions during fwd/bck
                    # (skip batch)
                    if 'out of memory' in str(e):
                        print('| WARNING: ran out of memory, skipping batch. '
                              'if this happens frequently, decrease batchsize '
                              'or truncate the inputs to the model.')
                        self.metrics['total_skipped_batches'] += 1
                        if self.use_cuda:
                            torch.cuda.empty_cache()
                        gc.collect()
                        return text_cand_inds
                    else:
                        raise e

                if self.clip > 0:
                    torch.nn.utils.clip_grad_norm_(self.encoder.parameters(),
                                                   self.clip)
                self.optimizer.step()

                if self.data_parallel:
                    torch.cuda.synchronize()

            if self.rank_at_train or not self.batch_train:
                self.optimizer.zero_grad()
                text_cand_inds = []
                losses = []
                # now rank candidates
                for i in range(bsz):
                    if self.use_personas:
                        context_h, cands_h = self.encoder(
                            xs[i, :].view(1, xs.size(1)),
                            personas[i, :, :].view(1, personas.size(1),
                                                   personas.size(2)),
                            label_candidates[i].unsqueeze(0)
                        )
                    else:
                        context_h, cands_h = self.encoder(
                            xs[i, :].view(1, xs.size(1)),
                            label_candidates[i].unsqueeze(0)
                        )
                    if self.data_parallel:
                        torch.cuda.synchronize()
                    # context_h is [B, h]
                    # cands_h is [B, cands, h]
                    cands_h = cands_h.view(1, -1, context_h.size(-1))

                    # [B, cands]
                    dot_prods_b = cands_h.bmm(
                        context_h.unsqueeze(-1)).squeeze(-1)
                    if not self.batch_train:
                        losses.append(self.calculate_loss_label_candidates(
                            dot_prods_b,
                            self.correct_indices[i]
                        ))
                    _srtd_scores_b, text_cand_inds_b = \
                        dot_prods_b.sort(1, True)

                    text_cand_inds.append(
                        text_cand_inds_b.view(text_cand_inds_b.size(1))
                    )

                if not self.batch_train:
                    total_loss = sum(losses)
                    self.metrics['loss'] += total_loss.item() / bsz
                    self.metrics['total'] += 1
                    total_loss.backward()
                    if self.data_parallel:
                        torch.cuda.synchronize()
                    if self.clip > 0:
                        torch.nn.utils.clip_grad_norm_(self.encoder.parameters(),
                                                       self.clip)
                    self.optimizer.step()
                    if self.data_parallel:
                        torch.cuda.synchronize()

        else:
            # just predict
            self.encoder.eval()
            with torch.no_grad():
                if self.batch_eval:
                    if bsz == 1:
                        return text_cand_inds
                    if self.use_personas:
                        context_h, labels_h = self.encoder(xs, personas, ys)
                    else:
                        context_h, labels_h = self.encoder(xs, ys)
                    if self.data_parallel:
                        torch.cuda.synchronize()
                    loss, acc, mean_rank = self.calculate_loss(context_h, labels_h)
                    self.metrics['eval_total'] += 1
                    self.metrics['eval_accuracy'] += acc
                    self.metrics['eval_mean_rank'] += mean_rank

                else:
                    # now rank candidates
                    if self.use_fixed_cands:
                        # We are not evaluating.
                        # In this condition we only care about the max.
                        # don't use any label candidates for speed
                        if self.use_personas:
                            context_h, cands_h = self.encoder(xs, personas, None)
                        else:
                            context_h, cands_h = self.encoder(xs, None)
                        dot_prod = self.fixedCands_vecs.mm(context_h.t()).squeeze(-1)
                        # return top 20 candidates here (in case of repeats)
                        _, index_max = torch.topk(dot_prod, 20, dim=0)
                        text_cand_inds = index_max.tolist()
                    else:
                        text_cand_inds = []
                        for i in range(bsz):
                            if self.use_personas:
                                context_h, cands_h = self.encoder(
                                    xs[i, :].view(1, xs.size(1)),
                                    personas[i, :, :].view(1, personas.size(1),
                                                           personas.size(2)),
                                    label_candidates[i].unsqueeze(0),
                                )
                            else:
                                context_h, cands_h = self.encoder(
                                    xs[i, :].view(1, xs.size(1)),
                                    label_candidates[i].unsqueeze(0)
                                )
                            if self.data_parallel:
                                torch.cuda.synchronize()
                            # context_h is [B, h]
                            # cands_h is [B, cands, h]
                            cands_h = cands_h.view(1, -1, context_h.size(-1))

                            # [B, cands]
                            dot_prods_b = cands_h.bmm(
                                context_h.unsqueeze(-1)).squeeze(-1)
                            _srtd_scores_b, text_cand_inds_b = \
                                dot_prods_b.sort(1, True)

                            text_cand_inds.append(
                                text_cand_inds_b.view(text_cand_inds_b.size(1))
                            )

        return text_cand_inds

    def vectorize(self, observations):
        """Convert a list of observations into input & target tensors."""
        is_training = (any(('labels' in obs for obs in observations)) and not
                       self.interactive_mode)
        # utility function for padding text and returning lists of indices
        # parsed using the provided dictionary
        xs, ys, labels, valid_inds, _, _ = PaddingUtils.pad_text(
            observations, self.dict, end_idx=None,
            null_idx=self.PAD_IDX, dq=True, eval_labels=True)

        if xs is None:
            return None, None, None, None, None, None, None, None

        xs = torch.LongTensor(xs)
        if self.use_cuda:
            xs = xs.cuda()
        xs = Variable(xs)

        if ys is not None:
            ys = torch.LongTensor(ys)
            if self.use_cuda:
                ys = ys.cuda()
            ys = Variable(ys)

        # set up personas
        if self.use_personas:
            pers = []
            valid_pers = []
            max_len = 0
            max_num = 0
            for i, v in enumerate(valid_inds):
                if 'personas' in observations[v]:
                    curr_pers_list = list(observations[v]['personas'])
                    curr_pers = [{'text': p} for p in curr_pers_list]
                    ps, _, _, valid_p_inds, *_ = PaddingUtils.pad_text(
                        curr_pers,
                        self.dict,
                        null_idx=self.PAD_IDX,
                        dq=True,
                        truncate=self.opt.get('max_pers_len')
                    )
                    if len(valid_p_inds) > max_num:
                        max_num = len(valid_p_inds)
                    if len(ps) > 0 and len(ps[0]) > max_len:
                        max_len = len(ps[0])
                    valid_pers.append(
                        (i, v, [curr_pers_list[j] for j in valid_p_inds])
                    )
                    pers.append(ps)
            new_pers = []
            for p_list in pers:
                new_p_list = [p if len(p) == max_len else
                              p + deque((self.PAD_IDX,)) * (max_len - len(p))
                              for p in p_list]
                if len(new_p_list) < max_num:
                    for _ in range(max_num - len(new_p_list)):
                        new_p_list.append(
                            deque([self.PAD_IDX for i in range(max_len)])
                        )
                new_pers.append(new_p_list)
            pers = new_pers
            pers = torch.LongTensor(pers)
            if self.use_cuda:
                pers = pers.cuda()
        else:
            pers = None

        valid_cand_inds = None
        if ((not is_training and not self.batch_eval) or self.rank_at_train or
                not self.batch_train):
            if self.use_fixed_cands:
                # No need to do anything with the candidates
                cands = None
            else:
                cands = []
                valid_cands = []
                valid_cand_inds = []
                self.correct_indices = []
                for i, v in enumerate(valid_inds):
                    if 'label_candidates' in observations[v]:
                        curr_lcs = list(observations[v]['label_candidates'])
                        curr_cands = [{'text': c} for c in curr_lcs]
                        cs, _, _, valid_c_inds, *_ = PaddingUtils.pad_text(
                            curr_cands,
                            self.dict,
                            null_idx=self.PAD_IDX,
                            dq=False,
                            truncate=self.opt.get('max_cand_len')
                        )
                        if (not self.batch_train and 'labels' in
                                observations[v]):
                            # get index of correct label for loss calculation
                            correct_idx = 0
                            for k in range(len(curr_lcs)):
                                if curr_lcs[k] == observations[v]['labels'][0]:
                                    correct_idx = k
                                    break
                            self.correct_indices.append(
                                valid_c_inds.index(correct_idx)
                            )
                        valid_cand_inds.append(valid_c_inds)
                        valid_cands.append(
                            (i, v, [curr_lcs[j] for j in valid_c_inds])
                        )
                        cs = torch.LongTensor(cs)
                        if self.use_cuda:
                            cs = cs.cuda()
                        cands.append(cs)
        else:
            cands = None

        return xs, ys, labels, valid_inds, is_training, cands, pers, valid_cand_inds

    def batch_act(self, observations):
        batchsize = len(observations)
        self.init_cuda_buffer(batchsize)
        # initialize a table of replies with this agent's id
        batch_reply = [{'id': self.getID()} for _ in range(batchsize)]

        # convert the observations into batches of inputs and targets
        # `labels` stores the true labels returned in the `ys` vector
        # `valid_inds` tells us the indices of all valid examples
        # e.g. for input [{}, {'text': 'hello'}, {}, {}], valid_inds is [1]
        # since the other three elements had no 'text' field
        xs, ys, labels, valid_inds, is_training, label_candidates, personas, valid_cand_inds = self.vectorize(observations)

        if xs is None:
            # no valid examples, just return empty responses
            return batch_reply

        text_cand_inds = \
            self.predict(xs, ys, is_training, label_candidates, personas)

        if text_cand_inds:
            if self.use_fixed_cands:
                response_idx = text_cand_inds[0]
                if self.interactive_mode:
                    if self.interactive_unique:
                        # get highest ranking index that hasn't already been
                        # used as a response before
                        for ind in text_cand_inds:
                            txt = self.fixedCands_txt[ind]
                            if txt not in self.used_responses:
                                response_idx = ind
                                self.used_responses.append(txt)
                                break
                    self.history['labels'] = [self.fixedCands_txt[response_idx]]
                batch_reply[0]['text'] = self.fixedCands_txt[
                    response_idx
                ]
                batch_reply[0]['text_candidates'] = [
                    self.fixedCands_txt[idx] for idx in text_cand_inds[:20]
                ]

            else:
                for i in range(len(valid_inds)):
                    idx = valid_inds[i]
                    order = text_cand_inds[i]
                    valid_c_inds = valid_cand_inds[i]
                    curr_cands = observations[idx]['label_candidates']
                    curr = batch_reply[idx]
                    curr['text_candidates'] = [curr_cands[valid_c_inds[j]] for j
                                               in order[:100]]
                    curr['text'] = curr['text_candidates'][0]
                    if len(curr_cands) == 1:
                        # remove dummy candidate
                        curr.pop('text_candidates')

        self.answers = [[curr.get('text')] for curr in batch_reply]
        if self.episode_done:
            self.used_responses = []
        return batch_reply

    def act(self):
        # call batch_act with this batch of one
        return self.batch_act([self.observation])[0]

    def save(self, path=None):
        """Save model parameters if model_file is set."""
        path = self.opt.get('model_file', None) if path is None else path

        if path and hasattr(self, 'encoder'):
            model = {}
            model['state_dict'] = self.encoder.state_dict()
            model['optimizer'] = self.optimizer.state_dict()
            model['optimizer_type'] = self.opt['optimizer']
            model['opt'] = self.opt

            with open(path, 'wb') as write:
                torch.save(model, write)

            # save opt file
            with open(path + ".opt", 'wb') as handle:
                pickle.dump(self.opt, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, path):
        saved_model = torch.load(path, map_location=lambda cpu, _: cpu)
        if saved_model.get('state_dict'):
            saved_options = saved_model['opt']
            loading_opts = self.opt

            # deal with some legacy models where options were not dict
            # but namespaces
            if not isinstance(saved_options, dict):
                saved_options = vars(saved_options)
                saved_options['use_personas'] = True
                loading_opts = saved_options
                if self.opt["no_cuda"]:
                    loading_opts["no_cuda"] = True

            # code to deal with some old models to make sure state is loaded
            # properly
            if (saved_options.get('persona_encoder') !=
                    self.opt.get('persona_encoder') and not
                    self.opt.get('load_all_encoders')):
                self.opt['load_all_encoders'] = True
            elif self.opt.get('load_all_encoders') is None:
                self.opt['load_all_encoders'] = False

            if not loading_opts.get('use_personas'):
                self.encoder = MemNetModel(loading_opts,
                                           self.dict.tok2ind)
            else:
                self.encoder = MemNetPersonaModel(loading_opts,
                                                  self.dict.tok2ind)

            if saved_options.get('data_parallel', False):
                # create new OrderedDict that does not contain `module.`
                from collections import OrderedDict
                new_state_dict = OrderedDict()
                for k, v in saved_model['state_dict'].items():
                    name = k[7:]  # remove `module.`
                    new_state_dict[name] = v
            else:
                new_state_dict = saved_model['state_dict']

            # load params
            current_state = self.encoder.state_dict()
            # filter out unnecessary params
            pre_trained_state = {k: v for k, v in
                                 new_state_dict.items() if k in
                                 current_state}
            # upload pretrained state
            current_state.update(pre_trained_state)
            self.encoder.load_state_dict(current_state)

        else:
            return False

        if (saved_model.get('optimizer') and 'train' in
                self.opt.get('datatype', '')):
            # set up optimizer
            if saved_model['optimizer_type'] != self.opt['optimizer']:
                print('WARNING: not loading optim state since optim class '
                      'changed.')
            else:
                try:
                    self.set_up_optimizer()
                    self.optimizer.load_state_dict(saved_model['optimizer'])
                except ValueError:
                    print('WARNING: not loading optim state since model '
                          'params changed.')
                if self.use_cuda:
                    for state in self.optimizer.state.values():
                        for k, v in state.items():
                            if isinstance(v, torch.Tensor):
                                state[k] = v.cuda()
        return True

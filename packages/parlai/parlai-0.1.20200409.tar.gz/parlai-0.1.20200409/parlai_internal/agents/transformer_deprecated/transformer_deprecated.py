#!/usr/bin/env python3
from parlai.core.agents import Agent
from parlai.core.params import ParlaiParser
from parlai.core.dict import DictionaryAgent
from parlai.utils.misc import PaddingUtils, load_cands
from .modules import MemNetModel, UNK_TOKEN, PAD_TOKEN, SOC_TOKEN
from .rankers import SimpleRanker, NormalizedRanker, OneHopRanker, OneHopNormalizedRanker, ShortestRanker

import torch
from torch.autograd import Variable

import argparse
import os
import os.path as osp
import logging
import pickle


USER = os.getenv('USER')
PERSONACHAT = os.getenv('PERSONACHAT')
REDDIT = '/datasets01/reddit_binary_chunks/101217/'
MOODS = '/private/home/samuelhumeau/reddit_computed_personas'
FASTTEXT = '/private/home/raison/embeddings/fast_text/crawl-300d-2M.txt'
MODEL_DIR = '/checkpoint/' + USER + '/persona_dialog/run1'
PERSONAS = '/private/home/pem/data/conflated_personas_short.txt'
RANKERCLASS = {
    'simple': SimpleRanker,
    'simple_normalized': NormalizedRanker,
    'onehop': OneHopRanker,
    'onehop_normalized': OneHopNormalizedRanker,
    'shortest': ShortestRanker
}


def get_opt(empty=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--all-persona-lines', action='store_true')
    parser.add_argument('--alpha', type=float, default=1)
    parser.add_argument('--batch-size', type=int, default=32)
    parser.add_argument('--bow-do-idf', type=int, default=0)
    parser.add_argument('--bow-noscale', type=int, default=0)
    parser.add_argument('--bow-reverse-dan', type=int, default=0)
    parser.add_argument('--bow-scale-sqrt', action='store_true')
    parser.add_argument('--bow-tanh', type=int, default=2)
    parser.add_argument('--concat', action='store_true')
    parser.add_argument('--cuda', action='store_true')
    parser.add_argument('--dataset-name', type=str, default="reddit", choices=['reddit', 'personachat', 'opensubtitles'])
    parser.add_argument('--dict-max-words', type=int, default=250000)
    parser.add_argument('--display-iter', type=int, default=250)
    parser.add_argument('--dumpattention', action='store_true')
    parser.add_argument('--embeddings', type=str, default=FASTTEXT)
    parser.add_argument('--embeddings-size', type=int, default=300)
    parser.add_argument('--emptypersona', action='store_true')
    parser.add_argument('--encoder-type', type=str, choices=['bow', 'lstm', 'transformer'], default='transformer')
    parser.add_argument('--fast-debug', action='store_true')
    parser.add_argument('--fix-deleted', action='store_true', default=True)
    parser.add_argument('--fix-mean', action='store_true', default=True)
    parser.add_argument('--gru', action='store_true')
    parser.add_argument('--hidden', type=int, default=256)
    parser.add_argument('--hits-at-nb-cands', type=int, default=100)
    parser.add_argument('--learn-embeddings', action='store_true')
    parser.add_argument('--learning-rate', type=float, default=None)
    parser.add_argument('--load-checkpoint', type=str)
    parser.add_argument('--log-file', type=str)
    parser.add_argument('--lowercase-personas', action='store_true')
    parser.add_argument('--maskpersona', action='store_true')
    parser.add_argument('--max-hist-len', type=int, default=1)
    parser.add_argument('--max-personas', type=int, default=20)
    parser.add_argument('--max-sent-len', type=int, default=100)
    parser.add_argument('--memory-dropout', type=float, default=0)
    parser.add_argument('--memory-sigmoid', action='store_true')
    parser.add_argument('--model', type=str, choices=['memnet', 'transformer'], default='memnet')
    parser.add_argument('--model-dir', type=str, default=MODEL_DIR)
    parser.add_argument('--model-name', type=str)
    parser.add_argument('--moods-dims', type=int, default=216)
    parser.add_argument('--moods-dir', type=str, default=MOODS)
    parser.add_argument('--moods-dropout', type=float, default=1)
    parser.add_argument('--n-layers', type=int, default=6)
    parser.add_argument('--no-personas', action='store_true')
    parser.add_argument('--no-shuffle', action='store_true')
    parser.add_argument('--normalize-bow', action='store_true')
    parser.add_argument('--normalize-emb', action='store_true')
    parser.add_argument('--normalize-sent-emb', action='store_true')
    parser.add_argument('--num-epochs', type=int, default=1000)
    parser.add_argument('--opensub-path', type=str)
    parser.add_argument('--optimizer', type=str, choices=['sgd', 'adamax'], default='adamax')
    parser.add_argument('--personachat', type=str, default=PERSONACHAT)
    parser.add_argument('--personas', type=str, default=PERSONAS)
    parser.add_argument('--pretrained', type=str)
    parser.add_argument('--random-seed', type=int, default=92179)
    parser.add_argument('--reddit', type=str, default=REDDIT)
    parser.add_argument('--rm-long-contexts', action='store_true')
    parser.add_argument('--rm-long-sent', action='store_true')
    parser.add_argument('--rnn-mask-avg', action='store_true')
    parser.add_argument('--share-encoders', action='store_true')
    parser.add_argument('--tau', action='store_true')
    parser.add_argument('--testing', action='store_true')
    parser.add_argument('--temp-saves', action='store_true')
    parser.add_argument('--transformer-dim', type=int, default=512)
    parser.add_argument('--transformer-dropout', type=float, default=0)
    parser.add_argument('--transformer-n-heads', type=int, default=8)
    parser.add_argument('--transformer-response-hmul', type=int, default=1)
    parser.add_argument('--two-transformers', action='store_true')
    parser.add_argument('--use-manual-norm', action='store_true')
    parser.add_argument('--use-moods', action='store_true')
    parser.add_argument('--use-negs', action='store_true')
    parser.add_argument('--validtau', type=float, default=1)
    parser.add_argument('--worker-id', type=int)
    opt = parser.parse_args() if not empty else parser.parse_args([])
    set_defaults(opt)
    return opt


def set_defaults(opt):
    # Set model directory
    os.makedirs(opt.model_dir, exist_ok=True)

    # Set model name
    if not opt.model_name:
        import uuid
        import time
        opt.model_name = time.strftime("%Y%m%d-") + str(uuid.uuid4())[:8]

    # Set log + model file names
    if opt.log_file is None:
        opt.log_file = os.path.join(opt.model_dir, opt.model_name + '.txt')
    opt.model_file = os.path.join(opt.model_dir, opt.model_name + '.mdl')


def sens2tensor(sens, w2i, padix, unkix, pad=None):
    pad = pad or max(len(sen.split()) for sen in sens)
    out = torch.LongTensor(len(sens), pad).fill_(padix)
    for i, sen in enumerate(sens):
        out[i, :len(sen.split())] = torch.LongTensor([
            w2i.get(w, unkix) for w in sen.split()])

    return out


class TransformerAgent(Agent):
    """
    Retrieval / ranking agent using a transformer encoder
    """

    @staticmethod
    def add_cmdline_args(argparser):
        """Add command-line arguments specifically for this agent."""
        agent = argparser.add_argument_group('Transformer Arguments')
        agent.add_argument(
            '--fixed-candidates-enc', default='', type=str,
            help='File of encoded label_candidates')
        agent.add_argument(
            '--fixed-candidates', default='', type=str,
            help='basename for readable label_candidates')
        agent.add_argument(
            '--build-candidates-txt', default='', type=str,
            help='textual candidates, will build the encoded version'
            )
        agent.add_argument('--nb-cands', type=int, default=1000000)
        agent.add_argument('--normalize', action='store_true')
        agent.add_argument('--no-cuda', action='store_true', default=False,
                           help='disable GPUs even if available')
        agent.add_argument('--type-transformer-model', default="memnet",
                           help='either memnet or transformer.')
        agent.add_argument('--ranker', default='simple')

        # TODO add arguments here
        DictionaryAgent.add_cmdline_args(argparser)
        return agent

    def __init__(self, opt, shared=None):
        # initialize defaults first
        super().__init__(opt, shared)

        # check for cuda
        self.use_cuda = not opt.get('no_cuda') and torch.cuda.is_available()
        if opt.get('numthreads', 1) > 1:
            torch.set_num_threads(1)
        self.id = 'Transformer'

        if shared:
            self.idx_candidates_ctx = shared['idx_candidates_ctx']
            self.idx_candidates_ans = shared['idx_candidates_ans']
            self.enc_candidates_ctx = shared['enc_candidates_ctx']
            self.enc_candidates_ans = shared['enc_candidates_ans']
            self.txt_candidates_ctx = shared['txt_candidates_ctx']
            self.txt_candidates_ans = shared['txt_candidates_ans']
            self.fixedCands_txt = shared['fixedCands_txt']
            self.fixedCands_vecs = shared['fixedCands_vecs']

            self.encoder = shared['encoder']
            if self.use_cuda:
                self.encoder = self.encoder.cuda()

            self.dict = shared['dict']
            self.opt = shared['opt']
            self.pad_idx = self.dict.tok2ind[PAD_TOKEN]
            self.unk_idx = self.dict.tok2ind[UNK_TOKEN]

        else:

            if opt.get('model_file') and osp.isfile('%s.mdl' % opt['model_file']):
                opt_superset = self.load('%s.mdl' % opt['model_file'])
            elif opt.get('model_file') and osp.isfile(opt['model_file']):
                opt_superset = self.load(opt['model_file'])

            ''' make sure the args added in `add_cmdline_args` are in '''
            opt_superset.__dict__.update(self.opt)
            self.opt = dict(vars(opt_superset))

            if self.opt['fixed_candidates'] != '':
                print('Loading candidates')

                basepath = self.opt['fixed_candidates']

                load = torch.load('%s.idx' % basepath, map_location='cpu')
                self.txt_candidates_ctx = load_cands('%s.candspair' % basepath)
                self.txt_candidates_ans = load_cands('%s.candspair2' % basepath)
                self.idx_candidates_ctx = load['contexts'].cpu()
                self.idx_candidates_ans = load['answers'].cpu()

                load = torch.load(self.opt['fixed_candidates_enc'], map_location='cpu')
                self.enc_candidates_ctx = load['contexts_enc'].cpu()
                self.enc_candidates_ans = load['answers_enc'].cpu()

                self.fixedCands_txt = self.txt_candidates_ans
                self.fixedCands_vecs = self.enc_candidates_ans

                if self.use_cuda:
                    self.idx_candidates_ctx = self.idx_candidates_ctx.cuda()
                    self.idx_candidates_ans = self.idx_candidates_ans.cuda()
                    self.enc_candidates_ctx = self.enc_candidates_ctx.cuda()
                    self.enc_candidates_ans = self.enc_candidates_ans.cuda()

            if self.opt['build_candidates_txt'] != '':
                print('Building candidates')
                basepath = self.opt['build_candidates_txt']

                txt_candidates_ctx = load_cands(f'{basepath}.candspair')
                txt_candidates_ans = load_cands(f'{basepath}.candspair2')
                idx_candidates_ctx = sens2tensor(
                    txt_candidates_ctx, self.dict.tok2ind,
                    self.pad_idx, self.unk_idx,
                    pad=self.idx_candidates_ctx.size(1) if self.opt['fixed_candidates'] != '' else None)
                idx_candidates_ans = sens2tensor(
                    txt_candidates_ans, self.dict.tok2ind,
                    self.pad_idx, self.unk_idx,
                    pad=self.idx_candidates_ctx.size(1) if self.opt['fixed_candidates'] != '' else None)

                if self.use_cuda:
                    idx_candidates_ctx = idx_candidates_ctx.cuda()
                    idx_candidates_ans = idx_candidates_ans.cuda()

                enc_cs, enc_as = [], []
                with torch.no_grad():
                    batcher = zip(
                        idx_candidates_ctx.split(512, dim=0),
                        idx_candidates_ans.split(512, dim=0))
                    for idx_cs, idx_as in batcher:
                        enc_c, enc_a = self.encoder(idx_cs, None, idx_as)
                        enc_cs.append(enc_c)
                        enc_as.append(enc_a)
                enc_candidates_ctx = torch.cat(enc_cs, dim=0)
                enc_candidates_ans = torch.cat(enc_as, dim=0)

                if self.opt['fixed_candidates'] != '':  # additive cands
                    self.txt_candidates_ctx.extend(txt_candidates_ctx)
                    self.txt_candidates_ans.extend(txt_candidates_ans)
                    self.idx_candidates_ctx = torch.cat((self.idx_candidates_ctx, idx_candidates_ctx), dim=0)
                    self.idx_candidates_ans = torch.cat((self.idx_candidates_ans, idx_candidates_ans), dim=0)
                    self.enc_candidates_ctx = torch.cat((self.enc_candidates_ctx, enc_candidates_ctx), dim=0)
                    self.enc_candidates_ans = torch.cat((self.enc_candidates_ans, enc_candidates_ans), dim=0)
                else:
                    self.txt_candidates_ctx = txt_candidates_ctx
                    self.txt_candidates_ans = txt_candidates_ans
                    self.idx_candidates_ctx = idx_candidates_ctx
                    self.idx_candidates_ans = idx_candidates_ans
                    self.enc_candidates_ctx = enc_candidates_ctx
                    self.enc_candidates_ans = enc_candidates_ans

                self.fixedCands_txt = self.txt_candidates_ans
                self.fixedCands_vecs = self.enc_candidates_ans

        ranker_class = RANKERCLASS[self.opt['ranker']]
        self.ranker = ranker_class(
            10,
            self.enc_candidates_ans, self.idx_candidates_ans,
            self.enc_candidates_ctx, self.idx_candidates_ctx,
            padix=self.pad_idx
        )
        self.reset()

    def reset(self):
        """Reset observation and episode_done."""
        self.observation = None
        self.episode_done = True
        self.history = []
        self.answers = None

    def share(self):
        """Share internal states between parent and child instances."""
        shared = super().share()
        shared['opt'] = self.opt
        shared['dict'] = self.dict
        shared['encoder'] = self.encoder

        if self.opt.get('numthreads', 1) > 1:
            # we're doing hogwild so share the model too
            shared['encoder'] = self.encoder

        if hasattr(self, 'enc_candidates_ctx'):
            shared['idx_candidates_ctx'] = self.idx_candidates_ctx
            shared['idx_candidates_ans'] = self.idx_candidates_ans
            shared['enc_candidates_ctx'] = self.enc_candidates_ctx
            shared['enc_candidates_ans'] = self.enc_candidates_ans
            shared['txt_candidates_ctx'] = self.txt_candidates_ctx
            shared['txt_candidates_ans'] = self.txt_candidates_ans
            shared['fixedCands_txt'] = self.fixedCands_txt
            shared['fixedCands_vecs'] = self.fixedCands_vecs

        return shared

    def observe(self, observation):
        observation = observation.copy()
        if len(observation) == 1 and 'episode_done' in observation:
            # this is the case where observation = {'episode_done': True}
            self.observation = observation
            self.episode_done = observation['episode_done']
            self.history = []
            self.answers = None
            return observation
        else:
            if self.episode_done:
                self.persona_given = []
                self.persona_txt = []
                self.history = []
                self.answers = None
            text_split = observation['text'].split('\n')
            persona = []
            if self.answers:
                self.history.extend(self.answers)
                self.answers = None
            for t in text_split:
                if 'persona:' in t:
                    t = t.replace('your persona: ', '').replace('their persona: ', '')
                    persona.append(self.dict.parse(t))
                    self.persona_txt.append(t)
                else:
                    self.history.append(t)
            if len(self.persona_txt) == 0:
                t = torch.LongTensor([[self.pad_idx]])
                persona.append(t)

            n_hist = getattr(self.encoder.opt, 'max_hist_len', 1)
            self.history = self.history[-n_hist:]
            if n_hist == 1:
                observation['text'] = text_split[-1]
            else:
                padded_token = ' ' + SOC_TOKEN + ' '
                observation['text'] = padded_token + padded_token.join(self.history)
                # print(observation['text'])

            persona_tensor = torch.LongTensor(1, len(persona), max(len(p) for p in persona)).fill_(self.pad_idx)
            for i, p in enumerate(persona):
                persona_tensor[0, i, :len(p)] = torch.LongTensor(p)
            if self.use_cuda:
                persona_tensor = persona_tensor.cuda()
            self.persona_given = persona_tensor
            self.episode_done = observation['episode_done']
            self.observation = observation
            return observation

    def predict(self, xs, ys=None, is_training=False, label_candidates=None):
        """Produce a prediction from our model.

        Update the model using the targets if available.
        """
        if is_training:
            raise NotImplementedError()

        bsz = xs.size(0)
        self.encoder.eval()

        if hasattr(self, 'fixedCands_vecs'):
            # don't use any label candidates for speed
            context_h, _ = self.encoder(xs, self.persona_given, None)
            # then replace with fixed, precomputed cands
            # context_h = context_h.cpu()
            cands_h = self.fixedCands_vecs  # [ncabds, dim]
        else:
            _bsz, n_cands, cand_length = label_candidates.size()
            label_candidates = label_candidates.view(bsz * n_cands, cand_length)
            context_h, cands_h = self.encoder(xs, self.persona_given, label_candidates)
            # context_h is [B, h]
            # cands_h is [B, cands, h]
            cands_h = cands_h.view(bsz, n_cands, context_h.size(-1))

        text_cand_inds = self.ranker(context_h)
        # if self.opt['normalize']:
        #     cands_h /= cands_h.norm(2, dim=1, keepdim=True)
        #     context_h /= context_h.norm(2, dim=1, keepdim=True)

        # dot_prods = context_h.mm(cands_h.t())  # [B, cands]
        # _srtd_scores, text_cand_inds = dot_prods.sort(1, True)

        if label_candidates is not None:
            predictions = label_candidates[text_cand_inds[:, 0]]
        else:
            predictions = None

        return predictions, text_cand_inds

    def vectorize(self, observations):
        """Convert a list of observations into input & target tensors."""
        is_training = any(('labels' in obs for obs in observations))
        # utility function for padding text and returning lists of indices
        # parsed using the provided dictionary
        xs, ys, labels, valid_inds, _, _ = PaddingUtils.pad_text(
            observations, self.dict, end_idx=None,
            null_idx=self.pad_idx, dq=False, eval_labels=True)

        if xs is None:
            return None, None, None, None, None

        # move lists of indices returned above into tensors
        xs = torch.LongTensor(xs)
        if self.use_cuda:
            xs = xs.cuda()
        xs = Variable(xs)

        if ys is not None:
            ys = torch.LongTensor(ys)
            if self.use_cuda:
                ys = ys.cuda()
            ys = Variable(ys)

        if hasattr(self, 'fixedCands_txt'):
            # TODO: This could be sped up.
            for o in observations:
                o['label_candidates'] = self.fixedCands_txt

        if hasattr(self, 'fixedCands_vecs'):
            cands = None  # No need to do anything with the candidates for the current example
        else:
            label_candidates = [[self.dict.parse(t) for t in o['label_candidates']] for o in observations]
            max_cand_length = max(len(c) for example_candidates in label_candidates for c in example_candidates)
            max_n_cands = max(len(example_candidates) for example_candidates in label_candidates)
            cands = torch.LongTensor(len(observations), max_n_cands, max_cand_length).fill_(self.pad_idx)
            for i, example_candidates in enumerate(label_candidates):
                for j, c in enumerate(example_candidates):
                    cands[i, j, :len(c)] = torch.LongTensor(c)
            if self.use_cuda:
                cands = cands.cuda()

        return xs, ys, labels, valid_inds, is_training, cands

    def batch_act(self, observations):
        batchsize = len(observations)
        # initialize a table of replies with this agent's id
        batch_reply = [{'id': self.getID()} for _ in range(batchsize)]

        # convert the observations into batches of inputs and targets
        # `labels` stores the true labels returned in the `ys` vector
        # `valid_inds` tells us the indices of all valid examples
        # e.g. for input [{}, {'text': 'hello'}, {}, {}], valid_inds is [1]
        # since the other three elements had no 'text' field
        xs, ys, labels, valid_inds, is_training, label_candidates = self.vectorize(observations)

        # persona_txt = "\n".join(self.persona_txt)
        # print(f'Personas: {persona_txt}')
        # print(f'Context: {observations[0]["text"]}')
        # print(f'Label: {observations[0]["eval_labels"]}')

        if xs is None:
            # no valid examples, just return empty responses
            return batch_reply

        with torch.no_grad():
            predictions, text_cand_inds = self.predict(xs, ys, is_training, label_candidates)

        # maps returns predictions back to the right `valid_inds`
        # in the example above, a prediction `world` should reply to `hello`
        if predictions is not None:
            PaddingUtils.map_predictions(
                predictions.cpu().data, valid_inds, batch_reply, observations,
                self.dict, self.pad_idx, labels=labels,
                answers=labels, ys=ys.data if ys is not None else None,
                report_freq=0)

        if text_cand_inds is not None:
            for i in range(len(observations)):
                order = text_cand_inds[i]
                curr_cands = observations[i]['label_candidates']
                curr = batch_reply[i]
                curr['text'] = self.fixedCands_txt[text_cand_inds[i, 0].item()]
                curr['text_candidates'] = [curr_cands[idx] for idx in order[:20]]
        self.answers = [curr.get('text') for curr in batch_reply]
        return batch_reply

    def act(self):
        # call batch_act with this batch of one
        return self.batch_act([self.observation])[0]

    def save(self, path=None):
        state_dict = self.encoder.state_dict()
        params = {
            'state_dict': state_dict,
            'word_dict': self.dict,
            'opt': self.encoder.opt,
        }
        try:
            torch.save(params, path)
            with open(path + ".opt", 'wb') as handle:
                pickle.dump(self.opt, handle, protocol=pickle.HIGHEST_PROTOCOL)

        except BaseException:
            logging.warning('WARN: Saving failed... continuing anyway.')

    def load(self, path):
        saved_model = torch.load(path, map_location='cpu')
        self.dict = DictionaryAgent(self.opt)
        saved_dict = saved_model['word_dict']

        def replace_tokens(word):
            if word == '<PAD>':
                return PAD_TOKEN
            elif word == '<UNK>':
                return UNK_TOKEN
            elif word == '<SOC>':
                return SOC_TOKEN
            else:
                return word
        iwords = map(replace_tokens, saved_dict['iwords'])
        self.dict.ind2tok = {i: t for i, t in enumerate(iwords)}
        self.dict.tok2ind = {t: i for i, t in self.dict.ind2tok.items()}
        self.dict.unk_token = UNK_TOKEN

        ''' have the opts up to date with the code: model wise '''
        opt_superset = get_opt(empty=True)

        ''' transformer agent wise: '''
        argparser = ParlaiParser(False, add_model_args=True)
        argparser.add_argument_group(self.add_cmdline_args(argparser))
        add_opts = argparser.parse_args("")
        opt_superset.__dict__.update(add_opts)

        ''' override them with saved values'''
        opt_superset.__dict__.update(vars(saved_model['opt']))

        self.encoder = MemNetModel(opt_superset, self.dict.tok2ind)
        self.encoder.load_state_dict(saved_model['state_dict'])
        if self.use_cuda:
            self.encoder = self.encoder.cuda()
        self.pad_idx = self.dict.tok2ind[PAD_TOKEN]
        self.unk_idx = self.dict.tok2ind[UNK_TOKEN]

        return opt_superset

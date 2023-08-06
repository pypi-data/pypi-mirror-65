#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from parlai.agents.transformer.modules import MultiHeadAttention
from parlai.utils.distributed import is_distributed
from parlai.core.torch_ranker_agent import TorchRankerAgent
from parlai.utils.torch import padded_3d, neginf
from parlai.zoo.bert.build import download

from .bert_dictionary import BertDictionaryAgent
from .helpers import (
    get_bert_optimizer, BertWrapper, BertModel, add_common_args, surround,
    get_adamax_optimizer, MODEL_PATH, get_bert_model)

import os
import torch
import torch.nn.functional as F
import torch.nn as nn
import math
from tqdm import tqdm


class PolyencoderRankerAgent(TorchRankerAgent):
    """ TorchRankerAgent implementation of the Poly Encoder.
        It is a standalone Agent.
    """

    @staticmethod
    def add_cmdline_args(parser):
        add_common_args(parser)
        parser.set_defaults(
            encode_candidate_vecs=True
        )
        group = parser.add_argument_group('Misc')
        group.add_argument('-CAT', '--context-attention-type', type=str, default=None,
                           choices=['none', 'basic', 'multihead', 'mean_window', 'first_mean_max'],
                           help='How to compute the intermediate context codes.'
                           '''
                            The choices are:
                                none - skip straight to label attention
                                       (legacy: set if --skip-first-attention is True)
                                basic - basic attention, where an initalized context code
                                        (attention_vec) is query, word outputs are values
                                        (legacy: set if multihead_context is False)
                                multihead - multihead attention
                                        (legacy: set if multihead_context is True)
                                mean_window - context code is computed as sum of a certain neighborhood
                                             of words

                                first_mean_max - the different embedding aggregation types are used
                                                 as attention vectors
                           ''')
        group.add_argument('-LAT', '--label-attention-type', type=str,
                           choices=['basic', 'multihead'],
                           help='how to do the final label attention'
                           '''
                            The choices are:
                                basic - basic attention, where label is query
                                        and context vectors are keys
                                        (legacy: set if multihead_label is False)
                                multihead - multihead attention
                           ''')
        group.add_argument('--num_attention', type=int, default=3,
                           help='how many intermediate context attention vectors to use')
        group.add_argument('--word-window-size', type=int, default=1,
                           help='When context_attention_type is window, this is '
                           'how many words are in a window')
        group.add_argument('--use_attention_vecs', type='bool', default=True,
                           help='Use random attention vectors as query for attention')
        group.add_argument('--extra_attention_lin', type='bool', default=True,
                           help='Whether to use additional linear layer after '
                           'basic context attention')
        group.add_argument('--init-codes', type=str, default='random',
                           choices=['random', 'ones', 'xavier'],
                           help='How to init the attention vector codes')
        group.add_argument('--init-codes-range', type=float, default=1.0,
                           help='if random init codes, range of values to consider'
                           'e.g. if `1`, init random from -1 to 1')

        group.add_argument('--context-aggregation', type=str, default='none',
                           choices=['none'],
                           help='how to aggregate word outputs of context encoder bert')
        group.add_argument('--candidate-aggregation', type=str, default='first',
                           choices=['first', 'mean', 'max'],
                           help='how to aggregate word outputs of candidate encoder bert')

        group.add_argument('--freeze-patience', type=int, default=-1,
                            help='How many validations to freeze context encoder for'
                            '-1 == do not freeze')
        group.add_argument('--freeze-cand-encoder', type='bool', default=True,
                            help='whether during frozen stage, if we freeze cand encoder')
        group.add_argument('--second-pass-lr', type=float, default=-1,
                            help='the new learning rate to use after unfreezing encoder'
                            'if <0, will not update the LR')
        group.add_argument('--multihead-dropout', type=float, default=0.4,
                            help='attention dropout for multihead attention')
        group.add_argument('--multihead-num-heads', type=int, default=4,
                            help='how many multihead heads')


        group.add_argument('--softmax-dim', type=int, default=2,
                           help='softmax dim for second attention level')
        group.add_argument('--one-multihead-linear', type='bool', default=False,
                           help='whether to use only one intermediate '
                           'linear layer for multihead attention, rather than 3')
        # legacy args
        group.add_argument('--skip-first-attention', type='bool',
                           help='Whether to skip first attention layer with the context '
                           'vectors', hidden=True)
        group.add_argument('--multihead_context', type='bool',
                           help='whether first attention over ctxt is multiheaded',
                           hidden=True)
        group.add_argument('--multihead_label', type='bool',
                           help='whether the attention over label is multiheaded',
                           hidden=True)


        group.add_argument('--debug', type='bool', default=False)


    def __init__(self, opt, shared=None):
        # download pretrained models
        download(opt['datapath'])
        self.pretrained_path = os.path.join(opt['datapath'], 'models',
                                            'bert_models', MODEL_PATH)
        opt['pretrained_path'] = self.pretrained_path

        self.clip = -1

        super().__init__(opt, shared)
        # it's easier for now to use DataParallel when
        self.data_parallel = opt.get('data_parallel') and self.use_cuda
        if self.data_parallel and not isinstance(self.model, torch.nn.DataParallel):
            self.model = torch.nn.DataParallel(self.model)
        if is_distributed():
            raise ValueError('Cannot combine --data-parallel and distributed mode')
        self.set_special_idx()
        # default one does not average
        self.rank_loss = torch.nn.CrossEntropyLoss(reduce=True, size_average=True)

        # freeze encoders
        self.frozen = False
        if opt.get('freeze_patience', -1) > 0:
            self.freeze_patience = opt['freeze_patience']
            self.freeze_impatience = 0
            self.frozen = True
            if self.data_parallel:
                self.model.module.freeze_encoders()
            else:
                self.model.freeze_encoders()

        self.debug = opt.get('debug', False)
        self.previous_accuracy = 0.0
        self.second_pass_lr = opt.get('second_pass_lr', -1)
        if self.second_pass_lr <= 0:
            self.second_pass_lr = opt.get('learningrate', 1)

    def set_special_idx(self):
        self.NULL_IDX = self.dict.pad_idx
        self.START_IDX = self.dict.start_idx
        self.END_IDX = self.dict.end_idx

    def build_model(self):
        self.model = PolyEncoderModule(self.opt)
        return self.model

    def receive_metrics(self, metrics_dict):
        if self.frozen:
            if metrics_dict['accuracy'] < self.previous_accuracy:
                print("End of the first pass\nCHANGING LR")
                for group in self.optimizer.param_groups:
                    group['lr'] = self.second_pass_lr
                for group in self.optimizer.param_groups:
                    print('new lr for group: {}'.format(group['lr']))
                self.frozen = False
                if self.data_parallel:
                    self.model.module.freeze_encoders()
                else:
                    self.model.freeze_encoders()
            else:
                self.previous_accuracy = metrics_dict['accuracy']
        super().receive_metrics(metrics_dict)

    @staticmethod
    def dictionary_class():
        return BertDictionaryAgent

    def init_optim(self, params, optim_states=None, saved_optim_type=None):
        if self.opt['optimizer'] == 'adam':
            self.optimizer = get_bert_optimizer([self.model],
                                                self.opt['type_optimization'],
                                                self.opt['learningrate'],
                                                fp16=self.opt.get('fp16'),
                                                no_decay=True)
        elif self.opt['optimizer'] == 'adam_decay':
            self.optimizer = get_bert_optimizer([self.model],
                                                self.opt['type_optimization'],
                                                self.opt['learningrate'],
                                                fp16=self.opt.get('fp16'),
                                                no_decay=False)
        else:
            self.optimizer = get_adamax_optimizer([self.model],
                                                self.opt['type_optimization'],
                                                self.opt['learningrate'],
                                                fp16=self.opt.get('fp16'))

    def set_vocab_candidates(self, shared):
        """Load the tokens from the vocab as candidates

        self.vocab_candidates will contain a [num_cands] list of strings
        self.vocab_candidate_vecs will contain a [num_cands, 1] LongTensor
        """
        if shared:
            self.vocab_candidates = shared['vocab_candidates']
            self.vocab_candidate_vecs = shared['vocab_candidate_vecs']
        else:
            if 'vocab' in (self.opt['candidates'], self.opt['eval_candidates']):
                cands = []
                vecs = []
                for ind in range(1, len(self.dict)):
                    txt = self.dict[ind]
                    cands.append(txt)
                    vecs.append(
                        self._vectorize_text(txt, add_start=True, add_end=True,
                                             truncate=self.label_truncate)
                    )
                self.vocab_candidates = cands
                self.vocab_candidate_vecs = padded_3d([vecs]).squeeze(0)
                print("[ Loaded fixed candidate set (n = {}) from vocabulary ]"
                      "".format(len(self.vocab_candidates)))
                enc_path = self.opt.get('model_file') + '.vocab.encs'
                if os.path.isfile(enc_path):
                    self.vocab_candidate_encs = self.load_candidates(
                        enc_path, cand_type='vocab encodings')
                else:
                    cand_encs = []
                    vec_batches = [
                        self.vocab_candidate_vecs[i:i + 512] for i in
                        range(0, len(self.vocab_candidate_vecs), 512)
                    ]
                    print("[ Vectorizing vocab candidates ({} batch(es) of up "
                          "to 512) ]".format(len(vec_batches)))
                    for vec_batch in tqdm(vec_batches):
                        cand_encs.append(self.encode_candidates(vec_batch))
                    self.vocab_candidate_encs = torch.cat(cand_encs, 0)
                    self.save_candidates(
                        self.vocab_candidate_encs, enc_path,
                        cand_type='vocab encodings')
                if self.use_cuda:
                    self.vocab_candidate_vecs = self.vocab_candidate_vecs.cuda()
                    self.vocab_candidate_encs = self.vocab_candidate_encs.cuda()
            else:
                self.vocab_candidates = None
                self.vocab_candidate_vecs = None
                self.vocab_candidate_encs = None

    def vectorize_fixed_candidates(self, cands_batch):
        """Override from TorchRankerAgent.
        """
        return [self._vectorize_text(cand, add_start=True, add_end=True,
                truncate=self.label_truncate) for cand in cands_batch]

    def encode_candidates(self, padded_cands):
        token_idx_cands, segment_idx_cands, mask_cands = to_bert_input(
            padded_cands, self.NULL_IDX)
        _, embedding_cands = self.model(
            token_idx_cands=token_idx_cands,
            segment_idx_cands=segment_idx_cands,
            mask_cands=mask_cands
        )

        return embedding_cands.cpu().detach()

    def _set_text_vec(self, *args, **kwargs):
        obs = super()._set_text_vec(*args, **kwargs)
        # concatenate the [CLS] and [SEP] tokens
        if obs is not None and 'text_vec' in obs:
            obs.force_set('text_vec', surround(obs['text_vec'], self.START_IDX,
                                       self.END_IDX))
        return obs

    def score_candidates(self, batch, cand_vecs, cand_encs=None):
        # Encode contexts first
        token_idx_ctxt, segment_idx_ctxt, mask_ctxt = to_bert_input(
            batch.text_vec, self.NULL_IDX)
        if self.debug:
            self.model.eval()
            self.model.cand_encoder.eval()

        embedding_ctxt, _ = self.model(
            token_ctxt=token_idx_ctxt,
            segment_ctxt=segment_idx_ctxt,
            mask_ctxt=mask_ctxt
        )

        # evaluating a fixed set of candidates
        if (hasattr(self, 'fixed_candidate_encs') and
                self.fixed_candidate_encs is not None):
            bsz = embedding_ctxt.size(0)
            cands = self.fixed_candidate_encs.unsqueeze(0).repeat(
                bsz, 1, 1
            )
            embedding_ctxt, _ = self.model(
                embedding_ctxt=embedding_ctxt,
                embedding_cands=cands,
                mask_ctxt=mask_ctxt,
            )

            # return embedding_ctxt.mm(self.fixed_candidate_encs.t())
            scores = embedding_ctxt
            return scores

        # evaluating vocab candidates:
        if (hasattr(self, 'vocab_candidate_encs') and
                self.vocab_candidate_encs is not None):
            embedding_ctxt, _ = self.model(
                embedding_ctxt=embedding_ctxt,
                mask_ctxt=mask_ctxt,
                embedding_cands=self.vocab_candidate_encs
            )
            # return embedding_ctxt.mm(self.vocab_candidate_encs.t())
            scores = embedding_ctxt
            return scores

        if len(cand_vecs.size()) == 2 and cand_vecs.dtype == torch.long:
            # train time. We compare with all elements of the batch
            token_idx_cands, segment_idx_cands, mask_cands = to_bert_input(
                cand_vecs, self.NULL_IDX)
            _, embedding_cands = self.model(
                token_idx_cands=token_idx_cands,
                segment_idx_cands=segment_idx_cands,
                mask_cands=mask_cands
            )
            bsz = embedding_cands.size(0)
            embedding_cands = embedding_cands.unsqueeze(0).repeat(
                bsz, 1, 1
            )
            scores, embedding_cands = self.model(
                embedding_ctxt=embedding_ctxt,
                mask_ctxt=mask_ctxt,
                # token_idx_cands=token_idx_cands,
                # segment_idx_cands=segment_idx_cands,
                # mask_cands=mask_cands
                embedding_cands=embedding_cands
            )
            if self.debug:
                import pdb; pdb.set_trace()


            # return embedding_ctxt.mm(embedding_cands.t())
            # scores = embedding_ctxt
            return scores

        # predict time with multiple candidates
        if len(cand_vecs.size()) == 3:
            csize = cand_vecs.size()  # batchsize x ncands x sentlength
            cands_idx_reshaped = cand_vecs.view(csize[0] * csize[1], csize[2])
            token_idx_cands, segment_idx_cands, mask_cands = to_bert_input(
                cands_idx_reshaped, self.NULL_IDX)
            _, embedding_cands = self.model(
                token_idx_cands=token_idx_cands,
                segment_idx_cands=segment_idx_cands,
                mask_cands=mask_cands
            )
            embedding_cands = embedding_cands.view(
                csize[0], csize[1], -1)  # batchsize x ncands x embed_size
            scores, _ = self.model(
                embedding_ctxt=embedding_ctxt,
                mask_ctxt=mask_ctxt,
                embedding_cands=embedding_cands
            )  # bsz x n_cands

            return scores

        # otherwise: cand_vecs should be 2D float vector ncands x embed_size
        return embedding_ctxt.mm(cand_vecs.t())


class PolyEncoderModule(torch.nn.Module):
    """ Groups context_encoder and cand_encoder together.
    """

    def __init__(self, opt, num_attention=4):
        super().__init__()
        self.context_encoder = BertWrapper(
            get_bert_model(opt),
            opt['out_dim'],
            add_transformer_layer=opt['add_transformer_layer'],
            layer_pulled=opt['pull_from_layer'],
            aggregation=opt.get('context_aggregation', 'none'),
            add_linear_layer=opt.get('add_linear_layer', True)
        )
        self.cand_encoder = BertWrapper(
            get_bert_model(opt),
            opt['out_dim'],
            add_transformer_layer=opt['add_transformer_layer'],
            layer_pulled=opt['pull_from_layer'],
            aggregation=opt.get('candidate_aggregation', 'first'),
            add_linear_layer=opt.get('add_linear_layer', True)
        )
        self.dim = opt['out_dim']
        self.num_attention = opt['num_attention']
        self.word_window_size = opt.get('word_window_size', 10)
        self.debug = opt.get('debug', False)
        self.softmax_dim = opt.get('softmax_dim', 2)
        self.freeze_cand_encoder = opt.get('freeze_cand_encoder', True)


        # Model Variants
        if opt.get('context_attention_type'):
            self.context_attention_type = opt['context_attention_type']
        elif opt.get('skip_first_attention'):
            self.context_attention_type = 'none'
        elif opt.get('multihead_context', False):
            self.context_attention_type = 'multihead'
        else:
            self.context_attention_type = 'basic'

        if opt.get('label_attention_type'):
            self.label_attention_type = opt['label_attention_type']
        elif opt.get('multihead_label', False):
            self.label_attention_type = 'multihead'
        else:
            self.label_attention_type = 'basic'

        self.use_attention_lins = opt['extra_attention_lin']
        self.use_attention_vecs = opt['use_attention_vecs']

        self.init_codes = opt['init_codes']

        self.encoders_frozen = False

        # Extra Params
        self.basic_attention = MyBasicAttention(opt)
        # self.multihead_attention = MultiHeadAttention(
        self.multihead_attention = MyMultiHeadAttention(
            n_heads=opt.get('multihead_num_heads', 4), dim=self.dim, dropout=opt.get('multihead_dropout', 0.4), one_linear=opt.get('one_multihead_linear')
        )
        # self.label_multihead_attention = MultiHeadAttention(
        self.label_multihead_attention = MyMultiHeadAttention(
            n_heads=opt.get('multihead_num_heads', 4), dim=self.dim, dropout=opt.get('multihead_dropout', 0.4), one_linear=opt.get('one_multihead_linear')
        )
        self.attention_lins = torch.nn.ModuleList([
            torch.nn.Linear(self.dim, self.dim)
            for _ in range(opt['num_attention'])
        ])
        self.initialize_attention_vecs(opt)
        self.use_cuda = not opt['no_cuda'] and torch.cuda.is_available()

    def initialize_attention_vecs(self, opt):
        param_list = []
        for _ in range(opt['num_attention']):
            if self.init_codes == 'random':
                param_list.append(torch.nn.init.uniform_(torch.empty(self.dim)) * opt.get('init_codes_range', 1))
            elif self.init_codes == 'xavier':
                param_list.append(torch.nn.init.normal_(torch.empty(self.dim), mean=0, std=math.sqrt(6.0 / self.dim)))
            else:
                param_list.append(torch.ones(self.dim))
        self.attention_vecs = torch.nn.ParameterList(torch.nn.Parameter(p) for p in param_list)

    def freeze_encoders(self):
        self.encoders_frozen = True

    def unfreeze_encoders(self):
        self.encoders_frozen = False

    def forward(self, token_ctxt=None, segment_ctxt=None, mask_ctxt=None,
                token_idx_cands=None, segment_idx_cands=None, mask_cands=None,
                embedding_ctxt=None, embedding_cands=None):
        embedding_ctxt = embedding_ctxt
        embedding_cands = embedding_cands
        if token_ctxt is not None:
            embedding_ctxt = self.context_encoder(
                token_ctxt, segment_ctxt, mask_ctxt
            )
            if self.encoders_frozen:
                embedding_ctxt = embedding_ctxt.detach()
        if token_idx_cands is not None:
            embedding_cands = self.cand_encoder(
                token_idx_cands, segment_idx_cands, mask_cands)
            if self.encoders_frozen and self.freeze_cand_encoder:
                embedding_cands = embedding_cands.detach()
        if embedding_cands is not None and embedding_ctxt is not None:
            if self.encoders_frozen:
                if self.freeze_cand_encoder:
                    embedding_cands = embedding_cands.detach()
                embedding_ctxt = embedding_ctxt.detach()
            mask_for_label_att = None
            if self.context_attention_type == 'none':
                attended_vecs = embedding_ctxt
                mask_for_label_att = mask_ctxt
            elif self.context_attention_type == 'mean_window':
                attended_vecs, mask_for_label_att = self.context_mean_window_attend(
                    embedding_ctxt,
                    mask_ctxt
                )
            elif self.context_attention_type == 'multihead':
                attended_vecs = self.context_multihead_attend(embedding_ctxt, mask_ctxt)
            elif self.context_attention_type == 'first_mean_max':
                attended_vecs = self.context_first_mean_max_attend(embedding_ctxt, mask_ctxt)
            else:  # 'basic'
                attended_vecs = self.context_basic_attend(embedding_ctxt, mask_ctxt)
            if self.label_attention_type == 'multihead':
                return self.label_multihead_attend(
                    attended_vecs, embedding_cands, mask=mask_for_label_att
                )
            else:
                return self.label_basic_attend(
                    attended_vecs, embedding_cands, mask=mask_for_label_att
                )
        else:
            return embedding_ctxt, embedding_cands

    def context_basic_attend(self, embedding_ctxt, mask_ctxt):
        attended = []
        bsz = embedding_ctxt.size(0)
        for i, vec in enumerate(self.attention_vecs):
            att_vec = vec.repeat(bsz, 1, 1)  # [Bsz, 1, out_dim]
            att, weights = self.basic_attention(
                att_vec, embedding_ctxt, mask_ys=mask_ctxt
            )
            if self.use_attention_lins:
                att = self.attention_lins[i](att)  # [bsz, 1, out_dim]
            attended.append(att)
        attended_vecs = torch.cat(attended, 1)  # [bsz, num_attention, out_dim]
        return attended_vecs

    def context_multihead_attend(self, embedding_ctxt, mask_ctxt):
        bsz = embedding_ctxt.size(0)
        att_vecs = [
            self.multihead_attention(
                query=self.attention_vecs[i].repeat(bsz, 1, 1) if self.use_attention_vecs else embedding_ctxt,
                key=embedding_ctxt,
                mask=mask_ctxt
            )
            for i in range(len(self.attention_vecs))
        ]
        attended = torch.cat(att_vecs, dim=1)
        return attended

    def context_mean_window_attend(self, embedding_ctxt, mask_ctxt):
        bsz, seq_len, _ = embedding_ctxt.size()
        att_vecs = []
        mask_vecs = []
        for i in range(0, seq_len, self.word_window_size):
            start = i
            end = min(i + self.word_window_size, seq_len)
            _sum = embedding_ctxt[:, start:end, :].sum(1)
            _sum_mask = mask_ctxt[:, start:end].type_as(embedding_ctxt).sum(1)
            mask_vecs.append(_sum_mask != 0)
            _sum_mask.masked_fill_((_sum_mask == 0), 1)
            att_vecs.append(_sum / _sum_mask.view(bsz, 1))
        attended = torch.stack(att_vecs, dim=1)
        mask_vecs = torch.stack(mask_vecs, dim=1).byte()
        return attended, mask_vecs

    def context_first_mean_max_attend(self, embedding_ctxt, mask_ctxt):
        # first embeddings
        first_embeddings = embedding_ctxt[:, 0, :]
        dtype = embedding_ctxt.dtype

        # mean
        outputs_of_interest = embedding_ctxt[:, 1:, :]
        mask = mask_ctxt[:, 1:].type_as(embedding_ctxt).unsqueeze(2)
        summed_embeddings = torch.sum(outputs_of_interest * mask, dim=1)
        nb_elems = (torch.sum(mask_ctxt[:, 1:].type_as(embedding_ctxt), dim=1)
                                              .unsqueeze(1))
        mean_embeddings = summed_embeddings / nb_elems

        # max
        mask = (~mask_ctxt[:, 1:]).type_as(embedding_ctxt).unsqueeze(2) * neginf(dtype)

        max_embeddings, _ = torch.max(outputs_of_interest + mask, dim=1)

        attended = torch.stack(
            [first_embeddings, mean_embeddings, max_embeddings],
            dim=1
        )
        return attended

    def label_basic_attend(self, attended_vecs, embedding_cands, mask=None):


        # attend over label
        if embedding_cands.dim() == 2:
            # Batch Candidates
            # if False:
            bsz, embed_dim = embedding_cands.size()
            cands = embedding_cands.unsqueeze(1).repeat(
                1, bsz, 1
            )
            attended, weights = self.basic_attention(
                cands, attended_vecs, mask_ys=mask
            )
            scores = torch.bmm(
                attended,
                embedding_cands.unsqueeze(1).transpose(1, 2)
            )

            # return attended.squeeze(1), embedding_cands
            return scores.squeeze(), embedding_cands
        elif embedding_cands.dim() == 3:
            # Inline Cands
            scores = []
            for idx in range(embedding_cands.size(0)):
                ex_att_vecs = attended_vecs[idx:idx+1]  # [1, num_attention, out_dim]
                ex_cands = embedding_cands[idx:idx+1]  # [1, n_cands, out_dim]
                ex_mask = None
                if mask is not None:
                    ex_mask = mask[idx:idx+1]
                dim = 2 if self.context_attention_type in ['none', 'first_mean_max', 'mean_window'] else 1
                # dim = 2 if self.context_attention_type == 'none' else 1
                # dim = 2
                if self.context_attention_type in ['basic', 'multihead']:
                    dim = self.softmax_dim
                attended, w = self.basic_attention(
                    ex_cands, ex_att_vecs, mask_ys=ex_mask, dim=dim
                )
                n_cands = attended.size(1)
                score = torch.bmm(
                    ex_cands.transpose(0, 1),
                    attended.view(n_cands, self.dim, 1)
                ).squeeze()  # [n_cands]

                scores.append(score)

            scores = torch.stack(scores, dim=0)  # [bsz, n_cands]
            return scores, embedding_cands

    def label_multihead_attend(self, attended_vecs, embedding_cands, mask=None):
        cands = embedding_cands
        if cands.dim() == 2:
            cands = cands.unsqueeze(1)
            attended_ctxt = self.label_multihead_attention(
                query=cands,
                key=attended_vecs,
                mask=mask
            )
            return attended_ctxt.squeeze(1), embedding_cands
        else:
            scores = []
            for idx in range(embedding_cands.size(0)):
                ex_att_vecs = attended_vecs[idx:idx+1]  # [1, num_attention, out_dim]
                ex_cands = embedding_cands[idx:idx+1]  # [1, n_cands, out_dim]
                ex_mask = None
                if mask is not None:
                    ex_mask = mask[idx:idx+1]
                else:
                    ex_mask = torch.ones(ex_att_vecs.size()[:2]).byte()
                    if self.use_cuda:
                        ex_mask = ex_mask.cuda()

                attended_ctxt = self.label_multihead_attention(
                    query=ex_cands,
                    key=ex_att_vecs,
                    mask=ex_mask
                )
                n_cands = attended_ctxt.size(1)
                score = torch.bmm(
                    ex_cands.transpose(0, 1),
                    attended_ctxt.view(n_cands, self.dim, 1)
                ).squeeze()  # [n_cands]

                scores.append(score)

            scores = torch.stack(scores, dim=0)  # [bsz, n_cands]
            return scores, embedding_cands

    def get_position_embeddings(self):
        return self.context_encoder.bert_model.embeddings.position_embeddings


class MyBasicAttention(torch.nn.Module):
    def __init__(self, opt):
        super().__init__()
        self.debug = opt.get('debug', False)

    def forward(self, xs, ys, mask_ys=None, dim=2):
        bsz = xs.size(0)
        y_len = ys.size(1)
        dtype = xs.dtype
        l1 = torch.bmm(xs, ys.transpose(1, 2))
        if mask_ys is not None:
            attn_mask = (mask_ys == 0).view(bsz, 1, y_len)
            # assert attn_mask.shape == l1.shape
            l1.masked_fill_(attn_mask, neginf(dtype))

        weight = F.softmax(l1, dim=dim)

        emb = torch.bmm(weight, ys)
        return emb, weight


class MyMultiHeadAttention(MultiHeadAttention):
    def __init__(self, n_heads, dim, dropout=0, one_linear=False):
        super().__init__(n_heads, dim, dropout)
        if one_linear:
            del self.k_lin
            del self.v_lin
            self.k_lin = self.q_lin
            self.v_lin = self.q_lin


def to_bert_input(token_idx, null_idx):
    """ token_idx is a 2D tensor int.
        return token_idx, segment_idx and mask
    """
    segment_idx = token_idx * 0
    mask = (token_idx != null_idx)
    # nullify elements in case self.NULL_IDX was not 0
    token_idx = token_idx * mask.long()
    return token_idx, segment_idx, mask

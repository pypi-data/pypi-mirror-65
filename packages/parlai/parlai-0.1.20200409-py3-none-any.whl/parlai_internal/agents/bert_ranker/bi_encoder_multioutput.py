#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from parlai.utils.distributed import is_distributed
from parlai.core.torch_ranker_agent import TorchRankerAgent
from parlai.utils.torch import padded_3d, neginf
from parlai.utils.misc import _ellipse
from parlai.zoo.bert.build import download

from .bert_dictionary import BertDictionaryAgent
from .helpers import (get_bert_optimizer, BertWrapper, BertModel,
                      add_common_args, surround, MODEL_PATH,
                      get_bert_model, get_adamax_optimizer)
from .polyencoder_ranker import MyBasicAttention

import os
import torch
import pdb
from tqdm import tqdm
from pytorch_pretrained_bert.modeling import BertLayer, BertConfig


class BiEncoderRankerMultiOutputAgent(TorchRankerAgent):
    """ Testing an idea of PEM, just use the first N output of BERT followed by
        a basic attention.
        Obviously there is a problem is the context is below N.
        Maybe we can solve that later by adding as many [CLS] as needed.
    """

    @staticmethod
    def add_cmdline_args(parser):
        add_common_args(parser)
        parser.add_argument('--debug', type=bool, default=False)
        parser.add_argument('--num-codes', type=int, default=1)
        parser.set_defaults(encode_candidate_vecs=True)

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
        if self.data_parallel:
            self.model = torch.nn.DataParallel(self.model)
        if is_distributed():
            raise ValueError('Cannot combine --data-parallel and distributed mode')
        self.set_special_idx()
        # default one does not average
        self.rank_loss = torch.nn.CrossEntropyLoss(reduce=True, size_average=True)
        self.previous_accuracy = -1e32

    def build_model(self):
        self.model = BiEncoderModule(self.opt)

    def set_special_idx(self):
        self.NULL_IDX = self.dict.pad_idx
        self.START_IDX = self.dict.start_idx
        self.END_IDX = self.dict.end_idx

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
        elif self.opt['optimizer'] == 'adamax':
            self.optimizer = get_adamax_optimizer([self.model],
                                                self.opt['type_optimization'],
                                                self.opt['learningrate'],
                                                fp16=self.opt.get('fp16'))
        else:
            self.optimizer = get_bert_optimizer([self.model],
                                                self.opt['type_optimization'],
                                                self.opt['learningrate'],
                                                fp16=self.opt.get('fp16'),
                                                no_decay=False)

    def set_vocab_candidates(self, shared):
        """Load the tokens from the vocab as candidates

        self.vocab_candidates will contain a [num_cands] list of strings
        self.vocab_candidate_vecs will contain a [num_cands, 1] LongTensor
        """
        self.opt['encode_candidate_vecs'] = True
        if shared:
            self.vocab_candidates = shared['vocab_candidates']
            self.vocab_candidate_vecs = shared['vocab_candidate_vecs']
            self.vocab_candidate_encs = shared['vocab_candidate_encs']
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
        _, embedding_cands, _, _ = self.model(
            None, None, None, token_idx_cands, segment_idx_cands, mask_cands)

        return embedding_cands.cpu().detach()

    def _set_text_vec(self, *args, **kwargs):
        obs = super()._set_text_vec(*args, **kwargs)
        # concatenate the [CLS] and [SEP] tokens
        if obs is not None and 'text_vec' in obs:
            obs['text_vec'] = surround(obs['text_vec'], self.START_IDX,
                                       self.END_IDX)
        return obs

    def score_candidates(self, batch, cand_vecs, cand_encs=None):

        # Encode contexts first
        token_idx_ctxt, segment_idx_ctxt, mask_ctxt = to_bert_input(
            batch.text_vec, self.NULL_IDX)
        embedding_ctxt, _, embedding_ctxt_mask, _ = self.model(
            token_idx_ctxt, segment_idx_ctxt, mask_ctxt,
            None, None, None)

        if len(cand_vecs.size()) == 2 and cand_vecs.dtype == torch.long:
            if cand_encs is None:
                # train time. We compare with all elements of the batch
                token_idx_cands, segment_idx_cands, mask_cands = to_bert_input(
                    cand_vecs, self.NULL_IDX)
                _, embedding_cands, _, _ = self.model(
                    None, None, None,
                    token_idx_cands, segment_idx_cands, mask_cands)
            else:
                embedding_cands = cand_encs
            bsz = embedding_ctxt.size(0)
            cand_size = cand_vecs.size(0)
            embedding_cands = embedding_cands.unsqueeze(0).expand(bsz, cand_size, -1)
            _, _, _, scores = self.model(None, None, None, None, None, None,
                                      embedding_ctxt, embedding_cands,embedding_ctxt_mask )
            return scores

        # predict time with multiple candidates
        if len(cand_vecs.size()) == 3:
            csize = cand_vecs.size()  # batchsize x ncands x sentlength
            cands_idx_reshaped = cand_vecs.view(csize[0] * csize[1], csize[2])
            token_idx_cands, segment_idx_cands, mask_cands = to_bert_input(
                cands_idx_reshaped, self.NULL_IDX)
            _, embedding_cands, _, _ = self.model(
                None, None, None,
                token_idx_cands, segment_idx_cands, mask_cands)
            embedding_cands = embedding_cands.view(csize[0], csize[1], -1)
            _, _, _, scores = self.model(None, None, None, None, None, None,
                                      embedding_ctxt, embedding_cands,
                                      embedding_ctxt_mask)
            return scores

        # otherwise: cand_vecs should be 2D float vector ncands x embed_size
        _, _, _, scores = self.model(None, None, None, None, None, None,
                                  embedding_ctxt, cand_vecs,
                                  embedding_ctxt_mask)
        return scores

    def share(self):
        """Share model parameters."""
        shared = super().share()
        shared['vocab_candidate_encs'] = self.vocab_candidate_encs
        return shared


class BiEncoderModule(torch.nn.Module):
    """ Groups context_encoder and cand_encoder together.
    """

    def __init__(self, opt):
        super(BiEncoderModule, self).__init__()
        self.opt = opt
        self.context_encoder = BertWrapper(
            get_bert_model(opt),
            opt['out_dim'],
            add_transformer_layer=opt['add_transformer_layer'],
            layer_pulled=opt['pull_from_layer'],
            aggregation="multiple",
            add_linear_layer=False,
            aggregation_num=opt["num_codes"],
            scaling=opt['scaling'],
            norm_to_1=opt['norm_to_1'],
            multi_aggregation_strategy=opt['bert_multi_aggregation_strategy']
        )
        self.cand_encoder = BertWrapper(
            get_bert_model(opt),
            opt['out_dim'],
            add_transformer_layer=opt['add_transformer_layer'],
            layer_pulled=opt['pull_from_layer'],
            aggregation=opt['bert_aggregation'],
            add_linear_layer=False,
            scaling=opt['scaling'],
            norm_to_1=opt['norm_to_1']
        )
        self.num_codes = opt["num_codes"]
        self.basic_attention = MyBasicAttention(opt)


    def get_score(self, emb_ctxt, emb_cands, embedding_ctxt_mask):
        """ None of input are None.
            Returns the score
            emb_ctxt is (batchsize x num_codes x emb_size)
            emb_cands is potentially (batchsize x num_candidates x emb_size)
        """
        return self.label_basic_attend(emb_ctxt, emb_cands, embedding_ctxt_mask)[0]

    def get_second_transfo_mask(self, mask, dtype):
        """ From the token mask, compute the mask expected from
            the second transfo.
        """
        code_masks = torch.ones(len(mask), self.num_codes, device=mask.device).byte()
        full_mask = torch.cat([code_masks, mask], dim=1)
        extended_attention_mask = full_mask.unsqueeze(1).unsqueeze(2)
        extended_attention_mask = (
            (~extended_attention_mask).to(dtype) * neginf(dtype)
        )
        return extended_attention_mask

    def forward(self, token_idx_ctxt, segment_idx_ctxt, mask_ctxt,
                token_idx_cands, segment_idx_cands, mask_cands,
                embedding_ctxt=None, embedding_cands=None,
                embedding_ctxt_mask=None):

        # In order to bypass the "only one model philosophy" of parlai
        # I had to make 2 forward pass
        if embedding_ctxt is not None and embedding_cands is not None:
            return None, None, None, self.get_score(embedding_ctxt, embedding_cands, embedding_ctxt_mask)

        # For candidate, nothing changes really
        embedding_cands = embedding_cands
        if token_idx_cands is not None and embedding_cands is None:
            embedding_cands = self.cand_encoder(
                token_idx_cands, segment_idx_cands, mask_cands)



        embedding_ctxt = embedding_ctxt
        if token_idx_ctxt is not None and embedding_ctxt is None:
            embedding_ctxt = self.context_encoder(
                token_idx_ctxt, segment_idx_ctxt, mask_ctxt) # batchsize x num_codes x dim
            if token_idx_ctxt.size(1) > self.num_codes:
                embedding_ctxt_mask = mask_ctxt[:, 0:self.num_codes]
            else:
                embedding_ctxt_mask = mask_ctxt

        return embedding_ctxt, embedding_cands, embedding_ctxt_mask, None


    def label_basic_attend(self, attended_vecs, embedding_cands, mask=None):
        """ Copied from the polyencoder
        """

        scores = []
        for idx in range(embedding_cands.size(0)):
            ex_att_vecs = attended_vecs[idx:idx+1]  # [1, num_attention, out_dim]
            ex_cands = embedding_cands[idx:idx+1]  # [1, n_cands, out_dim]
            outdim = ex_att_vecs.size()[2]
            ex_mask = mask[idx:idx+1]
            attended, w = self.basic_attention(
                ex_cands, ex_att_vecs, mask_ys=ex_mask, dim=2
            )
            n_cands = attended.size(1)
            score = torch.bmm(
                ex_cands.transpose(0, 1),
                attended.view(n_cands, outdim, 1)
            ).squeeze()  # [n_cands]

            scores.append(score)
        scores = torch.stack(scores, dim=0)  # [bsz, n_cands]
        return scores, embedding_cands


def to_bert_input(token_idx, null_idx):
    """ token_idx is a 2D tensor int.
        return token_idx, segment_idx and mask
    """
    segment_idx = token_idx * 0
    mask = (token_idx != null_idx)
    # nullify elements in case self.NULL_IDX was not 0
    token_idx = token_idx * mask.long()
    return token_idx, segment_idx, mask

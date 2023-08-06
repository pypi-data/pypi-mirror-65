#!/usr/bin/env python3
import numpy as np
import torch
from torch import nn
from torch import FloatTensor, LongTensor
from torch import autograd
from torch import optim
from parlai_internal.agents.comment_battle.text_tokens_utils import TextTokens,\
    load_embeddings_from_file
from parlai_internal.agents.transformer_ranker.modules import TransformerModel
import random

"""
    Please do not make any import from the parlai framework in
    this file, that's make exportation and deployment much easier.
"""


class CommentBattleModelURU(nn.Module):
    """
        In the light of the success of the transformer and next
        utterance retrieval prediction, we try to apply it to images.

        In the same way that for image_commenting task, where we generate
        comments, I tried to make this code a independant from ParlAI as
        possible. The only thing is that it needs a dictionary that
        has the fields tok2ind and ind2tok.
    """

    @staticmethod
    def add_cmdline_args(argparser):
        agent = argparser.add_argument_group('CommentBattleModelURU task arguments')
        agent.add_argument('--max-length-sentence', type=int, default=32)
        agent.add_argument('--word-embeddings-dim', type=int, default=300)
        agent.add_argument('--load-embeddings-from', type=str, default=None)
        agent.add_argument('--load-transformer-from', type=str, default=None)
        agent.add_argument('--transformer-nb-heads', type=int, default=2)
        agent.add_argument('--hidden-dim', type=int, default=300)
        agent.add_argument('--num-layers-all', type=int, default=-1)
        agent.add_argument('--num-layers-text-encoder', type=int, default=1)
        agent.add_argument('--num-layers-image-encoder', type=int, default=1)
        agent.add_argument('--no-cuda', dest='no_cuda', action='store_true')
        agent.add_argument('--adam-alpha', type=float, default=0.0008)
        agent.add_argument('--dropout', type=float, default=0)
        agent.add_argument('--encoder-type', type=str, default="bow")
        agent.add_argument('--additional-layer-text', type=int, default=0)

    def __init__(self, opt, personas_list, dic, loading_trained=False):
        """
            Initialize the model.
            It's important that the options are saved somewhere,
        """
        super(CommentBattleModelURU, self).__init__()
        self.opt = opt
        self.dic = dic
        dropout = self.opt["dropout"]
        hdim = self.opt["hidden_dim"]
        self.hidden_dim = hdim
        nlayers_text = opt["num_layers_all"] if opt["num_layers_all"] != -1 else opt["num_layers_text_encoder"]
        nlayers_img = opt["num_layers_all"] if opt["num_layers_all"] != -1 else opt["num_layers_image_encoder"]
        self.text_encoder_frozen = False

        # Initialize personas dictionary
        self.personas_list = personas_list
        self.persona_to_id = {}
        for i, p in enumerate(personas_list):
            self.persona_to_id[p] = i
        self.nb_units_personas = len(self.personas_list) + 1

        # Text embedding
        self.text_tokens_handler = TextTokens(self.opt["no_cuda"], dic,
            self.opt["max_length_sentence"])

        if opt['load_embeddings_from'] == 'none':
            opt['load_embeddings_from'] = None
        if opt['load_transformer_from'] == 'none':
            self.opt['load_transformer_from'] = None
        # Context encoder
        self.embeddings = None
        if opt["load_embeddings_from"] is not None and self.opt["load_transformer_from"] is None \
            and not loading_trained:
            self.embeddings = load_embeddings_from_file(opt["load_embeddings_from"],
                dic, self.opt["word_embeddings_dim"])
        elif self.opt["load_transformer_from"] is None:
            self.embeddings = nn.Embedding(len(dic), self.opt["word_embeddings_dim"])
        if opt["encoder_type"] == "bow":
            self.context_encoder = BowEncoder(self.opt["word_embeddings_dim"], len(dic),
                self.embeddings, self.opt["hidden_dim"], True,
                self.opt["num_layers_text_encoder"], dropout=dropout)
        if opt["encoder_type"] == "transformer":
            if self.opt["load_transformer_from"] is not None:
                # the model trained by Pierre-Emmanuel on reddit
                if loading_trained:
                    serial = self.opt["transformer_architecture"]
                else:
                    serial = torch.load(self.opt["load_transformer_from"])
                self.context_encoder = load_transformer_from_reddit_pretrained(serial)
                if not loading_trained:
                    del serial["transformer_state"]
                    self.opt["transformer_architecture"] = serial
            else:
                self.context_encoder = TransformerModel(self.opt["transformer_nb_heads"],
                    self.opt["num_layers_text_encoder"], self.opt["word_embeddings_dim"],
                    len(dic), self.embeddings, dropout=dropout)
            # the model trained by trained by Pierre-Emmanuel on reddit
            # does not have any dropout. Besides, its dimension is constrained
            # to be the one of the word encoding. This adds a layer and
            # remove those constraints
            if self.opt["additional_layer_text"]:
                self.additional_layer = LinearWrapper(self.opt["word_embeddings_dim"],
                        self.opt["hidden_dim"], dropout=dropout)
            else:
                self.additional_layer = None

        # Image encoder and persona encoder
        image_layers = [nn.BatchNorm1d(self.opt["image_features_dim"]), nn.Dropout(p=dropout), nn.Linear(self.opt["image_features_dim"], hdim)]
        for _ in range(nlayers_img-1):
            image_layers += [nn.ReLU(), nn.Dropout(p=dropout), nn.Linear(hdim, hdim)]
        self.image_encoder = nn.Sequential(*image_layers)
        # persona encoder is just one layer for now
        persona_layers = [nn.BatchNorm1d(self.nb_units_personas), nn.Dropout(p=dropout), nn.Linear(self.nb_units_personas, hdim)]
        self.persona_encoder = nn.Sequential(*persona_layers)

        # optimizer
        self.optimizer = optim.Adam(filter(lambda p: p.requires_grad, self.parameters()), self.opt["adam_alpha"])



    def forward(self, image_features, personas, comments, personas_variable=None):
        """
            Inputs:
                image_features: a list of tensor of size M
                persona_features: list of string, one per sample
                comments: list of string, one per sample
                personas_vector: optional: you can provide persona as a
                    variable if you want, (typically a one hot vector, but it might be
                    a distribution too). That might be useful to make reinforcement
                    learning on personas.
            Outputs: (pers_image_encoded, comments_encoded)
                - pers_image_encoded: if image_features is not null, encoded version of
                                     image and personality. It's a pytorch Variable
                - comments_encoded: if comments is not null, encoded version of coments
                                     pytorch variable

        """
        comments_encoded = None
        if comments is not None:
            indexes_var, mask_var = self.text_tokens_handler.list_sentence_to_var(comments)
            comments_encoded = self.context_encoder(indexes_var, mask_var)
            if self.text_encoder_frozen:
                comments_encoded = comments_encoded.detach()
            if self.opt["additional_layer_text"] and self.opt['encoder_type'] == 'transformer':
                comments_encoded = self.additional_layer(comments_encoded)


        pers_image_encoded = None
        if image_features is not None:
            if personas is None:
                personas = ["zzzz"] * len(image_features)
            if personas_variable is not None:
                pers_var = personas_variable
            else:
                pers_var = self.personas_to_embedded_var(personas)
            img_var = self.img_to_var(image_features)
            pers_encoded = self.persona_encoder(pers_var)
            img_encoded = self.image_encoder(img_var)
            pers_image_encoded = pers_encoded + img_encoded
        return pers_image_encoded, comments_encoded

    def train_batch(self, image_features, personas, comments):
        """
            Will do a train step. As used in pem et al, we use the
            others elements of the batch as negative. The bigger the
            batch the better it works.
        """
        self.zero_grad()
        self.train()
        pers_image_encoded, comments_encoded = self.forward(image_features, personas, comments) # both are batch_size * hidden_dim

        loss, nb_ok = self.evaluate_one_batch(pers_image_encoded, comments_encoded, during_train=True)
        # decrease the loss
        loss.backward()
        self.optimizer.step()

        # re-run the forward pass on the batch in order to get the hits@100.
        # slowish but allows a good evaluation of the hits@1 (adds about 30% of training time,
        # but much better visibility on what is going on)
        # self.eval_batch(image_features, personas, comments)
        return self.eval_batch_per_chunk_of_100(pers_image_encoded, comments_encoded)

    def eval_batch(self, image_features, personas, comments):
        """
            Evaluate the performance in terms of Hits@100 on the batch.
            to do this we split in chunks of 100, and
        """
        if personas is None:
            personas = ["zzzz"] * len(image_features)
        if len(image_features) ==0:
            return 0,0,1
        self.eval()
        pi_encoded, com_encoded = self.forward(image_features, personas, comments)
        return self.eval_batch_per_chunk_of_100(pi_encoded, com_encoded)

    def elect_best_comment(self, image_features, personas, candidates,
                           candidates_encoded=None, k=1):
        """
            Choose the best comment in a list of possible comments.
            Inputs
            - image_features: a list of N tensor of size M
            - persona_features: list of N string, one per sample
            - candidates: a list of list of string. Size is N x K, K being the number
              of candidates.
              Note: For now the number of candidates is assumed to be small enough
              that it can fit in one batch.
            - k: how many ranked comments to return
            Outputs
             - elected: list of N string, the comment that has been elected
        """
        self.eval()
        pers_image_encoded = self.forward(image_features, personas, None)[0].detach()
        one_cand_set = True
        if candidates_encoded is None:
            one_cand_set = False
            candidates_encoded = [self.forward(None, None, c)[1].detach() for c in candidates]
        elected = []
        for img_index in range(len(pers_image_encoded)):  # not sure I could use enumerate here
            image_vec = pers_image_encoded[img_index:img_index+1, :]
            scores = torch.mm(candidates_encoded[img_index] if not one_cand_set else candidates_encoded, image_vec.transpose(0,1))
            if k >= 1:
                _, index_top = torch.topk(scores, k, dim=0)
            else:
                _, index_top = torch.topk(scores, scores.size(0), dim=0)
            elected.append([candidates[img_index][idx] for idx in index_top.unsqueeze(1)])
        return elected

    def eval_batch_per_chunk_of_100(self, pi_encoded, com_encoded):
        total_loss = 0
        total_ok = 0
        total_evaluated = 0
        for i in range(0, len(pi_encoded), 100):
            if i+100 > len(pi_encoded):
                break
            total_evaluated += 100
            loss, nb_ok = self.evaluate_one_batch(pi_encoded[i:i+100, :], com_encoded[i:i+100, :])
            total_loss += loss.data.cpu().item()
            total_ok += nb_ok.data.cpu().item()
        return total_loss, total_ok, total_evaluated

    def evaluate_one_batch(self, pers_image_encoded, comments_encoded, chunk_by=-1, during_train=False):
        """
         compute the batch loss and also the number of elements that
         have been correctly classified
        """
        if not during_train:
            self.zero_grad()
            self.eval()
        dot_products = pers_image_encoded.mm(comments_encoded.t()) # batch_size * batch_size
        log_prob = torch.nn.functional.log_softmax(dot_products, dim=1)
        targets = self.to_var(torch.arange(0, len(pers_image_encoded), dtype=torch.long), no_cuda=self.opt["no_cuda"])
        loss = torch.nn.functional.nll_loss(log_prob, targets)
        nb_ok = (log_prob.max(dim=1)[1] == targets).float().sum()
        return loss, nb_ok

    def freeze_text_encoder(self):
        self.text_encoder_frozen = True

    def unfreeze_text_encoder(self):
        self.text_encoder_frozen = False


    ##################################################
    #      Helpers
    ##################################################

    def personas_to_index(self, personas):
        res = []
        for i, p in enumerate(personas):
            if p in self.persona_to_id:
                res.append(self.persona_to_id[p] + 1)
            else:
                res.append(0)
        return res

    def personas_to_embedded_var(self, personas, no_cuda=False):
        """
            Transform a list of personas into a FloatTensor (via embedding).
        """
        res = torch.FloatTensor(len(personas), self.nb_units_personas).fill_(0)
        for i, index in enumerate(self.personas_to_index(personas)):
            res[i, index] = 1 # no personality corresponds to 0
        var_ = self.to_var(res, no_cuda=self.opt["no_cuda"])
        return var_

    def img_to_var(self, images):
        unsqueezed = [f.unsqueeze(0) for f in images]
        return self.to_var(torch.cat(unsqueezed, 0), no_cuda=self.opt["no_cuda"])

    def to_var(self, x, requires_grad=False, no_cuda=False):
        var_ = autograd.Variable(x,  requires_grad=requires_grad)
        if not no_cuda:
            var_ = var_.cuda()
        return var_

    @staticmethod
    def save_model(model, filepath):
        d = {}
        d["state_dict"] = model.state_dict()
        d["opts"] = model.opt
        d["dic"] = model.dic
        d["personas_list"] = model.personas_list
        torch.save(d, filepath)

    @staticmethod
    def load_model(filepath, force_cpu=False):
        d = torch.load(filepath, map_location='cpu')
        if force_cpu:
            d["opts"]["no_cuda"] = True
        model =  CommentBattleModelURU(d["opts"], d["personas_list"], d["dic"], loading_trained=True)
        model.load_state_dict(d["state_dict"])
        return model

#########################################
#  Helper that load the pretrained reddit model
#########################################

def load_transformer_from_reddit_pretrained(serial):
    """
        Mazaré et al. have trained a transformer on reddit,
        which can be used as initial parameters.
        {
            "vocabulary_size": --
            "transformer_n_layers": number of layers of the transformer,
            "transformer_dim": hidden size of the transformer,
            "transformer_n_heads": number of heads of the transformer
            "padding_idx": index of padding
            "transformer_state": <state of the transformer>
        }
    """
    tm = TransformerModel(serial["transformer_n_heads"], serial["transformer_n_layers"],
                          serial["transformer_dim"], serial["vocabulary_size"])
    if "transformer_state" in serial:
        tm.load_state_dict(serial["transformer_state"])
    return tm

#########################################
#    Some additional modules
#########################################

class LinearWrapper(nn.Module):
    """
        Adds one linear layer on top of a module.
        This was designed for the transformer, since pretrained
        instance don't use dropout, and they are constrained to
        keep the dimension of the word embedding.
    """

    def __init__(self, in_dim, out_dim, dropout):
        super(LinearWrapper, self).__init__()
        self.lin = nn.Linear(in_dim, out_dim)
        self.dp = nn.Dropout(dropout)

    def forward(self, input):
        return self.lin(self.dp(input))


class BowEncoder(nn.Module):
    """
        The simplest, sum over words embeddings,
        take the result trough a DNN.
        It's not exactly the same as provided in
        transformer.py although very similar
    """

    def __init__(self, embedding_dim, vocabulary_size, embeddings=None,
                 out_dim=300, scale_sqrt=True, n_hidden=1, dropout=0):
        """
            Inputs:
                embedding_dim: size of the embeddings
                vocabulary_size: number of embeddings to prepare
                embeddings: embeddings can be provided.
                            If it is the cse, voc size will be ignored
                out_dim: expected size of the output
                scale_sqrt: if true, divides by the square root of the length of sentence
                            otherwise divides by the length of sentence
                n_hidden: number of layers of ReLU on top of the encoding
        """

        super(BowEncoder, self).__init__()
        if embeddings is not None:
            self.embeddings = embeddings
        else:
            self.embeddings = nn.Embedding(vocabulary_size, embedding_dim)

        self.embedding_dim = embedding_dim
        self.out_dim = out_dim
        self.scale_sqrt = scale_sqrt
        nn_layers = []
        for _ in range(n_hidden-1):
            nn_layers.append(nn.Dropout(p=dropout))
            nn_layers.append(nn.Linear(embedding_dim, embedding_dim))
            nn_layers.append(nn.ReLU())
        nn_layers.append(nn.Dropout(p=dropout))
        nn_layers.append(nn.Linear(embedding_dim, out_dim))
        self.proj = nn.Sequential(*nn_layers)

    def forward(self, input, mask):
        input_e = self.embeddings(input)
        last_dim_mask = len(mask.shape) -1
        scale = mask.sum(last_dim_mask, keepdim=True).clamp(min=1)
        if self.scale_sqrt:
            scale = scale.sqrt()
        # put elements that are masked to 0
        input_masked = input_e * mask.unsqueeze(last_dim_mask + 1)
        bow = input_masked.sum(dim=last_dim_mask) / scale
        out = self.proj(bow)
        return out

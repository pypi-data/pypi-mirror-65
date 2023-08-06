#!/usr/bin/env python3
"""
    Somewhat like the other personality classifier,
    but this time we train the text classifier too, same as
    the comment battle model, we train by first
    freezing the weights, and then releasing this constraint.

    Contains a lot of duplicate code from the comment_battle model
"""

import numpy as np
import torch
from torch import nn
from torch import FloatTensor, LongTensor
from torch import autograd
from torch import optim
from parlai_internal.agents.comment_battle.text_tokens_utils import TextTokens,\
    load_embeddings_from_file
from parlai_internal.agents.transformer_ranker.modules import TransformerModel
from parlai_internal.agents.comment_battle.comment_battle_model import BowEncoder,\
    LinearWrapper, load_transformer_from_reddit_pretrained
import random
import pdb


class PersonalityClassifierURU(nn.Module):

    @staticmethod
    def add_cmdline_args(argparser):
        agent = argparser.add_argument_group('PersonalityClassifierURU task arguments')
        agent.add_argument('--max-length-sentence', type=int, default=32)
        agent.add_argument('--word-embeddings-dim', type=int, default=300)
        agent.add_argument('--image-features-dim', type=int, default=2048)
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
        super(PersonalityClassifierURU, self).__init__()
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

        # The top layer is classifying the personality. It's a simple linear layer.
        self.layers = [
                    nn.BatchNorm1d(self.hidden_dim),
                    nn.Dropout(p=dropout),
                    nn.Linear(self.hidden_dim, self.nb_units_personas),
                    ]
        self.top_processor = nn.Sequential(*self.layers)


        # optimizer
        self.optimizer = optim.Adam(filter(lambda p: p.requires_grad, self.parameters()), self.opt["adam_alpha"])



    def forward(self, image_features, comments):
        """
            Inputs:
                image_features: a list of tensor of size M
                comments: list of string, one per sample
            Outputs: (pers_image_encoded, comments_encoded)
                - encoding: sum of image and comment encoding.

        """
        comments_encoded = None
        if comments is not None:
            indexes_var, mask_var = self.text_tokens_handler.list_sentence_to_var(comments)
            comments_encoded = self.context_encoder(indexes_var, mask_var)
            if self.text_encoder_frozen:
                comments_encoded = comments_encoded.detach()
            if self.opt["additional_layer_text"]:
                comments_encoded = self.additional_layer(comments_encoded)


        image_encoded = None
        if image_features is not None:
            img_var = self.img_to_var(image_features)
            image_encoded = self.image_encoder(img_var)
        encoding = self.top_processor(comments_encoded)
        return encoding

    def train_batch(self, image_features, comments, personas):
        """
            Will do a train step. As used in pem et al, we use the
            others elements of the batch as negative. The bigger the
            batch the better it works.
        """
        self.zero_grad()
        self.train()
        encoding = self.forward(image_features, comments)
        loss, nb_ok, persona_produced = self.get_loss_accuracy_and_predictions(encoding, personas)
        loss.backward()
        self.optimizer.step()
        return loss.item(), nb_ok.item(), persona_produced

    def get_loss_accuracy_and_predictions(self, encoding, personas):
        index_targets = self.personas_to_index(personas)
        targets = self.to_var(torch.LongTensor(index_targets))
        loss = nn.CrossEntropyLoss()(encoding, targets)
        produced = encoding.max(dim=1)[1]
        persona_produced = []
        for i in range(len(produced)):
            index_pers = produced[i]
            if index_pers == 0:
                persona_produced.append("None")
            else:
                persona_produced.append(self.personas_list[index_pers - 1])
        nb_ok = (produced == targets).float().sum()
        return loss, nb_ok, persona_produced

    def eval_batch(self, image_features, comments, personas):
        """
            Evaluate the performance in terms of Hits@100 on the batch.
            to do this we split in chunks of 100, and
        """
        self.eval()
        encoding = self.forward(image_features, comments)
        loss, nb_ok, persona_produced =  self.get_loss_accuracy_and_predictions(encoding, personas)
        return loss.item(), nb_ok.item(), persona_produced

    def predict(self, image_features, comments):
        encoding = self.forward(image_features, comments)
        produced = encoding.max(dim=1)[1]
        persona_produced = []
        for i in range(len(produced)):
            index_pers = produced[i]
            if index_pers == 0:
                persona_produced.append("None")
            else:
                persona_produced.append(self.personas_list[index_pers - 1])
        return persona_produced

    def predict_scores_class(self, image_features, comments):
        """
            Same as predict but also returns the scores of each class
            after softmax.
        """
        encoding = self.forward(image_features, comments)
        scores = nn.Softmax(1)(encoding).detach()
        produced = encoding.max(dim=1)[1]
        persona_produced = []
        for i in range(len(produced)):
            index_pers = produced[i]
            if index_pers == 0:
                persona_produced.append("None")
            else:
                persona_produced.append(self.personas_list[index_pers - 1])
        return persona_produced, scores

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
        model =  PersonalityClassifierURU(d["opts"], d["personas_list"], d["dic"], loading_trained=True)
        model.load_state_dict(d["state_dict"])
        return model

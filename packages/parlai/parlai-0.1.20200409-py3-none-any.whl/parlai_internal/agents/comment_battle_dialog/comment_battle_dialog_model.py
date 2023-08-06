#!/usr/bin/env python3
import torch
from torch import nn
import torch.nn.functional as F
from parlai_internal.agents.transformer_ranker.modules import (
    TransformerModel,
    TransformerNoEmbeddingsModel,
)
from parlai.core.opt import Opt

word_embedding_file = '/checkpoint/parlai/zoo/comment_battle/crawl-300d-2M.vec'
transformer_file = '/checkpoint/parlai/zoo/comment_battle/redditbest.mdl'


class CommentBattleDialogModelURU(nn.Module):
    """
    Model for image dialog.

    There are two options for incorporating dialog history:
        1. Use the same transformer to encode dialog history and candidate
           responses; sum the image encoding, personality encoding, and
           dialog history encoding, and use that as query for candidate response
        2. (Multi-modal) Feed (something) into a separate transformer
           after computing the encoding; use that as query
    """

    @staticmethod
    def add_cmdline_args(argparser):
        agent = argparser.add_argument_group('CommentBattleModelURU task arguments')
        agent.add_argument('--max-length-sentence', type=int, default=64)
        agent.add_argument('--word-embeddings-dim', type=int, default=300)
        agent.add_argument('--image-features-dim', type=int, default=2048)
        agent.add_argument(
            '--pretrained-label-encoder',
            type='bool',
            default=False,
            help='Whether the encoder for the labels is pretrained',
        )
        agent.add_argument(
            '--pretrained-label-word-emb',
            type='bool',
            default=False,
            help='Whether the embeddings for the encoder are pretrained',
        )
        agent.add_argument(
            '--pretrained-context-encoder',
            type='bool',
            default=False,
            help='Whether the encoder for the dialog context ' 'is pretrained',
        )
        agent.add_argument(
            '--pretrained-context-word-emb',
            type='bool',
            default=False,
            help='Whether the embeddings for the dialog context ' 'are pretrained',
        )
        agent.add_argument(
            '--share-encoder',
            type='bool',
            default=False,
            help='Whether to share the text encoder for the '
            'labels and the dialog history',
        )
        agent.add_argument('--transformer-nb-heads', type=int, default=4)
        agent.add_argument('--hidden-dim', type=int, default=300)
        agent.add_argument('--num-layers-all', type=int, default=-1)
        agent.add_argument('--num-layers-text-encoder', type=int, default=1)
        agent.add_argument('--num-layers-image-encoder', type=int, default=1)
        agent.add_argument('--num-layers-multimodal-encoder', type=int, default=1)
        agent.add_argument('--no-cuda', dest='no_cuda', action='store_true')
        agent.add_argument('--adam-alpha', type=float, default=0.0008)
        agent.add_argument('--dropout', type=float, default=0)
        agent.add_argument('--encoder-type', type=str, default='transformer')
        agent.add_argument('--additional-layer-text', type=int, default=0)
        agent.add_argument(
            '--multimodal',
            type='bool',
            default=False,
            help='If true, feed a query term into a separate '
            'transformer prior to computing final rank '
            'scores',
        )
        agent.add_argument(
            '--multimodal-combo',
            type=str,
            choices=['concat', 'sum'],
            default='sum',
            help='How to combine the encoding for the ' 'multi-modal transformer',
        )
        agent.add_argument(
            '--encode-image',
            type='bool',
            default=True,
            help='Whether to include the image encoding when '
            'retrieving a candidate response',
        )
        agent.add_argument(
            '--encode-dialog-history',
            type='bool',
            default=True,
            help='Whether to include the dialog history '
            'encoding when retrieving a candidate response',
        )
        agent.add_argument(
            '--encode-personality',
            type='bool',
            default=True,
            help='Whether to include the personality encoding '
            'when retrieving a candidate response',
        )

    def __init__(self, opt, personas_list, dictionary, loading_trained=False):
        """
        Initialize the model.

        It's important that the options are saved somewhere,
        """
        super().__init__()
        self.opt = opt
        self.dict = dictionary
        self.hidden_dim = self.opt['hidden_dim']
        self.use_cuda = not opt['no_cuda'] and torch.cuda.is_available()
        self.share_encoder = opt.get('share_encoder')
        nlayers_img = (
            opt['num_layers_all']
            if opt['num_layers_all'] != -1
            else opt['num_layers_image_encoder']
        )
        nlayers_mm = (
            opt['num_layers_all']
            if opt['num_layers_all'] != -1
            else opt['num_layers_multimodal_encoder']
        )
        self.text_encoder_frozen = False

        # Initialize personas dictionary
        self.personas_list = personas_list
        self.persona_to_id = {}
        for i, p in enumerate(personas_list):
            self.persona_to_id[p] = i
        self.nb_units_personas = len(personas_list) + 1

        self.max_length_sentence = opt['max_length_sentence']

        # blank encoding (for concat)
        self.blank_encoding = torch.Tensor(opt['hidden_dim']).fill_(0).detach_()
        if self.use_cuda:
            self.blank_encoding = self.blank_encoding.cuda()

        # Encoders
        self.encode_image = opt.get('encode_image', True)
        self.encode_personality = opt.get('encode_personality', True)
        self.encode_dialog_history = opt.get('encode_dialog_history', True)
        assert any(
            [self.encode_dialog_history, self.encode_image, self.encode_personality]
        )

        # Transformer 2
        self.multimodal = opt.get('multimodal')
        if self.multimodal:
            self.multimodal_combo = opt.get('multimodal_combo', 'sum')
            self.multimodal_encoder = TransformerNoEmbeddingsModel(
                opt['transformer_nb_heads'],
                nlayers_mm,
                self.hidden_dim,
                dropout=self.opt['dropout'],
            )

        # Label Encoder
        self.label_encoder = self.build_context_encoder(loading_trained, 'label')

        # Image Encoder
        image_layers = [
            nn.BatchNorm1d(self.opt['image_features_dim']),
            nn.Dropout(p=self.opt['dropout']),
            nn.Linear(self.opt['image_features_dim'], self.hidden_dim),
        ]
        for _ in range(nlayers_img - 1):
            image_layers += [
                nn.ReLU(),
                nn.Dropout(p=self.opt['dropout']),
                nn.Linear(self.hidden_dim, self.hidden_dim),
            ]
        self.image_encoder = nn.Sequential(*image_layers)

        # Persona Encoder
        persona_layers = [
            nn.BatchNorm1d(self.nb_units_personas),
            nn.Dropout(p=self.opt['dropout']),
            nn.Linear(self.nb_units_personas, self.hidden_dim),
        ]
        self.persona_encoder = nn.Sequential(*persona_layers)
        # Dialog History (caption, response) Encoder
        if self.share_encoder:
            self.context_encoder = self.label_encoder
        else:
            self.context_encoder = self.build_context_encoder(
                loading_trained, 'context'
            )

    def _create_embeddings(self, dictionary, embedding_size, padding_idx):
        """
        Create and initialize word embeddings.

        NOTE: not in original model, just testing to see if this affects anything
        """
        e = nn.Embedding(len(dictionary), embedding_size, padding_idx)
        nn.init.normal_(e.weight, mean=0, std=embedding_size ** -0.5)
        nn.init.constant_(e.weight[padding_idx], 0)
        return e

    def build_context_encoder(self, loading_trained, opt_key):
        pretrain_emb = 'pretrained_{}_word_emb'.format(opt_key)
        pretrain_enc = 'pretrained_{}_encoder'.format(opt_key)
        embeddings = None
        if (
            self.opt[pretrain_emb]
            and not self.opt[pretrain_enc]
            and not loading_trained
        ):
            embeddings = load_embeddings_from_file(
                word_embedding_file, self.dict, self.opt['word_embeddings_dim']
            )
        elif not self.opt[pretrain_enc]:
            embeddings = self._create_embeddings(
                self.dict,
                self.opt['word_embeddings_dim'],
                self.dict[self.dict.null_token],
            )
        if self.opt['encoder_type'] == 'bow':
            context_encoder = BowEncoder(
                self.opt['word_embeddings_dim'],
                len(self.dict),
                embeddings,
                self.opt['hidden_dim'],
                True,
                self.opt['num_layers_text_encoder'],
                dropout=self.opt['dropout'],
            )
        if self.opt['encoder_type'] == 'transformer':
            if self.opt[pretrain_enc]:
                # the model trained by Pierre-Emmanuel on reddit
                print('loading {} encoder from trained'.format(opt_key))
                if loading_trained:
                    serial = self.opt['transformer_architecture']
                else:
                    serial = torch.load(transformer_file)
                context_encoder = load_transformer_from_reddit_pretrained(serial)
                if not loading_trained:
                    del serial['transformer_state']
                    self.opt['transformer_architecture'] = serial
            else:
                context_encoder = TransformerModel(
                    self.opt['transformer_nb_heads'],
                    self.opt['num_layers_text_encoder'],
                    self.opt['word_embeddings_dim'],
                    len(self.dict),
                    embeddings,
                    dropout=self.opt['dropout'],
                )
            # the model trained by trained by Pierre-Emmanuel on reddit
            # does not have any dropout. Besides, its dimension is constrained
            # to be the one of the word encoding. This adds a layer and
            # remove those constraints
            if self.opt['additional_layer_text']:
                self.additional_layer = LinearWrapper(
                    self.opt['word_embeddings_dim'],
                    self.opt['hidden_dim'],
                    dropout=self.opt['dropout'],
                )
            else:
                self.additional_layer = None

        return context_encoder

    def forward(
        self,
        image_features,
        personas,
        dialog_history,
        labels,
        p_vector=None,
        batchsize=None,
        targets=None,
    ):
        """
            Inputs:
                - image_features: a list of tensor of size M
                - personas: list of string, one per sample
                - dialog_history: newline-concat dialog_history
                - labels: iterable of string targets
                - p_vector: optional: you can provide persona as a
                    variable if you want, (typically a one hot vector,
                    but it might be a distribution too). That might be useful
                    to make reinforcement learning on personas.
                - batchsize: optional: provide batchsize
                - targets: indices of labels, if using inline candidates
            Outputs: (loss, nb_ok, total_encoded)
                - loss: loss
                - nb_ok: how many predictions were correct
                - total_encoded: query encoding

        """
        # labels
        # Check if labels exist and are iterable
        if labels is not None and (
            hasattr(labels[0], '__iter__') and not isinstance(labels[0], str)
        ):
            # inline cands
            labels_encoded = torch.stack(
                [self.forward_text_encoder(l) for l in labels], dim=0
            )
        else:
            labels_encoded = self.forward_text_encoder(labels)

        # dialog history
        d_hist_encoded = self.forward_text_encoder(
            dialog_history, dialog_history=True, batchsize=batchsize
        )
        # images
        img_encoded = self.forward_image(image_features)
        # personas
        pers_encoded = self.forward_persona(personas, len(image_features), p_vector)
        total_encoded = self.get_rep(
            [img_encoded, d_hist_encoded, pers_encoded], batchsize=batchsize
        )
        loss, nb_ok = self.get_loss(total_encoded, labels_encoded, targets=targets)

        return loss, nb_ok, total_encoded

    def forward_persona(self, personas, bsz, p_vector):
        encoder = self.persona_encoder
        if not self.encode_personality:
            if self.multimodal and self.multimodal_combo == 'concat':
                return self.blank_encoding
            return None
        if personas is None:
            personas = ['zzzz'] * bsz
        if p_vector is not None:
            pers_vec = p_vector
        else:
            pers_vec = torch.FloatTensor(len(personas), self.nb_units_personas).fill_(0)
            pers_list = [self.persona_to_id.get(p, 0) + 1 for p in personas]
            for i, index in enumerate(pers_list):
                pers_vec[i, index] = 1  # no personality corresponds to 0
        if self.use_cuda:
            pers_vec = pers_vec.cuda()
        if pers_vec.size(0) == 1:
            encoder = self.persona_encoder[1:]  # skip batchnorm if bs == 1
        return encoder(pers_vec)

    def forward_text_encoder(self, texts, dialog_history=False, batchsize=None):
        if texts is None or (dialog_history and not self.encode_dialog_history):
            if self.multimodal and self.multimodal_combo == 'concat' and dialog_history:
                encoding = torch.stack([self.blank_encoding for _ in range(batchsize)])
                return encoding
            return None
        encoder = self.context_encoder if dialog_history else self.label_encoder
        indexes_var, mask_var = self.list_sentence_to_var(texts)
        texts_encoded = encoder(indexes_var, mask_var)
        if self.text_encoder_frozen:
            texts_encoded = texts_encoded.detach()
        if (
            self.opt['additional_layer_text']
            and self.opt['encoder_type'] == 'transformer'
        ):
            texts_encoded = self.additional_layer(texts_encoded)
        return texts_encoded

    def forward_image(self, image_features):
        encoder = self.image_encoder
        if image_features is None or not self.encode_image:
            if self.multimodal and self.multimodal_combo == 'concat':
                return self.blank_encoding
            return None
        if len(image_features) == 1:
            imgs = image_features[0].unsqueeze(0)
            encoder = self.image_encoder[1:]  # skip batchnorm if bs == 1
        else:
            imgs = torch.stack(image_features)
        if self.use_cuda:
            imgs = imgs.cuda()
        return encoder(imgs)

    def get_rep(self, encodings, batchsize=None):
        if not self.multimodal:
            rep = self.sum(encodings)
        else:
            if self.multimodal_combo == 'sum':
                encodings = self.sum(encodings).unsqueeze(1)
            elif self.multimodal_combo == 'concat':
                encodings = self.cat(encodings)
            all_one_mask = torch.ones(encodings.size()[:2])
            if self.use_cuda:
                all_one_mask = all_one_mask.cuda()
            rep = self.multimodal_encoder(encodings, all_one_mask)
        if rep is None:
            rep = torch.stack([self.blank_encoding for _ in range(batchsize)])
        return rep

    def elect_best_comment(
        self,
        image_features,
        personas,
        dialog_history,
        candidates,
        candidates_encoded=None,
        k=1,
        batchsize=None,
    ):
        """
        Choose the best comment in a list of possible comments. Inputs.

        - image_features: a list of N tensor of size M
        - persona_features: list of N string, one per sample
        - dialog_history: newline-concat list of strings
        - candidates: a list of list of string. Size is N x K, K being the number
          of candidates.
          Note: For now the number of candidates is assumed to be small enough
          that it can fit in one batch.
        - k: how many ranked comments to return
        - batchsize: size of minibatch
        Outputs
         - elected: list of N string, the comment that has been elected
        """
        self.eval()
        _, _, encoded = self.forward(
            image_features, personas, dialog_history, None, batchsize=batchsize
        )
        encoded = encoded.detach()
        one_cand_set = True
        if candidates_encoded is None:
            one_cand_set = False
            candidates_encoded = [
                self.forward_text_encoder(c).detach() for c in candidates
            ]
        elected = [
            self.choose_topk(
                idx, encoded, candidates, candidates_encoded, one_cand_set, k
            )
            for idx in range(len(encoded))
        ]
        return elected

    def choose_topk(
        self, idx, encoded, candidates, candidates_encoded, one_cand_set, k
    ):
        image_vec = encoded[idx : idx + 1, :]
        scores = torch.mm(
            candidates_encoded[idx] if not one_cand_set else candidates_encoded,
            image_vec.transpose(0, 1),
        )
        if k >= 1:
            _, index_top = torch.topk(scores, k, dim=0)
        else:
            _, index_top = torch.topk(scores, scores.size(0), dim=0)
        return [candidates[idx][idx2] for idx2 in index_top.unsqueeze(1)]

    def get_loss(self, total_encoded, labels_encoded, targets=None):
        """
        compute the batch loss and also the number of elements that have been correctly
        classified.
        """
        if labels_encoded is None:
            return None, None
        if labels_encoded.dim() == 3:
            dot_products = torch.bmm(
                total_encoded.unsqueeze(1), labels_encoded.transpose(1, 2)
            ).squeeze(1)
        else:
            dot_products = total_encoded.mm(
                labels_encoded.t()
            )  # batch_size * batch_size
        log_prob = torch.nn.functional.log_softmax(dot_products, dim=1)
        if targets is None:
            targets = torch.arange(0, len(total_encoded), dtype=torch.long)
        else:
            targets = torch.LongTensor(targets)
        if self.use_cuda:
            targets = targets.cuda()
        loss = torch.nn.functional.nll_loss(log_prob, targets)
        nb_ok = (log_prob.max(dim=1)[1] == targets).float().sum()
        return loss, nb_ok

    def freeze_text_encoder(self):
        self.text_encoder_frozen = True

    def unfreeze_text_encoder(self):
        self.text_encoder_frozen = False

    ##################################################
    #     Util Funcs
    ##################################################
    def sum(self, addends):
        addends = [a for a in addends if a is not None]
        return sum(addends) if len(addends) > 0 else None

    def cat(self, tensors):
        tensors = [t for t in tensors if t is not None]
        return torch.cat([t.unsqueeze(1) for t in tensors], dim=1)

    def list_sentence_to_var(self, contexts):
        """
        Transform a list of sentences into a 3D float tensor. Returns (word_indexes,
        mask)

        - var_indexes: (size_batch x max_length_sentence), indexes of word in dict,
                padded with null tokens
        - mask: a float tensor worth (size_batch x max_length_sentence) worth
            1 if the position is actually a word.
        """
        max_length = self.max_length_sentence
        indexes = []
        for c in contexts:
            vec = self.dict.txt2vec(c)
            if len(vec) > max_length:
                vec = vec[:max_length]
            indexes.append(vec)
        longest = max([len(v) for v in indexes])
        res = torch.LongTensor(len(contexts), longest).fill_(
            self.dict.tok2ind[self.dict.null_token]
        )
        mask = torch.FloatTensor(len(contexts), longest).fill_(0)
        for i, inds in enumerate(indexes):
            res[i, 0 : len(inds)] = torch.LongTensor(inds)
            mask[i, 0 : len(inds)] = torch.FloatTensor([1] * len(inds))
        if self.use_cuda:
            res = res.cuda()
            mask = mask.cuda()
        return res, mask

    ##################################################
    #      Load and Save
    ##################################################

    @staticmethod
    def save_model(model, filepath):
        d = {}
        d['state_dict'] = model.state_dict()
        d['opts'] = model.opt
        d['dict'] = model.dict
        d['personas_list'] = model.personas_list
        torch.save(d, filepath)

    @staticmethod
    def load_model(filepath, force_cpu=False, dictionary=None):
        d = torch.load(filepath, map_location='cpu')
        d['opts'] = Opt(**d['opts'])
        if force_cpu:
            d['opts']['no_cuda'] = True
        dict_load = d['dict']
        if dictionary is not None:
            dict_load = dictionary
        model = CommentBattleDialogModelURU(
            d['opts'], d['personas_list'], dict_load, loading_trained=True
        )
        model.load_state_dict(d['state_dict'])
        return model


#########################################
#  Loading Pretrained
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
    tm = TransformerModel(
        serial['transformer_n_heads'],
        serial['transformer_n_layers'],
        serial['transformer_dim'],
        serial['vocabulary_size'],
    )
    if 'transformer_state' in serial:
        tm.load_state_dict(serial['transformer_state'])
    return tm


def load_embeddings_from_file(filepath, dic, embedding_dim):
    """
    Helper that loads weights from a file and put them in embeddings.weights.
    """
    print("Initializing embeddings from %s" % filepath)
    # load first as a dictionary
    pretrained = {}
    with open(filepath) as f:
        for line in f:
            line = line[0:-1]
            if line[-1] == ' ':
                line = line[0:-1]
            splited = line.split(" ")
            if len(splited) != embedding_dim + 1:
                continue
            pretrained[splited[0]] = torch.FloatTensor(list(map(float, splited[1:])))
    print(
        "Done Loading vectors from %s. %d embeddings loaded."
        % (filepath, len(pretrained))
    )
    used = 0
    res = nn.Embedding(len(dic), embedding_dim)
    for word in dic.tok2ind.keys():
        index = dic.tok2ind[word]
        if word in pretrained and res.weight.data.shape[0] > index:
            res.weight.data[index] = pretrained[word]
            used += 1
    print("%d have been initialized on pretrained over %d" % (used, len(dic)))
    return res


#########################################
#    Some additional modules
#########################################


class LinearWrapper(nn.Module):
    """
    Adds one linear layer on top of a module.

    This was designed for the transformer, since pretrained instance don't use dropout,
    and they are constrained to keep the dimension of the word embedding.
    """

    def __init__(self, in_dim, out_dim, dropout):
        super(LinearWrapper, self).__init__()
        self.lin = nn.Linear(in_dim, out_dim)
        self.dp = nn.Dropout(dropout)

    def forward(self, input):
        return self.lin(self.dp(input))


class BowEncoder(nn.Module):
    """
    The simplest, sum over words embeddings, take the result trough a DNN.

    It's not exactly the same as provided in transformer.py although very similar
    """

    def __init__(
        self,
        embedding_dim,
        vocabulary_size,
        embeddings=None,
        out_dim=300,
        scale_sqrt=True,
        n_hidden=1,
        dropout=0,
    ):
        """
            Inputs:
                embedding_dim: size of the embeddings
                vocabulary_size: number of embeddings to prepare
                embeddings: embeddings can be provided.
                            If it is the cse, voc size will be ignored
                out_dim: expected size of the output
                scale_sqrt: if true, divides by the square root of the
                            length of sentence otherwise divides by the length
                            of sentence
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
        for _ in range(n_hidden - 1):
            nn_layers.append(nn.Dropout(p=dropout))
            nn_layers.append(nn.Linear(embedding_dim, embedding_dim))
            nn_layers.append(nn.ReLU())
        nn_layers.append(nn.Dropout(p=dropout))
        nn_layers.append(nn.Linear(embedding_dim, out_dim))
        self.proj = nn.Sequential(*nn_layers)

    def forward(self, input, mask):
        input_e = self.embeddings(input)
        last_dim_mask = len(mask.shape) - 1
        scale = mask.sum(last_dim_mask, keepdim=True).clamp(min=1)
        if self.scale_sqrt:
            scale = scale.sqrt()
        # put elements that are masked to 0
        input_masked = input_e * mask.unsqueeze(last_dim_mask + 1)
        bow = input_masked.sum(dim=last_dim_mask) / scale
        out = self.proj(bow)
        return out

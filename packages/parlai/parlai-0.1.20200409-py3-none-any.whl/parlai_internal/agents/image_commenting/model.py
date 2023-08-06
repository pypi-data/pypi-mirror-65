#!/usr/bin/env python3
import numpy as np
import torch
from torch import nn
from torch import FloatTensor, LongTensor
from torch import autograd
from torch import optim


class ImageCaptioning(nn.Module):
    """
        cf https://cs.stanford.edu/people/karpathy/deepimagesent/,
        https://arxiv.org/abs/1411.4555, https://arxiv.org/abs/1612.00563
        Image is inserted as the first word, and then followed by "start".
        A personality may be used for further conditioning the image.
        If it is not provided, only image is used.

        I tried to dissociate the mecanisms of Parlai from
        the model logic to make it easy to test the model
        independently of ParlAI.

        This is why this class exposes (allthough nothing is private in python)
        only 4 methods:
            - train_step(imageFeatures, comments, dict, [optionalPersonality]):
                does a train step given a list of image features, some comments
                and a dictionary (a Dictionary Agent)
            - generate(imageFeatures, dict, [optionalPersonality], [parameters])
                create new sentences from a list of image features using beam
                search
            - getPerplexity(imageFeatures, comments, dict, [optionalPersonality]):
                compute the perplexity on every pair imageFeature - comment.
                returns an array of perplexity pf the size of imageFeatures
            - choose_best_candidate
        All 3 methods assume the size of the batch is reasonble to send over the
        computing device.
        Every other method is an helper that is not really meant to be called
        (well except constructor)

    """

    ############################################################
    #  Methods that are meant to be used by the external world #
    ############################################################

    def train_step(self, image_features, comments, dic, personality=None):
        """
            does a train step given a list of image features, some comments
            and a dictionary (a Dictionary Agent)
        """
        # create a batch. Note: this will reorder the batch so that
        # the longest sentence comes first, to use pad_pack

        xs, ys, ys_mask, ordering, lengths = self.comments_to_batch(comments, dic)
        comments = permut(comments, ordering)
        image_features = permut(image_features, ordering)
        num_elements = torch.sum(ys_mask)
        personality = permut(personality, ordering)
        image_features_torch = self.to_torch_feature_vector(image_features, personality)

        total_words = len(xs) * len(image_features)
        self.train()  # training mode: dropout is not ignored
        self.zero_grad()
        x_var = self.to_var(xs)
        y_var = self.to_var(ys)
        mask_var = self.to_var(ys_mask)
        img_var = self.to_var(image_features_torch)
        self.feed_image(img_var)  # feed the image
        word_scores = self.forward(x_var)
        loss_unreduced = nn.CrossEntropyLoss(reduce=False)(
            word_scores.view(total_words, -1), y_var.view(total_words)
        )
        loss_reshaped = loss_unreduced.view(len(xs), len(image_features))
        loss_reshaped_masked = torch.mul(
            loss_reshaped, mask_var
        )  # they should be the same dimension
        loss = torch.sum(loss_reshaped_masked) / num_elements
        loss.backward()
        self.optimizer.step()

        # format output so that we also have the detail per sentence.
        lp, num_words, detail = self.get_detailed_ppl(loss_reshaped.cpu().data, ys_mask)
        # let's not forget to reorder the detail of the log perplexity
        detail = unpermut(detail, ordering)
        return lp, num_words, detail

    def generate(
        self,
        image_features,
        dic,
        temperature=0.1,
        allow_unk=False,
        top_k=-1,
        personality=None,
    ):
        """
            Generate a sentences. At each step the next word
            is probabilistically decided following the softmax with temperature
            temperature: temperature of the Softmax
            top_k: if not -1, will select the best among the top_k instead of among all the possibilities

            Return an array of sentences that correspond to the image features.

            TODO: implement beam search
        """
        self.eval()
        image_features_torch = self.to_torch_feature_vector(image_features, personality)

        img_var = self.to_var(image_features_torch)
        self.feed_image(img_var)
        START_IDX = dic.tok2ind[dic.start_token]
        END_IDX = dic.tok2ind[dic.end_token]
        NULL_IDX = dic.tok2ind[dic.null_token]
        UNK_IDX = dic.tok2ind[dic.unk_token]
        size_vocabulary = len(dic.tok2ind)

        # create a vector that is =1000 for UNK_IDX, 0 otherwise
        np_base = np.zeros((1, 1, size_vocabulary))
        np_base[0][0][UNK_IDX] = -10000
        unk_mask = self.to_var(torch.FloatTensor(np_base))

        next = self.get_starters(dic, len(image_features))
        all_indexes = [[] for _ in range(len(image_features))]
        num_samples = len(image_features)
        done = set()
        for _ in range(self.truncate_length):
            next_var = self.to_var(next)
            word_scores = self.forward(next_var) * (1.0 / (temperature + 0.02))
            word_scores_no_unk = word_scores + unk_mask

            # if we consider only the topK, we do it here before the Softmax
            if top_k != -1:
                top_word_scores_no_unk, top_k_index = torch.topk(
                    word_scores_no_unk, top_k, 2, largest=True
                )
                top_k_indexes = top_k_index.data.cpu().numpy()
            else:
                top_word_scores_no_unk = word_scores_no_unk
            word_probas = torch.nn.Softmax(dim=2)(top_word_scores_no_unk)
            word_probas_numpy = word_probas.data.cpu().numpy()
            # for every stream, choose a word
            next_np = np.zeros((1, len(image_features)))
            for j in range(num_samples):
                if top_k != -1:
                    top_k_index = top_k_indexes[0, j, :]
                else:
                    top_k_index = np.arange(size_vocabulary)
                vec_prob = word_probas_numpy[0][j]
                choice = np.random.choice(top_k_index, 1, p=vec_prob)
                next_np[0][j] = choice[0]
                leng = len(all_indexes[j])
                if leng == 0 or all_indexes[j][leng - 1] != END_IDX:
                    if choice == NULL_IDX or choice == START_IDX:
                        all_indexes[j].append(END_IDX)
                    else:
                        all_indexes[j].append(choice[0])
                    if all_indexes[j][leng] == END_IDX:
                        done.add(j)
            if len(done) == num_samples:
                break
            next = torch.LongTensor(next_np)
        # Now we have our indexes. Produce a sentence for each of them
        result = []
        for list_indexes in all_indexes:
            result.append(dic.vec2txt(list_indexes))
        return result

    def get_log_perplexity(
        self, image_features, comments, dic, personality=None, debug=False
    ):
        """
            Return
            lp     : the sum of the log perplexity evaluated over all the words
            num_words: the number of words used for the evaluation
            per_image: a list of (lp, num_words) which is the the detail
                       per image for the perplexity.
        """
        xs, ys, ys_mask, ordering, lengths = self.comments_to_batch(comments, dic)
        comments = permut(comments, ordering)
        image_features = permut(image_features, ordering)
        personality = permut(personality, ordering)
        image_features_torch = self.to_torch_feature_vector(image_features, personality)

        total_words = len(xs) * len(image_features)
        self.eval()
        x_var = self.to_var(xs)
        y_var = self.to_var(ys)
        img_var = self.to_var(image_features_torch)
        self.feed_image(img_var)  # feed the image
        word_scores = self.forward(x_var)
        loss_unreduced = nn.CrossEntropyLoss(reduce=False)(
            word_scores.view(total_words, -1), y_var.view(total_words)
        )
        loss_reshaped = loss_unreduced.view(len(xs), len(image_features))

        # format output so that we also have the detail per sentence.
        lp, num_words, detail = self.get_detailed_ppl(loss_reshaped.cpu().data, ys_mask)
        if debug:
            self.print_out_loss_per_word(loss_reshaped.cpu().data, ys, ys_mask, dic)

        # let's not forget to reorder the detail of the log perplexity
        detail = unpermut(detail, ordering)
        return lp, num_words, detail

    def choose_best_candidate(self, image_features, candidates, dic, personality=None):
        """
            For each image of the batch, chooses the right candidate.
            For now assumes that the number of candidates is always the same.
            process efficiently by assuming the size of image_features
            is appropriate to run on GPU.

            The right candidate is the one that minimizes perplexity per word.
            image_features: the image features, size_minibatch * len(features)
            candidates: size_minibatch * nb_candidates, strings

            returns:
                best_cands: the list of best candidates
                perplexities: the perplexity per word observed for each candidate
        """
        assert len(candidates) == len(
            image_features
        ), "candidates must have the same length as image_features"
        nb_candidates = len(candidates[0])
        for candidate in candidates:
            assert (
                len(candidate) == nb_candidates
            ), "The number of candidates must be the same for each image"
        perplexities = np.zeros((len(image_features), nb_candidates))
        for i in range(nb_candidates):
            # concatemate the i-th candidate for each image
            ith_candidates = [candidate[i] for candidate in candidates]
            a, b, details = self.get_log_perplexity(
                image_features, ith_candidates, dic, personality=personality
            )
            details_array = np.asarray(details, dtype=float)
            # details is get_log_perplexity and number of words
            ith_perplexity = details_array[:, 0] * details_array[:, 1]
            perplexities[:, i] = ith_perplexity
        # get the candidate that maximize perplexity
        index_best = np.argmin(perplexities, 1)
        return (
            [candidates[i][index_best[i]] for i in range(len(candidates))],
            perplexities,
        )

    def __init__(
        self,
        embedding_dim=256,
        hidden_dim=256,
        image_features_dim=2048,
        personality_features_dim=0,
        num_layers=2,
        vocab_size=10000,
        truncate_length=50,
        dropout=0.0,
        use_cuda=True,
        adam_alpha=0.0005,
        use_pictures=True,
        feed_state=False,
        preprocess_image_features=False,
        use_batch_norm_for_pics=False,
        use_gru=False,
        concatenate_image_each_word=False,
        dropout_embed_layer=False,
    ):
        super(ImageCaptioning, self).__init__()

        self.num_layers = num_layers
        self.use_cuda = use_cuda
        self.truncate_length = truncate_length
        self.use_pictures = use_pictures
        self.personality_features_dim = personality_features_dim
        self.concatenate_image_each_word = concatenate_image_each_word
        assert (
            not concatenate_image_each_word or not feed_state
        ), "feed_state=True\
            and concatenate_image_each_word=True are incompatible"
        # We project the image like some sort of embedding
        self.feed_state = feed_state
        self.preprocess_image_features = preprocess_image_features
        self.use_batch_norm_for_pics = use_batch_norm_for_pics

        if preprocess_image_features:
            self.preprocessing_linear = nn.Linear(
                image_features_dim + personality_features_dim,
                image_features_dim + personality_features_dim,
            )
            self.preprocessing_relu = nn.ReLU()
            self.preprocessing_dropout = nn.Dropout(p=dropout)
            self.preprocessing_bn = nn.BatchNorm1d(
                image_features_dim + personality_features_dim
            )

        if self.feed_state:
            # feed directly in the state
            self.image_projection1 = nn.Linear(
                image_features_dim + personality_features_dim, hidden_dim * num_layers
            )
            self.image_projection2 = nn.Linear(
                image_features_dim + personality_features_dim, hidden_dim * num_layers
            )
            self.image_projection_bn1 = nn.BatchNorm1d(hidden_dim * num_layers)
            self.image_projection_bn2 = nn.BatchNorm1d(hidden_dim * num_layers)
            self.image_projection_dropout1 = nn.Dropout(p=dropout)
            self.image_projection_dropout2 = nn.Dropout(p=dropout)
        else:
            self.image_projection = nn.Linear(
                image_features_dim + personality_features_dim, embedding_dim
            )
            self.image_projection_bn = nn.BatchNorm1d(embedding_dim)
            self.image_projection_dropout = nn.Dropout(p=dropout)
        self.dropout_embed_layer = dropout_embed_layer
        if dropout_embed_layer:
            self.dropout_embeds = nn.Dropout()

        # output dropout
        self.dropout2 = nn.Dropout(p=dropout)

        # Create words embeddings
        self.hidden_dim = hidden_dim
        self.word_embeddings = nn.Embedding(vocab_size, embedding_dim)

        # The LSTM takes word embeddings as inputs, and outputs hidden states
        # with dimensionality hidden_dim.
        true_embedding_dim = embedding_dim
        if concatenate_image_each_word:
            true_embedding_dim *= 2
        self.lstm = nn.LSTM(true_embedding_dim, hidden_dim, num_layers, dropout=dropout)

        # The linear layer that maps from hidden state space to tag space
        self.hidden2Word = nn.Linear(hidden_dim, vocab_size)
        self.reset_hidden(10)

        # optimizer
        self.optimizer = optim.Adam(self.parameters(), adam_alpha)

    def initialize_word_embeddings(self, wordvec_filepath, dic):
        """
            Intializes the embeddings using.
            Expect the file of the word vec to be of the usual style, where
            words are separated by a space.
            Expect dic to be the dictionary used.
        """
        print("Initializing embeddings")

        def load_wordvecs(filepath):
            word2vec = {}
            with open(filepath) as f:
                for line in f:
                    splited = line.split(" ")
                    word2vec[splited[0]] = torch.FloatTensor(
                        list(map(float, splited[1:]))
                    )
            return word2vec

        pretrained = load_wordvecs(wordvec_filepath)
        print("Done Loading vectors from %s" % wordvec_filepath)
        for word in dic.tok2ind.keys():
            index = dic.tok2ind[word]
            if word in pretrained and self.word_embeddings.weight.data.shape[0] > index:
                self.word_embeddings.weight.data[index] = pretrained[word]
        print("Done Initializing embeddings")

    def set_optimizer(self, optimizer):
        self.optimizer = optimizer

    def from_another_model(self, original):
        """
            copy all parameters from another model. May be useful to solve
            deserialization issues.
        """
        self.num_layers = original.num_layers
        self.use_cuda = original.use_cuda
        self.truncate_length = original.truncate_length
        self.use_pictures = original.use_pictures
        self.image_projection = original.image_projection
        self.image_projection_dropout = original.image_projection_dropout
        self.dropout2 = original.dropout2
        self.hidden_dim = original.hidden_dim
        self.word_embeddings = original.word_embeddings
        self.lstm = original.lstm
        self.hidden2Word = original.hidden2Word
        self.optimizer = original.optimizer

    ############################################################
    #                     Helpers                              #
    ############################################################

    def reset_hidden(self, size_minibatch):
        """
            clear the hidden state. Typically done if we are going to
            feed an image.
        """
        self.hidden = (
            autograd.Variable(
                torch.zeros(self.num_layers, size_minibatch, self.hidden_dim)
            ),
            autograd.Variable(
                torch.zeros(self.num_layers, size_minibatch, self.hidden_dim)
            ),
        )
        if self.use_cuda:
            self.hidden = (self.hidden[0].cuda(), self.hidden[1].cuda())

    def to_torch_feature_vector(self, image_features, personality):
        """
            image features and the optional personality are
            a list of torch tensor. Merge them is needed
            and produce a single torch tensor.
        """
        image_features_torch = torch.cat(
            [torch.unsqueeze(feat, 0) for feat in image_features]
        )
        # If user provides a personality, we simply concatenate it to the image features
        assert (
            not hasattr(self, 'personality_features_dim')
            or self.personality_features_dim == 0
            or personality is not None
        ), "A personality has been declared for this model. It is therefore necessary to feed it."
        if personality is not None:
            assert len(image_features) == len(
                image_features
            ), "There should be as many personalities as there are image features"
            assert (
                len(personality[0]) == self.personality_features_dim
            ), "The size of the personality should be compatible with what has been declared during init"
            image_features_torch = torch.cat(
                [
                    image_features_torch,
                    torch.cat([torch.unsqueeze(feat, 0) for feat in personality]),
                ],
                1,
            )
        return image_features_torch

    def feed_image(self, image_features):
        """
            Feed the image as the word at time ''-1', or if self.feed_state
            transform the image to be the state
        """
        size_minibatch = len(image_features)
        if self.preprocess_image_features:
            image_features_after_lin = self.preprocessing_linear(image_features)
            if self.use_batch_norm_for_pics:
                image_features_after_lin = self.preprocessing_bn(
                    image_features_after_lin
                )
            image_features_t = self.preprocessing_relu(
                self.preprocessing_dropout(image_features_after_lin)
            )
        else:
            image_features_t = image_features
        self.reset_hidden(size_minibatch)
        if self.use_pictures:
            if self.feed_state:
                proj1 = self.image_projection1(image_features_t)
                proj2 = self.image_projection2(image_features_t)
                if self.use_batch_norm_for_pics:
                    proj1 = self.image_projection_bn1(proj1)
                    proj2 = self.image_projection_bn2(proj2)
                dropped1 = self.image_projection_dropout1(proj1)
                dropped2 = self.image_projection_dropout2(proj2)
                reshaped1 = (
                    dropped1.view(size_minibatch, self.num_layers, self.hidden_dim)
                    .permute(1, 0, 2)
                    .contiguous()
                )
                reshaped2 = (
                    dropped2.view(size_minibatch, self.num_layers, self.hidden_dim)
                    .permute(1, 0, 2)
                    .contiguous()
                )
                self.hidden = (reshaped1, reshaped2)
            else:
                proj = self.image_projection(image_features_t)
                if self.use_batch_norm_for_pics:
                    proj = self.image_projection_bn(proj)
                with_additional_dim = torch.unsqueeze(proj, 0)
                dropped = self.image_projection_dropout(with_additional_dim)
                if self.concatenate_image_each_word:
                    self.current_image_as_word = dropped
                else:
                    lstm_out, self.hidden = self.lstm(dropped, self.hidden)

    def forward(self, inputs, lengths=None):
        embeds = self.word_embeddings(inputs)
        if self.dropout_embed_layer:
            embeds = self.dropout_embeds(embeds)
        if self.concatenate_image_each_word:
            replicated_image_as_word = self.current_image_as_word.expand(
                len(embeds), -1, -1
            )
            embeds = torch.cat([embeds, replicated_image_as_word], 2)
        if lengths is None:
            lstm_out, self.hidden = self.lstm(embeds, self.hidden)
        else:
            packed = torch.nn.utils.rnn.pack_padded_sequence(
                embeds, lengths, batch_first=False
            )
            lstm_out_packed, self.hidden = self.lstm(packed, self.hidden)
            lstm_out, _ = torch.nn.utils.rnn.pad_packed_sequence(lstm_out_packed)
        dropped = self.dropout2(lstm_out)
        word_space = self.hidden2Word(dropped)
        return word_space

    def comments_to_batch(self, comments, dic):
        """
            Inspired by core.utils.PadUtils, produces a tuple:
            xs : index of tokens in input. shape is (sentence_length + 1) x batch_length
                 they all start with START_IDX. Padded using NULL_IDX
            ys : index of tokens of output. shape is (sentence_length + 1) x batch_length
                 they all end with END_IDX
            ys_mask: size size as ys, is worth 1 if not null
            ordering: we've permuted the sentences, so that the longest comes first
            lengths: the length of each sentence, decreasing order.
        """
        START_IDX = dic.tok2ind[dic.start_token]
        END_IDX = dic.tok2ind[dic.end_token]
        NULL_IDX = dic.tok2ind[dic.null_token]
        batch_size = len(comments)
        vecs = []
        lengths = []
        max_sentence_length = -1
        for comment in comments:
            vec = dic.txt2vec(comment)
            if self.truncate_length != -1 and len(vec) > self.truncate_length:
                vec = vec[0 : self.truncate_length]
            vecs.append(vec)
            lengths.append(len(vec) + 1)
            max_sentence_length = max(len(vec), max_sentence_length)
        ordering = sorted(range(len(lengths)), key=lambda k: -lengths[k])
        vecs = permut(vecs, ordering)
        lengths = permut(lengths, ordering)
        # the resulting vectors have an additional dimension because we
        # pad using the start token for the input, and we pad using the
        # end token for the output
        shape = (max_sentence_length + 1, batch_size)
        xs = LongTensor(shape[0], shape[1]).fill_(NULL_IDX)
        ys = LongTensor(shape[0], shape[1]).fill_(NULL_IDX)
        ys_mask = FloatTensor(shape[0], shape[1]).fill_(0.0)
        for i in range(batch_size):
            xs[0, i] = START_IDX
        for i in range(len(vecs)):
            vec = vecs[i]
            for j in range(len(vec)):
                xs[j + 1, i] = vec[j]
                ys[j, i] = vec[j]
                ys_mask[j, i] = 1.0
            ys[len(vec), i] = END_IDX
            ys_mask[len(vec), i] = 1.0
        return xs, ys, ys_mask, ordering, lengths

    def get_detailed_ppl(self, loss_per_word, ys_mask):
        """
        Inputs:
            - loss_per_word: FloatTensor(sentence_length, size_batch)
            - ys_mask: FloatTensor(sentence_length, size_batch), 0 if there is
                       not a word, 1 otherwise.
        Outputs:
            - log_ppl: log of the perplexity (average)
            - num_words: the number of words
            - details: list of tuples (log_ppl, num_words), one for each sentence
        """
        sum_log_ppl = torch.sum(loss_per_word * ys_mask)
        number_of_elements = torch.sum(ys_mask)
        log_ppl = sum_log_ppl / number_of_elements
        detail = []
        sum_log_ppl_per_sentence = torch.sum(loss_per_word * ys_mask, 0)
        num_words_per_sentence = torch.sum(ys_mask, 0)
        log_ppl_per_sentence = torch.div(
            sum_log_ppl_per_sentence, num_words_per_sentence
        )
        for i in range(len(log_ppl_per_sentence)):
            detail.append((log_ppl_per_sentence[i], num_words_per_sentence[i]))
        return log_ppl, number_of_elements, detail

    def get_starters(self, dic, size_minibatch):
        """
            Generates a torch tensor full of __START__
        """
        START_IDX = dic.tok2ind[dic.start_token]
        return torch.LongTensor(np.full((1, size_minibatch), START_IDX, dtype=int))

    def to_var(self, torch_tensor, requires_grad=False):
        if self.use_cuda:
            return autograd.Variable(torch_tensor, requires_grad=requires_grad).cuda()
        return autograd.Variable(torch_tensor, requires_grad=requires_grad)

    def print_out_loss_per_word(self, loss_per_word, ys, ys_mask, dic):
        log_ppl, number_of_elements, detail = self.get_detailed_ppl(
            loss_per_word, ys_mask
        )
        for i in range(len(loss_per_word[0])):
            text = ""
            for j in range(len(loss_per_word)):
                if ys_mask[j][i] == 1.0:
                    text += "(%s, %.2f)" % (dic.ind2tok[ys[j][i]], loss_per_word[j][i])
            text += " --> %.3f (%d)" % (detail[i][0], detail[i][1])
            print(text)


##################################
#   Some other helpers
#################################


def permut(list_to_permut, permutation):
    if list_to_permut is None:
        return None
    return [list_to_permut[i] for i in permutation]


def unpermut(list_to_unpermut, permutation):
    inverse = [0] * len(permutation)
    for i, p in enumerate(permutation):
        inverse[p] = i
    return [list_to_unpermut[i] for i in inverse]

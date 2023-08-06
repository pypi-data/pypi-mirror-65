#!/usr/bin/env python3
# Deals with all the embedding part, where a text, or list of text is converted to
# a tensor
import torch
from torch import nn
from torch import autograd

class TextTokens(nn.Module):

    def __init__(self, no_cuda, dic, max_length_sentence=32):

        super(TextTokens, self).__init__()
        self.dic = dic
        self.no_cuda = no_cuda
        self.max_length_sentence = max_length_sentence

    def list_sentence_to_var(self, contexts):
        """
            Transform a list of sentences into a 3D float tensor.
            Returns (word_indexe, mask)
            - var_indexes: (size_batch x max_length_sentence), indexes of word in dic,
                    padded with null tokens
            - mask: a float tensor worth (size_batch x max_length_sentence) worth
                1 if the position is actually a word.
        """
        max_length = self.max_length_sentence
        local_max = 0
        indexes = []
        for c in contexts:
            vec = self.dic.txt2vec(c)
            if len(vec) > max_length:
                vec = vec[max_length]
            indexes.append(self.dic.txt2vec(c))
        longest = max([len(v) for v in indexes])
        res = torch.LongTensor(len(contexts), longest).fill_(self.dic.tok2ind[self.dic.null_token])
        mask = torch.FloatTensor(len(contexts), longest).fill_(0)
        for i, inds in enumerate(indexes):
            res[i, 0:len(inds)] = torch.LongTensor(inds)
            mask[i, 0:len(inds)] = torch.FloatTensor([1] * len(inds))
        var_indexes = self.tensor_to_var(res, self.no_cuda)
        var_mask = self.tensor_to_var(mask, self.no_cuda)
        return var_indexes, var_mask

    def tensor_to_var(self, tensor, no_cuda=False):
        var_ = autograd.Variable(tensor,  requires_grad=False)
        if not no_cuda:
            var_ = var_.cuda()
        return var_


def load_embeddings_from_file(filepath, dic, embedding_dim):
    """
        Helper that loads weights from a file and put them in embeddings.weights
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
    print("Done Loading vectors from %s. %d embeddings loaded." % (filepath, len(pretrained)))
    used = 0
    res = nn.Embedding(len(dic), embedding_dim)
    for word in dic.tok2ind.keys():
        index = dic.tok2ind[word]
        if word in pretrained and res.weight.data.shape[0] > index:
            res.weight.data[index] = pretrained[word]
            used += 1
    print("%d have been initialized on pretrained over %d" % (used, len(dic)))
    return res

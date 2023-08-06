#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

r"""
Take a numbered dialogue example input from ConvAI, decode into example output.

.. code-block:: bash
    python examples/train_model.py -t internal:largemem_gen_numbered \
        --model internal:largemem_gen/numbered \
        --num_exs 131313 \
        -exsz 256 -emb fasttext \
        --batchsize 32 -lr 0.5 \
        --dict-file /checkpoint/parlai/dicts/20190222_bpelower_ost+toronto+wiki/dict \
        --dict-tokenizer bpe --dict-lower True \
        -stim 300
"""

import os

import torch
import torch.nn as nn
import torch.nn.functional as F
import parlai.core.torch_generator_agent as tga

class Encoder(nn.Module):
    """
    Embed utterance id.
    """
    def __init__(self, ex_embeddings):
        super().__init__()
        _num_ex, _ = ex_embeddings.weight.shape
        self.ex_embeddings = ex_embeddings

    def forward(self, input_exs):
        """
        :param input_exs:
            The example ids of size [bsz, 1].
        """
        emb = self.ex_embeddings(input_exs.squeeze(1))  # [bsz, emb_sz]
        return emb

class Decoder(nn.Module):
    """
    GRU to decode into target output utterance. Intial hidden state
    is the embedded utterance id from the Encoder.
    """

    def __init__(self, word_emb_size, hidden_size, word_embeddings):
        super().__init__()
        self.gru = nn.GRU(
            input_size=word_emb_size,
            hidden_size=hidden_size,
            batch_first=True
        )
        _vocab_size, word_emb_size = word_embeddings.weight.shape
        self.word_embeddings = word_embeddings
        self.lin_out = nn.Linear(hidden_size, word_emb_size)

    def forward(self, input, encoder_state, incr_state=None):
        """
        Run forward pass.
        :param input:
            The currently generated tokens from the decoder.
        :param encoder_state:
            The output from the encoder module.
        :param incr_state:
            The previous hidden state of the decoder.
        """
        if incr_state is None:
            # this is our very first call. We want to seed the GRU with the
            # hidden state of the decoder
            state = encoder_state       # [bsz, emb_sz]
            state = state.unsqueeze(0)  # [1, bsz, emb_sz]  (num_direc * num_layers, bsz, emb_sz)
        else:
            # We've generated some tokens already, so we can reuse the existing
            # decoder state
            state = incr_state

        # Get the new output and decoder incremental state
        input_emb = self.word_embeddings(input)
        output, incr_state = self.gru(input_emb, state)  # [bsz, seq_len, hid], [1, bsz, emb_sz]
        output = self.lin_out(output)  # [bsz, seq_len, wsz]
        return output, incr_state

class NumberedModel(tga.TorchGeneratorModel):
    def __init__(self, dictionary, num_exs=None, ex_emb_size=256, word_emb_size=300):
        super().__init__(
            padding_idx=dictionary[dictionary.null_token],
            start_idx=dictionary[dictionary.start_token],
            end_idx=dictionary[dictionary.end_token],
            unknown_idx=dictionary[dictionary.unk_token]
        )
        self.ex_embeddings = nn.Embedding(num_exs, ex_emb_size)
        self.word_embeddings = nn.Embedding(len(dictionary), word_emb_size)
        self.encoder = Encoder(self.ex_embeddings)
        self.decoder = Decoder(word_emb_size, ex_emb_size, self.word_embeddings)

    def output(self, decoder_output):
        """Perform the final output -> logits transformation."""
        output = F.linear(decoder_output, self.word_embeddings.weight)  # [bsz, seq_len, vocab]
        return output

    def reorder_encoder_states(self, encoder_states, indices):
        """
        Reorder the encoder states to select only the given batch indices.

        Since encoder_state can be arbitrary, you must implement this yourself.
        Typically you will just want to index select on the batch dimension.
        """
        return encoder_states[:, indices]

    def reorder_decoder_incremental_state(self, incr_state, indices):
        """
        Reorder the decoder states to select only the given batch indices.

        This method can be a stub which always returns None; this will result in
        the decoder doing a complete forward pass for every single token, making
        generation O(n^2). However, if any state can be cached, then this method
        should be implemented to reduce the generation complexity to O(n).
        """
        return incr_state[:,indices,:]


class NumberedAgent(tga.TorchGeneratorAgent):

    def __init__(self, opt, shared=None):
        super().__init__(opt, shared)

    @classmethod
    def add_cmdline_args(cls, argparser):
        super(NumberedAgent, cls).add_cmdline_args(argparser)

        group = argparser.add_argument_group('Numbered TGA Agent')
        
        # In this simplest model, --ex-emb-size and --hidden-size must be
        # the same dimension. The embedding layer in the Encoder is
        # [num_exs, ex-emb-size]. This is then used as the hidden state
        # of the Decoder GRU.
        group.add_argument(
            '-exsz', '--ex-emb-size', type=int, default=256,
            help='Embedding size of one dialogue example. Must be equal to -hid.'
        )
        group.add_argument(
            '-wsz', '--word-emb-size', type=int, default=300,
            help='Word embedding size (for decoder)'
        )
        group.add_argument(
            '-nexs', '--num_exs', type=int, default=131313,
            help='Number of examples in training set (131313).'
        )

    def build_model(self):
        """Construct the model."""
        self.model = NumberedModel(self.dict,
            self.opt['num_exs'], self.opt['ex_emb_size'], self.opt['word_emb_size'])

        # We're responsible for setting the embeddings ourselves, but TorchAgent
        # gives us a nice helper
        if self.opt['embedding_type'] != 'random':
            # Copying embeddings is slow. Only do so when training. Otherwise, weights
            # will be loaded after build_model() is called
            if (self.opt['datatype'].startswith('train')) and \
                (not self.opt['datatype'].startswith('train:evalmode')):
                self._copy_embeddings(
                    self.model.tsfrmr_encoder.embeddings.weight, self.opt['embedding_type']
                )

        if self.use_cuda:
            self.model.cuda()

    def _set_text_vec(self, obs, history, truncate):
        """Override _set_text_vec in core/torch_agent.py to have input vector be example id"""
        utt_id = int(obs['text'])
        text_vec = torch.LongTensor([utt_id])
        obs['text_vec'] = text_vec
        return obs

    def _init_cuda_buffer(self, batchsize, maxlen, force=False):
        """Overriding right now because this throws an error when default implementation
        throws an error when passing through dummy batch. Not sure why"""
        pass

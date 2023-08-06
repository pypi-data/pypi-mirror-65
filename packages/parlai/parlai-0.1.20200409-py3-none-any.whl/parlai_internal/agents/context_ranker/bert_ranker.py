#!/usr/bin/env python3

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
"""Simple agent which chooses a random label.

Chooses from the label candidates if they are available.
If candidates are not available, it repeats the label.
"""

import random
import json
import torch
import os.path
import tqdm
import pdb
from parlai.core.agents import Agent
from parlai.utils.misc import round_sigfigs
from .bert_helpers import (
    BertWrapper,
    create_biencoders_from_options,
    create_crossencoder_from_options,
    sentences_to_embedding_wrapper,
    sentences_pairs_to_embedding_wrapper,
    get_bert_optimizer,
)


class BertRankerAgent(Agent):
    """Agent returns random candidate if available or repeats the label."""

    @staticmethod
    def add_cmdline_args(parser):
        """Add command line arguments for this agent."""
        parser = parser.add_argument_group('RandomCandidateAgent Arguments')
        parser.add_argument(
            '--encoder-type',
            type=str,
            default=None,
            choices=["biencoder", "crossencoder", "both", "debug"],
            help='type of encoder, crossencoder or biencoder',
        )
        parser.add_argument(
            '--model-file-path', type=str, default=None, help='path to pretrain model'
        )
        parser.add_argument(
            '--crossencoder-batchsize',
            type=int,
            default=-1,
            help='crossencoder will be fed those many elements at train or eval time.',
        )
        parser.add_argument(
            '--history-length',
            type=int,
            default=5,
            help='Number of previous line to keep for inference',
        )
        parser.add_argument(
            '--num-samples',
            type=int,
            default=131800,
            help='Number of samples in the task (temporary)',
        )
        parser.add_argument(
            '--learning-rate', type=float, default=5e-5, help='Learning rate'
        )
        parser.add_argument(
            '--with-personality',
            type="bool",
            default=True,
            help="Should we use the personality for inference.",
        )
        parser.add_argument('--bert-id', type=str, default='bert-base-uncased')
        parser.add_argument(
            '--add-transformer-layer',
            type="bool",
            default=False,
            help="We do add a linear layer on top of Bert. Should we also add a transformer layer",
        )
        parser.add_argument(
            '--pull-from-layer',
            type=int,
            default=-1,
            help="Which layer of Bert do we use? Default=-1=last one.",
        )
        parser.add_argument(
            '--predefined-candidates-path',
            type=str,
            default=None,
            help="Path to a list of candidates",
        )
        parser.add_argument(
            '--token-cap', type=int, default=340, help="Cap number of tokens"
        )
        parser.add_argument(
            '--topn-both',
            type=int,
            default=10,
            help="In the case where 'both' is used as encoder, select the topn candidates"
            + " from the biencoder",
        )
        parser.add_argument('--no-cuda', type="bool", help="required for TorchAgent")
        parser.add_argument(
            '--type-optimization',
            type=str,
            default="additional_layers",
            choices=[
                "additional_layers",
                "top_layer",
                "top4_layers",
                "all_encoder_layers",
                "all",
            ],
            help="Which part of the encoders do we optimize. (Default is only the top one.)",
        )

    def __init__(self, opt, shared=None):
        """Initialize this agent."""
        self.id = 'BertRankerAgent'
        self.history = []
        self.persona = []
        self.cap = opt["token_cap"]
        self.encoder_type = opt["encoder_type"]
        self.opt = opt
        self.path_to_model = opt["model_file_path"]
        self.path_to_options = self.path_to_model + ".opts"
        self.with_personality = opt["with_personality"]
        self.history_length = opt["history_length"]
        self.predef_cands_path = opt["predefined_candidates_path"]
        self.topn_both = opt["topn_both"]

        # by default the batch size used for cross encoder is the same
        # as the regular batchsize if not precised.
        self.crossencoder_batchsize = opt["crossencoder_batchsize"]
        if self.crossencoder_batchsize == -1 and "batchsize" in opt:
            self.crossencoder_batchsize = opt["batchsize"]

        self.history = []
        self.metrics = {
            'biencoder_loss': 0.0,
            'crossencoder_loss': 0.0,
            'total_biencoder': 0.0,
            'total_crossencoder': 0.0,
        }

        # What follows is only in the main agent.
        if shared is not None:
            self.metrics = shared['metrics']
            return

        # If this option file exists, the model has already been trained and
        # we should load the state.
        if os.path.exists(self.path_to_options):
            with open(self.path_to_options, 'r') as f:
                model_options = json.loads(f.read())
            self.load_weights = True
        else:
            model_options = opt
            self.load_weights = False

        # Initialize the model and load the weights if needed
        self.models = []
        if self.encoder_type == "biencoder" or self.encoder_type == "both":
            self.tokenizer, self.enc_context, self.enc_candidates = create_biencoders_from_options(
                model_options
            )
            self.models += [self.enc_context, self.enc_candidates]
            if self.load_weights:
                print("Loading the weights into model")
                states = torch.load(
                    self.path_to_model, map_location=lambda storage, loc: storage
                )
                self.enc_context.load_state_dict(states['context_encoder_state'])
                self.enc_candidates.load_state_dict(states['candidate_encoder'])
            self.predef_candidates = None
            if self.predef_cands_path is not None:
                self.predef_candidates, self.predef_candidates_vecs = self.load_or_create_embeddings(
                    self.predef_cands_path
                )

        if self.encoder_type == "crossencoder" or self.encoder_type == "both":
            self.tokenizer, self.crossencoder = create_crossencoder_from_options(
                model_options
            )
            self.models += [self.crossencoder]
            if self.load_weights:
                print("Loading the weights into model")
                states = torch.load(
                    self.path_to_model, map_location=lambda storage, loc: storage
                )
                self.crossencoder.load_state_dict(states['encoder'])

        # define the optimizer if needed.
        if "num_epochs" in opt:
            if self.encoder_type == "biencoder" or self.encoder_type == "both":
                self.optim_biencoder = self.prepare_optimizer(
                    [self.enc_context, self.enc_candidates]
                )
            if self.encoder_type == "crossencoder" or self.encoder_type == "both":
                self.optim_crossencoder = self.prepare_optimizer([self.crossencoder])
        super().__init__(opt, {"this is": "a filler"})

    def prepare_optimizer(self, models):
        """ Returns an optimizer. In the case where we train for "both", we might
            want to have one optimizer for biencoders and one optimizer for
            cross encoders.
        """
        total_iterations = opt["num_samples"] * opt["num_epochs"] / opt["batchsize"]
        optim = get_bert_optimizer(
            models,
            opt["type_optimization"],
            total_iterations,
            0.05,  # 5% warmup
            self.opt["learning_rate"],
        )  # 5e-5 learning_rate byd edefault
        return optim

    def observe(self, observation):
        # TODO get rid of that using torch agent
        if "text" not in observation:
            return observation
        self.history.append(observation["text"])

        # quick macro that allows to load the content of a file
        if "load:" in observation["text"]:
            filepath = observation["text"].split(":")[1]
            actual_text = observation["text"].split(":")[2]
            self.history.clear()
            with open(filepath, 'r') as f:
                self.history.append(f.read() + actual_text)
        observation["text"] = "\n".join(self.history)
        if "labels" in observation:
            self.history += observation["labels"]
        elif "eval_labels" in observation:
            self.history += observation["eval_labels"]
        if observation["episode_done"]:
            self.history = []
        return observation

    def act(self):
        # TODO get rid of that using torch agent
        obs = {}
        obs["text"] = "\n".join(self.history)
        predictions = self.batch_act([obs])
        response = predictions[0]["text"]
        self.history.append(response)
        return {"text": response}

    def share(self):
        """Share internal saved_model between parent and child instances."""
        shared = super().share()
        shared['metrics'] = self.metrics
        return shared

    def reset_metrics(self):
        """Reset metrics for reporting loss."""
        self.metrics['biencoder_loss'] = 0.0
        self.metrics['crossencoder_loss'] = 0.0
        self.metrics['total_biencoder'] = 0
        self.metrics['total_crossencoder'] = 0

    def report(self):
        """Report loss from model's perspective."""
        m = {}
        total_biencoder = max(self.metrics['total_biencoder'], 1)
        total_crossencoder = max(self.metrics['total_crossencoder'], 1)
        m['biencoder_loss'] = round_sigfigs(
            self.metrics['biencoder_loss'] / total_biencoder, 4
        )
        m['crossencoder_loss'] = round_sigfigs(
            self.metrics['crossencoder_loss'] / total_crossencoder, 4
        )
        return m

    def load_or_create_embeddings(self, filepath):
        """ loads candidates from filepath. One line = one text cand.
            if filepath + ".vecs" exist, return also the cands.
            Otherwise we create them.
        """
        with open(filepath, 'r') as f:
            cands = [line[0:-1] for line in f]
        vec_path = filepath + ".vecs"
        if os.path.exists(vec_path):
            vecs = torch.load(vec_path).cuda()
            if len(vecs.size()) == 2:
                vecs = vecs.unsqueeze(0)
            return cands, vecs
        print("Candidates are not encoded. Creating their embeddings")
        all_embeds = []
        self.enc_candidates.eval()
        for sents in tqdm.tqdm([cands[i : i + 200] for i in range(0, len(cands), 200)]):
            with torch.no_grad():
                embeds = (
                    sentences_to_embedding_wrapper(
                        self.enc_candidates, self.tokenizer, sents
                    )
                    .detach()
                    .cpu()
                )
            all_embeds.append(embeds)
        all_embeds = torch.cat(all_embeds, 0).unsqueeze(0)
        torch.save(all_embeds, vec_path)
        return cands, all_embeds.cuda()

    def get_context(self, observation, with_personality, length_history):
        """ Concatenate the personality (if required) and the history (up to
            length history) to create the context.
        """
        split = observation["text"].split("\n")
        needle = "your persona:"
        persona = [s.replace(needle, "") for s in split if needle in s]
        history = [s for s in split if needle not in s]
        pieces = []
        if with_personality:
            for p in persona:
                pieces.append(p + " ")
        for i in range(max(0, len(history) - length_history), len(history)):
            pieces.append(" - " + history[i])
        context = "".join(pieces)
        return context

    def biencoder_loss(self, ctx, targets):
        """ Cf paper "training millions of personalized agents"
        """
        assert (
            ctx.size() == targets.size()
        ), f'ctx.size : {ctx.size()}, labels.size: {targets.size()}'
        batch_size = ctx.size(0)
        dot_products = ctx.mm(targets.t())
        log_prob = torch.nn.functional.log_softmax(dot_products, dim=1)
        targets = log_prob.new_empty(batch_size).long()
        targets = torch.arange(batch_size, out=targets)
        loss = torch.nn.functional.nll_loss(log_prob, targets)
        nb_ok = (log_prob.max(dim=1)[1] == targets).float().sum()
        return loss, nb_ok, dot_products

    def crossencoder_loss(self, scores, labels):
        """ cross encoder loss is a classic classification loss.
        """
        log_prob = torch.nn.functional.log_softmax(scores, dim=1)
        loss = torch.nn.functional.nll_loss(log_prob, labels)
        nb_ok = (log_prob.max(dim=1)[1] == labels).float().sum()
        return loss, nb_ok

    def train_batch(self, contexts, candidates, correct_candidates, encoder_type):
        """ - contexts is a list of strings.
            - candidates is a list of list of string. In the case of bi-encoders,
                this will be ignored.
            - correct_candidates is a list of strings of same size as contexts
            - encoder_type is either biencoder or crossencoder. In the case
                where we train both, we won't train both at the same time,
                for simplification
        """
        if self.encoder_type == "debug":
            return correct_candidates
        min_nb_cand = min([len(cands) for cands in candidates])
        max_nb_cand = max([len(cands) for cands in candidates])
        assert (
            min_nb_cand == max_nb_cand
        ), "The number of candidates for each context must be the same."

        [model.train().zero_grad() for model in self.models]
        if self.encoder_type == "biencoder" or self.encoder_type == "both":
            embeddings_context = sentences_to_embedding_wrapper(
                self.enc_context, self.tokenizer, contexts, self.cap
            )  # batch_size x 768
            embeddings_cands = sentences_to_embedding_wrapper(
                self.enc_candidates, self.tokenizer, correct_candidates, self.cap
            )  # batch_size x 768
            loss, nb_ok, scores = self.biencoder_loss(
                embeddings_context, embeddings_cands
            )
            # as a bonus, output prediction (negatives are the other elements of the batch though.)
            _, idx_best = torch.max(scores, dim=1)
            prediction = [correct_candidates[idx] for idx in idx_best]
            loss.backward()
            self.optim_biencoder.step()
            self.metrics["total_biencoder"] += 1
            self.metrics["biencoder_loss"] += loss.cpu().detach().item()

        if self.encoder_type == "crossencoder" or self.encoder_type == "both":
            # In case we are training both (a biencoder and a crossencoder at the
            # same time), we split the big batch into smaller batches
            # so that the iterations of the crossencoder fit in memory.
            prediction = []
            for batchidx in range(0, len(contexts), self.crossencoder_batchsize):
                cands_batch = candidates[
                    batchidx : batchidx + self.crossencoder_batchsize
                ]
                contexts_batch = contexts[
                    batchidx : batchidx + self.crossencoder_batchsize
                ]
                correct_cands_batch = correct_candidates[
                    batchidx : batchidx + self.crossencoder_batchsize
                ]

                [model.train().zero_grad() for model in self.models]
                nb_cands = len(cands_batch[0])
                pairs = [
                    (contexts_batch[i], c)
                    for i, cands in enumerate(cands_batch)
                    for c in cands
                ]
                scores = sentences_pairs_to_embedding_wrapper(
                    self.crossencoder, self.tokenizer, pairs, self.cap
                )  # (batch_size * nb_cands) x 1
                scores = scores.view(len(contexts_batch), nb_cands)
                idx_right_candidates = [
                    cands.index(correct_cands_batch[i])
                    for i, cands in enumerate(cands_batch)
                ]
                idx_right_candidates = torch.cuda.LongTensor(
                    idx_right_candidates
                )  # batch_size
                loss, nb_ok = self.crossencoder_loss(scores, idx_right_candidates)
                # as a bonus, output prediction (cheap)
                _, idx_best = torch.max(scores, dim=1)
                prediction += [
                    cands[idx_best[i].item()] for i, cands in enumerate(cands_batch)
                ]
                loss.backward()
                self.optim_crossencoder.step()
                self.metrics["total_crossencoder"] += 1
                self.metrics["crossencoder_loss"] += loss.cpu().detach().item()
        return prediction

    def predict_batch(self, contexts, candidates, precomputed_cands_embeddings=None):
        """ We consider the batch is small enough for a crossencoder prediction to
            happen.
            - contexts is a list of strings.
            - candidates is a list of list of string of same length of contexts
                  (except when precomputed_cands_embeddings != None)
                  We expect the batch size to be rather small to be able to handle
                  the bacth
            - precomputed_cands_embeddings: In the case where the candidates are already
                  pre-computed, you can provide the embeddings of the cands.
        """
        if self.encoder_type == "debug":
            return [cands[0] for cands in candidates]
        min_nb_cand = min([len(cands) for cands in candidates])
        max_nb_cand = max([len(cands) for cands in candidates])
        assert (
            min_nb_cand == max_nb_cand
        ), "The number of candidates for each context must be the same."
        [model.eval() for model in self.models]

        with torch.no_grad():
            if self.encoder_type == "biencoder" or self.encoder_type == "both":
                topn = []
                embeddings_context = sentences_to_embedding_wrapper(
                    self.enc_context, self.tokenizer, contexts, self.cap
                )  # batch_size x 768
                all_cands = [cand for cands in candidates for cand in cands]
                if precomputed_cands_embeddings is None:
                    embeddings_cands = sentences_to_embedding_wrapper(
                        self.enc_candidates, self.tokenizer, all_cands, self.cap
                    )  # (batch_size * nb_cands) x 768
                    embeddings_cands = embeddings_cands.view(
                        len(contexts), min_nb_cand, -1
                    )
                else:
                    embeddings_cands = precomputed_cands_embeddings
                idx_best = []
                for i in range(len(contexts)):
                    # compute the top n elements according to the bi-encoder.
                    scores = embeddings_context[i : i + 1].mm(embeddings_cands[i].t())[
                        0
                    ]
                    tops, top_indexes = torch.sort(scores, dim=0, descending=True)
                    topn.append(
                        [
                            candidates[i][top_indexes[j].cpu().item()]
                            for j in range(self.topn_both)
                        ]
                    )
                    idx_best.append(torch.max(scores, dim=0)[1])
                response = [
                    cands[idx_best[i].item()] for i, cands in enumerate(candidates)
                ]

            if self.encoder_type == "crossencoder" or self.encoder_type == "both":
                cands_to_consider = topn if self.encoder_type == "both" else candidates
                nb_cands = (
                    self.topn_both if self.encoder_type == "both" else min_nb_cand
                )
                pairs = [
                    (contexts[i], c)
                    for i, cands in enumerate(cands_to_consider)
                    for c in cands
                ]
                scores = sentences_pairs_to_embedding_wrapper(
                    self.crossencoder, self.tokenizer, pairs, self.cap
                )  # (batch_size * nb_cands) x 1
                scores = scores.view(len(contexts), nb_cands)
                _, idx_best = torch.max(scores, dim=1)
                response = [
                    cands[idx_best[i].item()]
                    for i, cands in enumerate(cands_to_consider)
                ]
        return response

    def batch_act(self, observations):
        valid_obs = [obs for obs in observations if "text" in obs]
        valid_obs_idxs = [i for i, obs in enumerate(observations) if "text" in obs]
        response = [{"text": "filler"} for _ in range(len(observations))]
        if len(valid_obs) == 0:
            return response

        is_training = "labels" in valid_obs[0]
        contexts = [
            self.get_context(obs, self.with_personality, self.history_length)
            for obs in valid_obs
        ]

        optional_vecs = None
        if self.predef_candidates is not None:
            candidates = [self.predef_candidates]
            optional_vecs = self.predef_candidates_vecs
        elif "label_candidates" in valid_obs[0]:
            candidates = [obs["label_candidates"] for obs in valid_obs]
        else:
            print("No candidates is found")

        if is_training:
            good_candidates = [obs["labels"][0] for obs in valid_obs]
            prediction = self.train_batch(contexts, candidates, good_candidates)
        else:
            prediction = self.predict_batch(contexts, candidates, optional_vecs)

        for i, idx in enumerate(valid_obs_idxs):
            response[idx]["text"] = prediction[i]
        return response

    def save(self, path=None):
        """Save the model.
        """
        print("save models")
        if self.encoder_type == "debug":
            return
        # save the options in any cases.
        with open(self.path_to_options, 'w') as f:
            f.write(json.dumps(self.opt))

        # TODO: those field names are dumb. Change them once we're
        # sure the trainloop works.
        state_dict = []
        if self.encoder_type == "biencoder":
            state_dict["context_encoder_state"] = self.enc_context.state_dict()
            state_dict["candidate_encoder"] = self.enc_candidates.state_dict()
        else:
            state_dict["encoder"] = self.crossencoder.state_dict()
        torch.save(state_dict, self.path_to_model)


class BertRankerAgentWizard(BertRankerAgent):
    """ Special Ranker agent for the wizard.
    """

    def get_context(self, observation, with_personality, length_history):
        """ Concatenate the knowledge with the history, ignore the history
            length just concatenate everything
        """
        history = observation["text"].split("\n")
        starter = observation["checked_sentence"] if self.with_personality else ""
        offset_history = 1
        context = starter + " - ".join(history[offset_history:])
        while len(context) > 1024:
            offset_history += 1
            if offset_history == len(history):
                break
            context = starter + " " + " - ".join(history[offset_history:])
        return context

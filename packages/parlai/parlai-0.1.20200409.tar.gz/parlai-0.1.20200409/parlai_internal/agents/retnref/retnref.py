#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from parlai.agents.transformer.transformer import TransformerGeneratorAgent
from parlai.core.message import Message
from parlai.core.metrics import F1Metric
from parlai.core.torch_agent import History
from parlai.core.agents import create_agent, create_agent_from_shared

from parlai.utils.misc import warn_once

import numpy as np
import torch
import random


RETRIEVAL_MODEL_FILE = 'zoo:pretrained_transformers/model_poly/model'
RET_FCP = 'data/models/pretrained_transformers/convai_trainset_cands.txt'
SEP_TOKEN = ' RETPRED '


class RetnrefHistory(History):
    """
    Modify history to save the retriever's response.
    """

    def __init__(self, opt, **kwargs):
        super().__init__(opt, **kwargs)
        self.retriever_response = None

    def reset(self):
        super().reset()
        self.retriever_response = None

    def update_history(self, obs, retriever_response=None):
        super().update_history(obs)
        self.retriever_response = retriever_response

    def get_history_str(self):
        history_str = super().get_history_str()
        if history_str is not None and self.retriever_response is not None:
            history_str += SEP_TOKEN + self.retriever_response

        return history_str

    def get_history_vec(self):
        history = super().get_history_vec()
        if history is not None and self.retriever_response is not None:
            retriever_response = SEP_TOKEN + self.retriever_response
            retriever_response_tok = self.parse(retriever_response)
            if self.vec_type == 'deque':
                history.extend(retriever_response_tok)
            else:
                history += retriever_response_tok

        return history

    def get_history_vec_no_ret(self):
        """
        Get the history response without the.
        """
        hist = super().get_history_vec()
        if hist is None:
            return []
        return hist


class RetnrefAgent(TransformerGeneratorAgent):
    """
    General purpose retrieve and refine generator.
    """

    @classmethod
    def history_class(cls):
        """
        Determine the history class.
        """
        return RetnrefHistory

    @classmethod
    def add_cmdline_args(cls, argparser):
        """
        Add command-line arguments specifically for this agent.
        """
        TransformerGeneratorAgent.add_cmdline_args(argparser)
        agent = argparser.add_argument_group('Retnref Arguments')
        agent.add_argument(
            '--ret-model-file',
            type=str,
            default=RETRIEVAL_MODEL_FILE,
            help='Retrieval model file',
        )
        agent.add_argument(
            '--ret-model',
            type=str,
            default='transformer/polyencoder',
            help='Retrieval model',
        )
        agent.add_argument(
            '--ret-fcp',
            type=str,
            default=RET_FCP,
            help='Fixed candidates path for retrieval model',
        ),
        agent.add_argument(
            '--choose-label-pct',
            type=float,
            default=0.2,
            help='Choose the label some of the time',
        )
        agent.add_argument(
            '--block-repeats',
            type='bool',
            default=True,
            help='Block evaluation repeats',
        )
        agent.add_argument(
            '--print-retrieval',
            type='bool',
            default=True,
            help='Print the response retrieved by retrieval model',
        )
        agent.add_argument(
            '--cache-retriever-response',
            type='bool',
            default=False,
            help='Cache the retriever response before training.',
        )
        agent.add_argument(
            '--data-parallel', type='bool', default=False, help='Data parallel'
        )
        return agent

    def __init__(self, opt, shared=None):
        """
        Set up model.
        """
        super().__init__(opt, shared)

        self.choose_label_pct = opt['choose_label_pct']
        self.block_repeats = opt['interactive_mode'] and opt['block_repeats']
        if self.block_repeats:
            self.already_retrieved_utts = []
        # init retrieval model
        if shared:
            if opt['cache_retriever_response']:
                self.retrieval_model = None
            else:
                self.retrieval_model = create_agent_from_shared(
                    shared['retrieval_model_opt']
                )
        else:
            if opt['cache_retriever_response']:
                if opt['interactive_mode']:
                    raise RuntimeError(
                        'You should not cache the retriever response in interactive mode.'
                    )

                self._build_cache_directions(opt)
                self.retrieval_model = None
            else:
                retrieval_model_opt = {
                    'model_file': self.opt['ret_model_file'],
                    'model': self.opt['ret_model'],
                    'datapath': self.opt['datapath'],
                    'encode_candidate_vecs': True,
                    'model_parallel': self.opt['model_parallel'],
                    'data_parallel': (
                        False if opt['model_parallel'] else opt['data_parallel']
                    ),
                    'eval_candidates': 'fixed',
                    'interactive_mode': True,
                    'fp16': opt['fp16'],
                    'use_reply': 'label',  # this is important for tracking history in eval mode
                    'fixed_candidates_path': self.opt['ret_fcp'],
                    'override': {},
                }
                for k, v in retrieval_model_opt.items():
                    retrieval_model_opt['override'][k] = v
                self.retrieval_model = create_agent(retrieval_model_opt)
            self.metrics['ret_f1'] = F1Metric(0.0)

    def _build_cache_directions(self, opt):
        task = opt['task']
        if 'fromfile' in task:
            return

        print('\n' * 50)
        print('=' * 50)
        script = 'parlai_internal/agents/retnref/cache_retrieval_preds.py'
        mf = opt['ret_model_file']
        fcp = opt['ret_fcp']
        command = f'python {script} -t {task} -mf {mf} -fcp {fcp}'
        print(
            'WARNING: Please run the following script to cache retriever '
            'predictions for your task, and then use `fromfile`:\n{}'.format(command)
        )
        print('=' * 50)
        import sys

        sys.exit()

    def _validate_self_observe_invariants(self):
        # TODO: emily check that this is actually what we want
        pass

    def _validate_observe_invariants(self):
        # TODO: emily check that this is actually what we want
        pass

    def _get_retrieval_response(self):
        act = self.retrieval_model.act()

        if not self.block_repeats:
            return act.get('text')

        for response in act['text_candidates']:
            if response not in self.already_retrieved_utts:
                self.already_retrieved_utts.append(response)
                return response

        # Went through all text candidates
        return act.get('text')

    def _get_context(self, batch, batch_idx):
        """
        Override from TGA to avoid n-gram blocking on the retrieval response.
        """
        return batch.text_vec_no_ret[batch_idx]

    def batchify(self, obs_batch, sort=False):
        """
        Override from TGA to avoid n-gram blocking on the retrieval response.
        """
        batch = super().batchify(obs_batch, sort)
        text_vecs_no_ret = [
            torch.LongTensor(obs.get('text_vec_no_ret', [])) for obs in obs_batch
        ]
        batch.text_vec_no_ret = text_vecs_no_ret
        return batch

    def _set_text_vec(self, obs, history, truncate):
        """
        Override from TGA to avoid n-gram blocking on the retrieval response.
        """
        obs = super()._set_text_vec(obs, history, truncate)
        obs['text_vec_no_ret'] = history.get_history_vec_no_ret()

        return obs

    def observe(self, observation):
        """
        Process incoming message in preparation for producing a response.

        This includes remembering the past history of the conversation.
        """
        # TODO: Migration plan: TorchAgent currently supports being passed
        # observations as vanilla dicts for legacy interop; eventually we
        # want to remove this behavior and demand that teachers return Messages
        observation = Message(observation)
        is_training = 'labels' in observation

        # Sanity check everything is in order
        self._validate_observe_invariants()
        self.observation = observation

        # ranker observe/act
        if self.retrieval_model is not None:
            # remove labels / any vectorization for ranker
            if not self.opt['interactive_mode']:
                ranker_obs = {
                    'text': observation.get('text', ''),
                    'episode_done': observation['episode_done'],
                }
            else:
                # in interactive mode, we reset the history every time
                delim = self.retrieval_model.history.delimiter
                hist = self.history.history_strings + [observation.get('text', '')]
                ranker_obs = {'text': delim.join(hist), 'episode_done': True}
            self.retrieval_model.observe(ranker_obs)
            retriever_response = self._get_retrieval_response()
        else:
            if 'retriever_reply' not in observation:
                assert 'text' not in observation  # This is a batch padding act
                warn_once(
                    f'No retriever reply in observation! Observation: {observation}'
                )
            retriever_response = observation.get('retriever_reply', '')
        if is_training:
            # replace retriever response with gold label some percentage
            # of the time
            replace = random.random()
            if replace < self.choose_label_pct:
                # randomly choose a label
                retriever_response = random.choice(observation['labels'])
        elif self.opt['interactive_mode'] and self.opt['print_retrieval']:
            print(f'\n[ ({self.id}) Retriever response ]: {retriever_response}\n')

        # update history
        self.history.update_history(observation, retriever_response=retriever_response)
        # save in the observation
        observation['retriever_response_obs'] = retriever_response

        return self.vectorize(
            observation,
            self.history,
            text_truncate=self.text_truncate,
            label_truncate=self.label_truncate,
        )

    def batch_act(self, observations):
        batch_reply = super().batch_act(observations)
        # compute f1 between retriever response and generated reply
        ret_responses = [obs.get('retriever_response_obs', '') for obs in observations]
        replies = [act.get('text', '') for act in batch_reply]
        for ret, reply, batch_act in zip(ret_responses, replies, batch_reply):
            batch_act['retriever_response'] = ret
            if reply is not None and ret is not None:
                self.metrics['ret_f1'] += F1Metric.compute(reply, [ret])
            # now check for __unks__
            if reply is not None and self.dict.unk_token in reply:
                # replace with the retriever response
                warn_once(
                    'UNK detected: Generator reply replaced with retriever reply.'
                )
                batch_act.force_set('text', ret)

        return batch_reply

    def reset_metrics(self):
        super().reset_metrics()
        self.metrics['ret_f1'] = F1Metric(0.0)

    def report(self):
        metrics = super().report()
        metrics['ret_f1'] = self.metrics['ret_f1'].value()
        return metrics

    def share(self):
        shared = super().share()
        if self.retrieval_model is not None:
            shared['retrieval_model_opt'] = self.retrieval_model.share()

        return shared

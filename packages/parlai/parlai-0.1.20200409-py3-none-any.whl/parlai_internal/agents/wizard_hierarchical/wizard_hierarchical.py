#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
"""Hierachical wizard agent with 3 parts:
1. TFIDF retriever (optional, task may already provide knowledge)
2. Knowledge selector/reader (chooses one sentence from the knowledge for
   generator to condition on)
3. Generator (generates a reply)

NOTE: this model only works for eval, it assumes all training is already done.
"""

import pickle
from parlai.core.agents import Agent
from parlai.core.agents import create_agent
from parlai.core.params import get_model_name
from parlai_internal.projects.wizard.generator.tasks import (
    TOKEN_KNOWLEDGE,
    TOKEN_NOCHOSEN,
)

WIKI_MAP = (
    '/private/home/kshuster/ParlAI/parlai_internal2/mturk/'
    'tasks/wizard_of_perZOna/data/title_to_passage.pkl'
)


def _clone_agent(original):
    return type(original)(original.opt, original.share())


class WizardHierarchicalAgent(Agent):
    def __init__(self, opt, shared=None):
        super().__init__(opt)
        if opt.get('numthreads', 1) != 1:
            raise RuntimeError(
                "Multithreading not supported, until the retriever supports batch_act"
            )

        self.id = 'WizardHierarchicalAgent'
        self.debug = opt.get('debug')
        self.interactive_mode = opt.get('interactive_mode')
        self.retrieve_knowledge = opt.get('retrieve_knowledge') or self.interactive_mode
        self.dont_reuse = opt.get('dont_reuse', False)
        batchsize = opt['batchsize']

        if shared:
            self.opt = shared['opt']
            if self.retrieve_knowledge:
                self.retriever = shared['retriever']
                self.sent_tok = shared['sent_tok']
                self.wiki_map = shared['wiki_map']
                self.ret_history = {}
            self.main_reader = shared['main_reader']
            self.main_gen = shared['main_gen']
        else:
            if self.retrieve_knowledge:
                # Create retriever
                retriever_opt = {
                    'model_file': opt['retriever_model_file'],
                    'remove_title': False,
                    'override': {'remove_title': False},
                }
                self.retriever = create_agent(retriever_opt, True)
                self.set_up_sent_tok()
                self.wiki_map = pickle.load(open(WIKI_MAP, 'rb'))
                self.ret_history = {}

            if self.retrieve_knowledge and batchsize != 1:
                raise RuntimeError("Can only fetch knowledge with -batchsize 1")

            # strip stuff out
            override_opt = {
                k: v
                for k, v in opt['override'].items()
                if not (k.endswith("model_file") or k == "model")
            }
            opt['override'] = override_opt
            modelless_opt = {
                k: v
                for k, v in opt.items()
                if not (k.endswith("model_file") or k == "model")
            }
            # Create reader
            reader_opt = {**modelless_opt, 'model_file': opt['reader_model_file']}
            self.main_reader = create_agent(reader_opt, True)
            # Create generator
            generator_opt = {**modelless_opt, 'model_file': opt['generator_model_file']}
            self.main_gen = create_agent(generator_opt, True)

        self.readers = [_clone_agent(self.main_reader) for _ in range(batchsize)]
        self.generators = [_clone_agent(self.main_gen) for _ in range(batchsize)]

        # for remembering what things we already talked about
        for r in self.readers:
            r.past_knowledge = set()

    @staticmethod
    def add_cmdline_args(argparser):
        """Add command-line arguments specifically for this agent."""
        agent = argparser.add_argument_group('WizardHierarchical Arguments')
        agent.add_argument('--retriever-model-file', type=str, default=None)
        agent.add_argument('--reader-model-file', type=str, default=None)
        agent.add_argument('--generator-model-file', type=str, default=None)
        agent.add_argument(
            '--num-retrieved',
            type=int,
            default=7,
            help='how many passages to retrieve for each' 'category',
        )
        agent.add_argument(
            '--interactive-mode',
            type='bool',
            default=False,
            help='interacting with model',
        )
        agent.add_argument(
            '--retrieve-knowledge',
            type='bool',
            default=False,
            help='use retriever to retrieve from wikipedia',
        )
        agent.add_argument('--dont-reuse', type='bool', default=False)
        agent.add_argument(
            '--debug',
            type='bool',
            default=False,
            help='debug mode, prints some outputs',
        )

        # try to get command sub args
        optguess, _ = argparser.parse_known_args()
        optguess = vars(optguess)
        for k in ['reader_model_file', 'generator_model_file']:
            if optguess.get(k):
                m = get_model_name({'model_file': optguess[k]})
                if m is not None:
                    argparser.add_model_subargs(m)

        return agent

    def set_up_sent_tok(self):
        try:
            import nltk
        except ImportError:
            raise ImportError('Please install nltk (e.g. pip install nltk).')
        # nltk-specific setup
        st_path = 'tokenizers/punkt/{0}.pickle'.format('english')
        try:
            self.sent_tok = nltk.data.load(st_path)
        except LookupError:
            nltk.download('punkt')
            self.sent_tok = nltk.data.load(st_path)

    def get_chosen_topic_passages(self, chosen_topic, title_dict):
        retrieved_txt_format = []
        if chosen_topic in self.wiki_map:
            retrieved_txt = self.wiki_map[chosen_topic]
            retrieved_txts = retrieved_txt.split('\n')

            if len(retrieved_txts) > 1:
                combined = ' '.join(retrieved_txts[2:])
                sentences = self.sent_tok.tokenize(combined)
                total = 0
                for sent in sentences:
                    if total >= 10:
                        break
                    if len(sent) > 0:
                        title_dict.setdefault(chosen_topic, []).append(sent)
                        retrieved_txt_format.append(
                            ' '.join([chosen_topic, TOKEN_KNOWLEDGE, sent])
                        )
                        total += 1

        if len(retrieved_txt_format) > 0:
            passages = '\n'.join(retrieved_txt_format)
        else:
            passages = ''

        return passages

    def get_passages(self, act, title_dict):
        """Format passages retrieved by taking the first paragraph of the
        top `num_retrieved` passages.
        """
        retrieved_txt = act.get('text', '')
        cands = act.get('text_candidates', [])
        if len(cands) > 0:
            retrieved_txts = cands[: self.opt['num_retrieved']]
        else:
            retrieved_txts = [retrieved_txt]

        retrieved_txt_format = []
        for ret_txt in retrieved_txts:
            paragraphs = ret_txt.split('\n')
            if len(paragraphs) > 2:
                sentences = self.sent_tok.tokenize(paragraphs[2])
                for sent in sentences:
                    retrieved_txt_format.append(
                        ' '.join([paragraphs[0], TOKEN_KNOWLEDGE, sent])
                    )
                title_dict[paragraphs[0]] = sentences

        passages = '\n'.join(retrieved_txt_format)
        return passages

    def retriever_act(self, history):
        """Combines and formats texts retrieved by the TFIDF retriever for the
        chosen topic, the last thing the wizard said, and the last thing the
        apprentice said.
        """
        title_dict = {}
        # retrieve on chosen topic
        chosen_topic_txts = None
        if self.ret_history.get('chosen_topic'):
            chosen_topic_txts = self.get_chosen_topic_passages(
                self.ret_history['chosen_topic'], title_dict
            )

        # retrieve on apprentice
        apprentice_txts = None
        if self.ret_history.get('apprentice'):
            apprentice_act = {
                'text': self.ret_history['apprentice'],
                'episode_done': True,
            }
            self.retriever.observe(apprentice_act)
            apprentice_txts = self.get_passages(self.retriever.act(), title_dict)

        # retrieve on wizard
        wizard_txts = None
        if self.ret_history.get('wizard'):
            wizard_act = {'text': self.ret_history['wizard'], 'episode_done': True}
            self.retriever.observe(wizard_act)
            wizard_txts = self.get_passages(self.retriever.act(), title_dict)

        # combine everything
        combined_txt = []
        if chosen_topic_txts:
            combined_txt.append(chosen_topic_txts)
        if wizard_txts:
            combined_txt.append(wizard_txts)
        if apprentice_txts:
            combined_txt.append(apprentice_txts)

        return '\n'.join(combined_txt), title_dict

    def observe(self, observation):
        obs = observation.copy()

        # get retrieved texts
        if self.retrieve_knowledge:
            self.maintain_retrieved_texts(self.ret_history, obs)
            reader_knowledge, self.title_dict = self.retriever_act(self.ret_history)
            obs['knowledge'] = reader_knowledge

        self.observation = obs
        return obs

    def maintain_retrieved_texts(self, history, observation):
        if 'chosen_topic' not in history:
            history['episode_done'] = False
            history['chosen_topic'] = ''
            history['wizard'] = ''
            history['apprentice'] = ''

        if history['episode_done']:
            history['chosen_topic'] = ''
            history['wizard'] = ''
            history['apprentice'] = ''
            if 'next_wizard' in history:
                del history['next_wizard']
            history['episode_done'] = False

        # save chosen topic
        if 'chosen_topic' in observation:
            history['chosen_topic'] = observation['chosen_topic']
        if 'text' in observation:
            history['apprentice'] = observation['text']
        if 'next_wizard' in history:
            history['wizard'] = history['next_wizard']
        # save last thing wizard said (for next time)
        if 'labels' in observation:
            history['next_wizard'] = observation['labels'][0]
        elif 'eval_labels' in observation:
            history['next_wizard'] = observation['eval_labels'][0]

        history['episode_done'] = observation['episode_done']

    def _build_reader_obs(self, obs):
        """Remove eval labels, get label candidates, and remove all
        appearances of the special knowledge token in the observation.
        """
        if 'eval_labels' in obs:
            del obs['eval_labels']
        reverse_lookup = None
        if 'knowledge' in obs:
            # strip out the knowledge tokens and return the reverse mapper
            knowledges = obs['knowledge'].split('\n')
            reverse_lookup = {}
            for k in knowledges:
                no_know_tok = k.replace(TOKEN_KNOWLEDGE + ' ', '')
                reverse_lookup[no_know_tok] = k
            obs['knowledge'] = obs['knowledge'].replace(TOKEN_KNOWLEDGE + ' ', '')
            if reverse_lookup:
                obs['label_candidates'] = list(reverse_lookup.keys())
            else:
                # TODO replace with special token
                obs['label_candidates'] = ['no_passages_used no_passages_used']
        # note: if we return reverse_lookup as None, it means this was a pad batch
        return obs, reverse_lookup

    def act(self):
        """Call batch_act with the singleton batch."""
        act = self.batch_act([self.observation])[0]

        if self.interactive_mode:
            # make sure wizard observes itself, so it is able to retrieve
            # on the last thing it said
            self.ret_history['next_wizard'] = act.get('text', '')

        return act

    def batch_act(self, observations):
        # make sure this is the "main" agent
        assert self.main_reader is not None

        global_reverse_lookup = {}
        reader_observations = []
        for obs, reader in zip(observations, self.readers):
            reader_obs, rl = self._build_reader_obs(obs.copy())
            reader_obs['title'] = ''
            reader_obs['checked_sentence'] = ''
            if rl:
                global_reverse_lookup.update(rl)
            reader_observations.append(reader.observe(reader_obs))

        reader_acts = self.main_reader.batch_act(reader_observations)

        # the reader has picked all its knowledge out, time to map
        # it back the form with special tokens and pass it to the generator

        generator_observations = []
        loop_iter = zip(observations, self.readers, reader_acts, self.generators)
        for obs, reader, reader_act, gen in loop_iter:
            gen_obs = obs.copy()
            if 'text' not in gen_obs:
                generator_observations.append(gen_obs)
                continue

            # choose the reader's best sentence, but don't let it pick
            # the same thing twice
            title = chosen_sent = TOKEN_NOCHOSEN
            for candidate_knowledge in reader_act['text_candidates']:
                if self.dont_reuse and candidate_knowledge in reader.past_knowledge:
                    continue
                reader.past_knowledge.add(candidate_knowledge)
                chosen_knowledge = global_reverse_lookup[candidate_knowledge]
                title, chosen_sent = chosen_knowledge.split(' ' + TOKEN_KNOWLEDGE + ' ')
                break
            else:
                import warnings

                warnings.warn("Uh oh, didn't pick knowledge!")

            gen_obs['title'] = title
            gen_obs['checked_sentence'] = chosen_sent
            gen_obs = gen.observe(gen_obs)
            generator_observations.append(gen_obs)

        generator_acts = self.main_gen.batch_act(generator_observations)
        for act in generator_acts:
            act['id'] = 'Hierarchical' + act['id']

        return generator_acts

    def share(self):
        """Share internal saved_model between parent and child instances."""
        shared = super().share()
        shared['opt'] = self.opt
        if self.retrieve_knowledge:
            shared['retriever'] = self.retriever
            shared['sent_tok'] = self.sent_tok
            shared['wiki_map'] = self.wiki_map
        shared['main_reader'] = self.main_reader
        shared['main_gen'] = self.main_gen

        return shared

    def report(self):
        reader_report = self.main_reader.report()
        gen_report = self.main_gen.report()
        return {**reader_report, **gen_report}

    def reset_metrics(self):
        self.retriever.reset_metrics()
        self.reader.reset_metrics()
        self.generator.reset_metrics()

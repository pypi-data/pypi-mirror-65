#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from parlai.mturk.core.worlds import MTurkOnboardWorld, MTurkTaskWorld
from parlai.core.worlds import validate
from joblib import Parallel, delayed
from parlai_internal.projects.coopRL.env import make_env
from parlai_internal.projects.coopRL.strategy import (
    OnPolicyStrategy, GrimTriggerStrategy,
    ForgivingPenaltyStrategy, BootstrapStrategy)
import parlai_internal.projects.coopRL.models as models
import sys
import time
import random
import torch

sys.modules['models'] = models


QA_PAIRS = [
    ('This is an example question for which the answer is answer', ['answer']),
]


def instantiate_strategy(strat_type, strat_opts, player, env):
    model_opt, coop_models, _ = torch.load(
        strat_opts['coop_model'],
        map_location=lambda storage, loc: storage
    )
    model_opt, defect_models, _ = torch.load(
        strat_opts['defect_model'],
        map_location=lambda storage, loc: storage
    )
    for m in coop_models + defect_models:
        m.eval()
    model_opt = vars(model_opt)
    if strat_type == "coop":
        return OnPolicyStrategy(coop_models[player], "C")
    elif strat_type == "defect":
        return OnPolicyStrategy(defect_models[player], "D")
    elif strat_type == "grim" or strat_type == "strict":
        return GrimTriggerStrategy(
            coop_models[player], defect_models[player],
            coop_models[1 - player],
            env, player, rollout=strat_opts['rollout'],
            flowers=strat_opts['flowers'],
            strict=(strat_type == "strict")
        )
    elif strat_type == "TFT" or strat_type == "WSLS":
        return ForgivingPenaltyStrategy(
            strat_type == "TFT",
            coop_models[player], defect_models[player],
            coop_models[1 - player], defect_models[1 - player],
            env, player, rollout=strat_opts['rollout'],
            flowers=strat_opts['flowers'],
            punish_multiple=strat_opts['punish_multiple'],
            use_q=strat_opts['use_q'],
            min_gain_harm=strat_opts['min_gain_harm']
        )
    elif strat_type == "BT" or strat_type == "BG":
        def make_env_curry():
            return make_env(model_opt)

        return BootstrapStrategy(
            coop_models[player], defect_models[player],
            coop_models[1 - player], defect_models[1 - player],
            make_env_curry, player,
            grim=(strat_type == "BG"),
            quantile=strat_opts['bootstrap_quantile']
        )
    else:
        assert False, "Unknown strategy: %s" % strat_type


class MTurkGridWorldOnboardWorld(MTurkOnboardWorld):
    def parley(self):
        pair = random.choice(QA_PAIRS)
        self.mturk_agent.observe({
            'id': 'System',
            'text': 'Welcome onboard! You\'re about to play with another '
                    'player, so please validate that you\'ve read the rules '
                    'by answering the following question: {}'.format(pair[0])
        })
        response = self.mturk_agent.act()
        while response['text'] not in pair[1]:
            self.mturk_agent.observe({
                'id': 'System',
                'text': 'Sorry that answer was incorrect. Please review and '
                'answer the following question: {}'.format(pair[0])
            })
            response = self.mturk_agent.act()
        self.mturk_agent.observe({
            'id': 'System',
            'text': 'Thank you for confirming! Please wait '
                    'while we match you with another player...'
        })
        self.episodeDone = True


class MTurkGridWorldGameWorld(MTurkTaskWorld):
    """Game world where players may be able to participate in a chat while also
    playing the gridworld game.
    """
    def __init__(self, opt, agents=None, shared=None):
        # Add passed in agents directly.
        self.agents = agents
        self.moves = [None] * len(agents)
        self.episodeDone = False
        self.game = make_env(opt)
        self.rewards = [0] * len(agents)
        self.round = 0
        self.init = True
        self.rounds = opt['rounds']
        self.game_data = []

    def parley(self):
        """For each agent, attempt to act to grab either moves or text. For
        text, send it to the other agent. For moves, store them and then act
        when both are gotten.
        """
        if self.init:
            self.init = False
            for _index, agent in enumerate(self.agents):
                state = self.game.get_state(player=0).numpy()
                msg = {
                    'type': 'state',
                    'data': {
                        'state': state.tolist(),
                        'scores': self.rewards,
                        'round': self.round,
                        'rounds': self.rounds
                    },
                }
                agent.observe(msg)
        for index, agent in enumerate(self.agents):
            if self.round >= self.rounds:
                self.episodeDone = True
                return
            message = None
            try:
                message = agent.act(timeout=None, blocking=False)
            except TypeError:
                message = agent.act()  # not MTurkAgent, acting as a model
            if message is None:
                continue  # Agent didn't act yet
            self.game_data.append((
                index,
                message,
                self.game.get_state(player=index),
                self.rewards,
                self.round,
            ))
            if message['episode_done']:
                self.episodeDone = True
            elif 'type' in message and message['type'] == 'move':
                # Get the move from the message
                self.moves[index] = message['data']
                # Act if everyone has moved
                if self.moves[0] is not None and self.moves[1] is not None:
                    self.round += 1
                    r0, r1 = self.game.step(self.moves[0], self.moves[1])
                    self.rewards[0] += r0
                    self.rewards[1] += r1
                    state = self.game.get_state(player=0).numpy()
                    msg = {
                        'type': 'state',
                        'data': {
                            'state': state.tolist(),
                            'scores': self.rewards,
                            'round': self.round,
                            'rounds': self.rounds
                        },
                    }
                    self.agents[0].observe(msg)
                    self.agents[1].observe(msg)
                    self.moves = [None] * len(self.agents)
            elif 'text' in message:
                for other_agent in self.agents:
                    if other_agent != agent:
                        other_agent.observe(validate(message))
            time.sleep(0.1)  # Non-blocking parleys should sleep

    def episode_done(self):
        return self.episodeDone

    def shutdown(self):
        """Shutdown all mturk agents in parallel, otherwise if one mturk agent
        is disconnected then it could prevent other mturk agents from finishing
        """
        # TODO give agents bonuses based on how well they did

        global shutdown_agent

        def shutdown_agent(agent):
            try:
                agent.shutdown(timeout=None)
            except Exception:
                agent.shutdown()  # not MTurkAgent
        Parallel(
            n_jobs=len(self.agents),
            backend='threading'
        )(delayed(shutdown_agent)(agent) for agent in self.agents)


class MTurkGridWorldModelGameWorld(MTurkTaskWorld):
    """Game world where a player competes against a model
    """
    def __init__(self, opt, agents, experiment, mturk_player, shared=None):
        # Add passed in agents directly.
        self.agent = agents[0]
        self.states = [None] * 2
        self.moves = [None] * 2
        self.episodeDone = False
        self.game = make_env(opt)
        self.rewards = [0] * 2
        self.round = 0
        self.init = True
        self.mturk_index = mturk_player
        self.rounds = opt['rounds']
        self.game_data = []
        self.strategy = instantiate_strategy(
            experiment['strat_type'],
            experiment['strat_params'],
            1 - self.mturk_index,
            self.game,
        )

    def parley(self):
        """Grab moves or text from the agent. If it's a move, create a response
        from the model and forward the game state.
        """
        if self.init:
            self.init = False
            state = self.game.get_state(player=0).numpy()
            msg = {
                'type': 'state',
                'data': {
                    'state': state.tolist(),
                    'scores': self.rewards,
                    'round': self.round,
                    'rounds': self.rounds
                },
            }
            self.agent.observe(msg)
        if self.round >= self.rounds:
            self.episodeDone = True
            return
        message = None
        try:
            message = self.agent.act(timeout=None, blocking=False)
        except TypeError:
            message = self.agent.act()  # not MTurkAgent, acting as a model
        if message is None:
            return  # Agent didn't act yet
        self.game_data.append((
            self.mturk_index,
            message,
            self.game.get_state(player=self.mturk_index),
            self.rewards,
            self.round,
        ))
        if message['episode_done']:
            self.episodeDone = True
        elif 'type' in message and message['type'] == 'move':
            human = self.mturk_index
            model = 1 - human
            # Get the move from the message
            self.moves[human] = message['data']
            self.states[human] = self.game.get_state(player=human)
            self.states[model] = self.game.get_state(player=model)
            self.moves[model] = self.strategy.step(self.states[model])
            self.game_data.append((
                1 - self.mturk_index,
                {'id': 'model', 'move': self.moves[model]},
                self.states[model],
                self.rewards,
                self.round,
            ))

            r0, r1 = self.game.step(self.moves[0], self.moves[1])
            self.round += 1
            self.rewards[0] += r0
            self.rewards[1] += r1
            self.strategy.observe_opponent(self.states[human],
                                           self.moves[human])
            self.strategy.observe_reward(self.rewards[model])

            state = self.game.get_state(player=0).numpy()
            msg = {
                'type': 'state',
                'data': {
                    'state': state.tolist(),
                    'scores': self.rewards,
                    'round': self.round,
                    'rounds': self.rounds
                },
            }

            # Wait up to 1.5 seconds to simulate human decision making
            wait_time = random.random() * 2 - 1
            if wait_time > 0:
                time.sleep(wait_time)

            self.agent.observe(msg)
        elif 'text' in message:
            # Opportunity to develop opponents that communicate back with the
            # player based on something, perhaps learned conversations?
            pass
        time.sleep(0.1)  # Non-blocking parleys should sleep

    def episode_done(self):
        return self.episodeDone

    def shutdown(self):
        """Shutdown all mturk agents in parallel, otherwise if one mturk agent
        is disconnected then it could prevent other mturk agents from finishing
        """
        # TODO give agents bonuses based on how well they did
        try:
            self.agent.shutdown(timeout=None)
        except Exception:
            self.agent.shutdown()  # not MTurkAgent

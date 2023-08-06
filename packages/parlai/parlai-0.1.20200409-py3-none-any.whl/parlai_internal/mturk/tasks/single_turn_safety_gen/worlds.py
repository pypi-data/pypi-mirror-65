#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from parlai.mturk.core.worlds import MTurkTaskWorld
from parlai_internal.mturk.tasks.single_turn_safety_review.worlds import (
    check_timeout,
    SingleTurnSafetyOnboardingWorld
)
import datetime
import enum
import time


# Soft block qual name
BLOCK_QUALIFICATION = 'SafetyGenMaxHITsQual'

# Task constants
OK = 'OK'
NOT_OK = 'NOT OK'
HTML = {
    OK: "<span style='color:green'><b>OK</b></span>",
    NOT_OK: "<span style='color:red'><b>NOT OK</b></span>"
}

SCRATCH_INTRO = (
    "Welcome! You will be asked to generate <b>{} messages</b> from scratch that "
    "you believe would be {} to send in a friendly conversation with someone "
    "you just met online. <br><br>NOTE: try to send messages that would naturally "
    "appear in the beginning, middle, <b>or</b> end of a short conversation. "
)
SCRATCH_INSTRUCTION = (
    "<i>[You have {} turn(s) left.]</i> Please enter a message that is {}:"
)

TOPIC_INTRO = (
    "Welcome! You will be asked to generate {} sentences that "
    "you believe would be {} to send in a friendly conversation with someone "
    "you just met online. <br><br>NOTE: try to send messages that would naturally "
    "appear in the beginning, middle, <b>or</b> end of a short conversation. "
    "<br><br>For each sentence, you will be given a topic. Try to write a "
    "message as if you were in a conversation about that topic."
)
TOPIC_INSTRUCTION = (
    "<i>[You have {} turn(s) left.]</i> Please enter a message that is {} as "
    "if you were discussing the following topic: <br><br>"
    "<span style='color:blue'><b>{}</b></span>"
)

RANGE_MSG = (
    "Your submitted message must be between {} and {} words. Please try again."
)
FINISHED_MSG = (
    "Thank you! You\'ve finished this HIT. Please click the button below to "
    "submit. "
)


class WorldAssignment(enum.Enum):
    SCRATCH = 1
    TOPIC = 2


class SingleTurnSafetyGenOnboardingWorld(SingleTurnSafetyOnboardingWorld):
    def block_loop(self):
        super().block_loop(qualification=BLOCK_QUALIFICATION)


class SingleTurnSafetyGenWorld(MTurkTaskWorld):
    """General world to take away some of the boilerplate from other worlds.
    """
    def __init__(self, opt, mturk_agents):
        self.opt = opt
        self.agent = mturk_agents[0]
        self.msg = {
            'id': 'System',
            'text': ''
        }
        self.ok = opt.get('ok_or_notok')
        self.range = [int(x) for x in opt['len_range'].split(',')]

        # data
        self.answers = []

        # turn control
        self.episodeDone = False
        self.total_turns = opt.get('num_per_eval')
        self.turn = 0
        self.start_time = time.time()

    def _observe_intro_msg(self):
        raise NotImplementedError(
            'Abstract class: child class must implement _observe_intro_msg()')

    def _observe_turn_msg(self):
        raise NotImplementedError(
            'Abstract class: child class must implement _observe_turn_msg()')

    def _check_range(self, act):
        text_len = len(act['text'].split(' '))
        if text_len < self.range[0] or text_len > self.range[1]:
            self.msg['text'] = RANGE_MSG.format(self.range[0], self.range[1])
            self.agent.observe(self.msg)
            return False
        return True

    def get_act(self):
        act = self.agent.act()
        return act

    def parley(self):
        if self.turn == 0:
            self._observe_intro_msg()

        if self.turn < self.total_turns:
            self._observe_turn_msg()
            completed_round = False
            while not completed_round:
                act = self.get_act()
                timeout = check_timeout(act)
                if timeout:
                    return
                if self._check_range(act):
                    completed_round = True
            self.answers.append(act['text'])
            self.turn += 1
        else:
            # observe message telling agent that they are done with the HIT
            self.msg['text'] = FINISHED_MSG
            self.msg['episode_done'] = True
            self.agent.observe(self.msg)
            self.episodeDone = True

        return

    def episode_done(self):
        return self.episodeDone

    def shutdown(self):
        self.agent.shutdown(timeout=None)

    def review_work(self):
        return self.turn >= self.total_turns

    def get_custom_task_data(self):
        completed = self.turn == self.total_turns
        now = datetime.datetime.now()
        date_completed = now.strftime("%Y-%m-%d %H:%M")
        return {
            'worker_id': self.agent.worker_id,
            'hit_id': self.agent.hit_id,
            'completed': completed,
            'answers': self.answers,
            'completion_time': time.time() - self.start_time,
            'task_world_assignment': self.agent.task_world_assignment,
            'date_completed': date_completed,
            'range': self.range,
        }


class SingleTurnSafetyGenScratch(SingleTurnSafetyGenWorld):
    """World where Turkers try to generate sentences that are OK or NOT OK
    from scrach.
    """
    def _observe_intro_msg(self):
        self.msg['text'] = SCRATCH_INTRO.format(
            self.total_turns,
            HTML[self.ok]
        )
        self.agent.observe(self.msg)

    def _observe_turn_msg(self):
        self.msg['text'] = SCRATCH_INSTRUCTION.format(
            self.total_turns - self.turn,  # turns left
            HTML[self.ok]  # ok or not ok
        )
        self.agent.observe(self.msg)


class SingleTurnSafetyGenTopic(SingleTurnSafetyGenWorld):
    """World where Turkers try to generate sentences that are OK or NOT OK
    on a given topic.
    """

    def __init__(self, opt, mturk_agents, topics):
        super().__init__(opt, mturk_agents)
        self.topics = topics

    def _observe_intro_msg(self):
        self.msg['text'] = TOPIC_INTRO.format(
            self.total_turns,
            HTML[self.ok]
        )
        self.agent.observe(self.msg)

    def _observe_turn_msg(self):
        self.msg['text'] = TOPIC_INSTRUCTION.format(
            self.total_turns - self.turn,  # turns left
            HTML[self.ok],  # ok or not ok
            self.topics[self.turn]  # topic for this message
        )
        self.agent.observe(self.msg)

    def get_custom_task_data(self):
        task_data = super().get_custom_task_data()
        task_data['topics'] = self.topics
        return task_data

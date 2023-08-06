#!/usr/bin/env python3

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from parlai.mturk.core.worlds import MTurkOnboardWorld, MTurkTaskWorld
from parlai.mturk.core.agents import MTURK_DISCONNECT_MESSAGE, RETURN_MESSAGE
import datetime
import random
import time

# Soft block qual name
QUAL_NAME = 'CompletedMaxReviewEvals1'

# Onboarding constants
ONBOARDING_TEST = {
    'do you get free pizza': 'ok',
    'i am great at catching a wave with my high school sweetheart': 'ok',
    'wow she is such a bitch': 'not ok',
}
INTRO_TEXT = ("<b><i>ONBOARDING:</b></i> Please try to evaluate some " +
              "sample messages. " +
              "The instructions are the same as for the main task.")
BLOCK_TEXT = ("Sorry, you did not complete the onboarding test correctly. " +
              "Please return the HIT.")
COMPLETION_TEXT = ("<b>Passed!</b> Now you will be sent to the task...")

# Task constants
EVALUATE_MSG = ("<i>({} messages left)</i> Is this message OK for a person " +
                "you just met online to send in a friendly " +
                "conversation?:<br><br>" +
                "<span style='color:blue'><b>{}</b></span>")
REASON_MSG = ("What is your reason for this answer?")
FINISHED_MSG = ("Thanks, you've completed the task! Click the button below " +
                "to finish.")


def is_disconnected(act):
    return 'text' in act and \
            act['text'] in [MTURK_DISCONNECT_MESSAGE, RETURN_MESSAGE]


def check_timeout(act):
    if act is None or act['text'] in ['[TIMEOUT]', '[RETURNED]',
                                      '[DISCONNECT]']:
        return True
    return False


class SingleTurnSafetyOnboardingWorld(MTurkOnboardWorld):
    """World in which we ask the user for demographic information first """
    def __init__(self, opt, mturk_agent, onboarding_tracker):
        super().__init__(opt, mturk_agent)
        self.opt = opt
        self.onboarding_tracker = onboarding_tracker
        self.EVALUATE_MSG = EVALUATE_MSG

    def parley(self):
        self.msg = {
            'id': 'System',
            'text': ''
        }

        self.msg['text'] = INTRO_TEXT
        self.mturk_agent.observe(self.msg)

        i = len(ONBOARDING_TEST)
        for key in ONBOARDING_TEST.keys():
            self.msg['text'] = self.EVALUATE_MSG.format(i, key)
            i -= 1
            self.mturk_agent.observe(self.msg)
            answer = self.mturk_agent.act()
            # check for timeout
            timed_out = check_timeout(answer)
            if timed_out:
                self.episodeDone = True
                return

            if answer['text'].lower() != ONBOARDING_TEST[key]:
                print(
                    'Worker {} failed onboarding'.format(
                        self.mturk_agent.worker_id
                    )
                )
                print('Answered {} to question: {}'.format(answer['text'],
                                                           key))
                if not self.opt.get('is_sandbox'):
                    self.onboarding_tracker.mark_worker_blocked(
                        self.mturk_agent.worker_id
                    )
                self.block_loop()
                self.episodeDone = True
                return

        # successfully completed onboarding
        self.msg['text'] = COMPLETION_TEXT
        self.mturk_agent.observe(self.msg)
        time.sleep(3)
        self.episodeDone = True

    def block_loop(self, qualification=QUAL_NAME):
        # Let worker know that they've failed
        self.msg['text'] = BLOCK_TEXT
        self.mturk_agent.observe(self.msg)
        # Soft block the worker
        if not self.opt.get('is_sandbox'):
            print('Soft blocking worker {} for failing onboarding.'.format(
                self.mturk_agent.worker_id
            ))
            self.mturk_agent.mturk_manager.give_worker_qualification(
                self.mturk_agent.worker_id,
                qualification
            )
        act = self.mturk_agent.act()
        while not is_disconnected(act):
            self.mturk_agent.observe(self.msg)
            act = self.mturk_agent.act()
        return True


class SingleTurnSafetyWorld(MTurkTaskWorld):
    """World in which which we ask workers to assess whether a sentence may
    be considered offensive.
    """

    def __init__(self, opt, mturk_agents, evaluation_stack, stack_idx,
                 bad_cand=None):
        self.agent = mturk_agents[0]
        self.episodeDone = False
        self.stack_idx = stack_idx
        self.total_stack = evaluation_stack.copy()
        # edit the to_evalute stack to get rid of the indices
        self.to_evaluate = evaluation_stack.copy()
        self.total_turns = len(evaluation_stack)
        self.completed = []
        self.answers = []
        self.flagged = {}
        self.turn = 0

        self.bad_cand = bad_cand
        if bad_cand is not None:
            self.bad_cand_ask_time = random.randint(0, 9)
            print('Will ask bad candidate question at turn {}'.format(
                self.bad_cand_ask_time
            ))
        else:
            self.bad_cand_ask_time = -1
        self.bad_cand_response = None
        self.bad_cand_reason = None

        self.msg = {
            'id': 'System',
            'text': ''
        }

        self.start_time = time.time()
        self.EVALUATE_MSG = EVALUATE_MSG
        self.REASON_MSG = REASON_MSG
        self.FINISHED_MSG = FINISHED_MSG

        self.get_reason_ans = ['ok']

    def format_eval_message(self, msg, text, num_left):
        punctuation_map = [
            (' !', '!'),
            (' .', '.'),
            (' ?', '?'),
            ('  (', ' ('),
            (' )', ')'),
            (' ,', ','),
            (" ' ", "'"),
        ]

        new_text = text.lower().replace('\n', '')
        for punc in punctuation_map:
            new_text = new_text.replace(punc[0], punc[1])

        msg['text'] = self.EVALUATE_MSG.format(num_left, new_text)

    def get_reason(self, rating, bad_cand=False):
        # get reason
        self.msg['text'] = self.REASON_MSG
        # let system know we need a text response next
        self.msg['text_response'] = True
        self.agent.observe(self.msg)
        answer = self.agent.act()
        timed_out = check_timeout(answer)
        if timed_out:
            self.episodeDone = True
            return False
        if not bad_cand:
            self.flagged[self.turn] = [rating, answer['text']]
        else:
            self.bad_cand_reason = answer['text']
        self.msg['text_response'] = False
        return True

    def parley(self):
        if len(self.completed) < len(self.total_stack):
            # check how many messages the Turker has left
            to_go = len(self.total_stack) - len(self.completed)
            if self.bad_cand is not None and self.bad_cand_response is None:
                to_go += 1
            # get the next evaluation message
            next = self.to_evaluate.pop(0)
            # observe evaluation message
            self.format_eval_message(self.msg, next, to_go)
            self.agent.observe(self.msg)
            answer = self.agent.act()
            # check for timeout
            timed_out = check_timeout(answer)
            if timed_out:
                self.episodeDone = True
                return

            # save answers
            self.completed.append(next)
            rating = answer['text']
            self.answers.append(rating)

            # check if they flagged this answers
            if rating.lower() not in self.get_reason_ans:
                # get reason
                if not self.get_reason(rating):
                    # timed out
                    return

            if self.turn == self.bad_cand_ask_time:
                # ask agent to evaluate a deliberately bad candidate to see
                # if they are doing the task correctly
                self.format_eval_message(
                    self.msg,
                    to_go - 1,
                    self.bad_cand
                )
                self.agent.observe(self.msg)
                answer = self.agent.act()
                # check for timeout
                timed_out = check_timeout(answer)
                if timed_out:
                    self.episodeDone = True
                    return
                self.bad_cand_response = answer['text'].lower()
                # get reason
                if self.bad_cand_response != 'ok':
                    if not self.get_reason(
                        self.bad_cand_response,
                        bad_cand=True
                    ):
                        # timed out
                        return

            self.turn += 1

        else:
            # agent completed the task
            self.msg['text'] = self.FINISHED_MSG
            self.msg['episode_done'] = True
            self.agent.observe(self.msg)
            self.episodeDone = True

    def episode_done(self):
        return self.episodeDone

    def shutdown(self):
        self.agent.shutdown(timeout=None)

    def review_work(self):
        block_worker = False
        if self.bad_cand_response is not None:
            block_worker = (self.bad_cand_response == 'ok')

        if len(self.completed) < len(self.total_stack):
            return False, None, block_worker
        else:
            return True, self.flagged, block_worker

    def get_custom_task_data(self):
        # brings important data together for the task, to later be used for
        # creating the dataset. If data requires pickling, put it in a field
        # called 'needs-pickle'.
        completed = len(self.completed) == len(self.total_stack)
        test_round = self.stack_idx == -1
        now = datetime.datetime.now()
        date_completed = now.strftime("%Y-%m-%d %H:%M")
        return {
            'worker_id': self.agent.worker_id,
            'hit_id': self.agent.hit_id,
            'completed': completed,
            'stack_idx': self.stack_idx,
            'evaluated': self.total_stack,
            'answers': self.answers,
            'flagged': self.flagged,
            'bad_cand': self.bad_cand,
            'bad_cand_response': self.bad_cand_response,
            'bad_cand_reason': self.bad_cand_reason,
            'test_round': test_round,
            'completion_time': time.time() - self.start_time,
            'date_completed': date_completed,
        }

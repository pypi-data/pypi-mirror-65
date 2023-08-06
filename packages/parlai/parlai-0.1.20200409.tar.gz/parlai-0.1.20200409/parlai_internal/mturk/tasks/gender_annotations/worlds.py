#!/usr/bin/env python3

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from parlai.mturk.core.agents import MTURK_DISCONNECT_MESSAGE, RETURN_MESSAGE
from parlai_internal.mturk.tasks.single_turn_safety_review.worlds import (
    SingleTurnSafetyWorld,
)
import datetime
import time


MAN = "<span style='color:green'><b>man</b></span>"
WOMAN = "<span style='color:blue'><b>woman</b></span>"
NB = "<span style='color:red'><b>non-binary</b></span>"
NEUTRAL = "<span style='color:orange'><b>neutral</b></span>"


# Task constants
GENDER_EVALUATE_MSG = (
    "<i>({} character descriptions left)</i> Please determine whether the "
    f"character is a {MAN}, {WOMAN}, {NB}, or {NEUTRAL}. "
    f"Choose {NEUTRAL} if the character is not "
    "given an explicit gender, or if there is not enough information to "
    "tell:<br><br>{}"
)

CHAR_DESCRIPTION = (
    "<span style='color:purple'><b>{}</b></span>"
)

SURENESS_MSG = (
    "How certain are you that the character is a {}?"
)


def is_disconnected(act):
    return 'text' in act and act['text'] in [MTURK_DISCONNECT_MESSAGE, RETURN_MESSAGE]


def check_timeout(act):
    if act is None or act['text'] in ['[TIMEOUT]', '[RETURNED]', '[DISCONNECT]']:
        return True
    return False


class GenderAnnotationWorld(SingleTurnSafetyWorld):
    """World in which which we ask workers to assess whether a sentence may
    be considered offensive.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.EVALUATE_MSG = GENDER_EVALUATE_MSG
        self.CHAR_DESCRIPTION = CHAR_DESCRIPTION
        self.SURENESS_MSG = SURENESS_MSG

        self.msg['response_type'] = 0
        self.get_reason_ans = ['neutral', 'non-binary']

    def format_eval_message(self, msg, persona_lst, num_left):
        char = '<br>'.join(persona_lst)
        character = self.CHAR_DESCRIPTION.format(char)
        text = self.EVALUATE_MSG.format(num_left, character)

        msg['response_type'] = 0  # let system know we need a category
        msg['text'] = text  # set the display message

    def get_reason(self, rating):
        """Override"""
        self.msg['response_type'] = 1
        self.msg['text'] = SURENESS_MSG.format(rating)
        self.agent.observe(self.msg)
        reason = self.agent.act()
        if not reason:
            return False

        self.flagged[self.turn] = [rating, reason['text']]

        return True

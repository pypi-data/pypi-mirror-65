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


# Task constants
LIGHT_EVALUATE_MSG = (
    "<i>({} character descriptions left)</i> Please determine if the following "
    "character description is "
    "<span style='color:red'><b>OFFENSIVE</b></span>:<br><br>{}"
)

CHAR_DESCRIPTION = (
    "<span style='color:890d09'><b>Character name: </b></span>{}<br><br> "
    "<span style='color:blue'><b>{}</b></span>"
)

CATEGORY_SELECT = (
    "Please place the character description into one of the following "
    "categories. See the task description for explanations and examples."
)


def is_disconnected(act):
    return 'text' in act and \
            act['text'] in [MTURK_DISCONNECT_MESSAGE, RETURN_MESSAGE]


def check_timeout(act):
    if act is None or act['text'] in ['[TIMEOUT]', '[RETURNED]',
                                      '[DISCONNECT]']:
        return True
    return False


class LIGHTPersonaSafetyWorld(SingleTurnSafetyWorld):
    """World in which which we ask workers to assess whether a sentence may
    be considered offensive.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.EVALUATE_MSG = LIGHT_EVALUATE_MSG
        self.CHAR_DESCRIPTION = CHAR_DESCRIPTION
        self.CATEGORY_SELECT = CATEGORY_SELECT

    def format_eval_message(self, msg, tup, num_left):
        name = tup[0]
        persona = tup[1]
        personas = '. <br> '.join(persona.split('. '))
        character = self.CHAR_DESCRIPTION.format(name, personas)
        msg['text'] = self.EVALUATE_MSG.format(num_left, character)

    def get_reason(self, rating):
        """Override to allow for categories."""
        # first have turkers select a category of offensiveness
        self.msg['text'] = self.CATEGORY_SELECT
        self.msg['response_type'] = 1
        self.agent.observe(self.msg)
        category = self.agent.act()
        timed_out = check_timeout(category)
        if timed_out:
            self.episodeDone = True
            return False

        # next have turkers provide a text response reason
        self.msg['text'] = self.REASON_MSG
        # let system know we need a text response next
        self.msg['response_type'] = 2
        self.agent.observe(self.msg)
        reason = self.agent.act()
        timed_out = check_timeout(reason)
        if timed_out:
            self.episodeDone = True
            return False

        self.flagged[self.turn] = [rating, category['text'], reason['text']]
        self.msg['response_type'] = 0
        return True

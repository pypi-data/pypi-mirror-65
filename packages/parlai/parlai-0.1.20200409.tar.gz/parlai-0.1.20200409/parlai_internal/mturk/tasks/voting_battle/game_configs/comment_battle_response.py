#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from .base import BaseGameConfig


class CommentBattleResponseGC(BaseGameConfig):
    TASK_NAME = 'parlai_internal.tasks.comment_battle.agents:DialogResponseTeacher'
    EXAMPLE_MODE = 'image_and_dialog'

    START_LABEL_MSG = '\nRound {}! Please look at the image and comment and provide \
        an engaging response. Your personality is <b>{}.</b>'

    TASK_DESCRIPTION = \
    '''
    <h2><b>Description</b></h2>
    In this task, you will attempt to come up with the best responses for various images and captions by either writing a response <b>with a personality</b> or voting on the best one.
    <br>
    <h3><span style='color:blue'><b>Parts of Game</b></span></h3>
    This progression repeats between 3-6 times, usually 5.
    <h4><span style='color:blue'><b>Responding</b></span></h4>
    You will see an image and caption, along with a message giving a personality. Write an engaging response or comment about the example <b>pretending you had that personality</b>.
    <br>
    <b>Do not copy the personality or any text from the example into your response.</b>
    <br>
    Remember, you're competing against other Turkers to write the best one, so stay relevant and be creative!
    <br>
    <h4><span style='color:blue'><b>Voting</b></span></h4>
    All the different responses written will appear under the example. Choose the response you believe is the <b>most engaging</b> response to the image and caption.
    Remember, an engaging response makes you want to continue the conversation and reply.
    <br>
    Try to choose engaging ones. There is no bonus for selecting your own if it does win, so only choose it if you truly think it is the best!
    <br>
    <h4><span style='color:blue'><b>Scoring and Bonuses</b></span></h4>
    After everyone has voted, the votes are tallied. The response with the most votes is the winner! If there is a tie for top response, then no bonuses are distributed.
    The player that wrote the winning response receives a bonus. All the players that voted for the winning response also receive a bonus.
    However, <b>you cannot receive two bonuses in one turn</b>. This means if your response wins and you voted for it, you only get the response bonus.
    <br>
    <h4><span style='color:blue'><b>Example</b></span></h4>
    <img src="https://www.publicdomainpictures.net/pictures/200000/velka/spy-cat-1474621661xRV.jpg" style="width: 20%"></img>
    <br>
    <span><b>Caption:</b> They can't see me if I can't see them...</span>
    <br>
    <span><b>Sample responses</b></span>
    <ul>
    <li>(Curious Personality) What prey is this mighty hunter stalking?</li>
    <li>(Stoic Personality) Those ears may not be hidden by the fence.</li>
    <li>(Discouraging Personality) Don't bother trying to hide from the neighbor's dog, he can smell your fear.</li>
    </ul>
    {}
    '''

    def __init__(self):
        super().__init__()

    def process_dialog(self, example):
        raw_dialog = example['text'].split('\n')[0]
        dialog = '<b>Response:</b> {}'
        return dialog.format(raw_dialog)

    def create_start_message(self, round_idx, example):
        personality = example['text'].split('\n')[1]
        return CommentBattleResponseGC.START_LABEL_MSG.format(
            round_idx, personality)

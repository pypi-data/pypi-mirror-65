#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from .base import BaseGameConfig
from parlai_internal.tasks.comment_battle.agents import image_id_to_zip_path
import random


class CommentBattleGC(BaseGameConfig):
    TASK_NAME = 'parlai_internal.tasks.comment_battle.agents'
    TASK_IDENTIFIER = 'comment_vanilla'
    EXAMPLE_MODE = 'image'

    START_LABEL_MSG = '\nRound {}! Please look at the image and provide \
        an engaging response. The personality is <b>{}.</b>'
    LABEL_START_FIELDS = ['text']

    TASK_DESCRIPTION = \
    '''
    <h2><b>Description</b></h2>
    In this task, you will attempt to come up with the best responses for examples by writing a response <b>with a personality</b> and voting on the best one.
    <br>
    <h3><span style='color:blue'><b>Parts of Game</b></span></h3>
    This progression repeats 5 times.
    <h4><span style='color:blue'><b>Responding</b></span></h4>
    You will see an example and a message will tell you a personality. Write an engaging response or comment about the example pretending you had that personality.
    <br>
    <b>Do not copy the personality or any text from the example into your response.</b>
    <br>
    Remember, you're competing against other Turkers to write the best one, so stay relevant and be creative!
    <br>
    <h4><span style='color:blue'><b>Voting</b></span></h4>
    All the different responses written will appear under the example. Choose the response you believe is the <b>most engaging</b> response to the example.
    Remember, an engaging response makes you want to continue the conversation and reply.
    <br>
    Try to choose engaging ones. Note that you cannot vote for your own response.
    <br>
    <h4><span style='color:blue'><b>Scoring and Bonuses</b></span></h4>
    After everyone has voted, the votes are tallied. The response with the most votes is the winner! If there is a tie for top response, then no bonuses are distributed - so be sure to vote for the right one.
    The player that wrote the winning response receives a bonus. All the players that voted for the winning response also receive a bonus.
    <br>
    <h4><span style='color:blue'><b>Sample responses</b></span></h4>
    <img src="https://www.publicdomainpictures.net/pictures/200000/velka/spy-cat-1474621661xRV.jpg" style="width: 20%"></img>
    <br>
    <ul>
    <li>(Adventurous Personality) The mighty hunter peers over the edge, preparing to strike!</li>
    <li>(Shy Personality) They can't see me if I can't see them...</li>
    <li>(Pensive Personality) The cat stares deep into the abyss, and it begins to stare back.</li>
    </ul>
    {}
    '''

    def __init__(self):
        super().__init__()
        self.ex_idcs = None
        self.exs = []

    def create_start_message(self, round_idx, example):
        personality = example['text']
        return CommentBattleGC.START_LABEL_MSG.format(
            round_idx, personality)

    def next_example(self, generator, total_rounds, offset):
        if self.ex_idcs is None:
            if offset != -1:
                # single player case
                self.ex_idcs = range(offset, offset+(total_rounds*5), 5)
            else:
                # multiplayer case
                self.ex_idcs = random.sample(range(generator.num_examples()), 5)
            for idx in self.ex_idcs:
                ex = generator.get(idx)
                # load the next image in the background
                img_path = image_id_to_zip_path(ex['image_id'])
                generator.data_loader.request_load(generator.receive_data,
                                                   generator.image_loader.load,
                                                   (img_path,))
                self.exs.append(ex)

        cur_ex = self.exs.pop(0)
        image = generator.data_queue.get()
        cur_ex['image'] = image
        return cur_ex


class CommentBattleRespondingOnlyGC(CommentBattleGC):
    """
    Variant of the CommentBattle game that only has the response stage.
    """

    TASK_IDENTIFIER = 'comment_response_solo'
    END_INFO = \
    """
    <h3><span style="color:blue"><b>Reward/Bonus</b></span></h3>
    There are two bonuses that can be won that push the average pay to $15/hr.
    <br>
    <ol>
        <li>Round Completion: successfully progress through all rounds without disconnecting or being kicked (all-or-nothing $0.70)</li>
        <li>Participation: do not time out at any point (all-or-nothing $0.40)</li>
    </ol>
    There is a base pay rate of $0.05. So, for a given HIT, if you do not time out and finish all the rounds, you will earn $0.05 + $0.70 + $0.40 = $1.15.
    Please note that bonuses are typically paid 2~4 days after the HIT is completed.
    <br>
    <h3><span style="color:blue"><b>Close Window/Timeout/Return HIT</b></span></h3>
    Once the conversation has started, close window/timeout or return HIT during the chat will result in
    <b>HIT EXPIRED</b> to you. You will still earn the bonuses already won to that point.
    <br>
    Please remember that each image has a time limit. If you timeout even once, you will be kicked out of the HIT.
    <br>
    <br>
    <h3><span style='color:red'><b>IMPORTANT NOTICE</b></span></h4>
    1. <b>Be aware the conversations you have will be made public, so act as you would e.g. on a public social network like Twitter.</b>
    <br>
    2. Please do not send any message that could make others uncomfortable, including any level of discrimination, racism, sexism and offensive religious/politics comments, otherwise the submission will be rejected.
    <br>
    3. This particular HIT can only be completed by an individual worker up to 3 times.
    <br>
    <br>
    """

    HIT_TITLE = 'Comment on Images with a Personality! (Average $15/hr with Bonuses)'

    HIT_DESCRIPTION = 'You will create the best response for each example by writing responses with a personality.'

    HIT_KEYWORDS = 'response,image,personality'

    ONBOARDING = \
    '''
    <h1><b>Player, prepare for a Comment Battle...</b></h1>
    <br>
    Your goal is to write the best responses for various examples.
    <br>
    In order to emerge victorious from this battle, your responses need to be engaging and creative.
    <br>
    <br>
    To ensure the game continues to progress, there is a time limit to submit a comment (60 seconds).
    <br>
    {}
    '''

    TASK_DESCRIPTION = \
    '''
    <h2><b>Description</b></h2>
    In this task, you will attempt to come up with the best responses for examples by writing a response <b>with a personality</b>.
    <br>
    <h3><span style='color:blue'><b>Gameplay</b></span></h3>
    This progression repeats between 3-6 times, usually 5.
    <h4><span style='color:blue'><b>Responding</b></span></h4>
    You will see an example and a message will tell you a personality. Write an engaging response or comment about the example pretending you had that personality.
    <br>
    <b>Do not copy the personality or any text from the example into your response.</b>
    <br>
    <h4><span style='color:blue'><b>Sample responses</b></span></h4>
    <img src="https://www.publicdomainpictures.net/pictures/200000/velka/spy-cat-1474621661xRV.jpg" style="width: 20%"></img>
    <br>
    <ul>
    <li>(Adventurous Personality) The mighty hunter peers over the edge, preparing to strike!</li>
    <li>(Shy Personality) They can't see me if I can't see them...</li>
    <li>(Pensive Personality) The cat stares deep into the abyss, and it begins to stare back.</li>
    </ul>
    {}
    '''

    def __init__(self):
        super().__init__()
        self.ex_idcs = None
        self.exs = []

    def next_example(self, generator, total_rounds, offset):
        if self.ex_idcs is None:
            self.ex_idcs = range(offset, offset+(total_rounds*5), 5)
            for idx in self.ex_idcs:
                ex = generator.get(idx)
                # load the next image in the background
                img_path = image_id_to_zip_path(ex['image_id'])
                generator.data_loader.request_load(generator.receive_data,
                                                   generator.image_loader.load,
                                                   (img_path,))
                self.exs.append(ex)

        cur_ex = self.exs.pop(0)
        image = generator.data_queue.get()
        cur_ex['image'] = image
        return cur_ex


class CommentBattleVotingOnlyGC(CommentBattleGC):
    """
    This currently requires using the validation set of Comment Battle, so
    be sure to set the -dt flag to valid when running your command. Also set
    --use_provided_candidates to True.
    """

    TASK_IDENTIFIER = 'comment_voting'
    START_LABEL_MSG = '\nRound {}! Please look at the image and vote for \
        the most engaging response that uses the personality. The personality \
        is <b>{}.</b>'

    END_INFO = \
    """
    <h3><span style="color:blue"><b>Reward/Bonus</b></span></h3>
    There are three bonuses that can be won that push the average pay to $15/hr.
    <br>
    <ol>
        <li>Round Completion: successfully progress through all rounds without disconnecting or being kicked (all-or-nothing $0.70)</li>
        <li>Participation: do not time out at any point (all-or-nothing $0.40)</li>
        <li>Voter Winner: vote for a response that is chosen as the winner for a single round ($0.15/occurrence)</li>
    </ol>
    There is a base pay rate of $0.05. So, for a given HIT, if you do not time out and finish all the rounds, you will earn $0.05 + $0.70 + $0.40 = $1.15.
    But, if you vote for all five winning responses, you can earn up to an extra $0.75 per HIT! Please note that bonuses are typically paid 2~4 days after the HIT is completed.
    <br>
    <b>Please note:</b> if another player disconnects in the middle of the game and not enough remain to play, your bonuses <b>will be pro-rated</b>.
    This means if 4/5 rounds are completed, you get 80% of the max Round Completion and Participation bonus if you qualify.
    <br>
    <h3><span style="color:blue"><b>Close Window/Timeout/Return HIT</b></span></h3>
    Once the conversation has started, close window/timeout or return HIT during the chat will result in
    <b>HIT EXPIRED</b> to you. You will still earn the bonuses already won to that point.
    <br>
    <br>
    <h3><span style='color:red'><b>IMPORTANT NOTICE</b></span></h4>
    1. <b>Be aware the conversations you have will be made public, so act as you would e.g. on a public social network like Twitter.</b>
    <br>
    2. Please do not send any message that could make others uncomfortable, including any level of discrimination, racism, sexism and offensive religious/politics comments, otherwise the submission will be rejected.
    <br>
    <br>
    """

    HIT_TITLE = 'Rate Comments with a Personality! (Average $15/hr with Bonuses)'

    HIT_DESCRIPTION = 'You will help determine the best response for each example with other people by voting on the most engaging ones.'

    HIT_KEYWORDS = 'vote,image,personality'

    ONBOARDING = \
    '''
    <h1><b>Player, prepare for a Comment Battle...</b></h1>
    <br>
    Your goal is to vote for the best responses for various examples.
    <br>
    In order to emerge victorious from this battle, you need to select the most engaging and creative responses.
    <br>
    <br>
    To ensure the game continues to progress, there is a time limit to vote for the best one (30 seconds).
    <br>
    {}
    '''

    TASK_DESCRIPTION = \
    '''
    <h2><b>Description</b></h2>
    In this task, you will attempt to determine the best responses for examples by voting for the best one.
    <br>
    <h3><span style='color:blue'><b>Parts of Game</b></span></h3>
    This progression repeats between 3-6 times, usually 5.
    <h4><span style='color:blue'><b>Voting</b></span></h4>
    Several different responses written will appear under the example. Choose the response you believe is the <b>most engaging</b> response to the example that <b>uses the personality</b>!
    Remember, an engaging response makes you want to continue the conversation and reply.
    <br>
    <h4><span style='color:blue'><b>Scoring and Bonuses</b></span></h4>
    After everyone has voted, the votes are tallied. The response with the most votes is the winner! If there is a tie for top response, then no bonuses are distributed.
    All the players that voted for the winning response also receive a bonus.
    <br>
    <h4><span style='color:blue'><b>Example</b></span></h4>
    <img src="https://www.publicdomainpictures.net/pictures/200000/velka/spy-cat-1474621661xRV.jpg" style="width: 20%"></img>
    <br>
    <span><b>Sample responses</b></span>
    <br>
    <ul>
    <li>(Adventurous Personality) The mighty hunter peers over the edge, preparing to strike!</li>
    <li>(Shy Personality) They can't see me if I can't see them...</li>
    <li>(Pensive Personality) The cat stares deep into the abyss, and it begins to stare back.</li>
    </ul>
    {}
    '''

    def __init__(self):
        super().__init__()
        self.ex_idcs = None
        self.exs = []

    def load_cands(self, example):
        truth = example['labels'][0]
        options = [ex for ex in example['label_candidates'] if ex != truth]
        to_display = random.sample(options, 4)
        to_display.append(truth)
        random.shuffle(to_display)
        cands = []
        for idx, lbl in enumerate(to_display):
            cands.append((idx, lbl, idx))
        return cands


class CommentBattleVotingOnlySoloGC(CommentBattleVotingOnlyGC):
    """
    This currently requires using the validation set of Comment Battle, so
    be sure to set the -dt flag to valid when running your command. Also set
    --use_provided_candidates to True.
    """

    TASK_IDENTIFIER = 'comment_voting_solo'

    END_INFO = \
    """
    <h3><span style="color:blue"><b>Reward/Bonus</b></span></h3>
    There is a bonus that can be won that pushes the average pay to $15/hr.
    <br>
    <ol>
        <li>Round Completion: successfully progress through all rounds without timing out (all-or-nothing $1.45)</li>
    </ol>
    There is a base pay rate of $0.05. So, for a given HIT, if you do not time out and finish all the rounds, you will earn $0.05 + $1.45 = $1.50.
    Please note that bonuses are typically paid 2~4 days after the HIT is completed.
    <br>
    <h3><span style="color:blue"><b>Close Window/Timeout/Return HIT</b></span></h3>
    Once the conversation has started, close window/timeout or return HIT during the chat will result in
    <b>HIT EXPIRED</b> to you. You will still earn the bonuses already won to that point.
    <br>
    Please remember that each image has a time limit. If you timeout even once, you will be kicked out of the HIT.
    <br>
    <br>
    <h3><span style='color:red'><b>IMPORTANT NOTICE</b></span></h4>
    1. <b>Be aware the conversations you have will be made public, so act as you would e.g. on a public social network like Twitter.</b>
    <br>
    2. Please do not send any message that could make others uncomfortable, including any level of discrimination, racism, sexism and offensive religious/politics comments, otherwise the submission will be rejected.
    <br>
    3. This particular HIT can only be completed by an individual worker up to 5 times.
    <br>
    <br>
    """

    HIT_DESCRIPTION = 'You will help determine the best response for each example by voting on the most engaging ones.'

    TASK_DESCRIPTION = \
    '''
    <h2><b>Description</b></h2>
    In this task, you will attempt to determine the best responses for examples by voting for the best one.
    <br>
    <h3><span style='color:blue'><b>Parts of Game</b></span></h3>
    This progression repeats 15 times.
    <h4><span style='color:blue'><b>Voting</b></span></h4>
    Several different responses written will appear under the example. Choose the response you believe is the <b>most engaging</b> response to the example that <b>uses the personality</b>!
    Remember, an engaging response makes you want to continue the conversation and reply.
    <br>
    <h4><span style='color:blue'><b>Example</b></span></h4>
    <img src="https://www.publicdomainpictures.net/pictures/200000/velka/spy-cat-1474621661xRV.jpg" style="width: 20%"></img>
    <br>
    <span><b>Sample responses</b></span>
    <br>
    <ul>
    <li>(Adventurous Personality) The mighty hunter peers over the edge, preparing to strike!</li>
    <li>(Shy Personality) They can't see me if I can't see them...</li>
    <li>(Pensive Personality) The cat stares deep into the abyss, and it begins to stare back.</li>
    </ul>
    {}
    '''

    def __init__(self):
        super().__init__()

    def load_cands(self, example):
        return [(idx, lbl[0], lbl[1]) for idx, lbl in enumerate(example['label_candidates'])]

    def next_example(self, generator, total_rounds, offset):
        if self.ex_idcs is None:
            self.ex_idcs = range(offset, offset+(total_rounds*1), 1)
            for idx in self.ex_idcs:
                ex = generator.get(idx)
                # load the next image in the background
                img_path = image_id_to_zip_path(ex['image_id'])
                generator.data_loader.request_load(generator.receive_data,
                                                   generator.image_loader.load,
                                                   (img_path,))
                self.exs.append(ex)

        cur_ex = self.exs.pop(0)
        image = generator.data_queue.get()
        cur_ex['image'] = image
        return cur_ex

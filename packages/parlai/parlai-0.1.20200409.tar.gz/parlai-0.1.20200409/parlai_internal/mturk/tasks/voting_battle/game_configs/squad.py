#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from .base import BaseGameConfig
import random

class SQuADGC(BaseGameConfig):
    TASK_NAME = 'squad'
    TASK_IDENTIFIER = 'squad_vanilla'
    EXAMPLE_MODE = 'dialog'

    EX_TEMPLATE = \
    '''
    <span style='font-size: 18px'><b>Relevant Paragraph</b></span>
    <br>
    {}
    <br>
    <br>
    <span style='font-size: 18px'><b>Question:</b> {}</span>
    '''

    START_LABEL_MSG = '\nRound {}! Please answer the question using the \
        given paragraph. Remember to directly quote the passage and use as \
        short a quote as possible! The answer could be as short as one word!'

    HIT_TITLE = 'Answer Questions with Friends! (Average $15/hr with Bonuses)'

    HIT_DESCRIPTION = 'You will help determine the best answer for each question with other people by writing answers and voting on which is most correct.'

    HIT_KEYWORDS = 'response,vote,question,answer'

    START_VOTE_MSG = '\nChoose which response is the best answer and click submit.'

    ONBOARDING = \
    '''
    <h1><b>Player, prepare for Question/Answering...</b></h1>
    <br>
    Your goal is to write and vote for the correct answer for various questions.
    <br>
    In order to emerge victorious from this battle, your responses need to be correct.
    <br>
    <br>
    To ensure the game continues to progress, there is a time limit to submit an answer (60 seconds) as well as vote for the correct one (30 seconds).
    <br>
    {}
    '''

    TASK_DESCRIPTION = \
    '''
    <h2><b>Description</b></h2>
    In this task, you will attempt to find answers to questions by answering and voting on the correct one.
    <br>
    <h3><span style='color:blue'><b>Parts of Game</b></span></h3>
    This progression repeats between 3-6 times, usually 5.
    <h4><span style='color:blue'><b>Responding</b></span></h4>
    You will see a question and a corresponding paragraph. Answer the question using the paragraph, <b>using direct quotes</b> and being <b>as short as possible</b>. It is perfectly fine to have a one word answer.
    <br>
    Remember, you're competing against other Turkers to find the correct answer, so stay alert!
    <br>
    <h4><span style='color:blue'><b>Voting</b></span></h4>
    All the unique answers will appear under the example. Choose the response you believe is the <b>most correct</b> answer to the question.
    <br>
    Try to choose the most correct answer. There is no bonus for selecting your own if it does win, so only choose it if you truly think it is correct!
    <br>
    <h4><span style='color:blue'><b>Scoring and Bonuses</b></span></h4>
    After everyone has voted, the votes are tallied. The answer with the most votes is the winner! If there is a tie for top answer, then no bonuses are distributed.
    The player(s) that wrote the winning answer receive a bonus. All the players that voted for the winning response also receive a bonus.
    However, <b>you cannot receive two bonuses in one turn</b>. This means if your answer wins and you voted for it, you only get the response bonus.
    <br>
    <h4><span style='color:blue'><b>Example</b></span></h4>
    <span style='font-size: 18px'><b>Relevant Paragraph</b></span>
    <br>
    All of Notre Dame's undergraduate students are a part of one of the five undergraduate colleges at the school or are in the First Year of Studies program. The First Year of Studies program was established in 1962 to guide incoming freshmen in their first year at the school before they have declared a major. Each student is given an academic advisor from the program who helps them to choose classes that give them exposure to any major in which they are interested. The program also includes a Learning Resource Center which provides time management, collaborative learning, and subject tutoring. This program has been recognized previously, by U.S. News & World Report, as outstanding.
    <br>
    <br>
    <span style='font-size: 18px'><b>Question:</b> What entity provides help with the management of time for new students at Notre Dame?</span>
    <br>
    <br>
    <span style='font-size: 18px'><b>Correct Answer:</b> Learning Resource Center (Note that this answer is a <b>direct quote</b> and as <b>short as possible</b>)</span>
    <br>
    {}
    '''

    def __init__(self):
        super().__init__()
        self.ex_idcs = None
        self.exs = []

    def process_dialog(self, example):
        raw_data = example['text']
        data = raw_data.split('\n')
        paragraph = data[0]
        question = data[1]
        return self.EX_TEMPLATE.format(paragraph, question)

    def next_example(self, generator, total_rounds, offset):
        if self.ex_idcs is None:
            if offset != -1:
                # Non-random
                self.ex_idcs = range(offset, offset+(total_rounds*5), 5)
            else:
                # Random
                self.ex_idcs = random.sample(range(2, generator.num_episodes() - 3), 5)
            for idx in self.ex_idcs:
                ex = generator.get(idx)
                self.exs.append(ex)
        return self.exs.pop()


class SQuADRespondingOnlyGC(SQuADGC):

    TASK_IDENTIFIER = 'squad_response_solo'
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
    <br>
    <h3><span style='color:red'><b>IMPORTANT NOTICE</b></span></h4>
    1. <b>Be aware the conversations you have will be made public, so act as you would e.g. on a public social network like Twitter.</b>
    <br>
    2. Please do not send any message that could make others uncomfortable, including any level of discrimination, racism, sexism and offensive religious/politics comments, otherwise the submission will be rejected.
    <br>
    <br>
    """

    HIT_TITLE = 'Answer Crazy Questions! (Average $15/hr with Bonuses)'

    HIT_DESCRIPTION = 'You will help determine the best answer for questions by reading a paragraph and writing answers.'

    HIT_KEYWORDS = 'response,question,answer'

    ONBOARDING = \
    '''
    <h1><b>Player, prepare for Question/Answering...</b></h1>
    <br>
    Your goal is to write the correct answer for various questions.
    <br>
    In order to emerge victorious from this battle, your responses need to be correct.
    <br>
    <br>
    To ensure the game continues to progress, there is a time limit to submit an answer (60 seconds).
    <br>
    {}
    '''

    TASK_DESCRIPTION = \
    '''
    <h2><b>Description</b></h2>
    In this task, you will attempt to find answers to questions.
    <br>
    <h3><span style='color:blue'><b>Parts of Game</b></span></h3>
    This progression repeats between 3-6 times, usually 5.
    <h4><span style='color:blue'><b>Responding</b></span></h4>
    You will see a question and a corresponding paragraph. Answer the question using the paragraph, <b>using direct quotes</b> and being <b>as short as possible</b>. It is perfectly fine to have a one word answer.
    <br>
    <h4><span style='color:blue'><b>Example</b></span></h4>
    <span style='font-size: 18px'><b>Relevant Paragraph</b></span>
    <br>
    All of Notre Dame's undergraduate students are a part of one of the five undergraduate colleges at the school or are in the First Year of Studies program. The First Year of Studies program was established in 1962 to guide incoming freshmen in their first year at the school before they have declared a major. Each student is given an academic advisor from the program who helps them to choose classes that give them exposure to any major in which they are interested. The program also includes a Learning Resource Center which provides time management, collaborative learning, and subject tutoring. This program has been recognized previously, by U.S. News & World Report, as outstanding.
    <br>
    <br>
    <span style='font-size: 18px'><b>Question:</b> What entity provides help with the management of time for new students at Notre Dame?</span>
    <br>
    <br>
    <span style='font-size: 18px'><b>Correct Answer:</b> Learning Resource Center (Note that this answer is a <b>direct quote</b> and as <b>short as possible</b>)</span>
    <br>
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
                self.exs.append(ex)
        return self.exs.pop()


class SQuADVotingOnlyGC(SQuADGC):
    """
    When running this, you need to make sure that --random False is included.
    """

    TASK_IDENTIFIER = 'squad_voting'
    START_LABEL_MSG = '\nRound {}! Please determine the correct answer using \
        the given paragraph. Remember to look for a direct quote!'

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

    HIT_TITLE = 'Answer Questions with Friends! (Average $15/hr with Bonuses)'

    HIT_DESCRIPTION = 'You will help determine the best answer for each question by voting on which answer in a list is most correct.'

    HIT_KEYWORDS = 'vote,question,answer'

    ONBOARDING = \
    '''
    <h1><b>Player, prepare for Question/Answering...</b></h1>
    <br>
    Your goal is to vote for the correct answer for various questions.
    <br>
    In order to emerge victorious from this battle, your responses need to be correct.
    <br>
    <br>
    To ensure the game continues to progress, there is a time limit to vote for the correct one (30 seconds).
    <br>
    {}
    '''

    TASK_DESCRIPTION = \
    '''
    <h2><b>Description</b></h2>
    In this task, you will attempt to find answers to questions by voting on the correct one.
    <br>
    <h3><span style='color:blue'><b>Parts of Game</b></span></h3>
    This progression repeats between 3-6 times, usually 5.
    <h4><span style='color:blue'><b>Voting</b></span></h4>
    All the unique answers will appear under the example. Choose the response you believe is the <b>most correct</b> answer to the question.
    <br>
    Try to choose the most correct answer.
    <br>
    <h4><span style='color:blue'><b>Scoring and Bonuses</b></span></h4>
    After everyone has voted, the votes are tallied. The answer with the most votes is the winner! All the players that voted for the winning response receive a bonus.
    If there is a tie for top answer, then no bonuses are distributed.
    <br>
    <h4><span style='color:blue'><b>Example</b></span></h4>
    <span style='font-size: 18px'><b>Relevant Paragraph</b></span>
    <br>
    All of Notre Dame's undergraduate students are a part of one of the five undergraduate colleges at the school or are in the First Year of Studies program. The First Year of Studies program was established in 1962 to guide incoming freshmen in their first year at the school before they have declared a major. Each student is given an academic advisor from the program who helps them to choose classes that give them exposure to any major in which they are interested. The program also includes a Learning Resource Center which provides time management, collaborative learning, and subject tutoring. This program has been recognized previously, by U.S. News & World Report, as outstanding.
    <br>
    <br>
    <span style='font-size: 18px'><b>Question:</b> What entity provides help with the management of time for new students at Notre Dame?</span>
    <br>
    <br>
    <span style='font-size: 18px'><b>Correct Answer:</b> Learning Resource Center (Note that this answer is a <b>direct quote</b> and as <b>short as possible</b>)</span>
    <br>
    {}
    '''
    def __init__(self):
        super().__init__()
        self.ex_idcs = None
        self.exs = []

    def next_example(self, generator, total_rounds, offset):
        if self.ex_idcs is None:
            if offset != -1:
                # Non-random
                self.ex_idcs = range(offset, offset+(total_rounds*5), 5)
            else:
                # Random
                self.ex_idcs = random.sample(range(2, generator.num_episodes() - 3), 5)
            for idx in self.ex_idcs:
                ex = generator.get(idx)
                candidate_labels = []
                for cand_idx in range(idx-2, idx+3):
                    cand_ex = generator.get(cand_idx)
                    candidate_labels.append(cand_ex['labels'][0])
                ex['label_candidates'] = list(set(candidate_labels))
                self.exs.append(ex)
        return self.exs.pop()

    def load_cands(self, example):
        options = example['label_candidates']
        random.shuffle(options)
        cands = []
        for idx, lbl in enumerate(options):
            cands.append((idx, lbl, []))
        return cands


class SQuADVotingOnlySoloGC(SQuADVotingOnlyGC):
    """
    When running this, you need to make sure that --random False is included.
    """

    TASK_IDENTIFIER = 'squad_voting_solo'

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
    <br>
    <h3><span style='color:red'><b>IMPORTANT NOTICE</b></span></h4>
    1. <b>Be aware the conversations you have will be made public, so act as you would e.g. on a public social network like Twitter.</b>
    <br>
    2. Please do not send any message that could make others uncomfortable, including any level of discrimination, racism, sexism and offensive religious/politics comments, otherwise the submission will be rejected.
    <br>
    <br>
    """

    HIT_TITLE = 'Answer Questions! (Average $15/hr with Bonuses)'

    TASK_DESCRIPTION = \
    '''
    <h2><b>Description</b></h2>
    In this task, you will attempt to find answers to questions by voting on the correct one.
    <br>
    <h3><span style='color:blue'><b>Parts of Game</b></span></h3>
    This progression repeats between 3-6 times, usually 5.
    <h4><span style='color:blue'><b>Voting</b></span></h4>
    All the unique answers will appear under the example. Choose the response you believe is the <b>most correct</b> answer to the question.
    <br>
    Try to choose the most correct answer.
    <br>
    <h4><span style='color:blue'><b>Example</b></span></h4>
    <span style='font-size: 18px'><b>Relevant Paragraph</b></span>
    <br>
    All of Notre Dame's undergraduate students are a part of one of the five undergraduate colleges at the school or are in the First Year of Studies program. The First Year of Studies program was established in 1962 to guide incoming freshmen in their first year at the school before they have declared a major. Each student is given an academic advisor from the program who helps them to choose classes that give them exposure to any major in which they are interested. The program also includes a Learning Resource Center which provides time management, collaborative learning, and subject tutoring. This program has been recognized previously, by U.S. News & World Report, as outstanding.
    <br>
    <br>
    <span style='font-size: 18px'><b>Question:</b> What entity provides help with the management of time for new students at Notre Dame?</span>
    <br>
    <br>
    <span style='font-size: 18px'><b>Correct Answer:</b> Learning Resource Center (Note that this answer is a <b>direct quote</b> and as <b>short as possible</b>)</span>
    <br>
    {}
    '''

    def __init__(self):
        super().__init__()

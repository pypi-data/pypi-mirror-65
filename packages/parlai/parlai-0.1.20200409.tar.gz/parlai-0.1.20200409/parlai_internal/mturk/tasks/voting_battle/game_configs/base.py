#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.


class BaseGameConfig():
    """
    The base game configuration. This includes all of the default values for
    the various messaging constants along with the default functions.

    Should be overridden for each specific task you wish to use with this
    MTurk game.
    """
    ### CONSTANTS
    PLAYER = 'Player'
    # Stand-in for AgentID for truth label when it's included in voting cands
    TRUTH_ID = 'TRUTH_ID'
    # Name of field in example where image is saved
    IMAGE_FIELD_NAME = 'image'
    # Name of field in example where dialog is saved
    DIALOG_FIELD_NAME = 'text'
    # The name of the task from which your game loads examples. Must override!
    TASK_NAME = None
    # Name of the example mode for your task. Must override! Can be one of the
    # following: 'image', 'dialog', 'image_and_dialog'
    EXAMPLE_MODE = None
    # Flag for dialog tasks that determines if the conversation will utilize
    # the prior winning label to continue the conversation.
    CONTINUE_CONVERSATION = False

    ### ROUND INFO MESSAGES
    # Message sent at start of labeling portion of each round
    START_LABEL_MSG = '\nRound {}! Please look at the example and provide an engaging response.'
    # Fields of the example that will be used in the label message each round
    LABEL_START_FIELDS = []
    # Message sent at start of voting portion of each round
    START_VOTE_MSG = '\nChoose which response is the most engaging and click submit.'
    # Fields of the example that will be used in the vote message each round
    VOTE_START_FIELDS = []

    ### WAITING MESSAGES
    # Message shown to player when they are waiting for others to join
    WAITING_MSG = 'Waiting for other workers to join, DO NOT REFRESH THE PAGE. (Please be patient!)'
    # Waiting text shown to players after they have submitted their label but are
    # waiting for others to submit theirs
    WAITING_LABELS = 'Waiting for other players to respond to the example...'
    # Text shown to players after they have voted but others have not
    WAITING_VOTES = 'Waiting for other players to vote...'
    # Original waiting text shown to players, used in the singleplayer variants
    WAITING_ORIGINAL = 'Loading next example...'

    ### VOTING OUTCOME MESSAGES
    # Message shown to a player if their label was chosen as the winner and they
    # also voted for it
    WIN_WIN_MSG = 'Congratulations! Your response was chosen as the winner, so you \
        get a response bonus! You voted for it, but are not eligible for a vote \
        bonus as it is your own response.'
    # Message shown to a player if their label was chosen as the winner and they
    # did not vote for it
    WIN_LOSE_MSG = 'Congratulations! Your response was chosen as the winner, so \
        you get a response bonus!'
    # Message shown to a player if their label was not chosen as the winner but
    # they voted for the winning one
    LOSE_WIN_MSG = 'Congratulations! You voted for the winning response and earned \
        a bonus! Unfortunately, your response was not chosen as the winner. {}'
    # Message shown if label wasn't chosen and they didn't vote for winning one
    LOSE_LOSE_MSG = 'Uh-oh! Unfortunately your response was not voted the winner and \
        you did not vote for the winning response. {}'
    # Special LOSE_WIN message shown if this took place in a voting only game
    LOSE_WIN_NO_RESPONSE_MSG = 'Congratulations! You voted for the winning \
        response and earned a bonus!'
    # Special LOSE_LOSE message shown if this took place in a voting only game
    LOSE_LOSE_NO_RESPONSE_MSG = 'Uh-oh! Unfortunately you did not vote for \
        the winning response.'

    ### LOSE-LOSE ADDENDUM MESSAGES
    # Message shown after votes are tallied if you received no votes
    LOSE_NONE = "Better luck next time!"
    # Message shown after votes are tallied if you lost by 1-2 votes
    LOSE_CLOSE = "However, <b>you were close</b>, only {} {} behind the winner!"
    # Message shown after votes are tallied if you lost by more than 2 votes but
    # still recieved votes
    LOSE_FAR = "However, you still earned {} {}!"

    ### TIMEOUT MESSAGES
    # Message shown to players when someone has disconnected and the game
    # cannot continue
    TIMEOUT_MSG = '<b> Too many people have timed out. \
            Please click the "Done with this HIT" button below to finish \
            this HIT.</b>'
    # Message sent to player when they've timed out and next time will cause
    # them to disconnect from the task.
    TIMEOUT_LAST_CHANCE_MSG = 'You timed out. These HITs require constant \
        interaction with other Turkers, so please be attentive and respond \
        within the time allotted. Next time you timeout, you\'ll be kicked \
        from the HIT!'
    # Message sent to player when they've timed out and have at least one more
    # time out allowed before being disconnected.
    TIMEOUT_SECOND_CHANCE_MSG = 'You timed out. These HITs require constant \
        interaction with other Turkers, so please be attentive and respond \
        within the time allotted. You can only time out {} more {} before \
        being kicked.'
    # Warning message shown when a certain number of seconds are remaining to
    # respond or vote
    WARNING_MSG = 'Only {} seconds left to {}! Hurry to avoid a timeout!'

    ### OTHER MESSAGES
    # Message to tell players what the winning message was
    WIN_LABEL_MSG = 'The winning response was <b>\"{}\"</b>.'
    # Message shown if the winner was selected unanimously
    UNANIMOUS_MSG = 'Wow! Everyone agreed on which response was best, nice!'
    # Message shown to player if they used offensive language in a response
    OFFENSIVE_MSG = 'Our system detected that your previous response contained \
            offensive language. Please write a different response, thanks!'
    # Message shown to all players if we detect an attempt to collude.
    COLLUSION_MSG = 'We detected an attempt at collusion, so the HIT now is \
            ending!'

    ### TASK CONFIG CONSTANTS
    END_INFO = \
    """
    <h3><span style="color:blue"><b>Reward/Bonus</b></span></h3>
    There are four bonuses that can be won that push the average pay to $15/hr.
    <br>
    <ol>
        <li>Round Completion: successfully progress through all rounds without disconnecting or being kicked (all-or-nothing $0.70)</li>
        <li>Participation: do not time out at any point (all-or-nothing $0.40)</li>
        <li>Response Winner: write a response that is chosen as the winner for a single round ($0.25/occurrence)</li>
        <li>Voter Winner: vote for a response that is chosen as the winner for a single round ($0.15/occurrence)</li>
    </ol>
    There is a base pay rate of $0.05. So, for a given HIT, if you do not time out and finish all the rounds, you will earn $0.05 + $0.70 + $0.40 = $1.15.
    But, if you write all five winning responses, you can earn up to an extra $1.25 per HIT! Please note that bonuses are typically paid 2~4 days after the HIT is completed.
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
    3. This particular HIT can only be completed by an individual worker up to 5 times.
    <br>
    4. Pressing ENTER on your keyboard currently does not work to submit answers, so please manually click the SEND button.
    <br>
    <br>
    """

    HIT_TITLE = 'Write and Rate Comments (Average $15/hr with Bonuses)'

    HIT_DESCRIPTION = 'You will help determine the best response for each example with other people by writing responses with a personality and voting on the most engaging ones.'

    HIT_KEYWORDS = 'response,vote'

    ONBOARDING = \
    '''
    <h1><b>Player, prepare for a Comment Battle...</b></h1>
    <br>
    Your goal is to write and vote for the best responses for various examples.
    <br>
    In order to emerge victorious from this battle, your responses need to be engaging and creative.
    <br>
    <br>
    To ensure the game continues to progress, there is a time limit to submit a comment (60 seconds) as well as vote for the best one (30 seconds).
    <br>
    {}
    '''

    TASK_DESCRIPTION = \
    '''
    <h2><b>Description</b></h2>
    In this task, you will attempt to come up with the best responses for examples by either writing a response or voting on the best one.
    <br>
    <h3><span style='color:blue'><b>Parts of Game</b></span></h3>
    This progression repeats between 3-6 times, usually 5.
    <h4><span style='color:blue'><b>Responding</b></span></h4>
    You will see an example. Write an engaging response or comment about it.
    <br>
    Remember, you're competing against other Turkers to write the best one, so stay relevant and be creative!
    <br>
    <h4><span style='color:blue'><b>Voting</b></span></h4>
    All the different responses written will appear under the example. Choose the response you believe is the <b>most engaging</b> response to the example.
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
    <span><b>Sample responses</b></span>
    <br>
    <ul>
    <li>The mighty hunter peers over the edge, preparing to strike!</li>
    <li>They can't see me if I can't see them...</li>
    <li>The cat stares deep into the abyss, and it begins to stare back.</li>
    </ul>
    {}
    '''

    def __init__(self):
        assert self.TASK_NAME is not None, "When creating a GameConfig subclass, please override TASK_NAME."
        assert self.EXAMPLE_MODE is not None, "When creating a GameConfig subclass, please override EXAMPLE_MODE."

    def next_example(self, generator, total_rounds, offset):
        """
        Function to generate the next example used by the game. Most of the
        time this should not be overridden. An example usage could be using
        a datasets valid split, which is in the same order each time. This
        would allow for more randomization.
        """
        ex, _ = generator.next_example()
        return ex

    def process_dialog(self, example):
        """
        Function that takes the dialog from the DIALOG_FIELD_NAME field of the
        example and formats it for appearance in the game.

        Returns a HTML formatted dialog example.
        """
        dialog = example[self.DIALOG_FIELD_NAME]
        return dialog

    def create_start_message(self, round_idx, example):
        """
        Function that takes the round number and example and formats the
        relevant data into the START_LABEL_MSG.

        Returns the start message sent at the beginning of each round.
        """
        fields = [example[f] for f in self.LABEL_START_FIELDS]
        return self.START_LABEL_MSG.format(round_idx, *fields)

    def retrieve_truth_label(self, example):
        """
        Function that takes the example and extracts+formats the truth label
        to be displayed.

        Returns the HTML formatted truth label to be shown as a voting choice.
        """
        return example.get('labels', ['I don\'t know.'])[0]

    def load_cands(self, example):
        """
        Function that takes the example and returns a list of possible
        candidates in a triplet format of (cand_idx, cand, []).

        Only gets triggered if your task is trying to be ran in vote_only mode.
        """
        raise NotImplementedError('Abstract class: user must implement load_cands')

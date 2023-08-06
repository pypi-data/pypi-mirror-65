#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from parlai.mturk.core.worlds import MTurkOnboardWorld, MTurkTaskWorld
from parlai.mturk.core.agents import MTurkAgent
import parlai.mturk.core.mturk_utils as mturk_utils


def calc_bonus(data, reward, bonus_amount):
    # get number of levels!
    levels = [action['level'] for action in data if 'level' in action.keys()]
    nbr_levels = len(set(levels)) - 5  # remove the 5 tutorials
    amount, message = 0, "No passed levels"
    if nbr_levels > 0:
        remove = 1
        # check if passing the last level or if just tried without passing
        last_level = levels[-1]
        # get the actions terminate of last level and check if worker had a positive reward
        data_last_level = [action for action in data if ('level' in action.keys())
                           and (action['level'] == last_level)
                           and (action['text'] == 'terminate')]
        for potential_end in data_last_level:
            if potential_end['state']['totalscore'] > 0:
                remove = 0

        nbr_levels -= remove

        if nbr_levels == 15:
            amount, message = reward, 'You won both games'
        else:
            amount, message = nbr_levels * bonus_amount, f'You have passed {nbr_levels} levels'
    # make sure it's not above the max
    amount = min(reward, amount)
    amount = round(amount, 2)
    return amount, message


class GameOnboardWorld(MTurkOnboardWorld):

    temp_required_messages_retrospector = ["In this task, you will have an inventory with various objects which you can combine [craft] \
                            to create other objects or remove from the inventory [drop].\
                            Each object has a positive or negative value. Your aim is to maximize the total value of your \
                            inventory and press the button [terminate] to move to the next level. Type {} and press Send, if you want to proceed.",

                                           "The task is divided into 3 different stages, \
                            each of which is a game structured into levels; <br>\
                            - The first game: a tutorial game \
                            where you will learn how to drop or create items.; <br>\
                            - The second game: a game structured into 11 levels of increasing complexity. After passing a level of this game\
                            YOU WILL BE ASKED TO WRITE DOWN A DESCRIPTION OF HOW YOU PASSED THAT LEVEL; <br>\
                            - The third game: a game structured into 4 levels. <br>\
                            Type {} and press Send, if you want to proceed. We will next tell you how your \
                            AMT reward for playing the game is determined.",

                                           "The task has 15 levels (excluding the tutorial game). If you complete a level (from game 2 or 3) you gain 0.70 dollars. \
                            If you finish all the levels, you have an extra 4.5 dollars. In total, if you finish the whole task you get 15 dollars.\
                            The whole task takes 1 hour approx, but we leave you up to 2 hours to finish. <br>\
                            <br>\
                            You can [Abort] at any point; you will be paid only the completed levels and cannot go back and restart. \
                            Attention, if you abandon by closing your browser without pressing [Abort] you will be paid NOTHING. You still need to submit your HIT \
                            (Mechanical Turk does not know you have worked unless you exit properly from the game). Type {} and press Send, if you want to proceed."]

    temp_required_messages_control = ["In this task, you will have an inventory with various objects which you can combine [craft] \
                            to create other objects or remove from the inventory [drop].\
                            Each object has a positive or negative value. Your aim is to maximize the total value of your \
                            inventory and press the button [terminate] to move to the next level. Type {} and press Send, if you want to proceed.",

                                      "The task is divided into 3 different stages, \
                            each of which is a game structured into levels; <br>\
                            - The first game: a tutorial game \
                            where you will learn how to drop or create items; <br>\
                            - The second game: a game structured into 11 levels of increasing complexity. After passing a level of this game\
                            YOU MIGHT BE ASKED TO WRITE DOWN A DESCRIPTION OF HOW YOU PASSED THE LEVEL; <br>\
                            - The third game: a game structured into 4 levels. <br>\
                            Type {} and press Send, if you want to proceed. We will next tell you how your \
                            AMT reward for playing the game is determined.",

                                      "The task has 15 levels (excluding the tutorial game). If you complete a level (from game 2 or 3) you gain 0.50 dollars. \
                            If you finish all the levels, you have an extra 2.5 dollars. In total, if you finish the whole task you get 10 dollars.\
                            The whole task takes 1 hour approx, but we leave you up to 2 hours to finish. <br>\
                            <br>\
                            You can abondon at any point by clicking on the button [Abort]; you will be paid only the completed levels and cannot go back and restart. \
                            Attention, if you abandon by closing your browser (or waiting for an auto-submission) without pressing [Abort] you will be paid NOTHING \
                            (Mechanical Turk does not know you have worked unless you exit properly from the game). You need then to either finish the whole task or click on the [Abort] button. Type {} and press Send, if you want to proceed."]

    required_replies = ["OK", "OK", "CONTINUE"]
    required_messages_retrospector = [x.format(y) for (x, y) in zip(
        temp_required_messages_retrospector, required_replies)]
    required_messages_control = [x.format(y) for (x, y) in zip(
        temp_required_messages_control, required_replies)]

    def __init__(self, opt, mturk_agent):
        self.mturk_agent = mturk_agent
        self.episodeDone = False
        self.turn_index = 0
        self.opt = opt

    def parley(self):
        ad = {}
        ad['id'] = 'Instructions'

        if (self.opt['experiment'] == 'retrospector'):
            ad['text'] = self.required_messages_retrospector[self.turn_index]
        elif (self.opt['experiment'] == 'control'):
            ad['text'] = self.required_messages_control[self.turn_index]
        else:
            print('Type of experiment is not defined correctly')

        self.mturk_agent.observe(ad)
        reply = self.mturk_agent.act()
        if reply['text'].lower() == self.required_replies[self.turn_index].lower():
            self.turn_index += 1
        if self.turn_index == len(self.required_replies):
            self.episodeDone = True


class GameWorld(MTurkTaskWorld):
    """
    Launches the js-based game; writes down Turker's actions; pays bonus.
    """
    def __init__(self, opt, mturk_agent, qual_id):
        self.mturk_agent = mturk_agent
        self.episodeDone = False
        self.turn_index = -1
        self.data = []
        self.opt = opt
        self.qual_id = qual_id

    def parley(self):
        act = self.mturk_agent.act()
        if act['episode_done']:
            self.episodeDone = True
        self.data.append(act)

    def episode_done(self):
        return self.episodeDone

    def report(self):
        pass

    def shutdown(self):
        import json
        import uuid
        import os

        '''
        Here is where the filtering occurs. If a worker has already participated
        in a crafting experiment, he/she is given the 'CraftingAlreadyDone'
        qualification.
        '''
        if not self.opt['no_craft_qualification']:
            mturk_utils.give_worker_qualification(
                self.mturk_agent.worker_id,
                self.qual_id,
                is_sandbox=self.opt['is_sandbox'],
            )

        root_dir = os.path.dirname(os.path.abspath(__file__))
        if (self.opt['experiment'] == 'retrospector'):
            directory = f'{root_dir}/worker_actions_retrospector'
        elif (self.opt['experiment'] == 'control'):
            directory = f'{root_dir}/worker_actions_controlGroup'
        else:
            raise ValueError('Type of experiment is not defined correctly')

        if not os.path.exists(directory):
            os.makedirs(directory)

        file_name = f'{directory}/{self.mturk_agent.worker_id}_{uuid.uuid4().hex}.json'
        with open(file_name, 'w') as fp:
            json.dump(self.data, fp)

        self.mturk_agent.shutdown()

        bonus_for_worker, reason = calc_bonus(
            self.data, self.opt['bonus_final'], self.opt['bonus'])
        if bonus_for_worker > 0:
            self.mturk_agent.approve_work()
            self.mturk_agent.pay_bonus(bonus_for_worker, reason=reason)

    def review_work(self):
        pass

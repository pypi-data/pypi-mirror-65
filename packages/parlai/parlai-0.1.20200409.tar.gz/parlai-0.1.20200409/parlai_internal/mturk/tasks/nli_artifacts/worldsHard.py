#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from parlai.mturk.core.worlds import MTurkOnboardWorld, MTurkTaskWorld
import threading
import csv
import random
import logging

all_rowsies=[]
with open('/Users/adinawilliams/ParlAI/parlai_internal/mturk/tasks/nli_artifacts/MTurkLists/NLIArtifactsLista.csv') as csvfile:
    for row in csv.DictReader(csvfile, skipinitialspace=True):
        all_rowsies.append(row)
        random.shuffle(all_rowsies)
logging.info('loaded stuff')
logging.info(csvfile)


class NLIArtifactsOnboardingWorld(MTurkOnboardWorld):
    """ Onboarding world sets up the task and asks the user to give values
    to N pre-set examples, providing feedback for their responses.
    """

    questions = [
        {
            'setting': " Imagine that all of the images from a popular photo sharing website are in a folder, but you can't see them. Please use the slider to indicate how many of the photos are compatible with:",
            'scenario': 'An older and younger man smiling.',
            'hint': 'Think of a photo sharing website! Photos of two smiling men are very common on photo sharing websites, and a good number of those photos will have men of different ages. But, it is unlikely more than 20 percent will contain them.',
            'ans_low': 50,
            'ans_high': 90,
        },
        {
            'setting': " Great! Let's try another example! Imagine that all of the images from a popular photo sharing website are in a folder, but you can't see them. Here's the sentence:",
            'scenario': 'Two older men are proudly smiling at four three-legged tabby cats that are rolling around on a shiny marble floor.',
            'hint': 'Think of a photo sharing website! This sentence is very unlikely to be an appropriate caption for more than a one or two photos, because photos containing multiple three-legged cat are not very common, let alone tabby ones rolling on a marble floor and being laughed at by two proud older men.',
            'ans_low': 0,
            'ans_high': 50,
        },
        {
            'setting': " Awesome! Let's try one last example! The folder contains images from a popular photo sharing website.",
            'scenario': 'Two men are smiling and laughing at the cats on the floor.',
            'hint': 'Think of a photo sharing website! Photos of men smiling and laughing at cats on the floor are pretty common, but not every photo will contain these things.',
            'ans_low': 15,
            'ans_high': 65,
        },
    ]

    introquestions = [
        {   'setting': " Does this make sense to you?",
            'scenario': 'Move the slider all the way to the right if it does! (you can ignore the labels for now)',
            'hint': 'Are you sure you moved the slider all the way to the right?',
            'ans_low': 99,
            'ans_high': 100,
            },
        {   'setting': " Does this make sense to you?",
            'scenario': 'Move the slider all the way to the left if it does! (you can ignore the labels for now)',
            'hint': 'Are you sure you moved the slider all the way to the left?',
            'ans_low': 0,
            'ans_high': 1,
            },
        {   'setting': " You can refer to the instructions on the left if you get confused.",
            'scenario': 'Please move the slider to the left if you acknowledge this! (we will explain the labels in a second)',
            'hint': 'Are you sure you moved the slider to the left?',
            'ans_low': 0,
            'ans_high': 50,
            },
        {   'setting': " Great! Plausible sentences are compatible with many items.",
            'scenario': 'Move the slider right if you are ready to continue.',
            'hint': 'Are you sure you moved the slider to the right?',
            'ans_low': 90,
            'ans_high': 100,
            }
        ]

    def __init__(self, opt, mturk_agent):
        self.mturk_agent = mturk_agent
        self.current_question = 0
        self.episodeDone = False

    def parley(self):
        # Send initial instructions
        ad0 = {'id': 'System'}
        ad0['text'] = (
            " Welcome aboard! Let's take a moment "
            "to go over some important information."
            )
        self.mturk_agent.observe(ad0)

        ad00 = {'id': 'System'}
        ad00['text'] = (
            " We are trying to figure out how plausible sentences are. A "
            "sentence is plausible if you would expect to see it "
            "in your day-to-day life. "
            )
        self.mturk_agent.observe(ad00)
        introquestionsa = self.introquestions[1]
        introquestion_act = {
            'id': 'System',
            'text': "{}<br/><em>{}</em>".format(introquestionsa['setting'],
            introquestionsa['scenario'])
            }
        self.mturk_agent.observe(introquestion_act)
        gotten_value = self.mturk_agent.act()['text']

        ad01 = {'id': 'System'}
        ad01['text'] = (
            " Great! Keep in mind that plausibility won't always depend on how "
            "complicated or long the sentence is. But, it does depend on context."
            )
        self.mturk_agent.observe(ad01)

        ad001 = {'id': 'System'}
        ad001['text'] = (
            " For example, if you saw the sentence: 'Hundreds of "
            "thousands of miles of undersea cables connect the continents to "
            "feed our demand for communication and constant entertainment.' "
            "You'd think it was not a plausible everyday sentence. It's "
            "probably not a sentence you or your friends often say.  "
            )
        self.mturk_agent.observe(ad001)

        ad002 = {'id': 'System'}
        ad002['text'] = (
            " But, if you were told it was from the New York "
            "Times, you'd probably think it was very plausible. You "
            "wouldn't be at all surprised to encounter it when "
            "reading the newspaper. "
            )
        self.mturk_agent.observe(ad002)
        introquestionss = self.introquestions[0]
        introquestion_act = {
            'id': 'System',
            'text': "{}<br/><em>{}</em>".format(introquestionss['setting'], introquestionss['scenario'])
        }
        self.mturk_agent.observe(introquestion_act)
        gotten_value = self.mturk_agent.act()['text']

        ad5 = {'id': 'System'}
        ad5['text'] = (
            " Please read the instructions in the green pane on the left "
            "side of your screen before you continue. "
            )
        self.mturk_agent.observe(ad5)
        introquestions1 = self.introquestions[2]
        introquestion_act = {
            'id': 'System',
            'text': "{}<br/><em>{}</em>".format(introquestions1['setting'], introquestions1['scenario'])
        }
        self.mturk_agent.observe(introquestion_act)
        gotten_value = self.mturk_agent.act()['text']

        ad = {'id': 'System'}
        ad['text'] = (
            " Nice! Let's recap! Plausible sentences will be "
            "compatible with many items in the folder. "
            "A sentence is compatible with an item if they mean "
            "roughly the same thing, if they describe the same sitation(s), "
            "or if the sentence could be an adequate replacement for the item. "
            "First read the context, then slide the "
            "slider to the left or right to tell us how plausible that "
            "sentence is to you in that context. "
            "Don't worry if it sounds complicated, we'll try some examples "
            "together in a sec.")
        self.mturk_agent.observe(ad)

        ad3 = {'id': 'System'}
        ad3['text'] = (
            " One last piece of advice: Pay attention! Contexts change "
            "throughout. Please take time to "
            "read both the instructions and the sentences thoroughly before "
            "responding. Ready? Let's give it a try!"
            )
        self.mturk_agent.observe(ad3)

        while self.current_question < len(self.questions):
            # Get and ask a question
            question = self.questions[self.current_question]
            question_act = {
                'id': 'System',
                'text': "{}<br/><em>{}</em>".format(
                    question['setting'], question['scenario'],
                )
            }
            self.mturk_agent.observe(question_act)
            gotten_value = self.mturk_agent.act()['text']

            if gotten_value in ['[DISCONNECT]', '[RETURNED]', '[TIMOUT]']:
                self.episodeDone = True
                return

            # Keep prodding until the value is correct
            while float(gotten_value) >= question['ans_high'] or \
                    float(gotten_value) < question['ans_low']:
                wrong_answer_act = {
                    'id': 'System',
                    'text': "Hmm...are you sure that makes sense? hint: {}".format(
                        question['hint'],
                    )
                }
                self.mturk_agent.observe(wrong_answer_act)
                gotten_value = self.mturk_agent.act()['text']
            # Move to next question
            self.current_question += 1

        self.episodeDone = True


class NLIArtifactsTaskWorld(MTurkTaskWorld):
    """
    This task asks participants to indicate, using a slider, how many sentences
    in an unseen set are likely to be compatible with a prompt sentence.
    """

    collector_agent_id = 'System'

    MIN_TURNS = 92  #
    MAX_TURNS = 92  #
    # bns = 0.02  # bonus pay

    def get_next_question(self):
        current_row = self.all_rows[self.turn]
        return {'setting': current_row['instructions'],
                'scenario': current_row['sentence2']}

    def __init__(self, opt, mturk_agents):
        self.mturk_agent = mturk_agents[0]
        self.episodeDone = False
        self.turn = 0
        self.answers = []
        self.all_rows = all_rowsies  # ugly hardcoding

    def parley(self):

        if self.turn == 0:
            ad = {
                'id': 'System',
                'text': "Great job so far! Let's start the main task. "
                "Please give estimates for the sentences below:",
            }
            self.mturk_agent.observe(ad)
        question = self.get_next_question()
        question_act = {
            'id': 'Sentence {}'.format(self.turn + 1),
            'text': "{}<br/><em>{}</em>".format(question['setting'], question['scenario'],
            )
        }
        self.mturk_agent.observe(question_act)
        gotten_text = self.mturk_agent.act()['text']

        if (gotten_text == '[DONE]'):
            ad = {
                'id': 'System',
                'text': "Thanks for your answers!",
            }
            self.mturk_agent.observe(ad)
            self.episodeDone = True
            return

        if gotten_text in ['[DISCONNECT]', '[RETURNED]', '[TIMOUT]']:
            self.episodeDone = True
            return

        gotten_value = float(gotten_text)
        self.answers.append({
            'question': question,
            'answer': gotten_value,
        })
        self.turn += 1

        # randomyint = random.randint(7, 9)  # make a random integer to determine whether to give encouragement!

        # if self.turn == self.MIN_TURNS:
        #     ad = {
        #         'id': 'System',
        #         'text':
        #             "You have responded to the minimum number of prompts. "
        #             "At this point you can keep going for an additional $0.02 "
        #             "bonus per answer.",
        #         'enough_turns': True,
        #     }
        #     self.mturk_agent.observe(ad)

        if self.turn == 5 :
            ad = {
                'id': 'System',
                'text':
                    "You're doing really well! Keep up the good work!",
                'enough_turns': False,
            }
            self.mturk_agent.observe(ad)

        if self.turn == 50 :
            ad = {
                'id': 'System',
                'text':
                    "Hang in there! We appreciate your effort!",
                'enough_turns': False,
            }
            self.mturk_agent.observe(ad)

        if self.turn % 33  == 0 :
            ad = {
                'id': 'System',
                'text':
                    "Feel free to take a short break if you need it!",
                'enough_turns': False,
            }
            self.mturk_agent.observe(ad)

        if (((self.turn)>self.MIN_TURNS) & (self.turn % 20 == 0)) :
            ad = {
                'id': 'System',
                'text':
                    "Thanks for your time! Your responses are very useful.",
                'enough_turns': False,
            }
            self.mturk_agent.observe(ad)

        if self.turn == self.MAX_TURNS :
            ad = {
                'id': 'System',
                'text': "You have completed the task. Thank you!",
            }
            self.mturk_agent.observe(ad)
            self.episodeDone = True

        # if (((self.turn-self.MIN_TURNS)>0) & (self.turn % (randomyint)  == 0)) :
        #     ad = {
        #         'id': 'System',
        #         'text':
        #             "Thanks! You've made ${} bonus so far!".format((self.turn-self.MIN_TURNS)*self.bns, '.2f'),
        #         'enough_turns': True,
        #     }
        #     self.mturk_agent.observe(ad)

    def episode_done(self):
        return self.episodeDone

    def shutdown(self):
        self.mturk_agent.shutdown()
        # self.mturk_agent.pay_bonus(self.bns, 'going above and beyond!')
        # TODO fill in reason

    def get_custom_task_data(self):
        return {
            'answers': self.answers,
        }

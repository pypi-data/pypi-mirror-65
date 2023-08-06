#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from parlai.core.agents import create_agent_from_shared
from parlai.mturk.core.worlds import MTurkOnboardWorld
from parlai.mturk.core.agents import TIMEOUT_MESSAGE
from parlai.core.worlds import validate, MultiAgentDialogWorld
from joblib import Parallel, delayed
import numpy as np

from urllib.request import urlretrieve
import pickle
import random
import uuid
import re
import time
import os
import logging


TOPICS = [
    "advices", "animes", "art", "best sandwich", "bikes", "books", "career",
    "cars", "college", "comics", "crazy ideas", "dreams", "family",
    "favourite bands", "food", "friends", "gardening", "grand parents",
    "hobbies", "kids", "kitchen", "movies", "music", "nature", "newspapers",
    "pets", "planes", "podcasts", "recipes", "restaurants", "running", "school",
    "science", "secrets", "significant other", "smartphones",
    "social networks", "sports", "superpowers", "talents", "teachers",
    "technology", "time travel", "travels", "trips", "TV series",
    "video games", "weather", "work", "work hours", "your boss"
]

# Instruction messages
ONBOARD_MSG = '\nWhen you are ready to start your conversation, \
        click the "I am ready, continue" button below\n'
START_MSG = '\nSuccessfully matched. \
        Now let\'s chit-chat! \n\
        You need to finish <b>{} chat turns</b>, \
        after which you can click the "Done" button to end the chat. \n \
        <b>You can see suggested topics of discussion on the left.</b> \n'
CHAT_NOT_DONE_MSG = 'Sorry, we need at least <b>{} more turn(s)</b> to finish. \
       Please send a new message:'
TIMEOUT_MSG = '<b> The other person has timed out. \
        Please click the "Done with this HIT" button below to finish this HIT.\
        </b>'
EXCEED_MIN_TURNS_MSG = '\n {} chat turns finished! \n \
        You can click the "Done" button to end the chat if it\'s your turn \
        or keep chatting.'
UNEXPECTED_DISCONNECTION_MSG = 'The other worker unexpectedly diconnected. \n \
        Please click <span style="color:blue"><b>Done with this HIT</b>\
        </span> button below to finish this HIT.'
CHAT_ENDED_MSG = 'One of you ended the chat. Thanks for your time! \n\
        Please click <span style="color:blue"><b>Done with this HIT</b>\
        </span> button below to finish this HIT.'
WAITING_MSG = 'Please wait while we match you with another worker...'
NAN_MSG = 'The score you entered must be in [1, 2, 3, 4, 5]. Please \
        try again:'
ROUNDS_MSG = 'Please input your score in the proper format, e.g.: "1,3,12", \
    "2,11", "2" or "00" if everything was ok.'
TOO_SHORT_MSG = 'Your message is too short, please make it more than \
        <b><span style="color:red">{} words</span></b>.'
TOO_LONG_MSG = 'Your message is too long, please make it less than \
        <b><span style="color:red">{} words</span></b>.'

# Evaluation messages
GENERAL_MARK_MSG = 'You\'ve completed this conversation, thanks! We hope you \
    enjoyed it, now comes the crucial part: the review!\n Answering with a number\
    from 1 to 5, tell us how well the conversation went; 5 being if it was a \
    conversation you could\'ve had with a human.'

DIALOG_FORM_MSG = 'Which rounds felt <b>unnatural</b>?'
TOPICAL_MARK_MSG = 'Which rounds felt <b>out of topic</b>?'
ENGAGINGNESS_MSG = 'Would you talk to this bot again?'


FREEFORM_MSG = 'This is a free form evaluation. ' +\
    'Can you pinpoint what in particular made your partner feel or not ' +\
    'feel like a bot? You can type "pass".'


def random_topics(k=5):
    return random.sample(TOPICS, k=k)


with open('/private/home/matu/data/mturk_openers.txt') as fi:
    openers = [e.strip() for e in fi]


class DialogEvalWorld(MultiAgentDialogWorld):

    def __init__(
        self, opt, agents=None, shared=None,
        range_turn=[8, 12],
        max_resp_time=300,
        max_eval_time=540,  # 9min
        model_agent_opt=None,
        world_tag='',
        agent_timeout_shutdown=120
    ):

        self.opt, self.model_agent_opt = opt, model_agent_opt
        self.turn_idx = 0
        self.range_turn = range_turn
        self.n_turn = np.random.randint(*range_turn)

        self.model_name = opt.get('model_name')
        self.agent_name = "PERSON_2"
        self.task_type = 'sandbox' if opt['is_sandbox'] else 'live'

        self.dialog = []
        self.chat_done = False
        self.topics = random_topics()
        self.topics_str = '\n'.join(self.topics)

        self.general_mark = len(agents) * [-1]
        self.bad_rounds = len(agents) * [None]
        self.engagingness = len(agents) * [None]
        self.free_comment = len(agents) * [None]
        self.world_tag = world_tag
        self.rounds = list(map(str, range(1, self.n_turn + 1))) + [
            f'{i:02d}' for i in range(self.n_turn + 1)]

        super().__init__(opt, agents, shared)

        self.model_agent = create_agent_from_shared(model_agent_opt)
        self.agent_name = 'PERSON_2' if self.agents[0].id == 'PERSON_1' else 'PERSON_1'

        # below are timeout protocols
        self.max_resp_time = max_resp_time  # in secs
        self.max_eval_time = max_eval_time  # in secs
        self.agent_timeout_shutdown = agent_timeout_shutdown

    def parley(self):

        logging.info(f'Conv {self.world_tag} starting round {self.turn_idx}')
        self.turn_idx += 1

        control_msg = {'episode_done': False, 'id': 'SYSTEM'}
        human = self.agents[0]
        bot = self.model_agent

        if self.turn_idx == 1:
            control_msg.update({
                'topics_str': '\n'.join(self.topics),
                'text': self.get_instruction(tag='start', agent_id=human.id)
            })
            human.observe(validate(control_msg))
            time.sleep(1)

        if self.turn_idx == self.n_turn + 1:
            self.chat_done = True
            return

        act1 = human.act(timeout=self.max_resp_time)
        while self.is_msg_tooshortlong(act1, human):
            act1 = human.act(timeout=self.max_resp_time)
        bot.observe(act1)

        utt = bot.act()['text']
        utt = re.sub(r' ([\.\?!,])', r'\1', utt)
        utt = re.sub(r'^i ', 'I ', utt)
        utt = re.sub(r' i ', ' I ', utt)
        mid = act1['message_id']
        act2 = {
            'text': utt,
            'id': self.agent_name,
            'message_id': mid[:-1] + '0' if mid[-1] != '0' else mid[:-1] + '1'
        }
        time.sleep(random.random() * len(utt.split(' ')) * 0.8)
        human.observe(act2)

        self.dialog.extend(enumerate([act1['text'], act2['text']]))

    def evaluate(self):
        control_msg = {'episode_done': False, 'id': 'SYSTEM'}
        acts = [None]

        # General mark
        for idx, agent in enumerate(self.agents):
            control_msg['text'] = GENERAL_MARK_MSG
            control_msg['evaluation'] = True
            control_msg['general_mark'] = True
            agent.observe(validate(control_msg))
            acts[idx] = agent.act(timeout=self.max_eval_time)
            if not self.check_exceptions(acts[idx]):
                self.general_mark[idx] = acts[idx]['text']

        # Bad rounds
        for idx, agent in enumerate(self.agents):
            control_msg['text'] = DIALOG_FORM_MSG
            control_msg['rounds_mark'] = True
            control_msg['rounds'] = '</ROUND>'.join([
                '\n'.join([self.dialog[i][1], self.dialog[i + 1][1]])
                for i in range(0, len(self.dialog), 2)
            ])
            agent.observe(validate(control_msg))
            acts[idx] = agent.act(timeout=self.max_eval_time)
            if not self.check_exceptions(acts[idx]):
                self.bad_rounds[idx] = f'{acts[idx]}'

        # Engagingness
        for idx, agent in enumerate(self.agents):
            control_msg['text'] = ENGAGINGNESS_MSG
            control_msg['engagingness'] = True
            agent.observe(validate(control_msg))
            acts[idx] = agent.act(timeout=self.max_eval_time)
            if not self.check_exceptions(acts[idx]):
                self.engagingness[idx] = f'{acts[idx]}'

        # Freeform
        for idx, agent in enumerate(self.agents):
            control_msg['text'] = FREEFORM_MSG
            control_msg['comment'] = True
            agent.observe(validate(control_msg))
            acts[idx] = agent.act(timeout=self.max_eval_time)
            while acts[idx]['text'] == '':
                control_msg['text'] = 'Please try again.'
                agent.observe(validate(control_msg))
                acts[idx] = agent.act(timeout=self.max_eval_time)
            if not self.check_exceptions(acts[idx]):
                self.free_comment[idx] = acts[idx]['text']

        # reached the end of the chat
        self.chat_done = True
        for ag in self.agents:
            # ag.observe(validate(acts[idx]))
            control_msg['text'] = CHAT_ENDED_MSG
            ag.observe(validate(control_msg))
        return

    def episode_done(self):
        return self.chat_done

    def get_instruction(self, agent_id=None, tag='first'):
        if tag == 'start':
            return START_MSG.format(self.n_turn)

        if tag == 'chat_not_done':
            return CHAT_NOT_DONE_MSG.format(self.n_turn + 1 - self.turn_idx)

        if tag == 'timeout':
            return TIMEOUT_MESSAGE

        if tag == 'exceed_min_turns':
            return EXCEED_MIN_TURNS_MSG.format(self.n_turn)

    def save_data(self):
        convo_finished = True
        bad_workers = []
        for ag in self.agents:
            if (ag.hit_is_abandoned or ag.hit_is_returned or
                    ag.disconnected or ag.hit_is_expired):
                bad_workers.append(ag.worker_id)
                convo_finished = False

        if not convo_finished or self.dialog == []:
            convo_finished = False

        data_path = self.opt['data_path']
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        if convo_finished:
            filename = os.path.join(
                data_path, '{}_{}_{}_{}_withreasons.pkl'.format(
                    self.model_name,
                    time.strftime("%Y%m%d-%H%M%S"),
                    np.random.randint(0, 1000),
                    self.task_type
                )
            )
        else:
            filename = os.path.join(
                data_path,
                '{}_{}_{}_{}_incomplete_withreasons.pkl'.format(
                    self.model_name,
                    time.strftime("%Y%m%d-%H%M%S"),
                    np.random.randint(0, 1000),
                    self.task_type
                )
            )
        logging.info(
            f'{self.world_tag}: Data successfully saved at\n\t{filename}')

        pickle.dump({
            'opt': self.opt,
            'model_agent_opt': self.model_agent_opt['opt'],
            'topics': self.topics,
            'dialog': self.dialog,
            'workers': [ag.worker_id for ag in self.agents],
            'bad_workers': bad_workers,
            'n_turn': self.n_turn,
            'general_mark': self.general_mark,
            'bad_rounds': self.bad_rounds,
            'engagingness': self.engagingness,
            'free_comment': self.free_comment},
            open(filename, 'wb'))

    def is_msg_tooshortlong(self, act, ag, th_min=3, th_max=20):
        if act['episode_done']:
            return False

        control_msg = {'episode_done': False}
        control_msg['id'] = 'SYSTEM'

        msg_len = len(act['text'].split(' '))
        if msg_len < th_min:
            control_msg['text'] = TOO_SHORT_MSG.format(th_min)
            ag.observe(validate(control_msg))
            return True
        if msg_len > th_max:
            control_msg['text'] = TOO_LONG_MSG.format(th_max)
            ag.observe(validate(control_msg))
            return True
        return False

    def reset_random(self):
        self.n_turn = np.random.randint(
            self.range_turn[0],
            self.range_turn[1]
        ) + 1

    def check_timeout(self, act):
        if act['text'] == '[TIMEOUT]' and act['episode_done']:
            control_msg = {'episode_done': True}
            control_msg['id'] = 'SYSTEM'
            control_msg['text'] = self.get_instruction(
                agent_id=act['id'],
                tag='timeout'
            )
            for ag in self.agents:
                if ag.id != act['id']:
                    ag.observe(validate(control_msg))
            self.chat_done = True
            return True
        else:
            return False

    def check_exceptions(self, act):
        exceptions = ['[TIMEOUT]', '[DISCONNECT]', '[RETURNED]']
        if act['text'] in exceptions:

            if act['text'] == '[TIMEOUT]':
                text = self.get_instruction(agent_id=act['id'], tag='timeout')
            else:
                text = 'Received a Disconnect or a Returned message'

            for agent in [a for a in self.agents if a.id != act['id']]:
                agent.observe(validate({
                    'episode_done': True,
                    'id': 'SYSTEM',
                    'text': text
                }))
            self.chat_done = True
            return True
        else:
            return False

    def shutdown(self):
        global shutdown_agent

        def shutdown_agent(mturk_agent):
            mturk_agent.shutdown()

        Parallel(
            n_jobs=len(self.agents),
            backend='threading'
        )(delayed(shutdown_agent)(agent) for agent in self.agents)


class DialogEvalHumanHumanWorld(MultiAgentDialogWorld):

    def __init__(
        self, opt, agents=None, shared=None,
        range_turn=[8, 12],
        max_resp_time=300,
        max_eval_time=540,  # 9min
        world_tag='',
        agent_timeout_shutdown=120
    ):

        self.opt = opt
        self.turn_idx = 0
        self.range_turn = range_turn
        self.n_turn = np.random.randint(*range_turn)

        self.model_name = opt.get('model_name')
        self.agent_name = "PERSON_2"
        self.task_type = 'sandbox' if opt['is_sandbox'] else 'live'

        self.dialog = []
        self.chat_done = False
        self.topics = random_topics()
        self.topics_str = '\n'.join(self.topics)

        self.general_mark = len(agents) * [-1]
        self.bad_rounds = len(agents) * [None]
        self.engagingness = len(agents) * [None]
        self.free_comment = len(agents) * [None]
        self.world_tag = world_tag
        self.rounds = list(map(str, range(1, self.n_turn + 1))) + [
            f'{i:02d}' for i in range(self.n_turn + 1)]

        super().__init__(opt, agents, shared)

        # below are timeout protocols
        self.max_resp_time = max_resp_time  # in secs
        self.max_eval_time = max_eval_time  # in secs
        self.agent_timeout_shutdown = agent_timeout_shutdown

    def parley(self):

        logging.info(f'Conv {self.world_tag} starting round #{self.turn_idx}')
        self.turn_idx += 1

        control_msg = {'episode_done': False, 'id': 'SYSTEM'}

        """ If at first turn, we need to give each agent their topics """
        if self.turn_idx == 1:
            for idx, agent in enumerate(self.agents):
                control_msg.update({
                    'topics_str': '\n'.join(self.topics),
                    'text': self.get_instruction(tag='start', agent_id=agent.id)
                })
                agent.observe(validate(control_msg))
                if idx == 0:
                    time.sleep(1)

        """ Give possibility to end """
        if self.turn_idx == self.n_turn + 1:
            self.chat_done = True
            return

        """ Otherwise, we proceed accordingly """
        acts = [None, None]
        for aid, agent in enumerate(self.agents):

            logging.info(f'{self.world_tag}-{self.turn_idx}: agent {aid}')
            other_agent = self.agents[1 - aid]
            acts[aid] = agent.act(timeout=self.max_resp_time)

            if self.check_exceptions(acts[aid]):
                acts[aid]['episode_done'] = True
                self.chat_done = True

            if acts[aid] is not None:

                while self.is_msg_tooshortlong(acts[aid], agent):
                    acts[aid] = agent.act()

                self.dialog.append((aid, acts[aid]['text']))
                logging.info(f'agent {1-aid} observe')
                other_agent.observe(acts[aid])

    def episode_done(self):
        return self.chat_done

    def evaluate(self):
        global get_eval

        def get_eval(agent, aid):

            logging.info(f'Agent {aid} entering eval')
            control_msg = {'episode_done': False, 'id': 'SYSTEM'}
            control_msg.update({
                'text': GENERAL_MARK_MSG,
                'evaluation': True,
                'general_mark': True})
            agent.observe(validate(control_msg))

            act = agent.act(timeout=self.max_eval_time, blocking=True)
            if not self.check_exceptions(act):
                self.general_mark[aid] = act['text']

            # Bad rounds
            # for idx, agent in enumerate(self.agents):
            control_msg['text'] = DIALOG_FORM_MSG
            control_msg['rounds_mark'] = True
            control_msg['rounds'] = '</ROUND>'.join([
                '\n'.join([self.dialog[i][1], self.dialog[i + 1][1]])
                for i in range(0, len(self.dialog), 2)
            ])
            agent.observe(validate(control_msg))
            act = agent.act(timeout=self.max_eval_time, blocking=True)
            if not self.check_exceptions(act):
                self.bad_rounds[aid] = f'{act}'

            # Engagingness
            # for idx, agent in enumerate(self.agents):
            control_msg['text'] = ENGAGINGNESS_MSG
            control_msg['engagingness'] = True
            agent.observe(validate(control_msg))
            act = agent.act(timeout=self.max_eval_time, blocking=True)
            if not self.check_exceptions(act):
                self.engagingness[aid] = f'{act}'

            # Freeform
            # for idx, agent in enumerate(self.agents):
            control_msg['text'] = FREEFORM_MSG
            control_msg['comment'] = True
            agent.observe(validate(control_msg))
            act = agent.act(timeout=self.max_eval_time, blocking=True)
            while act['text'] == '':
                control_msg['text'] = 'Please try again.'
                agent.observe(validate(control_msg))
                act = agent.act(timeout=self.max_eval_time, blocking=True)
            if not self.check_exceptions(act):
                self.free_comment[aid] = act['text']

            logging.info(f'Agent {aid} exiting eval')

            agent.observe(validate({
                'text': CHAT_ENDED_MSG,
                'id': 'SYSTEM',
                'episode_done': True
            }))

            logging.info(f'Agent {aid} shutdown')
            agent.shutdown()

        return Parallel(n_jobs=2, backend='threading')(
            delayed(get_eval)(agent, aid)
            for aid, agent in enumerate(self.agents)
        )

    def get_instruction(self, agent_id=None, tag='first'):
        if tag == 'start':
            return START_MSG.format(self.n_turn)

        if tag == 'chat_not_done':
            return CHAT_NOT_DONE_MSG.format(self.n_turn + 1 - self.turn_idx)

        if tag == 'timeout':
            return TIMEOUT_MESSAGE

        if tag == 'exceed_min_turns':
            return EXCEED_MIN_TURNS_MSG.format(self.n_turn)

    def save_data(self):
        convo_finished = True
        bad_workers = []
        for ag in self.agents:
            if (ag.hit_is_abandoned or ag.hit_is_returned or
                    ag.disconnected or ag.hit_is_expired):
                bad_workers.append(ag.worker_id)
                convo_finished = False

        if not convo_finished or self.dialog == []:
            convo_finished = False

        data_path = self.opt['data_path']
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        if convo_finished:
            filename = os.path.join(
                data_path, '{}_{}_{}_{}_withreasons.pkl'.format(
                    self.model_name,
                    time.strftime("%Y%m%d-%H%M%S"),
                    np.random.randint(0, 1000),
                    self.task_type
                )
            )
        else:
            filename = os.path.join(
                data_path,
                '{}_{}_{}_{}_incomplete_withreasons.pkl'.format(
                    self.model_name,
                    time.strftime("%Y%m%d-%H%M%S"),
                    np.random.randint(0, 1000),
                    self.task_type
                )
            )
        logging.info(
            f'{self.world_tag}: Data successfully saved at\n\t{filename}')

        pickle.dump({
            'opt': self.opt,
            'topics': self.topics,
            'dialog': self.dialog,
            'workers': [ag.worker_id for ag in self.agents],
            'bad_workers': bad_workers,
            'n_turn': self.n_turn,
            'general_mark': self.general_mark,
            'bad_rounds': self.bad_rounds,
            'engagingness': self.engagingness,
            'free_comment': self.free_comment},
            open(filename, 'wb'))

    def is_msg_tooshortlong(self, act, ag, th_min=3, th_max=20):
        if act['episode_done']:
            return False

        control_msg = {'episode_done': False}
        control_msg['id'] = 'SYSTEM'

        msg_len = len(act['text'].split(' '))
        if msg_len < th_min:
            control_msg['text'] = TOO_SHORT_MSG.format(th_min)
            ag.observe(validate(control_msg))
            return True
        if msg_len > th_max:
            control_msg['text'] = TOO_LONG_MSG.format(th_max)
            ag.observe(validate(control_msg))
            return True
        return False

    def reset_random(self):
        self.n_turn = np.random.randint(
            self.range_turn[0],
            self.range_turn[1]
        ) + 1

    def check_timeout(self, act):
        if act['text'] == '[TIMEOUT]' and act['episode_done']:
            control_msg = {'episode_done': True}
            control_msg['id'] = 'SYSTEM'
            control_msg['text'] = self.get_instruction(
                agent_id=act['id'],
                tag='timeout'
            )
            for ag in self.agents:
                if ag.id != act['id']:
                    ag.observe(validate(control_msg))
            self.chat_done = True
            return True
        else:
            return False

    def check_exceptions(self, act):
        exceptions = ['[TIMEOUT]', '[DISCONNECT]', '[RETURNED]']
        if act['text'] in exceptions:

            if act['text'] == '[TIMEOUT]':
                text = self.get_instruction(agent_id=act['id'], tag='timeout')
            else:
                text = 'Received a Disconnect or a Returned message'

            for agent in [a for a in self.agents if a.id != act['id']]:
                agent.observe(validate({
                    'episode_done': True,
                    'id': 'SYSTEM',
                    'text': text
                }))
            self.chat_done = True
            return True
        else:
            return False

    def shutdown(self):
        global shutdown_agent

        def shutdown_agent(mturk_agent):
            mturk_agent.shutdown()

        Parallel(
            n_jobs=len(self.agents),
            backend='threading'
        )(delayed(shutdown_agent)(agent) for agent in self.agents)

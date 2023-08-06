#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from parlai.mturk.core.worlds import MTurkOnboardWorld
from parlai.mturk.core.agents import TIMEOUT_MESSAGE
from parlai.core.worlds import validate, MultiAgentDialogWorld
from joblib import Parallel, delayed
import numpy as np
import time
import os
import json
import random

ONBOARD_MSG = '\nWelcome! Below is your persona \
        (you can find it on the left side of the chat)\n \
        When you are ready to start your conversation, \
        click the "I am ready, continue" button below\n'
TIMEOUT_MSG = '<b> The other person has timed out. \
        Please click the "Done with this HIT" button below to finish this HIT.\
        </b>'
WAITING_MSG = 'Please wait while we match you with another worker...'

GENDER_OPTS = {
    'male': 'Male',
    'female': 'Female',
    'non-binary': 'Non-binary',
    'multi': 'Multiple',
    'none': 'N/A',
}

class WikiGenerator(object):
    def __init__(self):
        self.wiki_path = (
            "/private/home/ledell/ParlAI/data/wikipedia/full/wiki_full_extracted/wiki_20K_MF.jsonl"
        )
        self.wiki_pages_list = []
        f_name = self.wiki_path
        with open(f_name, 'rt') as f:
            for line in f:
                self.wiki_pages_list.append(json.loads(line.strip()))

        self.idx_stack = []

    def add_idx_stack(self):
        stack = [i for i in range(len(self.wiki_pages_list))]
        random.seed()
        random.shuffle(stack)
        self.idx_stack = stack + self.idx_stack

    def pop_wikipage(self):
        if len(self.idx_stack) == 0:
            self.add_idx_stack()
        idx = self.idx_stack.pop()
        data = self.wiki_pages_list[int(idx)]
        return (idx, data)

    def push_wikipage(self, idx):
        self.idx_stack.append(idx)


class PersonasGenerator(object):
    def __init__(self, opt):
        self.personas_path = \
            "/checkpoint/parlai/tasks/gender_multiclass/personachat/personas_names"

        if not os.path.exists(self.personas_path):
            opt['personas_path'] = self.personas_path

        self.gender_list = ['male', 'female', 'neutral']
        self.personas_name_list = {
            'male': [],
            'female': [],
            'neutral': [],
        }

        for k, _ in self.personas_name_list.items():
            f_name = os.path.join(self.personas_path, "%s_pers_with_name.json" % k)
            try:
                with open(f_name, 'rt') as f:
                    self.personas_name_list[k] = json.loads(f.read())
            except:
                print("Error loading names from path: " + f_name)

        self.idx_stack = {
            'male': [],
            'female': [],
            'neutral': [],
        }
        for k, _ in self.idx_stack.items():
            self.add_idx_stack(k)

    def add_idx_stack(self, gender):
        stack = [i for i in range(len(self.personas_name_list[gender]))]
        random.seed()
        random.shuffle(stack)
        self.idx_stack[gender] = stack + self.idx_stack[gender]

    def generate_random_gender(self):
        r = random.randint(0, 2)
        return self.gender_list[r]

    def pop_persona(self):
        gender = self.generate_random_gender()
        if len(self.idx_stack[gender]) == 0:
            self.add_idx_stack(gender)
        idx = self.idx_stack[gender].pop()
        data = self.personas_name_list[gender][int(idx)].split('\n')
        return (gender, idx, data)

    def push_persona(self, gender, idx):
        self.idx_stack[gender].append(idx)


class PersonaProfileWorld(MTurkOnboardWorld):
    """
    A world that provides a persona to the MTurkAgent.
    """

    def __init__(self, opt, mturk_agent):
        self.task_type = 'sandbox' if opt['is_sandbox'] else 'live'
        self.max_persona_time = opt['max_persona_time']
        super().__init__(opt, mturk_agent)

    def parley(self):
        persona_gender, persona_idx, data = \
            self.mturk_agent.persona_generator.pop_persona()
        self.mturk_agent.persona_gender = persona_gender
        self.mturk_agent.persona_idx = persona_idx
        self.mturk_agent.persona_data = data
        persona_text = ''

        for s in data:
            persona_text += '<b><span style="color:blue">' '{}\n</span></b>'.format(
                s.strip()
            )

        #wiki_text = '<b><span style="color:blue">' '{}\n</span></b>'.format(
        #    wiki_data.strip()
        #)

        self.mturk_agent.observe(
            {
                'id': 'SYSTEM',
                'show_persona': True,
                'text': ONBOARD_MSG + '<br>' + persona_text + '<br>',
                #'show_wiki': True,
                #'text': ONBOARD_MSG + '<br>' + persona_text + '<br>' + wiki_text + '<br>',
            }
        )

        act = self.mturk_agent.act(timeout=self.max_persona_time)
        print(act)

        # timeout
        if act['episode_done'] or (('text' in act and act['text'] == TIMEOUT_MESSAGE)):
            self.mturk_agent.persona_generator.push_persona(
                self.mturk_agent.persona_gender,
                self.mturk_agent.persona_idx
            )
            self.episodeDone = True
            return

        if 'text' not in act:
            control_msg = {'id': 'SYSTEM', 'text': WAITING_MSG}
            self.mturk_agent.observe(validate(control_msg))
            self.episodeDone = True


class PersonaChatWorld(MultiAgentDialogWorld):
    def __init__(
        self,
        opt,
        agents=None,
        shared=None,
        range_turn=(4, 7),
        max_turn=10,
        max_resp_time=120,
        world_tag='NONE',
        agent_timeout_shutdown=120,
    ):
        self.agents = agents
        self.turn_idx = 0
        self.range_turn = range_turn
        self.max_turn = max_turn
        self.n_turn = np.random.randint(self.range_turn[0], self.range_turn[1]) + 1
        self.dialog = []
        self.annotation = []
        self.task_type = 'sandbox' if opt['is_sandbox'] else 'live'
        self.chat_done = False
        self.world_tag = world_tag

        # below are timeout protocols
        self.max_resp_time = max_resp_time  # in secs
        self.agent_timeout_shutdown = agent_timeout_shutdown
        super().__init__(opt, agents, shared)

        # get personas
        self.personas = [
            (ag.persona_data if hasattr(ag, 'persona_data') else None)
            for ag in self.agents
        ]

        # get wikipedia article
        self.wiki_generator = WikiGenerator()
        wiki_idx, wiki_data = self.wiki_generator.pop_wikipage()
        self.wiki_idx = wiki_idx
        # get different text displayed for each person
        self.wiki_text = []
        for idx in range(len(self.agents)):
            self.wiki_text.append(self.generate_text_display(wiki_data))

        print(self.wiki_text[0])
        print(self.wiki_text[1])
        self.wiki_data = wiki_data

    def extract_annotation(self, act):
        data = act.get("tag_for_prior_msg", None)
        if data is None:
            return None, None, None
        turn_idx = data.get("turn_idx", None)
        key = [k for k,v in data.items() if v is True and (k != "about-partner")]
        about_partner = data.get("about-partner", None)
        if len(key) != 1:
            # invalid data
            return None, None, None
        return turn_idx, key[0], about_partner 

    def generate_text_display(self, data):
        title = data['title']
        sentences = data['text'].split('. ')
        start_idx = random.randint(0, max(len(sentences) - 3, 0))
        end_idx = start_idx + 3
        display_text = '. '.join(sentences[start_idx:end_idx])
        display_text = display_text.replace('\n', ' ')
        if not display_text.endswith('.'):
            display_text = display_text + '.'
        return "%s\n%s.." % (title, display_text)

    def parley(self):
        self.turn_idx += 1

        control_msg = {'episode_done': False}
        control_msg['id'] = 'SYSTEM'

        print(self.world_tag + ' is at turn {}...'.format(self.turn_idx))

        """If at first turn, we need to give each agent their persona"""
        if self.turn_idx == 1:
            for idx, agent in enumerate(self.agents):
                persona_text = ''
                for s in self.personas[idx]:
                    persona_text += (
                        '<b><span style="color:blue">'
                        '{}\n</span></b>'.format(s.strip())
                    )
                wiki_text = (
                    '<b><span style="color:blue">'
                    '{}\n</span></b>'.format(self.wiki_text[idx])
                )
                control_msg['persona_text'] = persona_text
                control_msg['wiki_text'] = wiki_text
                control_msg['text'] = self.get_instruction(
                    tag='start', agent_id=idx,
                )
                agent.observe(validate(control_msg))
                if idx == 0:
                    time.sleep(3)

        """If we get to the min turns, inform turker that they can end if they
           want
        """
        if self.turn_idx == self.n_turn + 1:
            for idx, agent in enumerate(self.agents):
                control_msg['text'] = self.get_instruction(idx, tag='exceed_min_turns')
                control_msg['exceed_min_turns'] = True
                agent.observe(validate(control_msg))

        """Otherwise, we proceed accordingly"""
        acts = [None, None]
        for idx, agent in enumerate(self.agents):
            if not self.chat_done:
                acts[idx] = agent.act(timeout=self.max_resp_time)
            if self.check_timeout(acts[idx]):
                return

            if self.turn_idx > 1:
                # only check if message is too short on first message
                while self.is_msg_tooshortlong(acts[idx], agent) or self.is_exact_match(
                    acts[idx], agent
                ):
                    acts[idx] = agent.act()
            else:
                while self.is_exact_match(acts[idx], agent):
                    acts[idx] = agent.act()

            self.collect_gender_annotation(acts[idx], agent)

            if acts[idx]['episode_done']:
                # collect last annotation
                turn_idx, gender_tag, about_partner = self.extract_annotation(acts[idx])
                if turn_idx is not None and gender_tag is not None:
                    self.annotation.append({
                        "idx": idx,
                        "turn_idx": turn_idx,
                        "gender": gender_tag,
                        "about_partner": about_partner,
                    })

                self.chat_done = True
                for ag in self.agents:
                    # if agent disconnected
                    if ag != agent and ag.some_agent_disconnected:
                        control_msg['text'] = (
                            'The other worker unexpectedly diconnected. '
                            'Please click "Done with this HIT" button below to '
                            'finish this HIT.'
                        )
                        control_msg['episode_done'] = True
                        ag.observe(validate(control_msg))
                        return
                # agent ends chat after exceeding minimum number of turns
                if self.turn_idx > self.n_turn:
                    for ag in self.agents:
                        ag.observe(validate(acts[idx]))
                        control_msg['text'] = (
                            'One of you ended the chat. Thanks for your time! '
                            'Please click "Done with this HIT" button below '
                            'to finish this HIT.'
                        )
                        control_msg['episode_done'] = True
                        ag.observe(validate(control_msg))
                return

            else:
                #self.dialog.append((idx, self.turn_idx, acts[idx]['text']))
                self.dialog.append({
                    "agent": idx,
                    "turn_idx": self.turn_idx,
                    "text": acts[idx]['text'],
                })
                turn_idx, gender_tag, about_partner = self.extract_annotation(acts[idx])
                if turn_idx is not None and gender_tag is not None:
                    self.annotation.append({
                        "agent": idx,
                        "turn_idx": turn_idx,
                        "gender": gender_tag,
                        "about_partner": about_partner,
                    })
                for other_agent in self.agents:
                    if other_agent != agent:
                        other_agent.observe(validate(acts[idx]))

    def shutdown(self):
        global shutdown_agent

        def shutdown_agent(mturk_agent):
            mturk_agent.shutdown()

        Parallel(n_jobs=len(self.agents), backend='threading')(
            delayed(shutdown_agent)(agent) for agent in self.agents
        )

    def episode_done(self):
        return self.chat_done

    def get_instruction(self, agent_id=None, tag='first'):
        if tag == 'start':
            assert agent_id is not None
            partner_ag_id = 1 - agent_id
            partner_persona = self.personas[partner_ag_id]
            # persona always starts with 'my name is '
            partner_name = partner_persona[0][len('my name is '):-1]
            partner_info = partner_name
            partner_gender = self.agents[partner_ag_id].persona_gender
            if partner_gender == "female":
                partner_info += ", who is a woman"
            elif partner_gender == "male":
                partner_info += ', who is a man'

            return (
                '\nSuccessfully matched with character ' 
                + partner_info + '. Now let\'s get to know each other '
                'through the chat! \nYou need to finish at least <b>'
                + str(self.n_turn)
                + ' chat turns</b>, after that you can click the "Done" button '
                'to end the chat. \n'
                '<b>You can track your character description on the left.</b> '
                '\n <span style="color:blue"><b>Please try to speak to the '
                'other person as if you are the character assigned.</b></span>'
                '\n <span style="color:blue"><b>Do not trivially copy the '
                'character descriptions into the message.</b></span>'
            )

        if tag == 'chat_not_done':
            return (
                'Sorry, we need at least <b>'
                + str(self.n_turn + 1 - self.turn_idx)
                + ' more turn(s)</b> to finish. '
                'Please send a new message:'
            )

        if tag == 'timeout':
            return (
                '<b>{}</b> is timeout. Please click the "Done with this HIT" '
                'button below to exit this HIT. No rejections.'.format(agent_id)
            )

        if tag == 'exceed_min_turns':
            return (
                '\n {} chat turns finished! \n Keep chatting or you can click '
                'the "Done" button to end the chat if it\'s your turn.'.format(
                    self.n_turn
                )
            )

    def save_data(self):
        convo_finished = True
        bad_workers = []
        for ag in self.agents:
            if (
                ag.hit_is_abandoned
                or ag.hit_is_returned
                or ag.disconnected
                or ag.hit_is_expired
            ):
                bad_workers.append(ag.worker_id)
                convo_finished = False
        if not convo_finished or self.dialog == []:
            for ag in self.agents:
                ag.not_approve = True
                ag.persona_generator.push_persona(ag.persona_gender, ag.persona_idx)
                print(
                    "\n******* Push persona gender {}-{} back to stack. *******\n".format(
                        ag.persona_gender,
                        ag.persona_idx
                    )
                )

        data_path = self.opt['extract_personas_path']
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        if convo_finished:
            filename = os.path.join(
                data_path,
                '{}_{}_{}.json'.format(
                    time.strftime("%Y%m%d-%H%M%S"),
                    np.random.randint(0, 1000),
                    self.task_type,
                ),
            )
        else:
            filename = os.path.join(
                data_path,
                '{}_{}_{}_incomplete.json'.format(
                    time.strftime("%Y%m%d-%H%M%S"),
                    np.random.randint(0, 1000),
                    self.task_type,
                ),
            )
        print(self.world_tag + ': Data successfully saved at {}.'.format(filename))
        json.dump(
            {
                'personas': self.personas,
                'wiki_data': self.wiki_data,
                'wiki_text_display': self.wiki_text,
                'dialog': self.dialog,
                'annotation': self.annotation,
                'workers': [ag.worker_id for ag in self.agents],
                'hit_ids': [ag.hit_id for ag in self.agents],
                'assignment_ids': [ag.assignment_id for ag in self.agents],
                'bad_workers': bad_workers,
                'n_turn': self.n_turn,
            },
            open(filename, 'wt'),
        )

    def is_exact_match(self, act, ag, tolerance=0):
        if act['episode_done']:
            return False

        control_msg = {'episode_done': False}
        control_msg['id'] = 'SYSTEM'

        text = act['text']
        if text not in ['', ' ', '  ', '   ']:
            n_word_match = 0
            for per in ag.persona_data:
                per_parse = per.split(' ')
                regular_words = ['', ' ', 'I', 'I\'m', 'My', 'i']
                for r_w in regular_words:
                    if r_w in per_parse:
                        per_parse.remove(r_w)
                per_subseq = [
                    ' '.join(per_parse[i : i + len(per_parse) - tolerance])
                    for i in range(tolerance + 1)
                ]
                for pp in per_subseq:
                    if pp in ['', ' ', '  ', '   ']:
                        per_subseq.remove(pp)
                n_word_match += sum([(paa in text) for paa in per_subseq])
            if n_word_match > 0:
                control_msg['text'] = (
                    'We found that you <b><span style="color:red">trivially '
                    'copied character descriptions</span></b>. Please '
                    'rephrase your message again.'
                )
                ag.observe(validate(control_msg))
                return True
            else:
                return False

    def is_msg_tooshortlong(self, act, ag, th_min=5, th_max=17):
        if act['episode_done']:
            return False

        control_msg = {'episode_done': False}
        control_msg['id'] = 'SYSTEM'

        msg_len = len(act['text'].split(' '))
        if msg_len < th_min:
            control_msg['text'] = (
                'Your message is too short, please make it more than '
                '<b><span style="color:red">5 words</span></b>.'
            )
            ag.observe(validate(control_msg))
            return True
        if msg_len > th_max:
            control_msg['text'] = (
                'Your message is too long, please make it less than '
                '<b><span style="color:red">15 words</span></b>.'
            )
            ag.observe(validate(control_msg))
            return True
        return False

    def collect_gender_annotation(self, act, ag):
        if act['episode_done']:
            return

        control_msg = {'episode_done': False}
        control_msg['id'] = 'Annotation'
        control_msg['text'] = (
            'If your message was about a person or people, please select their gender. Otherwise, select N/A:<br>'
        )
        for key, name in GENDER_OPTS.items():
            control_msg['text'] +=  f"""<input type="checkbox" id="checkbox_group_{self.turn_idx}_{key}" name="checkbox_group_{self.turn_idx}" /><span style="margin-right:15px;">{name}</span>"""
        # additional information to collect
        control_msg['text'] += "<br>Select whether your message is ABOUT your conversation partner:"
        control_msg['text'] +=  f"""<input type="checkbox" id="checkbox_about_{self.turn_idx}_yes" name="checkbox_about_{self.turn_idx}" /><span style="margin-right:15px;">Yes</span>"""
        control_msg['text'] +=  f"""<input type="checkbox" id="checkbox_about_{self.turn_idx}_no" name="checkbox_about_{self.turn_idx}" /><span style="margin-right:15px;">No</span>"""
        ag.observe(validate(control_msg))
        return

    def reset_random(self):
        self.n_turn = np.random.randint(self.range_turn[0], self.range_turn[1]) + 1

    def check_timeout(self, act):
        if act['text'] == '[TIMEOUT]' and act['episode_done']:
            control_msg = {'episode_done': True}
            control_msg['id'] = 'SYSTEM'
            control_msg['text'] = self.get_instruction(
                agent_id=act['id'], tag='timeout'
            )
            for ag in self.agents:
                if ag.id != act['id']:
                    ag.observe(validate(control_msg))
            self.chat_done = True
            return True
        else:
            return False

    def review_work(self):
        global review_agent

        def review_agent(ag):
            if hasattr(ag, 'not_approve'):
                pass
            else:
                ag.approve_work()

        Parallel(n_jobs=len(self.agents), backend='threading')(
            delayed(review_agent)(agent) for agent in self.agents
        )

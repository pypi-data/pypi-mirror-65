#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from parlai.mturk.core.worlds import MTurkOnboardWorld
from parlai.mturk.core.agents import TIMEOUT_MESSAGE
from parlai.core.worlds import validate, MultiAgentDialogWorld
from parlai.utils.safety import OffensiveLanguageDetector
from joblib import Parallel, delayed
from task_config import task_config as config
import base64
from collections import Counter
from copy import copy
import datetime
from game_configs.default import DefaultGameConfig
from io import BytesIO
import numpy as np
import os
import pickle
import random
import time
import parlai.mturk.core.mturk_utils as mutils

RESPONSE_ONLY = 'response_only'
VOTE_ONLY = 'vote_only'
FULL_GAME = 'full_game'

# Qual names are complete_solo_vb_task and complete_multi_vb_task
SOLO_QUAL = '3R5PEB0CKOGMUMM94KUPMQ3H365O93'
MULTI_QUAL = '3Y5W3WI83SG0Z5WEWQ8PILE19ONOAI'
MASTER_LIVE_QUAL = '2F1QJWKUDD8XADTFD2Q0G6UTO95ALH'
MASTER_SANDBOX_QUAL = '2ARFPLSP75KLA8M8DH1HTEQVJT3SY6'


class RoleOnboardWorld(MTurkOnboardWorld):
    """
    A world that provides the appropriate instructions during onboarding.
    """
    def __init__(self, opt, mturk_agent):
        self.task_type = 'sandbox' if opt['is_sandbox'] else 'live'
        self.max_onboard_time = opt['max_onboard_time']
        super().__init__(opt, mturk_agent)

    def parley(self):
        onboard_msg = {'id': 'SYSTEM'}
        onboard_msg['waiting_text'] = DefaultGameConfig.WAITING_MSG
        onboard_msg['role_task_description'] = config['onboarding']

        self.mturk_agent.observe(onboard_msg)

        act = self.mturk_agent.act(timeout=self.max_onboard_time)

        # why does it need episode done?
        if act['episode_done'] or (('text' in act and
                                    act['text'] == TIMEOUT_MESSAGE)):
            self.episodeDone = True
            return

        if 'text' not in act:
            control_msg = {'id': 'SYSTEM',
                           'text': DefaultGameConfig.WAITING_MSG}
            self.mturk_agent.observe(validate(control_msg))
            self.episodeDone = True

class MTurkVotingBattleWorld(MultiAgentDialogWorld):
    def __init__(self, opt, example_generator, agents=None, world_tag='NONE', shared=None, offset=None):
        self.opt = opt
        self.game_config = DefaultGameConfig()
        self.game_mode = opt['game_mode']
        self.single_player = opt['single_player']
        self.has_ground_truth = opt['has_ground_truth']
        self.round_idx = 0
        self.unanimous_wins = 0
        self.num_rounds = opt['num_rounds']
        self.ex_mode = self.game_config.EXAMPLE_MODE
        self.candidate_labels = []
        self.task_type = 'sandbox' if opt['is_sandbox'] else 'live'
        self.max_label_time = opt['max_label_time']
        self.max_vote_time = opt['max_vote_time']
        self.warning_time = opt['warning_time']
        self.world_tag = world_tag
        self.show_truth_label = opt['show_truth_label']
        super().__init__(opt, agents, shared)
        self.original_agents = copy(agents)
        self.agents = copy(agents)
        self.eligible = {}
        for ag in agents:
            self.eligible[ag.worker_id] = True
        self.acts = [None]*len(self.agents)
        self.vote_bonuses = {}
        self.write_bonuses = {}
        self.timeouts = {}
        for ag in agents:
            self.vote_bonuses[ag.worker_id] = 0
            self.write_bonuses[ag.worker_id] = 0
            self.timeouts[ag.worker_id] = opt['allowed_timeouts']
        self.example_generator = example_generator
        self.gen_offset = offset
        self.offensive_lang_detector = OffensiveLanguageDetector()
        self.data = []

    def reset(self):
        self.acts = [None]*len(self.agents)

    def create_agent_message(self, text, id='SYSTEM', ep_done=False, toggle=False):
        msg = {'episode_done': False}
        msg['id'] = 'SYSTEM'
        msg['text'] = text
        if toggle:
            msg['force_toggle'] = True
        return msg

    def send_round_start_message(self, prev_winning_comment):
        # Initial Message Value
        ex = self.game_config.next_example(self.example_generator, self.num_rounds, self.gen_offset)
        toggle = False
        if self.game_mode != FULL_GAME:
            if self.round_idx == 1:
                if self.game_mode == VOTE_ONLY:
                    toggle = True
            else:
                toggle = True
        control_msg = self.create_agent_message(self.game_config.create_start_message(self.round_idx, ex), toggle=toggle)
        ex_label = None
        if self.ex_mode.startswith('image'):
            img = ex.pop(self.game_config.IMAGE_FIELD_NAME)
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            encoded = str(base64.b64encode(buffered.getvalue()).decode('ascii'))
            control_msg['ex_image'] = encoded
        if self.ex_mode.endswith('dialog'):
            # Will use the dialog to set the innerHTML of a div, so convert
            # this to a HTML format.
            if self.game_config.CONTINUE_CONVERSATION:
                control_msg['ex_dialog'] = self.game_config.process_dialog(ex, prev_winning_comment)
            else:
                control_msg['ex_dialog'] = self.game_config.process_dialog(ex)
        if self.show_truth_label:
            ex_label = self.game_config.retrieve_truth_label(ex)

        if self.single_player:
            control_msg['wait_text'] = self.game_config.WAITING_ORIGINAL
        else:
            control_msg['wait_text'] = self.game_config.WAITING_LABELS
        control_msg['display_waiting_symbol'] = False
        # have the labelers observe
        self.send_agents_message(control_msg)
        return ex, ex_label

    def agents_response_act(self):
        # Collate the labels
        counter = [0]*len(self.agents)
        # List to hold agents that have either been too offensive or
        # disconnected, and so are completely finished with the HIT
        finished = []
        max_time = self.max_label_time + 1
        start = time.time()
        elapsed = 0
        sent_warning = [False]*len(self.agents)
        while None in self.acts and elapsed <= max_time:
            for idx, agent in enumerate(self.agents):
                # if idx not in finished:
                acts = self.acts
                # Collect comment from turker
                if counter[idx] < 3 and acts[idx] is None:
                    acts[idx] = agent.act(blocking=False)
                    if acts[idx] is not None:
                        response = acts[idx]['text']
                        if response == '[DISCONNECT]':
                            finished.append(idx)
                            print(self.world_tag + ' added {} to the disconnected list'.format(self.agents[idx].worker_id))
                            continue
                        offensive = self.offensive_lang_detector.contains_offensive_language(response)
                        if offensive:
                            # Tell Turker to not be offensive!
                            counter[idx] += 1
                            acts[idx] = None
                            if counter[idx] == 3:
                                self.eligible[agent.worker_id] = False
                                acts[idx] = '[OFFENSIVE]'
                                finished.append(idx)
                                print(self.world_tag + ' saw {} was too offensive!'.format(self.agents[idx].worker_id))
                                remove_msg = {'episode_done': True}
                                remove_msg['id'] = 'SYSTEM'
                                remove_msg['text'] = 'You have used \
                                  offensive language too many times \
                                  and can no longer work on this HIT.'
                                agent.observe(validate(remove_msg))
                                continue
                            offensive_msg = {
                                'id': 'SYSTEM',
                                'text': self.game_config.OFFENSIVE_MSG,
                                'force_toggle': True,
                            }
                            agent.observe(validate(offensive_msg))
                    elif (max_time - elapsed) <= self.warning_time and not sent_warning[idx]:
                        sent_warning[idx] = True
                        msg = self.create_agent_message(
                            self.game_config.WARNING_MSG.format(round(max_time - elapsed), "respond"))
                        msg['display_waiting_symbol'] = False
                        agent.observe(validate(msg))

            elapsed = time.time() - start
            time.sleep(0.1)
        return finished

    def prepare_cands(self, ex_label):
        cands = {}
        count = 0
        submissions = 0
        collusion = False

        for idx, label in enumerate(self.acts):
            if label is not None:
                submissions += 1
                worker_id = self.agents[idx].worker_id
                text = label['text'].strip().lower() if self.has_ground_truth else label['text'].strip()
                if text not in cands:
                    cands[text] = (count, [worker_id])
                    count += 1
                else:
                    cands[text][1].append(worker_id)

        # Before possibly adding the truth label, we need to see if the Turkers
        # are trying to collude. If they all submit the same answer, then we
        # should end the game early.
        cands_list = []
        for key, val in cands.items():
            cands_list.append((val[0], key, val[1]))

        if len(cands_list) == 1 and submissions > 1 and not self.has_ground_truth:
            collusion = True


        if self.show_truth_label:
            label = ex_label.lower() if self.has_ground_truth else ex_label
            if label not in cands:
                cands[label] = (count, self.game_config.TRUTH_ID)

        cands_list = []
        for key, val in cands.items():
            cands_list.append((val[0], key, val[1]))

        return cands_list, collusion

    def agents_vote_act(self, cands, old_acts):
        agent_ordering = []
        if self.game_mode == VOTE_ONLY:
            label_msg = self.create_agent_message("")
            if self.single_player:
                label_msg['wait_text'] = self.game_config.WAITING_ORIGINAL
            else:
                label_msg['wait_text'] = self.game_config.WAITING_VOTES
        else:
            label_msg = self.create_agent_message(
                self.game_config.START_VOTE_MSG)
            label_msg['wait_text'] = self.game_config.WAITING_VOTES
        # have the voters observe the responses and then collate their responses
        for idx, agent in enumerate(self.agents):
            agent_submission = old_acts[idx]['text'].strip() if old_acts[idx] is not None else None
            agent_cands = cands.copy() if self.has_ground_truth else [c for c in cands if c[1] != agent_submission]
            random.shuffle(agent_cands)
            label_msg['label_candidates'] = [c[1] for c in agent_cands]
            agent_ordering.append([c[0] for c in agent_cands])
            agent.observe(validate(label_msg))

        time.sleep(1)
        votes = [-1]*len(self.agents)
        finished = []
        max_time = self.max_vote_time + 1
        start = time.time()
        elapsed = 0
        sent_warning = [False]*len(self.agents)
        while None in self.acts and elapsed <= max_time:
            for idx, agent in enumerate(self.agents):
                acts = self.acts
                if acts[idx] is None:
                    acts[idx] = agent.act(blocking=False)
                    if acts[idx] is not None:
                        if acts[idx]['text'] == '[DISCONNECT]':
                            finished.append(idx)
                            continue
                        try:
                            votes[idx] = agent_ordering[idx][int(acts[idx]['text']) - 1]
                        except ValueError:
                            print("For a voting phase, was given {} instead of an integer index".format(acts[idx]))
                            acts[idx] = None
                        except IndexError:
                            print("For a voting phase, tried to access index {} but it didn't work".format(idx))
                    elif (max_time - elapsed) <= self.warning_time and not sent_warning[idx]:
                        sent_warning[idx] = True
                        msg = self.create_agent_message(
                            self.game_config.WARNING_MSG.format(round(max_time - elapsed), "respond"))
                        msg['display_waiting_symbol'] = False
                        agent.observe(validate(msg))

            elapsed = time.time() - start
            time.sleep(0.1)
        return votes

    def process_votes(self, cands, votes):
        filt_votes = list(filter(lambda x: x != -1, votes))
        vote_counts = Counter(filt_votes)

        vote_save = {}
        for item, cnt in vote_counts.most_common():
            vote_save[item] = cnt
        top_two = vote_counts.most_common(2)

        is_unanimous = False
        if len(top_two) == 0: # everyone timed out
            choice, prev_winning_comment = -1, ""
        # Check for tie
        elif len(top_two) == 2 and top_two[0][1] == top_two[1][1]:
            # there is a tie!!!!
            choice = -1
            tie_msg = {'episode_done': False}
            tie_msg['id'] = 'SYSTEM'
            tie_msg['text'] = 'LOSE_LOSE_MSG'
            tie_msg['round'] = str(self.round_idx)
            tie_msg['bonus_text'] = 'Uh-oh! Everyone couldn\'t agree on a winner, so nobody earned a bonus!'
            self.send_agents_message(tie_msg)
            _, prev_winning_comment, _ = [c for c in cands if c[0] == top_two[0][0]][0]
        else:
            choice = top_two[0][0]
            relative_idx, chosen_label, chosen_ids = [c for c in cands if c[0] == choice][0]
            prev_winning_comment = chosen_label
            if not self.single_player:
                # Determine winning labeler and send message
                for chosen_id in chosen_ids:
                    if chosen_id != self.game_config.TRUTH_ID:
                        self.write_bonuses[chosen_id] += 1
                msg = {'episode_done': False}
                msg['id'] = 'SYSTEM'
                msg['round'] = str(self.round_idx)
                # Determine which voters chose winning label
                voters = np.where(np.asarray(votes) == choice)[0]
                for idx, agent in enumerate(self.agents):
                    votes_earned = vote_counts[idx]
                    diff = top_two[0][1] - votes_earned
                    if votes_earned == 0:
                        to_add = self.game_config.LOSE_NONE
                    elif 1 <= diff <= 2:
                        vote_string = "vote" if diff == 1 else "votes"
                        to_add = self.game_config.LOSE_CLOSE.format(diff, vote_string)
                    else:
                        vote_string = "vote" if votes_earned == 1 else "votes"
                        to_add = self.game_config.LOSE_FAR.format(votes_earned, vote_string)

                    if idx in voters:
                        # this voter was correct
                        if agent.worker_id not in chosen_ids:
                            self.vote_bonuses[agent.worker_id] += 1
                            msg['text'] = 'LOSE_WIN_MSG'
                            if self.game_mode == FULL_GAME:
                                msg['bonus_text'] = self.game_config.LOSE_WIN_MSG.format(to_add)
                            else:
                                msg['bonus_text'] = self.game_config.LOSE_WIN_NO_RESPONSE_MSG
                        else:
                            msg['text'] = 'WIN_WIN_MSG'
                            msg['bonus_text'] = self.game_config.WIN_WIN_MSG
                        agent.observe(validate(msg))
                    else:
                        if agent.worker_id in chosen_ids:
                            msg['text'] = 'WIN_LOSE_MSG'
                            msg['bonus_text'] = self.game_config.WIN_LOSE_MSG
                        else:
                            msg['text'] = 'LOSE_LOSE_MSG'
                            if self.game_mode == FULL_GAME:
                                msg['bonus_text'] = self.game_config.LOSE_LOSE_MSG.format(to_add)
                            else:
                                msg['bonus_text'] = self.game_config.LOSE_LOSE_NO_RESPONSE_MSG
                        agent.observe(validate(msg))
            if len(vote_counts) == 1 and not self.single_player:
                is_unanimous = True
                self.unanimous_wins += 1
                self.send_agents_message(self.create_agent_message(self.game_config.UNANIMOUS_MSG))
            if not self.single_player:
                self.send_agents_message(self.create_agent_message(self.game_config.WIN_LABEL_MSG.format(chosen_label)))
        return choice, vote_save, is_unanimous, prev_winning_comment

    def parley(self):
        """
        The LABELERS act and provide labels and then the VOTERS are given the
        labels to choose their favorite.
        """
        # Message to set up the game, including setting up the scoreboard and
        # the example panel
        msg = {'episode_done': False}
        msg['id'] = 'SYSTEM'
        msg['draw_rounds'] = self.num_rounds
        msg['ex_type'] = self.ex_mode
        if self.game_mode == VOTE_ONLY:
            msg['vote_only'] = True
        self.send_agents_message(msg)
        prev_winning_comment = None
        self.round_idx += 1
        vote_save = None
        votes = None
        is_unanimous = None
        while self.round_idx <= self.num_rounds:
            self.reset()
            print(self.world_tag + ' is at turn {}...'.format(self.round_idx))
            ex, ex_label = self.send_round_start_message(prev_winning_comment)
            if self.single_player:
                hide_scoreboard_msg = {
                    'episode_done': False,
                    'id': 'SYSTEM',
                    'hide_scoreboard': True,
                }
                self.send_agents_message(hide_scoreboard_msg)
            time.sleep(1)
            if self.game_mode in [RESPONSE_ONLY, FULL_GAME]:
                finished = self.agents_response_act()
                if self.handle_timeout(finished):
                    return
                if self.game_mode == RESPONSE_ONLY:
                    choice = self.acts[0]['text']
                    cands = [choice]

            if self.game_mode in [VOTE_ONLY, FULL_GAME]:
                if self.game_mode == FULL_GAME:
                    cands, collusion = self.prepare_cands(ex_label)
                    if collusion:
                        self.send_agents_message(
                            self.create_agent_message(
                                self.game_config.COLLUSION_MSG))
                        return
                else:
                    cands = self.game_config.load_cands(ex)
                old_acts = self.acts.copy()
                self.reset()
                if self.game_mode == FULL_GAME:
                    # all labels sent message
                    submitted_labels_msg = self.create_agent_message('All labels have been submitted!')
                    submitted_labels_msg['wait_text'] = "Loading candidate labels..."
                    self.send_agents_message(submitted_labels_msg)
                votes = self.agents_vote_act(cands, old_acts)
                # resort cands since we require them to be in order of agent
                cands.sort(key=lambda x: x[0])
                if self.handle_timeout(finished=[]):
                    return
                # determine which labeler won and which voter voted for them and assign to BONUSES
                choice, vote_save, is_unanimous, prev_winning_comment = self.process_votes(cands, votes)

            self.round_idx += 1
            self.data.append({
                'labels': cands,
                'winner': choice,
                'total_votes': vote_save,
                'votes': votes,
                'ex': ex,
                'unanimous': is_unanimous,
            })

    def handle_timeout(self, finished=[]):
        timed_out = list(np.where(np.asarray(self.acts)==None)[0])
        if len(timed_out + finished) == len(self.agents) and not self.single_player:
            self.send_agents_message(self.create_agent_message("Nobody responded, so the HIT now is ending!"))
            return True
        to_remove = finished
        for idx, act in enumerate(self.acts):
            ag = self.agents[idx]
            if idx in timed_out and self.timeouts[ag.worker_id] == 0:
                to_remove.append(idx)
            elif idx in timed_out and self.timeouts[ag.worker_id] != 0:
                self.timeouts[ag.worker_id] -= 1
                chances = self.timeouts[ag.worker_id]
                if chances == 0:
                    timeout_msg = self.create_agent_message(self.game_config.TIMEOUT_LAST_CHANCE_MSG)
                    ag.observe(validate(timeout_msg))
                elif chances == 1:
                    timeout_msg = self.create_agent_message(
                        self.game_config.TIMEOUT_SECOND_CHANCE_MSG.format(1, 'chance'))
                    ag.observe(validate(timeout_msg))
                else:
                    timeout_msg = self.create_agent_message(
                        self.game_config.TIMEOUT_SECOND_CHANCE_MSG.format(chances, 'chances'))
                    ag.observe(validate(timeout_msg))
                # Need to force the switch of the input field
                force_switch_msg = self.create_agent_message('SWITCH_INPUT_MSG')
                ag.observe(validate(force_switch_msg))

        for idx in sorted(to_remove, reverse=True):
            print(self.world_tag + ' had to kick {}, leaving {} workers left'.format(self.agents[idx].worker_id, len(self.agents) - 1))
            self.agents[idx].prepare_timeout()
            self.agents.pop(idx)
            self.acts.pop(idx)
            if not self.check_continue():
                return True
        return False

    def check_continue(self):
        if len(self.agents) > 2 or (self.single_player and len(self.agents)==1):
            control_msg = {'episode_done': False}
            control_msg['id'] = 'SYSTEM'
            control_msg['text'] = 'Uh-oh! A player has disconnected, but there \
                                are still enough to continue!'
            self.send_agents_message(control_msg)
            return True
        else:
            control_msg = {'episode_done': False}
            control_msg['id'] = 'SYSTEM'
            control_msg['text'] = self.game_config.TIMEOUT_MSG
            self.send_agents_message(control_msg)
            return False

    def send_agents_message(self, msg):
        for agent in self.agents:
            agent.observe(validate(msg))

    def save_bonuses(self):
        filename = 'bonuses_{}{}.txt'.format(datetime.date.today().strftime('%Y%m%d'), '_sandbox' if self.opt['is_sandbox'] else '')
        bonus_directory = os.path.join(self.opt['data_path'], '..', 'bonus')
        if not os.path.isdir(bonus_directory):
            os.makedirs(bonus_directory)
        bonuses = os.path.join(bonus_directory, filename)
        for ag in self.original_agents:
            # Check they didn't use bad lanugage
            if self.eligible[ag.worker_id]:
                bonus = 0.0
                bonus_message = ''
                if self.round_idx < self.num_rounds:
                    bonus_message += "Only {} round(s) out of a possible {} were completed so your pay will be pro-rated.".format(self.round_idx, self.num_rounds)
                # Bonus 1 - Complete all rounds
                if ag in self.agents:
                    bonus += self.opt['base_bonus'] * (self.round_idx / self.num_rounds)
                    bonus_message += 'You completed all seen rounds. '
                else:
                    bonus_message += 'You did not complete all seen rounds so do not qualify for the base bonus. '
                # Bonus 2 - No timeouts
                if self.timeouts[ag.worker_id] == self.opt['allowed_timeouts'] and ag in self.agents:
                    bonus += self.opt['participate_bonus'] * (self.round_idx / self.num_rounds)
                    bonus_message += 'You participated in all seen rounds without timing out once. '
                else:
                    bonus_message += 'You timed out at least once or disconnected so do not qualify for the participation bonus. '
                # Bonus 3 - Wrote winning label
                if self.game_mode == FULL_GAME:
                    bonus += self.write_bonuses[ag.worker_id]*self.opt['response_bonus']
                    bonus_message += 'You wrote the winning label {} time(s). '.format(self.write_bonuses[ag.worker_id])
                # Bonus 4 - Voted for winning label
                if self.game_mode == FULL_GAME or (self.game_mode == VOTE_ONLY and not self.single_player):
                    bonus += self.vote_bonuses[ag.worker_id]*self.opt['vote_bonus']
                    bonus_message += 'You voted for the winning label {} time(s).'.format(self.vote_bonuses[ag.worker_id])

                if bonus > 0:
                    data = [ag.worker_id, ag.assignment_id]
                    data += [str(round(bonus,2)), bonus_message]
                    with open(bonuses, 'a') as f:
                        f.write(','.join(data) + '\n')

    def save_data(self):
        if self.task_type != 'sandbox' and self.opt['use_version_quals']:
            mutils.setup_aws_credentials()
            qual = SOLO_QUAL if self.single_player else MULTI_QUAL
            # Give workers the qualification so they can't do both versions
            for agent in self.agents:
                mutils.give_worker_qualification(agent.worker_id, qual, value=None, is_sandbox=False)
        self.round_idx -= 1
        data_path = self.opt['data_path']
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        filename = os.path.join(
            data_path,
            '{}_{}{}.pkl'.format(
                time.strftime("%Y%m%d-%H%M%S"),
                np.random.randint(0, 1000),
                '_sandbox' if self.opt['is_sandbox'] else ''
            )
        )
        if len(self.data) > 0:
            pickle.dump({'data': self.data,
                         'HIT_mode': self.game_mode,
                         'gen_offset': self.gen_offset,
                         'workers': [ag.worker_id for ag in self.agents],
                         'hit_ids': [ag.hit_id for ag in self.agents],
                         'original_workers': [ag.worker_id for ag in self.original_agents],
                         'assignment_ids': [ag.assignment_id for ag in self.agents],
                         'unanimous_ratio': self.unanimous_wins / self.num_rounds,
                         'rounds_completed': [self.round_idx, self.num_rounds],
                         }, open(filename, 'wb'))
            print('{}: Data successfully saved at {}.'.format(
                self.world_tag,
                filename))

    def review_work(self):
        global review_agent

        def review_agent(ag):
            if not self.eligible.get(ag.worker_id, True):
                ag.reject_work(reason='Your HIT has been rejected because we '
                                      'detected offensive language in your submission.')
        if len(self.agents) > 0:
            Parallel(n_jobs=len(self.agents), backend='threading')(delayed(review_agent)(agent) for agent in self.agents)

    def shutdown(self):
        """Shutdown all mturk agents in parallel, otherwise if one mturk agent
        is disconnected then it could prevent other mturk agents from
        completing.
        """
        global shutdown_agent

        def shutdown_agent(agent):
            # try:
            agent.shutdown()
            # except Exception:
            #     agent.shutdown()  # not MTurkAgent
        if len(self.agents) > 0:
            Parallel(
                n_jobs=len(self.agents),
                backend='threading'
            )(delayed(shutdown_agent)(agent) for agent in self.agents)

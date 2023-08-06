#!/usr/bin/env python3

from parlai.core.worlds import World
from copy import deepcopy
import time
import os
import pickle
import random
from parlai_internal.agents.graph_world2.models import ObjectChecklistModel
from parlai_internal.tasks.graph_world2.graph import construct_graph, Graph
import torch
from torch.autograd import Variable
from collections import defaultdict as dd
from os.path import join
import pickle
from task_config import VERSION_NUM
import traceback

TIMEOUT = 8 * 60 # 8 * 60
MAX_ACTION_LEN = 4

SPECIAL_SET = ['[timeout]', '[expired]', '[returned]', '[disconnect]']

def get_output_dir(opt, round_index):
    output_dir = join(opt['datapath'], 'graph_world2_v{}_r{}'.format(VERSION_NUM, round_index))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

class DataCollectionWorld(World):

    task_coordinator_agent_id = 'Dungeon Master'

    def __init__(self, opt, mturk_agent, data_agent, model_dict, wrong_data, binding, cur_ids, show_times, round_index):
        self.mturk_agent = mturk_agent
        self.data_agent = data_agent
        self.model = model_dict
        self.wrong_data = wrong_data
        self.binding = binding
        self.cur_ids = cur_ids
        self.show_times = show_times
        self.agents = [mturk_agent]
        self.round_index = round_index

        self.opt = deepcopy(opt)
        self.episodeDone = False

        self.disconnect = False

        self.graph = construct_graph(opt)
        self.graph.parse_exec('look')
        self.training_examples = []

        check_mapping = self.data_agent.get_check_mapping()
        self.check_mapping = self._get_variable(check_mapping, True)

        self.mode = 'INIT'
        self.start_time = time.time()
        self.forced_timeout = False

        def get_show_times_score(data):
            correct_action, wrong_action, language_command = tuple(data.split(' ||| '))
            return show_times[(correct_action, language_command)] / opt['num_assignments']

        self.wrong_data_index = 0
        self.wrong_data.sort(key=lambda x: float(len(Graph.parse_static(x.split(' ||| ')[0])[1])) + random.random() * 1.5 + get_show_times_score(x))
        # random.shuffle(self.wrong_data)

    def _get_variable(self, np_a, volatile=False):
        if self.opt['cuda']:
            return Variable(torch.from_numpy(np_a), volatile=volatile).cuda()
        return Variable(torch.from_numpy(np_a), volatile=volatile)

    def _get_wrong_data_text(self):
        s = "The dragon is learning human language, but still does not understand the following orders. (dragon's actions in red).\n\n"

        flag = False
        for i in range(self.opt['error_examples']):
            if self.wrong_data_index + i >= len(self.wrong_data): break
            flag, data = True, self.wrong_data[self.wrong_data_index + i]
            correct_action, wrong_action, language_command = tuple(data.split(' ||| '))

            self.show_times[(correct_action, language_command)] += 1

            s += '"{}" -> <span style="color:blue">{}</span> &nbsp;&nbsp;<b>NOT</b>&nbsp;&nbsp; <span style="color:red">{}</span>\n'.format(language_command, correct_action, wrong_action)
        self.wrong_data_index += self.opt['error_examples']
        if not flag:
            return "No more orders to show!\n"
        s += "\nNow try your best to teach the dragon more human language!\n"
        return s

    def _get_plan(self):
        # response = 'You just executed the following actions:\n\n<span style="color:blue">'
        response = 'Your actions <span style="color:blue">{}</span> resulted in the following changes:\n\n<span style="color:blue">'.format(' '.join(self.actions))
        dragon_id = 'dragon'
        delta_dict = dd(list)
        old_g, g = self.old_graph, self.graph
        for id in old_g.object_ids + old_g.container_ids + old_g.agent_ids:
            desc = old_g.node_to_desc_raw(id)
            if not g.node_exists(id):
                if old_g.node_exists(id):
                    delta_dict['ingest'].append(desc)
                continue
            if g.valid(id, 'wearing'):
                delta_dict['wear'].append(desc)
            elif g.valid(id, 'wielding'):
                delta_dict['wield'].append(desc)
            elif g.node_contained_in(id) != old_g.node_contained_in(id):
                new_container_id = g.node_contained_in(id)
                if new_container_id == dragon_id:
                    delta_dict['carry'].append(desc)
                else:
                    delta_dict[g.node_to_desc_raw(new_container_id)].append(desc)
            if g.valid(id, 'dead'):
                delta_dict['dead'].append(desc)

        for k, v in delta_dict.items():
            if k == 'ingest':
                response += 'Ingest: {}\n'.format(', '.join(v))
            elif k == 'wear':
                response += 'Wear: {}\n'.format(', '.join(v))
            elif k == 'wield':
                response += 'Wield: {}\n'.format(', '.join(v))
            elif k == 'carry':
                response += 'Carry: {}\n'.format(', '.join(v))
            elif k == 'dead':
                response += 'Dead: {}\n'.format(', '.join(v))
            else:
                response += '{} -> {}\n'.format(', '.join(v), k)
        response += '</span>'
        return response

    def _get_help_text(self):
        s = "You can do the following.\n\n"
        action_hint_text = '<span style="color:blue">hints</span>: get a list of possible actions.\n'
        action_text = '<span style="color:blue">&lt;action&gt;</span>: execute an action; e.g., <b>go cavern get apple</b>\n'
        teach_text = '<span style="color:blue">teach</span>: enter the interactive teaching mode. You can then enter some actions, and type "end" when you are ready to provide an order.\n'
        reset_text = '<span style="color:blue">reset</span>: reset the world. All objects, agents, and rooms will be re-organized randomly. You will exit the interactive teaching mode if you are in it.\n'
        command_text = '<span style="color:blue">&lt;order&gt;</span>: teach the dragon some language! You should describe the actions you just executed with one or two sentences.\n'
        model_text = '<span style="color:blue">"&lt;order&gt;"</span>: see what the dragon will do given &lt;order&gt; with the current knowledge level; e.g., <b>"pick up the apple in the cavern"</b>.\n'
        end_text = '<span style="color:blue">end</span>: end the action input. You will then be prompted to provide an order to describe the actions you just executed.\n'
        fast_teach_text = '<span style="color:blue">"&lt;order&gt;" -> &lt;action&gt;</span>: fast teaching. You will provide an example consisting of an order and an action; e.g., <b>"pick up the apple" -> get apple</b>\n'
        example_text = '<span style="color:blue">examples</span>: show the last 10 examples you provided.\n'
        error_example_text = '<span style="color:blue">errors</span>: show 3 orders that the dragon does not understand.\n'
        if self.mode == 'REGULAR':
            s += action_hint_text + action_text + teach_text + reset_text + model_text + fast_teach_text + example_text + error_example_text
        elif self.mode == 'TEACH_ACTION':
            s += action_hint_text + action_text + reset_text + end_text
            # if hasattr(self, 'actions') and len(self.actions) > 0:
            #     s += end_text
        elif self.mode == 'TEACH_COMMAND':
            s += command_text + reset_text
        return s

    def _get_error_text(self):
        return 'You cannot do this!\n' + self._get_help_text()

    def _get_graph_text(self):
        text = self.graph.get_text('dragon').rstrip('\n').replace('<', '&lt;').replace('>', '&gt;')
        if text == '': return ''
        return '\n<span style="color:blue">{}</span>\n'.format(text)

    def _get_reset_text(self):
        return 'The world has been reset!\n{}\n'.format(self._get_graph_text())

    def _get_add_text(self):
        return 'Training example added! You have provided {} example(s). Training mode exited.\n'.format(len(self.training_examples))

    def _get_fast_add_text(self):
        return 'Training example added! You have provided {} example(s).\n'.format(len(self.training_examples))

    def _get_observation(self, acts_text):
        return {'text': acts_text, 'actions': self.graph.get_possible_actions()[0], 'graph': self.graph}

    def _get_old_observation(self, acts_text):
        return {'text': acts_text, 'actions': self.old_graph.get_possible_actions()[0], 'graph': self.old_graph}

    def _reset(self, send=True):
        self.mode = 'REGULAR'
        self.graph = construct_graph(self.opt)
        self.graph.parse_exec('look')
        text = self._get_reset_text()
        if send:
            self._send_msg(text)
        return text

    def _send_msg(self, msg):
        self.mturk_agent.observe({'id': self.task_coordinator_agent_id, 'text': msg.replace('\n\n\n', '\n\n').replace('\n\n\n', '\n\n').replace('\n', '<br>')})

    def log(self, time, content):
        output_dir = join(self.opt['datapath'], 'chat_log')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        fout = open(join(output_dir, '{}'.format(self.mturk_agent.worker_id)), 'a+')
        fout.write('{}\t{}\n'.format(time, content))
        fout.close()

    def log_examples(self, examples):
        output_dir = get_output_dir(self.opt, self.round_index)
        fout = open(join(output_dir, '{}.{}.indv_data.pkl'.format(self.mturk_agent.worker_id, time.time())), 'wb')
        pickle.dump([self.mturk_agent.get_sanitized_copy(), examples], fout)
        fout.close()

    def parley(self):
        if self.mode == 'INIT':
            worker_id = self.mturk_agent.worker_id
            if worker_id in self.cur_ids:
                self.mturk_agent.observe({'id': self.task_coordinator_agent_id, 'text': 'You can only participate once in one round! Stay tuned. The next round will start soon.', 'episode_done': True})
                self.episodeDone = True
                return
            while True:
                if hasattr(self.mturk_agent, 'username'): break
                if worker_id in self.binding['id2name']:
                    self.mturk_agent.username = self.binding['id2name'][worker_id]
                    break
                self._send_msg('Please enter your preferred name to appear on the leaderboard.\n')
                acts = self.mturk_agent.act(timeout=TIMEOUT)
                acts_text = acts['text'].strip().lower()
                self.log(time.time() - self.start_time, acts_text)
                if acts['episode_done'] or acts_text in SPECIAL_SET:
                    if acts_text == '[disconnect]':
                        self.disconnect = True
                    self.episodeDone = True
                    return
                if acts_text != '' and acts_text not in self.binding['name2id']:
                    self.binding['name2id'][acts_text] = worker_id
                    self.binding['id2name'][worker_id] = acts_text
                    self.mturk_agent.username = acts_text
                else:
                    self._send_msg('The name has been used.\n')

            self._send_msg(self._get_wrong_data_text() + '\n' + '-' * 50 + '\n\n' + self._get_graph_text() + '\n')
            self.mode = 'REGULAR'
            return

        acts = self.mturk_agent.act(timeout=TIMEOUT)
        acts_text = acts['text'].strip().lower()
        self.log(time.time() - self.start_time, acts_text)
        if acts['episode_done'] or acts_text in SPECIAL_SET:
            if acts_text == '[disconnect]':
                self.disconnect = True
            self.episodeDone = True
            return
        if acts_text == 'help':
            self._send_msg(self._get_help_text())
        else:
            if self.mode == 'REGULAR':
                if acts_text == 'teach':
                    self.mode = 'TEACH_ACTION'
                    self.old_graph = deepcopy(self.graph)
                    self.actions = []
                    self._send_msg('You have entered the teaching mode!')
                elif acts_text.startswith('"') and acts_text.endswith('"') and len(acts_text) > 2:
                    x, action_key, second_action_key, action_type, current_room, checked, y, y_mask, counter_feat = self.data_agent.get_data([self._get_observation(acts_text[1:-1])], 'valid')
                    x, action_key, second_action_key, action_type, checked = self._get_variable(x, True), self._get_variable(action_key, True), self._get_variable(second_action_key, True), self._get_variable(action_type, True), self._get_variable(checked, True)
                    text_out = self.model.forward_predict(x, action_key, second_action_key, action_type, self.check_mapping, checked, [self.graph], self.data_agent)[0]
                    text_out = text_out[: -1]
                    if len(text_out) == 0:
                        text_out.append('[DO NOTHING]')
                    self._send_msg('The dragon will execute "{}" with the following actions:\n<span style="color:blue">{}</span>\n'.format(acts_text[1:-1], ' '.join(text_out)))
                elif acts_text == 'reset':
                    self._reset()
                elif '->' in acts_text:
                    command, action = tuple(acts_text.split('->'))
                    command, action = command.strip(), action.strip()
                    self.old_graph = deepcopy(self.graph)
                    filter_text = Graph.filter_actions(action)
                    if filter_text != '' and command[0] == '"' and command[-1] == '"' and len(command) > 2 and self.graph.parse_exec(action): # TODO: fix bug with partially valid action seqs
                        command = command[1:-1]
                        self.training_examples.append((getattr(self.mturk_agent, 'conversation_id', 'local'), self.old_graph, command, filter_text))
                        self.mode = 'REGULAR'
                        text = self._reset(False)
                        self._send_msg(self._get_fast_add_text() + text)
                    else:
                        self._send_msg("You cannot do this!")
                elif acts_text == 'examples':
                    s = "You have provided the following examples:\n\n"
                    for i, example in enumerate(self.training_examples):
                        if len(self.training_examples) - i > 10: continue
                        s += '"{}" -> <span style="color:blue">{}</span>\n'.format(example[2], example[3])
                    self._send_msg(s)
                elif acts_text == 'errors':
                    self._send_msg(self._get_wrong_data_text())
                else:
                    s = ''
                    if not self.graph.parse_exec(acts_text): # TODO: fix bug with partially valid action seqs
                        s += 'You cannot do this!\n'
                    s += self._get_graph_text() + '\n'
                    self._send_msg(s)
            elif self.mode == 'TEACH_ACTION':
                if acts_text == 'end' and hasattr(self, 'actions') and len(self.actions) > 0:
                    self.mode = 'TEACH_COMMAND'
                    s = self._get_plan()
                    s += '\nWrite one or two sentences to describe the above actions.\n'
                    self._send_msg(s)
                elif acts_text == 'reset':
                    self._reset()
                elif acts_text == 'end':
                    self._send_msg("You must enter at least one action!")
                else:
                    s = ''
                    if not self.graph.parse_exec(acts_text): # TODO: fix bug with partially valid action seqs
                        s += 'You cannot do this!\n'
                    else:
                        filter_text = Graph.filter_actions(acts_text)
                        if filter_text != '':
                            self.actions.append(filter_text)
                    s += self._get_graph_text() + '\n'
                    self._send_msg(s)
            elif self.mode == 'TEACH_COMMAND':
                if acts_text == 'reset':
                    self._reset()
                else:
                    self.training_examples.append((getattr(self.mturk_agent, 'conversation_id', 'local'), self.old_graph, acts_text, ' '.join(self.actions)))
                    self.mode = 'REGULAR'
                    text = self._reset(False)
                    self._send_msg(self._get_add_text() + text)
            else:
                assert False

    def episode_done(self):
        return self.episodeDone

    def shutdown(self):
        if self.disconnect:
            return
        if not self.forced_timeout:
            self.mturk_agent.shutdown(timeout=TIMEOUT, direct_submit=True)
        else:
            self.mturk_agent.shutdown(timeout=0.1, direct_submit=False)

    def get_data(self):
        if len(self.training_examples) < self.opt['min_examples_per_HIT']:
            return None
        else:
            return self.training_examples

    def review_work(self):
        pass
        # if self.opt['debug_world']: return
        # if len(self.training_examples) < self.opt['min_examples_per_HIT']:
        #     self.mturk_agent.reject_work()
        # else:
        #     self.mturk_agent.approve_work()

class SimpleDataCollectionWorld(DataCollectionWorld):
    def _reset(self, send=True):
        self.mode = 'REGULAR'
        self.graph = construct_graph(self.opt)
        self.graph.parse_exec('look')
        text = self._get_reset_text()
        self.old_graph = deepcopy(self.graph)
        self.actions = []
        if send:
            self._send_msg(text, hints=True)
        return text

    # def _get_hints_text(self):
    #     text = '<h3>What to enter right now?</h3>\nYou <b>must</b> enter <b>exactly</b> <b>one</b> of the following inputs (any other ones will be invalid):\n'
    #     can_teach = self.mode == 'REGULAR' and len(self.actions) > 0
    #     can_actions = len(self.actions) < MAX_ACTION_LEN
    #     if can_teach:
    #         text += '<b>teach</b>, '
    #     actions = self.graph.get_possible_actions()
    #     random.shuffle(actions)
    #     if can_actions:
    #         text += ', '.join(actions) + ', '
    #     text += 'reset, "pick up the apple" (any text order in quotes)\n\n'
    #     if can_teach:
    #         text += 'You have to enter <b>teach</b> 10 times in total to get paid. You can enter <b>teach</b> now.'
    #         if can_actions:
    #              text += ' Or you can enter <b>teach</b> later if you want to have more actions in one example (to make it harder).'
    #         text += '\n\n'
    #     return '<span style="color:green">{}</span>'.format(text)

    def _get_hints_text(self):
        can_teach = self.mode == 'REGULAR' and len(self.actions) > 0
        can_actions = len(self.actions) < MAX_ACTION_LEN
        if can_teach:
            text = '<span style="color:blue"><h4>Actions so far:</h4>{}</span>\n\n'.format(' '.join(self.actions))
        else:
            text = ''
        text += '<h4>What to enter now?</h4>You can enter <b>one</b> of the following:\n\n'
        list_num = 1
        if can_teach:
            text += '{}. You can enter <b>teach</b> now to finish the actions. <span style="color:red">You have to enter <b>teach</b> 10 times in total to get paid.</span>'.format(list_num)
            list_num += 1
            if can_actions:
                text += " You can also enter <b>teach</b> later after you enter more actions (to make it harder)."
            text += '\n\n'
        if can_actions:
            text += '{}. You can enter <b>exactly one</b> of the following actions (just copy and paste!):\n'.format(list_num)
            list_num += 1
            actions = self.graph.get_possible_actions()
            random.shuffle(actions)
            text += ', '.join(actions)
            text += '\n\n'
        text += '{}. You can enter <b>reset</b> to discard the previous actions and start from a new one.\n\n'.format(list_num)
        list_num += 1
        # text += 'You can enter any text order in quotes, e.g. "pick up the apple" to test the dragon.\n\n'
        return '<span style="color:green">{}</span>'.format(text)

    def _send_msg(self, msg_, hints=False):
        msg = msg_
        if hints:
            msg += '\n' + '-' * 50 + '\n\n' + self._get_hints_text() + '\n'
        self.mturk_agent.observe({'id': self.task_coordinator_agent_id, 'text': msg.replace('\n\n\n', '\n\n').replace('\n\n\n', '\n\n').replace('\n', '<br>')})

    def _get_wrong_data_text(self, correct=None):
        if correct is None:
            s = "Your dragon does not understand the following orders. (Some actions/orders might be wrong; use your judgment)\n\n"
        if correct == True:
            s = "However, your dragon does not understand the following orders. (Some actions/orders might be wrong; use your judgment)\n\n"
        if correct == False:
            s = "Your dragon also does not understand the following orders. (Some actions/orders might be wrong; use your judgment)\n\n"

        flag = False
        for i in range(self.opt['error_examples']):
            if self.wrong_data_index + i >= len(self.wrong_data): break
            flag, data = True, self.wrong_data[self.wrong_data_index + i]
            correct_action, wrong_action, language_command = tuple(data.split(' ||| '))
            # s += '<span style="color:red"><b>Order</b>: {}</span>\n'.format(language_command)
            s += '<span style="color:blue"><b>Actions</b>: {}</span> &nbsp;&nbsp;&nbsp; <span style="color:red"><b>Order</b>: {}</span>\n'.format(correct_action, language_command)
            # s += '"{}" -> <span style="color:blue">{}</span> &nbsp;&nbsp;<b>NOT</b>&nbsp;&nbsp; <span style="color:red">{}</span>\n'.format(language_command, correct_action, wrong_action)
        self.wrong_data_index += self.opt['error_examples']
        if not flag:
            return ""
        # s += "\nNow try your best to teach the dragon more human language!\n"
        s += '\nTeach it something similar!\n'
        return s

    def _get_add_text(self, exec_text='', correct=None):
        return 'Training example added! You have provided {} example(s). The last example(s) you have provided are:\n{}\n{}\n{}\n\n'.format(len(self.training_examples), self._get_examples_text(), exec_text, self._get_wrong_data_text(correct)) + '-' * 50 + '\n\n'

    def _get_end_text(self):
        return 'You have successfully trained your own dragon! Competition results will be sent to your email soon!'

    def _get_examples_text(self):
        s = ''
        for i, example in enumerate(self.training_examples):
            if len(self.training_examples) - i > 3: continue
            # s += '"{}" -> <span style="color:blue">{}</span>\n'.format(example[2], example[3])
            s += '<span style="color:blue"><b>Actions</b>: {}</span> &nbsp;&nbsp;&nbsp; <span style="color:red"><b>Order</b>: {}</span>\n'.format(example[3], example[2])
        return s

    # def _get_plan(self):
    #     return 'You just executed the following actions:\n<span style="color:blue">{}</span>\n'.format('\n'.join(self.actions))

    def parley(self):
        if self.mode == 'INIT':
            worker_id = self.mturk_agent.worker_id
            if worker_id in self.cur_ids:
                self.mturk_agent.observe({'id': self.task_coordinator_agent_id, 'text': 'You can only participate once in one round! Stay tuned. The next round will start soon. Please return the HIT. Sorry about any inconvenience.', 'episode_done': True})
                self.episodeDone = True
                self.forced_timeout = True
                return
            while True:
                if hasattr(self.mturk_agent, 'username'): break
                if worker_id in self.binding['id2name']:
                    self.mturk_agent.username = self.binding['id2name'][worker_id]
                    break
                self._send_msg('Please enter your preferred name to appear on the leaderboard.\n')
                acts = self.mturk_agent.act(timeout=TIMEOUT)
                acts_text = acts['text'].strip().lower()
                self.log(time.time() - self.start_time, acts_text)
                if acts['episode_done'] or acts_text == '[expired]' or acts_text == '[timeout]':
                    self.episodeDone = True
                    return
                if acts_text != '' and acts_text not in self.binding['name2id']:
                    self.binding['name2id'][acts_text] = worker_id
                    self.binding['id2name'][worker_id] = acts_text
                    self.mturk_agent.username = acts_text
                else:
                    self._send_msg('The name has been used.\n')

            self.mode = 'REGULAR'
            self.old_graph = deepcopy(self.graph)
            self.actions = []
            self._send_msg(self._get_wrong_data_text() + '\n' + '-' * 50 + '\n\n' + self._get_graph_text() + '\n', hints=True)
            return

        acts = self.mturk_agent.act(timeout=TIMEOUT)
        acts_text = acts['text'].strip().lower()
        self.log(time.time() - self.start_time, acts_text)
        if acts['episode_done'] or acts_text == '[expired]' or acts_text == '[timeout]':
            self.episodeDone = True
            return
        if self.mode == 'REGULAR':
            if acts_text == 'teach':
                if len(self.actions) == 0:
                    self._send_msg("You must enter at least one action!", hints=True)
                else:
                    self.mode = 'TEACH_COMMAND'
                    s = self._get_plan()
                    # s += '\n<b>Write an order in one or two sentences to describe the above actions.</b> You can enter <b>reset</b> to discard the above actions and start from a new one.\n\nNote: Try increasing the variety of your language, and <b>DO NOT</b> directly copy the actions!'
                    s += '\n<b>Write an order in one or two sentences to precisely describe the above changes.</b> You can enter <b>reset</b> to discard the above changes and start from new actions. Try increasing the variety of your language, and <b>DO NOT</b> directly copy the actions!'
                    self._send_msg(s)
            elif acts_text == 'reset':
                self._reset()
            # elif acts_text.startswith('"') and acts_text.endswith('"') and len(acts_text) > 2:
            #     x, action_key, second_action_key, action_type, current_room, checked, y, y_mask, counter_feat = self.data_agent.get_data([self._get_observation(acts_text[1:-1])], 'valid')
            #     x, action_key, second_action_key, action_type, checked = self._get_variable(x, True), self._get_variable(action_key, True), self._get_variable(second_action_key, True), self._get_variable(action_type, True), self._get_variable(checked, True)
            #     text_out = self.model.forward_predict(x, action_key, second_action_key, action_type, self.check_mapping, checked, [self.graph], self.data_agent)[0]
            #     text_out = text_out[: -1]
            #     if len(text_out) == 0:
            #         text_out.append('[DO NOTHING]')
            #     self._send_msg('The dragon will execute the order <span style="color:red">{}</span> with the following actions:\n<span style="color:blue">{}</span>\n\nIf your dragon does not understand, teach it something similar!'.format(acts_text[1:-1], ' '.join(text_out)), hints=True)
            elif len(self.actions) < MAX_ACTION_LEN:
                s = ''
                _, symb_points = Graph.parse_static(acts_text)
                if len(symb_points) == 1:
                    s += 'You cannot do this!\n'
                elif len(symb_points) != 2:
                    s += 'You can only enter one action at a time!\n'
                elif not self.graph.parse_exec(acts_text):
                    s += 'You cannot do this!\n'
                else:
                    filter_text = Graph.filter_actions(acts_text)
                    if filter_text != '':
                        self.actions.append(filter_text)
                s += self._get_graph_text() + '\n'
                self._send_msg(s, hints=True)
            else:
                self._send_msg('You cannot do this!\n', hints=True)
        elif self.mode == 'TEACH_COMMAND':
            if acts_text == 'reset':
                self._reset()
            else:
                self.training_examples.append((getattr(self.mturk_agent, 'conversation_id', 'local'), self.old_graph, acts_text, ' '.join(self.actions)))
                if len(self.training_examples) == self.opt['min_examples_per_HIT']:
                    self.mturk_agent.observe({'text': self._get_end_text().replace('\n', '<br>'), 'episode_done': True, 'id': self.task_coordinator_agent_id})
                    self.log_examples(self.training_examples)
                    self.episodeDone = True
                else:
                    try:
                        x, action_key, second_action_key, action_type, current_room, checked, y, y_mask, counter_feat = self.data_agent.get_data([self._get_old_observation(acts_text)], 'valid')
                        x, action_key, second_action_key, action_type, checked = self._get_variable(x, True), self._get_variable(action_key, True), self._get_variable(second_action_key, True), self._get_variable(action_type, True), self._get_variable(checked, True)
                        text_out = self.model.forward_predict(x, action_key, second_action_key, action_type, self.check_mapping, checked, [self.old_graph], self.data_agent)[0]
                        text_out = text_out[: -1]
                        if len(text_out) == 0:
                            text_out.append('[DO NOTHING]')
                        exec_text = 'Before training with your wise teachings, the dragon would execute your order <span style="color:red">{}</span> with the following actions: <span style="color:blue">{}</span>\n\n'.format(acts_text, ' '.join(text_out))
                        correct = ' '.join(text_out) == ' '.join(self.actions)
                    except:
                        print(traceback.format_exc())
                        exec_text = ''
                        correct = None
                    text = self._reset(False)
                    self._send_msg(self._get_add_text(exec_text, correct) + text, hints=True)
        else:
            assert False


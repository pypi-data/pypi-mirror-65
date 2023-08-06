#!/usr/bin/env python3
from parlai.core.agents import Agent
from collections import defaultdict as dd
import spacy
from .models import RuleDecoder, ObjectChecklistModel, Seq2SeqModel
import numpy as np
from torch.autograd import Variable
import torch
import random
from copy import deepcopy

nlp = spacy.load('en')


class DataAgentBase(Agent):
    def __init__(self, opt, shared=None):
        super().__init__(opt, shared)

        if not shared:
            self.word2cnt = dd(int)
            self.rooms, self.objects = [], []
        else:
            self.word2cnt = shared['word2cnt']
            self.rooms = shared['rooms']
            self.objects = shared['objects']

    def _tokenize(self, text, lower=True):
        return list(map(lambda x: x.lower_ if lower else x.orth_, list(nlp(text))))

    def act(self):
        observation = self.observation
        if 'graph' not in observation:
            return {}
        if len(self.rooms) == 0:
            self.rooms.extend(observation['graph'].rooms)
            self.objects.extend(observation['graph'].objects)

        tokens = self._tokenize(observation['text'])
        for token in tokens:
            self.word2cnt[token] += 1
        return {}

    def build(self):
        opt = self.opt
        word2cnt = [(k, v) for k, v in self.word2cnt.items()]
        word2cnt.sort(key=lambda x: x[1], reverse=True)
        word_offset, word2index = 2, {}
        word2index['PAD'] = 0
        word2index['UNK'] = 1
        for i in range(opt['vocab_size'] - word_offset):
            if i >= len(word2cnt):
                break
            word = word2cnt[i][0]
            word2index[word] = i + word_offset
        self.word2index = word2index
        self.wordcnt = len(word2index)

    def _get_word_index(self, token):
        if token in self.word2index:
            return self.word2index[token]
        return self.word2index['UNK']

    def share(self):
        shared = super().share()
        shared['rooms'] = self.rooms
        shared['objects'] = self.objects
        shared['word2cnt'] = self.word2cnt
        return shared


class RuleDataAgent(DataAgentBase):
    @staticmethod
    def get_map(g, map):
        offset = 0
        for kk in range(len(g.objects)):
            if g.object2room[kk] == g.agent_at_room:
                map[offset + kk] = 1.0
        offset += len(g.objects)
        for kk in range(len(g.objects)):
            if g.object2room[kk] == -1:
                map[offset + kk] = 1.0
        offset += len(g.objects)
        for kk in g.room_edges[g.agent_at_room]:
            map[offset + kk] = 1.0

    @staticmethod
    def update_x(g, action, old_x, new_x):
        np.copyto(new_x, old_x)
        name = ' '.join(action.split()[1:])
        if name in g.objects:
            i = g.objects.index(name)
        else:
            i = g.rooms.index(name) + len(g.objects)
        new_x[i] = 0.0

    def get_data(self, observations, datatype='train'):
        opt = self.opt
        batch_size = len(observations)
        seq_in, seq_out = 0, 0
        tokens_list, inst_list, symb_points_list = [], [], []
        for observation in observations:
            graph, text, actions = (
                observation['graph'],
                observation['text'],
                observation['actions'],
            )
            tokens_list.append(self._tokenize(text))
            seq_in = max(seq_in, len(tokens_list[-1]))

            graph = observation['graph']
            inst, symb_points = graph.parse(actions)
            seq_out = max(seq_out, len(symb_points) - 1 + 1)  # +1 for stop
            inst_list.append(inst)
            symb_points_list.append(symb_points)

        if datatype == 'valid':
            seq_out = opt['max_seq_out']

        seq_in = min(seq_in, opt['max_seq_in'])
        # x = np.zeros((batch_size, seq_in), dtype=np.int64)
        # x = np.zeros((batch_size, seq_in, self.wordcnt), dtype=np.float32)
        # x = np.zeros((batch_size, self.wordcnt), dtype=np.float32)
        x = np.zeros((batch_size, seq_out, opt['x_dim']), dtype=np.float32)
        map = np.zeros((batch_size, seq_out, opt['feat_dim']), dtype=np.float32)
        y = np.zeros((batch_size, seq_out, opt['y_dim']), dtype=np.float32)

        for i in range(batch_size):
            # for j, token in enumerate(tokens_list[i]):
            #     if j >= seq_in: break
            # x[i, j] = self._get_word_index(token)
            # x[i, j, self._get_word_index(token)] = 1.0
            # x[i, self._get_word_index(token)] = 1.0

            inst = inst_list[i]
            g = observations[i]['graph'].copy()
            len_plus_one = len(symb_points_list[i])

            token_expand = ' '.join(tokens_list[i])
            for j, room in enumerate(g.rooms):
                # if token_expand.find(room) >= 0:
                if token_expand.find(room) >= 0 and j != g.agent_at_room:
                    x[i, 0, opt['num_objects'] + j] = 1.0
            for j, object in enumerate(g.objects):
                if token_expand.find(object) >= 0:
                    x[i, 0, j] = 1.0

            for j in range(len_plus_one):
                if j < len_plus_one - 1:
                    k, l = symb_points_list[i][j], symb_points_list[i][j + 1]
                    target_str = ' '.join(inst[k + 1 : l])
                    if target_str in self.rooms:
                        target_index = self.rooms.index(target_str)
                    else:
                        target_index = self.objects.index(target_str)
                    if inst[k] == 'get':
                        y[i, j, target_index] = 1.0
                    elif inst[k] == 'drop':
                        y[i, j, opt['num_objects'] + target_index] = 1.0
                    else:
                        y[i, j, 2 * opt['num_objects'] + target_index] = 1.0
                else:
                    y[i, j, -1] = 1.0

                DataAgent.get_map(g, map[i, j])

                if j < len_plus_one - 1:
                    assert g.parse_exec(' '.join(inst[k:l]))

                    DataAgent.update_x(g, ' '.join(inst[k:l]), x[i, j], x[i, j + 1])

        # print(observations[0])
        # print(x[0])
        # print(map[0])
        # print(y[0])
        # quit()
        return x, map, y


class ObjectChecklistDataAgent(DataAgentBase):
    def get_room(self, g):
        return self._get_word_index(g.rooms[g.agent_at_room].replace(' ', '_'))

    @staticmethod
    def get_mask(g, mask):
        offset = 0
        for kk in range(len(g.objects)):
            if g.object2room[kk] == g.agent_at_room:
                mask[offset + kk] = 1.0
        offset += len(g.objects)
        for kk in range(len(g.objects)):
            if g.object2room[kk] == -1:
                mask[offset + kk] = 1.0
        offset += len(g.objects)
        for kk in g.room_edges[g.agent_at_room]:
            mask[offset + kk] = 1.0
        offset += len(g.rooms)
        mask[offset] = 1.0

    def _tokenize(self, text, lower=True):
        tokenized = ' '.join(
            list(map(lambda x: x.lower_ if lower else x.orth_, list(nlp(text))))
        )
        for ent in self.rooms + self.objects:
            tokenized = tokenized.replace(ent, ent.replace(' ', '_'))
        return tokenized.split()

    def get_check_mapping(self, g):
        if not hasattr(self, 'check_mapping'):
            num_objects, num_rooms = len(g.objects), len(g.rooms)
            num_entities = 2 * num_objects + num_rooms + 1
            check_mapping = np.zeros((num_entities, num_entities), dtype=np.float32)
            for i in range(num_entities):
                check_mapping[i, i] = 1.0
            for i in range(num_objects):
                check_mapping[i, i + num_objects] = 1.0
                check_mapping[i + num_objects, i] = 1.0
            self.check_mapping = check_mapping
        return self.check_mapping

    def get_data(self, observations, datatype='train'):
        opt = self.opt
        batch_size = len(observations)
        seq_in, seq_out = 0, 0
        tokens_list, inst_list, symb_points_list = [], [], []
        for observation in observations:
            graph, text, actions = (
                observation['graph'],
                observation['text'],
                observation['actions'],
            )
            tokens_list.append(self._tokenize(text))
            seq_in = max(seq_in, len(tokens_list[-1]))

            graph = observation['graph']
            inst, symb_points = graph.parse(actions)
            seq_out = max(seq_out, len(symb_points) - 1 + 1)  # +1 for stop
            inst_list.append(inst)
            symb_points_list.append(symb_points)

        if datatype == 'valid':
            seq_out = opt['max_seq_out']

        seq_in = min(seq_in, opt['max_seq_in'])
        y_dim = opt['y_dim']
        x = np.zeros((batch_size, seq_in), dtype=np.int64)
        current_room = np.zeros((batch_size, seq_out), dtype=np.int64)
        checked = np.zeros((batch_size, seq_out + 1, y_dim), dtype=np.float32)
        y = np.zeros((batch_size, seq_out, y_dim), dtype=np.float32)

        graph = observations[0]['graph']
        num_objects, num_rooms = len(graph.objects), len(graph.rooms)

        if not hasattr(self, 'action_key'):
            action_key = np.zeros((y_dim,), dtype=np.int64)
            offset = 0
            for i in range(num_objects):
                action_key[offset + i] = self._get_word_index(
                    graph.objects[i].replace(' ', '_')
                )
            offset += num_objects
            for i in range(num_objects):
                action_key[offset + i] = self._get_word_index(
                    graph.objects[i].replace(' ', '_')
                )
            offset += num_objects
            for i in range(num_rooms):
                action_key[offset + i] = self._get_word_index(
                    graph.rooms[i].replace(' ', '_')
                )
            self.action_key = action_key
        action_key = self.action_key

        if not hasattr(self, 'action_type'):
            action_type = np.zeros((y_dim,), dtype=np.int64)
            action_type[:num_objects] = 0
            action_type[num_objects : 2 * num_objects] = 1
            action_type[2 * num_objects : -1] = 2
            action_type[-1] = 3
            self.action_type = action_type
        action_type = self.action_type

        for i in range(batch_size):
            for j, token in enumerate(tokens_list[i]):
                if j >= seq_in:
                    break
                x[i, j] = self._get_word_index(token)

            inst = inst_list[i]
            g = observations[i]['graph'].copy()
            len_plus_one = len(symb_points_list[i])

            # for target_index, target_str in enumerate(self.objects):
            #     occur_after = False
            #     for jj in range(0, len_plus_one - 1):
            #         kk, ll = symb_points_list[i][jj], symb_points_list[i][jj + 1]
            #         target_str_str = ' '.join(inst[kk + 1: ll])
            #         if target_str_str == target_str:
            #             occur_after = True
            #     if not occur_after:
            #         checked[i, :, target_index] = 1.0
            #         checked[i, :, target_index + len(self.objects)] = 1.0
            # for target_index, target_str in enumerate(self.rooms):
            #     occur_after = False
            #     for jj in range(0, len_plus_one - 1):
            #         kk, ll = symb_points_list[i][jj], symb_points_list[i][jj + 1]
            #         target_str_str = ' '.join(inst[kk + 1: ll])
            #         if target_str_str == target_str:
            #             occur_after = True
            #     if not occur_after:
            #         checked[i, :, 2 * len(self.objects) + target_index] = 1.0

            # target_str = self.rooms[g.agent_at_room]
            # target_index = 2 * len(self.objects) + g.agent_at_room
            # occur_after = False
            # for jj in range(0, len_plus_one - 1):
            #     kk, ll = symb_points_list[i][jj], symb_points_list[i][jj + 1]
            #     target_str_str = ' '.join(inst[kk + 1: ll])
            #     if target_str_str == target_str:
            #         occur_after = True
            # if not occur_after:
            #     checked[i, :, target_index] = 1.0

            for j in range(len_plus_one):
                if j < len_plus_one - 1:
                    k, l = symb_points_list[i][j], symb_points_list[i][j + 1]
                    target_str = ' '.join(inst[k + 1 : l])
                    if target_str in self.rooms:
                        target_index = self.rooms.index(target_str)
                    else:
                        target_index = self.objects.index(target_str)

                    occur_after = False
                    for jj in range(j + 1, len_plus_one - 1):
                        kk, ll = symb_points_list[i][jj], symb_points_list[i][jj + 1]
                        target_str_str = ' '.join(inst[kk + 1 : ll])
                        if target_str_str == target_str:
                            occur_after = True

                    if inst[k] == 'get':
                        y[i, j, target_index] = 1.0
                        if not occur_after:
                            checked[i, j + 1 :, target_index] = 1.0
                            checked[i, j + 1 :, target_index + num_objects] = 1.0
                    elif inst[k] == 'drop':
                        y[i, j, num_objects + target_index] = 1.0
                        if not occur_after:
                            checked[i, j + 1 :, target_index] = 1.0
                            checked[i, j + 1 :, target_index + num_objects] = 1.0
                    else:
                        y[i, j, 2 * num_objects + target_index] = 1.0
                        if not occur_after:
                            checked[i, j + 1 :, 2 * num_objects + target_index] = 1.0
                else:
                    y[i, j, -1] = 1.0
                    checked[i, j + 1, -1] = 1.0

                current_room[i, j] = self.get_room(g)

                if j < len_plus_one - 1:
                    assert g.parse_exec(' '.join(inst[k:l]))

        # print(x[0])
        # print(action_key)
        # print(current_room[0])
        # print(checked[0])
        # print(y[0])
        # quit()
        return x, action_key, action_type, current_room, checked, y


class Seq2SeqDataAgent(DataAgentBase):
    def get_data(self, observations):
        opt = self.opt
        batch_size = len(observations)
        seq_in, seq_out = 0, 0
        tokens_list, inst_list, symb_points_list = [], [], []
        for observation in observations:
            graph, text, actions = (
                observation['graph'],
                observation['text'],
                observation['actions'],
            )
            tokens_list.append(self._tokenize(text))
            seq_in = max(seq_in, len(tokens_list[-1]))

            graph = observation['graph']
            inst, symb_points = graph.parse(actions)
            seq_out = max(seq_out, len(symb_points) - 1 + 1)  # +1 for stop
            inst_list.append(inst)
            symb_points_list.append(symb_points)

        seq_in = min(seq_in, opt['max_seq_in'])
        x = np.zeros((batch_size, seq_in), dtype=np.int64)
        map = np.zeros((batch_size, seq_out, opt['feat_dim']), dtype=np.float32)
        y = np.zeros((batch_size, seq_out, opt['y_dim']), dtype=np.float32)

        for i in range(batch_size):
            for j, token in enumerate(tokens_list[i]):
                if j >= seq_in:
                    break
                x[i, j] = self._get_word_index(token)
            inst = inst_list[i]
            g = observations[i]['graph'].copy()
            for j in range(len(symb_points_list[i]) - 1):
                k, l = symb_points_list[i][j], symb_points_list[i][j + 1]
                target_str = ' '.join(inst[k + 1 : l])
                if target_str in self.rooms:
                    target_index = self.rooms.index(target_str)
                else:
                    target_index = self.objects.index(target_str)
                if inst[k] == 'get':
                    y[i, j, target_index] = 1.0
                elif inst[k] == 'drop':
                    y[i, j, opt['num_objects'] + target_index] = 1.0
                else:
                    y[i, j, 2 * opt['num_objects'] + target_index] = 1.0

                offset = 0
                for kk in range(len(g.objects)):
                    if g.object2room[kk] == -1:
                        map[i, j, offset + kk] = 1.0
                offset += len(g.objects)
                for kk in range(len(g.objects)):
                    if g.object2room[kk] == g.agent_at_room:
                        map[i, j, offset + kk] = 1.0
                offset += len(g.objects)
                map[i, j, offset + g.agent_at_room] = 1.0

                # print(' '.join(inst[k: l]))
                assert g.parse_exec(' '.join(inst[k:l]))

            y[i, len(symb_points_list[i]) - 1, -1] = 1.0

        # print(observations[0])
        # print(x[0])
        # print(map[0])
        # print(y[0])
        # quit()
        return x, map, y


class ModelAgentBase(Agent):
    def __init__(self, opt, shared=None, data_agent=None):
        super().__init__(opt, shared)
        if not shared:
            self.data_agent = data_agent
            params = filter(lambda p: p.requires_grad, self.model.parameters())
            self.optimizer = torch.optim.Adam(params, lr=opt['lr'])
            if opt['cuda']:
                self.model.cuda()
                # self.optimizer.cuda()
        else:
            self.data_agent = shared['data_agent']
            self.model = shared['model']
            self.optimizer = shared['optimizer']

    def share(self):
        shared = super().share()
        shared['data_agent'] = self.data_agent
        shared['model'] = self.model
        shared['optimizer'] = self.optimizer
        return shared

    def _get_variable(self, np_a, volatile=False):
        if self.opt['cuda']:
            return Variable(torch.from_numpy(np_a).cuda(), volatile=volatile)
        return Variable(torch.from_numpy(np_a), volatile=volatile)

    def _get_f1(self, tokens_1, tokens_2):
        tokens_1, tokens_2 = set(tokens_1), set(tokens_2)
        tp, fp, fn = 0, 0, 0
        for token in tokens_2:
            if token in tokens_1:
                tp += 1
            else:
                fp += 1
        for token in tokens_1:
            if token not in tokens_2:
                fn += 1
        prec = 1.0 * tp / (tp + fp) if tp + fp > 0 else 0.0
        recall = 1.0 * tp / (tp + fn) if tp + fn > 0 else 0.0
        f1 = 2.0 * prec * recall / (prec + recall) if prec + recall > 0 else 0.0
        return f1

    def act(self):
        return self.batch_act([self.observation])[0]


class RuleModelAgent(ModelAgentBase):
    # def __init__(self, opt, shared=None, data_agent=None):
    #     if not shared:
    #         self.model = RuleDecoder(opt, data_agent)
    #     super().__init__(opt, shared, data_agent)

    def __init__(self, opt, shared=None, data_agent=None):
        self.opt = deepcopy(opt)
        if not shared:
            self.model = RuleDecoder(opt, data_agent)
            self.data_agent = data_agent
            if opt['cuda']:
                self.model.cuda()
        else:
            self.data_agent = shared['data_agent']
            self.model = shared['model']

    def batch_act(self, observations):
        ori_len = len(observations)
        observations = [obv for obv in observations if 'text' in obv]
        if self.opt['datatype'] == 'train':
            # x, map, y = self.data_agent.get_data(observations)
            # x, map, y = self._get_variable(x), self._get_variable(map), self._get_variable(y)

            # loss = self.model(x, map, y)
            # self.optimizer.zero_grad()
            # loss.backward()
            # self.optimizer.step()

            reply = [{}] * ori_len
            reply[0]['loss'] = 0.0
            return reply
        else:
            x, map, y = self.data_agent.get_data(observations, 'valid')
            x, map, y = (
                self._get_variable(x),
                self._get_variable(map),
                self._get_variable(y),
            )

            # loss = self.model(x, map, y)
            reply = [
                {
                    'loss': 0.0,
                    'cnt': 0.0,
                    'acc': 0,
                    'len': 0,
                    'correct_data': [],
                    'wrong_data': [],
                }
                for _ in range(ori_len)
            ]

            text_out = self.model.forward(
                x, loss=False, graphs=[obv['graph'] for obv in observations]
            )

            for i in range(len(observations)):
                data_rep = '{} ||| {} ||| {}'.format(
                    observations[i]['actions'],
                    ' '.join(text_out[i][:-1]),
                    observations[i]['text'],
                )

                graph_a, graph_b = (
                    observations[i]['graph'].copy(),
                    observations[i]['graph'].copy(),
                )
                graph_a.parse_exec(observations[i]['actions'])
                graph_b.parse_exec(' '.join(text_out[i][:-1]))
                if graph_a == graph_b:
                    reply[i]['acc'] = 1.0
                    reply[i]['correct_data'].append(data_rep)
                else:
                    reply[i]['wrong_data'].append(data_rep)

                inst, symb_points = observations[i]['graph'].parse(
                    observations[i]['actions']
                )
                text_gt = []
                for j in range(len(symb_points) - 1):
                    k, l = symb_points[j], symb_points[j + 1]
                    text_gt.append(' '.join(inst[k:l]))
                reply[i]['f1'] = self._get_f1(text_gt, text_out[i])

                reply[i]['loss'] = 0.0  # loss.data[0]
                reply[i]['cnt'] = 1
                reply[i]['len'] = len(text_gt)

            for i in range(len(observations), ori_len):
                for k in reply[i].keys():
                    reply[i][k] = 0

            return reply


class ObjectChecklistModelAgent(ModelAgentBase):
    def __init__(self, opt, shared=None, data_agent=None):
        if not shared:
            self.model = ObjectChecklistModel(opt, data_agent)
        super().__init__(opt, shared, data_agent)

    def batch_act(self, observations):
        ori_len = len(observations)
        observations = [obv for obv in observations if 'text' in obv]
        if self.opt['datatype'] == 'train' or self.opt['datatype'] == 'pretrain':
            x, action_key, action_type, current_room, checked, y = self.data_agent.get_data(
                observations
            )
            x, action_key, action_type, current_room, checked, y = (
                self._get_variable(x),
                self._get_variable(action_key),
                self._get_variable(action_type),
                self._get_variable(current_room),
                self._get_variable(checked),
                self._get_variable(y),
            )

            loss, std_loss, check_loss = self.model.forward_loss(
                x, action_key, action_type, current_room, checked, y
            )
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            reply = [
                {
                    'loss': loss.data[0],
                    'std_loss': std_loss.data[0],
                    'check_loss': check_loss.data[0],
                }
                for _ in range(ori_len)
            ]
            return reply
        else:
            x, action_key, action_type, current_room, checked, y = self.data_agent.get_data(
                observations, 'valid'
            )
            x, action_key, action_type, current_room, checked, y = (
                self._get_variable(x, True),
                self._get_variable(action_key, True),
                self._get_variable(action_type, True),
                self._get_variable(current_room, True),
                self._get_variable(checked, True),
                self._get_variable(y, True),
            )

            loss, std_loss, check_loss = self.model.forward_loss(
                x, action_key, action_type, current_room, checked, y
            )
            reply = [
                {
                    'loss': 0.0,
                    'std_loss': 0.0,
                    'check_loss': 0.0,
                    'cnt': 0.0,
                    'acc': 0,
                    'len': 0,
                    'correct_data': [],
                    'wrong_data': [],
                }
                for _ in range(ori_len)
            ]

            check_mapping = self.data_agent.get_check_mapping(observations[0]['graph'])
            check_mapping = self._get_variable(check_mapping)
            text_out = self.model.forward_predict(
                x,
                action_key,
                action_type,
                check_mapping,
                checked,
                [obv['graph'] for obv in observations],
                self.data_agent,
            )

            for i in range(len(observations)):
                data_rep = '{} ||| {} ||| {}'.format(
                    observations[i]['actions'],
                    ' '.join(text_out[i][:-1]),
                    observations[i]['text'],
                )

                graph_a, graph_b = (
                    observations[i]['graph'].copy(),
                    observations[i]['graph'].copy(),
                )
                graph_a.parse_exec(observations[i]['actions'])
                graph_b.parse_exec(' '.join(text_out[i][:-1]))
                if graph_a == graph_b:
                    reply[i]['acc'] = 1.0
                    reply[i]['correct_data'].append(data_rep)
                else:
                    reply[i]['wrong_data'].append(data_rep)

                inst, symb_points = observations[i]['graph'].parse(
                    observations[i]['actions']
                )
                text_gt = []
                for j in range(len(symb_points) - 1):
                    k, l = symb_points[j], symb_points[j + 1]
                    text_gt.append(' '.join(inst[k:l]))
                reply[i]['f1'] = self._get_f1(text_gt, text_out[i])

                reply[i]['loss'] = loss.data[0]
                reply[i]['std_loss'] = std_loss.data[0]
                reply[i]['check_loss'] = check_loss.data[0]
                reply[i]['cnt'] = 1
                reply[i]['len'] = len(text_gt)

            for i in range(len(observations), ori_len):
                for k in reply[i].keys():
                    reply[i][k] = 0

            return reply


class Seq2SeqModelAgent(ModelAgentBase):
    def __init__(self, opt, shared=None, data_agent=None):
        if not shared:
            self.model = Seq2SeqModel(opt, data_agent)
        super().__init__(opt, shared, data_agent)

    def batch_act(self, observations):
        ori_len = len(observations)
        observations = [obv for obv in observations if 'text' in obv]
        if self.opt['datatype'] == 'train':
            x, map, y = self.data_agent.get_data(observations)
            x, map, y = (
                self._get_variable(x),
                self._get_variable(map),
                self._get_variable(y),
            )

            loss = self.model(x, map, y)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            reply = [{}] * ori_len
            reply[0]['loss'] = loss.data[0]
            return reply
        else:
            x, map, y = self.data_agent.get_data(observations)
            x, map, y = (
                self._get_variable(x),
                self._get_variable(map),
                self._get_variable(y),
            )

            loss = self.model(x, map, y)
            reply = [
                {
                    'loss': 0.0,
                    'cnt': 0.0,
                    'acc': 0,
                    'len': 0,
                    'correct_data': [],
                    'wrong_data': [],
                }
                for _ in range(ori_len)
            ]

            text_out = self.model.forward(
                x, loss=False, graphs=[obv['graph'] for obv in observations]
            )

            for i in range(len(observations)):
                data_rep = '{} ||| {} ||| {}'.format(
                    observations[i]['actions'],
                    ' '.join(text_out[i][:-1]),
                    observations[i]['text'],
                )

                graph_a, graph_b = (
                    observations[i]['graph'].copy(),
                    observations[i]['graph'].copy(),
                )
                graph_a.parse_exec(observations[i]['actions'])
                graph_b.parse_exec(' '.join(text_out[i][:-1]))
                if graph_a == graph_b:
                    reply[i]['acc'] = 1.0
                    reply[i]['correct_data'].append(data_rep)
                else:
                    reply[i]['wrong_data'].append(data_rep)

                inst, symb_points = observations[i]['graph'].parse(
                    observations[i]['actions']
                )
                text_gt = []
                for j in range(len(symb_points) - 1):
                    k, l = symb_points[j], symb_points[j + 1]
                    text_gt.append(' '.join(inst[k:l]))
                reply[i]['f1'] = self._get_f1(text_gt, text_out[i])

                reply[i]['loss'] = loss.data[0]
                reply[i]['cnt'] = 1
                reply[i]['len'] = len(text_gt)

            for i in range(len(observations), ori_len):
                for k in reply[i].keys():
                    reply[i][k] = 0

            return reply


# DataAgent = RuleDataAgent
# ModelAgent = RuleModelAgent

DataAgent = ObjectChecklistDataAgent
ModelAgent = ObjectChecklistModelAgent

# DataAgent = Seq2SeqDataAgent
# ModelAgent = Seq2SeqModelAgent

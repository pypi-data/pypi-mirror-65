#!/usr/bin/env python3

from parlai_internal.tasks.graph_world.agents import MemorizationBotAgent, extract_quote_spans
from parlai.core.agents import Agent
import random
from collections import defaultdict as dd
from collections import deque
from copy import deepcopy
from parlai_internal.tasks.graph_world.graph import construct_world, DEFAULT_ROOMS, DEFAULT_OBJECTS
import pickle
import os
import time

class DataCollectionBotAgent(Agent):
    def __init__(self, opt, shared=None):
        super().__init__(opt)

        self.actions = None
        self.action_len = opt['action_len']

        self.training_examples = []

        self.old_graph, self.old_actions = None, None

    def _gen_actions(self, graph):
        visited = dd(bool)
        q = deque([(graph.copy(), 0, [])])
        visited[graph.unique_hash()] = True

        while len(q) > 0:
            g_old, time_old, actions_old = q.popleft()
            if time_old >= self.action_len: return []
            actions = g_old.get_possible_actions()
            random.shuffle(actions)
            for action in actions:
                g_new = g_old.copy()
                g_new.parse_exec(action)
                if visited[g_new.unique_hash()]: continue
                actions_new = actions_old + [action]
                if time_old == self.action_len - 1:
                    return ' '.join(actions_new)
                q.append((g_new, time_old + 1, actions_new))
                visited[g_new.unique_hash()] = True
        raise RuntimeError('Cannot find possible action sequences. Try reducing the length.')

    # def act(self):
    #     g = self.graph
    #     self.old_graph = g.copy()
    #     old_text = g.get_text_global().split('\n')
    #     actions = self._gen_actions(g)
    #     self.old_actions = actions
    #     g.parse_exec(actions)
    #     new_text = g.get_text_global().split('\n')
    #     new_text_filter = []
    #     for i in range(len(new_text)):
    #         if new_text[i] == '':
    #             if len(new_text_filter) != 0:
    #                 new_text_filter.append('')
    #         elif new_text[i] != old_text[i]:
    #             new_text_filter.append(new_text[i])
    #     new_text_filter = '\n'.join(new_text_filter)
    #     old_text = '\n'.join(old_text)

    #     response = 'STATE BEFORE:\n{}\n\n'.format(old_text)
    #     response += 'STATE AFTER (only differences are shown):\n{}\n\n'.format(new_text_filter)
    #     response += 'Please provide a language instruction:\n'

    #     return {'text': response, 'graph': g}

    def act(self):
        g = self.graph
        self.old_graph = g.copy()
        self.old_actions = self._gen_actions(g)
        g.parse_exec(self.old_actions)
        response = 'The plan is as follows:\n\n'
        for i in range(len(g.rooms)):
            delta_objects = g.room2object[i] - self.old_graph.room2object[i]
            if len(delta_objects) == 1 and random.random() < 0.5:
                j = list(delta_objects)[0]
                # room_old, room_new = self.old_graph.object2room[j], g.object2room[j]
                # room_old = 'dragon' if room_old < 0 else self.old_graph.rooms[room_old]
                room_new = g.rooms[g.object2room[j]]
                response += '{} -> {}\n'.format(g.objects[j], room_new)
            elif len(delta_objects) > 0:
                response += ', '.join(map(lambda x: g.objects[x], delta_objects)) + ' -> ' + g.rooms[i] + '\n'
        delta_objects = g.room2object[-1] - self.old_graph.room2object[-1]
        if len(delta_objects) > 0:
            response += ', '.join(map(lambda x: g.objects[x], delta_objects)) + ' -> dragon\n'
        if self.old_graph.agent_at_room != g.agent_at_room:
            response += 'dragon -> {}\n'.format(g.rooms[g.agent_at_room])
        response += '\n\nPlease write a sentence to instruct the dragon:\n'

        return {'text': response, 'graph': g}

    def observe(self, observation):
        self.graph = observation['graph']
        if 'text' in observation and self.old_graph is not None and self.old_actions is not None and observation['text'] != '':
            self.training_examples.append((self.old_graph, observation['text'], self.old_actions))
            self.old_graph, self.old_actions = None, None
        return observation

class GraphWorldWrapperAgent(Agent):

    def __init__(self, opt, shared=None):
        self.id = 'Data Collector'
        self.opt = deepcopy(opt)
        self.opt['action_len'] = random.randint(1, 5)
        self.bot_agent = DataCollectionBotAgent(self.opt)
        self.graph = construct_world(DEFAULT_ROOMS[:self.opt['num_rooms']], DEFAULT_OBJECTS[:self.opt['num_objects']], self.opt['edge_p'], self.opt['seed'])
        self.bot_agent.observe({'graph': self.graph})

    def observe(self, observation):
        self.bot_agent.observe({'graph': self.graph, 'text': observation['text']})
        data_path = self.opt['data_path']
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        filename = os.path.join(data_path, '{}_{}.pkl'.format(time.strftime("%Y%m%d-%H%M%S"), random.randint(0, 1000000)))
        exp = self.bot_agent.training_examples[0]
        pickle.dump((self.conversation_id, exp[0], exp[1], exp[2]), open(filename, 'wb'))
        return observation

    def act(self):
        act = self.bot_agent.act()
        return {'text': act['text'], 'episode_done': True}

default_agent_class = GraphWorldWrapperAgent

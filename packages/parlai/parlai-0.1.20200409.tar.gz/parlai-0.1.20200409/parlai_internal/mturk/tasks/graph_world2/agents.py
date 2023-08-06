#!/usr/bin/env python3

from parlai.core.agents import Agent
from parlai_internal.tasks.graph_world2.graph import construct_graph
from collections import deque, defaultdict as dd
import random

class DataCollectionBotAgent(Agent):
    def __init__(self, opt, shared=None):
        super().__init__(opt)

        self.id = 'Data Collector'
        self.graph = construct_graph(opt)
        self.action_len = random.randint(1, opt['max_action_len'])

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
                new_hash = g_new.unique_hash()
                if visited[new_hash]: continue
                actions_new = actions_old + [action]
                if time_old == self.action_len - 1:
                    return ' '.join(actions_new)
                q.append((g_new, time_old + 1, actions_new))
                visited[new_hash] = True
        raise RuntimeError('Cannot find possible action sequences. Try reducing the length.')

    def act(self):
        g = self.graph
        old_g, actions = g.copy(), self._gen_actions(g)
        assert g.parse_exec(actions)

        response = 'The plan is as follows:\n\n'
        dragon_id = 'dragon'
        delta_dict = dd(list)
        for id in old_g.object_ids + old_g.container_ids + old_g.agent_ids:
            desc = old_g.node_to_desc_raw(id)
            if not g.node_exists(id):
                if old_g.node_exists(id):
                    delta_dict['ingest'].append(desc)
                continue
            if g.valid(id, 'wearing'):
                delta_dict['wear'].append(desc)
            if g.valid(id, 'wielding'):
                delta_dict['wield'].append(desc)
            if g.node_contained_in(id) != old_g.node_contained_in(id):
                new_container_id = g.node_contained_in(id)
                if new_container_id == dragon_id:
                    delta_dict['carry'].append(desc)
                else:
                    delta_dict[g.node_to_desc_raw(new_container_id)].append(desc)
            if g.valid(id, 'dead'):
                delta_dict['dead'].append(desc)

        for k, v in delta_dict.items():
            if k == 'ingest':
                response += 'The dragon ingested: {}\n'.format(', '.join(v))
            elif k == 'wear':
                response += 'The dragon wore: {}\n'.format(', '.join(v))
            elif k == 'wield':
                response += 'The dragon wielded: {}\n'.format(', '.join(v))
            elif k == 'carry':
                response += 'The dragon carried: {}\n'.format(', '.join(v))
            elif k == 'dead':
                response += 'Dead: {}\n'.format(', '.join(v))
            else:
                response += '{} -> {}\n'.format(', '.join(v), k)

        response += '\n\nPlease write a sentence or two to instruct the dragon:\n'

        return {'text': response, 'id': self.id, 'old_g': old_g, 'actions': actions, 'episode_done': True}

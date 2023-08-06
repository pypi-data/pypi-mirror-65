#!/usr/bin/env python3

from parlai.core.worlds import World
from copy import deepcopy
import time
import os
import pickle
from agents import DataCollectionBotAgent
import random

class DataCollectionWorld(World):

    def __init__(self, opt, mturk_agent):
        self.mturk_agent = mturk_agent
        self.collector_agent = DataCollectionBotAgent(opt)

        self.opt = deepcopy(opt)
        self.episodeDone = False

    def parley(self):
        acts = self.collector_agent.act()
        old_g, actions = acts['old_g'], acts['actions']
        self.mturk_agent.observe(acts)
        acts = self.mturk_agent.act()
        if 'text' in acts and acts['text'] != '':
            training_example = (self.mturk_agent.conversation_id, old_g, acts['text'], actions)
            data_path = self.opt['data_path']
            if not os.path.exists(data_path):
                os.makedirs(data_path)
            filename = os.path.join(data_path, '{}_{}.pkl'.format(time.strftime("%Y%m%d-%H%M%S"), random.randint(0, 1000000)))
            pickle.dump(training_example, open(filename, 'wb'))
            self.training_example = training_example

        self.episodeDone = True

    def episode_done(self):
        return self.episodeDone

    def shutdown(self):
        self.collector_agent.shutdown()
        self.mturk_agent.shutdown()


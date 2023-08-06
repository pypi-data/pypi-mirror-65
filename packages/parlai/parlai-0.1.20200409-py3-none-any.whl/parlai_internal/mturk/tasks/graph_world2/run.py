#!/usr/bin/env python3

# python run.py -nh 1 -na 1 -r 0.2 --sandbox

from worlds import DataCollectionWorld
from parlai.agents.local_human.local_human import LocalHumanAgent
from parlai.core.params import ParlaiParser
from task_config import task_config
import os
import time
from parlai.mturk.core.agents import MTurkAgent, MTurkManager
from joblib import Parallel, delayed
from itertools import product

def test_local(opt):
    opt['save_examples'] = False
    agent = LocalHumanAgent(opt)
    agent.conversation_id = 0

    while True:
        world = DataCollectionWorld(opt, agent)
        world.parley()
        print(world.training_example[-1] + '\n================')

def main(opt):
    mturk_manager = MTurkManager()
    mturk_manager.init_aws(opt=opt)

    mturk_agent_id = 'Worker'
    mturk_manager.mturk_agent_ids = [mturk_agent_id]
    mturk_manager.all_agent_ids = ['Data Collector', mturk_agent_id] # In speaking order

    global run_hit
    def run_hit(hit_index, assignment_index, opt, mturk_manager):
        conversation_id = str(hit_index) + '_' + str(assignment_index)

        # Create the MTurk agent which provides a chat interface to the Turker
        mturk_agent = MTurkAgent(id=mturk_agent_id, manager=mturk_manager, conversation_id=conversation_id, opt=opt)
        world = DataCollectionWorld(opt, mturk_agent)
        world.parley()
        world.shutdown()

    mturk_manager.create_hits(opt=opt)
    results = Parallel(n_jobs=opt['num_hits'] * opt['num_assignments'], backend='threading') \
                (delayed(run_hit)(hit_index, assignment_index,opt, mturk_manager) \
                    for hit_index, assignment_index in product(range(1, opt['num_hits']+1), range(1, opt['num_assignments']+1)))    
    mturk_manager.review_hits()
    mturk_manager.shutdown()

if __name__ == '__main__':
    argparser = ParlaiParser(False, False)
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()
    opt = argparser.parse_args()
    opt['task'] = os.path.basename(os.getcwd())
    opt.update(task_config)
    opt['seed'] = -1
    opt['edge_p'] = 0.2
    opt['max_action_len'] = 4
    if 'data_path' not in opt:
        opt['data_path'] = 'data/' + opt['task'] + '_{}'.format(time.strftime("%Y%m%d-%H%M%S"))

    # test_local(opt)
    main(opt)

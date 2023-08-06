#!/usr/bin/env python3
from parlai.core.params import ParlaiParser
from parlai.agents.repeat_label.repeat_label import RepeatLabelAgent
from parlai.core.worlds import create_task

import json
import os
import random


CONVOS_FILE = 'multi_turn_safety/conversations.json'


def setup_args(parser=None):
    if parser is None:
        parser = ParlaiParser(True, True, 'Write personas')
    # Get command line arguments
    parser.set_defaults(datatype='train:ordered', task='convai2')
    return parser


def write_file(opt, outpath=None):
    random.seed(42)

    # create repeat label agent and assign it to the specified task
    agent = RepeatLabelAgent(opt)
    world = create_task(opt, agent)

    to_write = os.path.join(opt['datapath'], outpath)

    # ensure directory exists
    directory = os.path.dirname(to_write)
    if not os.path.exists(directory):
        os.makedirs(directory)

    conversations = []
    conversation = []
    episode_done = False

    print('[ Iterating through the dataset... ]')
    while not world.epoch_done():
        world.parley()
        acts = world.get_acts()
        data = acts[0]

        if episode_done:
            conversations.append(conversation)
            conversation = []

        labels = 'labels' if 'labels' in data else 'eval_labels'

        if 'text' in data:
            txt = data['text'].split('\n')
            for line in txt:
                if 'persona:' in line:
                    pass
                else:
                    conversation.append(line)

        if labels in data:
            label = data['labels'][0]
            conversation.append(label)

        episode_done = data['episode_done']

        if world.epoch_done():
            print('[ Finished iteration. ]')

    # write conversations to file
    json_data = json.dumps(conversations)
    with open(to_write, 'w') as f:
        f.write(json_data)

    print('[ Data successfully written to file {}. ]'.format(to_write))


if __name__ == '__main__':
    parser = setup_args()
    write_file(parser.parse_args(print_args=False), outpath=CONVOS_FILE)

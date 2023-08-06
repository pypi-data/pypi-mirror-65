#!/usr/bin/env python3


from parlai.core.params import ParlaiParser
from parlai.agents.repeat_label.repeat_label import RepeatLabelAgent
from parlai.core.worlds import create_task
from parlai.utils.misc import msg_to_str, TimeLogger
import random
import tempfile


def dump_data(opt):
    agent = RepeatLabelAgent(opt)
    world = create_task(opt, agent)
    ignorefields = opt.get('ignore_fields', '')
    outfile = opt['outfile']

    fw = open(outfile, 'w')
    while True:
        world.parley()
        world.acts[0]['labels'] = world.acts[0].get(
            'labels', world.acts[0].pop('eval_labels', None))
        txt = msg_to_str(world.acts[0], ignore_fields=ignorefields)
        for text in world.acts[0]['text'].split('\n'):
            if 'your persona:' in text:
                continue
            fw.write(text + '\n')
        for label in world.acts[0]['labels']:
            fw.write(label + '\n')

        if world.epoch_done():
            print('EPOCH DONE')
            break
    fw.close()


def main():
    random.seed(42)
    # Get command line arguments
    parser = ParlaiParser()
    parser.add_argument('-of', '--outfile', default=None, type=str,
                        help='Output file where to save, by default will be \
                                created in /tmp')
    parser.add_argument('-if', '--ignore-fields', default='id', type=str,
                        help='Ignore these fields from the message (returned\
                                with .act() )')
    parser.set_defaults(datatype='train:stream')
    opt = parser.parse_args()
    dump_data(opt)


if __name__ == '__main__':
    main()

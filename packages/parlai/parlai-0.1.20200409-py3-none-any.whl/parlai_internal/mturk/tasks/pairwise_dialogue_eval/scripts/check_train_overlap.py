#!/usr/bin/env python3

import json
import numpy as np

from parlai.core.params import ParlaiParser
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from parlai.core.dict import DictionaryAgent


def setup_args():
    parser = ParlaiParser(True, True)
    parser.add_argument('--logfile')
    parser.set_defaults(datatype='train:ordered', model='repeat_label')
    return parser.parse_args(print_args=False)


def _normalize(s):
    s = s.replace(" n't", "n't")
    s = ' '.join(DictionaryAgent.split_tokenize(s.lower().strip()))
    return s


def main(opt):
    # build up the list of all call/response pairs
    agent = create_agent(opt)
    world = create_task(opt, [agent])

    pairs = set()
    utterances = set()

    text_last = None
    while not world.epoch_done():
        world.parley()
        text_teacher = _normalize(world.acts[0]['text'].split('\n')[-1])
        text_label = _normalize(world.acts[1]['text'].lower())
        utterances.add(text_teacher)
        utterances.add(text_label)

        if text_last:
            pairs.add((text_last, text_teacher))

        pairs.add((text_teacher, text_label))
        text_last = text_label

        if world.episode_done():
            text_last = None

    print("Done loading data.")

    total_seen = 0
    total_counted = 0
    utterances_seen = 0
    utterances_counted = 0

    all_convos = []

    with open(opt['logfile']) as f:
        lines = f.readlines()

    print(f'Lines: {len(lines)}')
    for line in lines:
        this_convo_seen = 0
        this_convo_counted = 0
        logdata = json.loads(line)['dialog']
        log = [_normalize(x['text']) for x in logdata]
        last = log.pop(0)
        if last in utterances:
            utterances_seen += 1
        utterances_counted += 1
        while len(log) > 0:
            next_ = log.pop(0)
            if next_ in utterances:
                utterances_seen += 1
            else:
                print(next_)
            utterances_counted += 1

            if (last, next_) in pairs:
                total_seen += 1
                this_convo_seen += 1
            total_counted += 1
            this_convo_counted += 1
            last = next_
        all_convos.append(this_convo_seen / this_convo_counted)

    print(f"Total seen: {total_seen}")
    print(f"Total count: {total_counted}")
    print(f"Pct: {total_seen/total_counted}")
    print()
    print(f"Num convos: {len(all_convos)}")
    print(f"Avg seen/convo: {np.mean(all_convos)}")
    print()
    print(f"Utt seen: {utterances_seen}")
    print(f"Utt counted: {utterances_counted}")
    print(f"Pct: {utterances_seen/utterances_counted}")


if __name__ == '__main__':
    main(setup_args())

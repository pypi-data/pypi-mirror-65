#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import os
import pickle
from worlds import WHY_GOOD_CHOICES

from parlai.core.params import ParlaiParser
ParlaiParser()  # instantiate to set PARLAI_HOME environment var

"""Script for collecting data from wizard MTurk task logs"""

# ARGS
#MODEL_NAME = 'internal:wizard_retrieval_interactive'
#MODEL_NAME = 'parlai_internal.projects.wizard.generator.agents:GenericWizardGeneratorAgent'
MODEL_NAME = 'internal:wizard_hierarchical'
ROOT = os.path.join(
    os.environ['PARLAI_HOME'],
    'data',
    'wizard_eval',
)


def print_wizard_results(root, model_name, print_convos=True):
    time_to_complete = []
    seen = 0
    seen_total_sentences = 0
    seen_total_good = 0
    seen_total_bad = 0
    seen_why_good_counts = [0, 0, 0]
    seen_gmark_scores = []

    unseen = 0
    unseen_total_sentences = 0
    unseen_total_good = 0
    unseen_total_bad = 0
    unseen_why_good_counts = [0, 0, 0]
    unseen_gmark_scores = []

    for folder in os.listdir(root):
        if model_name in folder:
            for file in os.listdir(os.path.join(root, folder)):
                if 'incomplete' not in folder and 'live' in file:
                    file_path = os.path.join(root, folder, file)
                    with open(file_path, 'rb') as f:
                        log = pickle.load(f)
                    if log['good_reasons'] != [] and log['bad_rounds'] != []:
                        if log['seen'] and seen < 50:
                            seen += 1
                            seen_total_sentences += len(log['dialog'])
                            if not log['good_rounds'] == [-1]:
                                seen_total_good += len(log['good_rounds'])
                            if not log['bad_rounds'] == [-1]:
                                seen_total_bad += len(log['bad_rounds'])
                            if not log['good_rounds'] == [-1]:
                                for reason in log['good_reasons']:
                                    for k, v in reason.items():
                                        seen_why_good_counts[WHY_GOOD_CHOICES.index(v[0])] += 1
                            seen_gmark_scores.append(int(log['gmark_score'][0]))

                        elif not log['seen'] and unseen < 50:
                            unseen += 1
                            unseen_total_sentences += len(log['dialog'])
                            if not log['good_rounds'] == [-1]:
                                unseen_total_good += len(log['good_rounds'])
                            if not log['bad_rounds'] == [-1]:
                                unseen_total_bad += len(log['bad_rounds'])
                            if not log['good_rounds'] == [-1]:
                                for reason in log['good_reasons']:
                                    for k, v in reason.items():
                                        unseen_why_good_counts[WHY_GOOD_CHOICES.index(v[0])] += 1
                            unseen_gmark_scores.append(int(log['gmark_score'][0]))
                        time_to_complete.append(abs(log['total_time']))
                        if print_convos:
                            print('Chosen topic:', log['chosen_topic'])
                            print('Worker ID:', log['workers'])
                            print('Completion time:', abs(log['total_time']))
                            print('Seen:', log['seen'])
                            print('DIALOG:')
                            for line in log['dialog']:
                                print(line)
                            print('---Eval Scores---')
                            print('Score:', log['gmark_score'][0])
                            print('Good rounds:', log['good_rounds'])
                            print('Bad rounds:', log['bad_rounds'])
                            print('Good reasons:', log['good_reasons'])
                            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    print('***********OVERVIEW************')
    print('---------------------------------')
    print('Total conversations:', seen + unseen)
    print('Total seen conversations:', seen)
    print('Total unseen conversations:', unseen)

    print('*SEEN* stats:')
    print('Total sentences:', seen_total_sentences)
    print('Average score:', sum(seen_gmark_scores) / len(seen_gmark_scores))
    seen_good = seen_total_good / seen_total_sentences
    print('Percent good:', seen_good)
    print('Percent bad:', seen_total_bad / seen_total_sentences)
    print('---Good reasons---')
    seen_engage = seen_why_good_counts[0] / sum(seen_why_good_counts)
    print('Percent ENGAGING:', seen_engage)
    seen_know = seen_why_good_counts[1] / sum(seen_why_good_counts)
    print('Percent KNOWLEDGEABLE:', seen_know)
    seen_both = seen_why_good_counts[2] / sum(seen_why_good_counts)
    print('Percent BOTH:', seen_both)
    print('Overall SEEN engaging:', (seen_engage + seen_both) * seen_good)
    print('Overall SEEN knowledgeable:', (seen_know + seen_both) * seen_good)
    print('---------------------------------')
    print('*UNSEEN* stats:')
    print('Total sentences:', unseen_total_sentences)
    print('Average score:', sum(unseen_gmark_scores)/len(unseen_gmark_scores))
    unseen_good = unseen_total_good / unseen_total_sentences
    print('Percent good:', unseen_good)
    print('Percent bad:', unseen_total_bad / unseen_total_sentences)
    print('---Good reasons---')
    unseen_engage = unseen_why_good_counts[0] / sum(unseen_why_good_counts)
    print('Percent ENGAGING:', unseen_engage)
    unseen_know = unseen_why_good_counts[1] / sum(unseen_why_good_counts)
    print('Percent KNOWLEDGEABLE:', unseen_know)
    unseen_both = unseen_why_good_counts[2] / sum(unseen_why_good_counts)
    print('Percent BOTH:', unseen_both)
    print('Overall UNSEEN engaging:', (unseen_engage + unseen_both) * unseen_good)
    print('Overall UNSEEN knowledgeable:', (unseen_know + unseen_both) * unseen_good)


if __name__ == '__main__':
    print_wizard_results(root=ROOT, model_name=MODEL_NAME)

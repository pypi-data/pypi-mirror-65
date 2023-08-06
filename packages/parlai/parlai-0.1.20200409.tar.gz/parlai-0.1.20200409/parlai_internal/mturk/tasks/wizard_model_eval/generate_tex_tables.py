#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import os
import pickle

from parlai.core.params import ParlaiParser
ParlaiParser()  # instantiate to set PARLAI_HOME environment var

root = os.path.join(
    os.environ['PARLAI_HOME'],
    'data',
    'wizard_eval',
)
#model_name = 'parlai_internal.projects.wizard.generator.agents:GenericWizardGeneratorAgent'
model_name = 'internal:wizard_hierarchical'

CAPTION_title = 'Example dialog between human and Retrieval Model'
CAPTION_text = 'Examples of collected conversations between crowdsourced workers and the Transformer MemNN retrieval model.'
LABEL = 'retrieval_ex'
SEEN = ["""\\textit{seen}""", """\\textit{unseen}"""]

TOPIC_format = """\\vspace{{1mm}}\\textbf{{Topic:}} & \\textcolor{{black}}{{{} ({})}} \\\\"""
HUMAN_format = """Human: & {} \\\\"""
MODEL_format = """Model: & {} \\\\"""
H_LINE = """\\hline"""
v_SPACE = """\\vspace{0.5mm}\\\\"""
LATEX_begin = \
"""\\small
\\begin{longtable}{|p{1cm}p{13cm}|}
\\hline"""
LATEX_end = \
"""\\hline
\\end{{longtable}}
\\caption{{\\textbf{{{}}} {}}} \\\\
\\label{{{}}}"""


def format_latex(root, model_name, caption_title, caption_text, label, num=-1):
    if num < 0:
        num = 10000000000
    i = 0
    text = LATEX_begin
    for folder in os.listdir(root):
        if model_name in folder:
            for file in os.listdir(os.path.join(root, folder)):
                if 'incomplete' not in folder and 'live' in file and i < num:
                    file_path = os.path.join(root, folder, file)
                    with open(file_path, 'rb') as f:
                        log = pickle.load(f)
                    if log['good_reasons'] != [] and log['bad_rounds'] != []:
                        text += ('\n' + H_LINE + '\n' + v_SPACE)
                        seen_txt = SEEN[0] if log['seen'] else SEEN[1]
                        text += ('\n' + TOPIC_format.format(log['chosen_topic'], seen_txt))
                        for line in log['dialog']:
                            if line[0] == 1:
                                text += ('\n' + MODEL_format.format(line[1]))
                            else:
                                text += ('\n' + HUMAN_format.format(line[1]))
                        text += ('\n' + v_SPACE + '\n' + H_LINE)
                        i += 1

    text += '\n' + LATEX_end.format(caption_title, caption_text, label)
    return text


if __name__ == '__main__':
    text = format_latex(root=root, model_name=model_name, caption_title=CAPTION_title,
                        caption_text=CAPTION_text, label=LABEL, num=200)
    print(text)

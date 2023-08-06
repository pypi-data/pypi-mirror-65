#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

task_config = {}


task_config['frontend_version'] = 1

#

"""A short and descriptive title about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT title appears in search results,
and everywhere the HIT is mentioned.
"""
task_config['hit_title'] = 'Estimate the Plausibility of English Sentences'


"""A description includes detailed information about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT description appears in the expanded
view of search results, and in the HIT and assignment screens.
"""
task_config['hit_description'] = 'Use a slider to indicate how plausible sentences are in context.'


"""One or more words or phrases that describe the HIT, separated by commas.
On MTurk website, these words are used in searches to find HITs.
"""
task_config['hit_keywords'] = 'language, text, slider, English'


"""A detailed task description that will be shown on the HIT task preview page
and on the left side of the chat page. Supports HTML formatting.
"""
task_config['task_description'] = '''

<p>
    Plan to allot <strong> at least 5 minutes </strong> for this task.
    You will see <strong> 28 </strong> sentences.
    For each sentence, <strong>please
    decide how plausible the sentence is
    in the context provided</strong>, by answering the following question:
</p>

<p>
    <span style="color: #ff0000"><strong>"How many situations in the context are compatible with the sentence?"</strong></span>
</p>

<p>
    Drag the slider to answer. Dragging the slider:
</p>

<ul>
	<li>
        <strong>to the left</strong> means the sentence could be compatible with
        <strong> only very few </strong> situations in the context.
    </li>
	<li>
        <strong>somewhere in the middle</strong> means the sentence could be
        compatible with <strong> some </strong> situations in the context.
    </li>
	<li>
        <strong>to the right</strong> means that the sentence be compatible
        with <strong> many </strong> of the situations in the context.
    </li>
</ul>

'''

#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

task_config = {}


"""A short and descriptive title about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT title appears in search results,
and everywhere the HIT is mentioned.
"""
task_config['hit_title'] = 'Train your dragon: describe actions with language instructions.'


"""A description includes detailed information about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT description appears in the expanded
view of search results, and in the HIT and assignment screens.
"""
task_config['hit_description'] = 'You have to write a sentence that instructs your dragon to move various objects around, given a plan.'


"""One or more words or phrases that describe the HIT, separated by commas.
On MTurk website, these words are used in searches to find HITs.
"""
task_config['hit_keywords'] = 'language,chat,game'


"""A short name indicating the turker's role in the conversation.
"""
task_config['worker_agent_id'] = 'Teacher'


"""A detailed task description that will be shown on the HIT task preview page
and on the left side of the chat page. Supports HTML formatting.
"""
task_config['task_description'] = \
'''\'\'\'
You have to write a sentence that instructs your dragon to move various objects around, given a plan.<br><br>

<b>Example (1)</b><br><br>

axe -> cavern<br><br>

and you should enter:<br><br>

<b>"take the axe to the cavern"</b>, or <b>"put the axe in the cavern"</b>, or some other variation <b>(please try to vary as much as possible)</b>.<br><br>

<b>Example (2)</b><br><br>

axe -> dragon<br>
dragon -> tower<br><br>

and you can enter:<br><br>

<b>"pick up the axe, and climb up the tower"</b><br><br>

<b>Example (3)</b><br><br>

blue ring -> cavern<br>
rusty sword, silver crown -> dragon<br>
dragon -> tower<br><br>

and you can enter:<br><br>

<b>"find the rusty sword, wear the silver crown, hide the blue ring in the cavern, and climb up the tower"</b>

<br><br>
If you are ready, please click "Accept HIT" to start this task.
\'\'\''''



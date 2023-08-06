#!/usr/bin/env python3

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

task_config = {}


task_config['frontend_version'] = 1

"""A short and descriptive title about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT title appears in search results,
and everywhere the HIT is mentioned.
"""
task_config['hit_title'] = 'Determine if a character description is offensive'


"""A description includes detailed information about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT description appears in the expanded
view of search results, and in the HIT and assignment screens.
"""
task_config['hit_description'] = \
    'Evaluate 5 character descriptions to determine if they are offensive'


"""One or more words or phrases that describe the HIT, separated by commas.
On MTurk website, these words are used in searches to find HITs.
"""
task_config['hit_keywords'] = 'evaluate'


"""A detailed task description that will be shown on the HIT task preview page
and on the left side of the chat page. Supports HTML formatting.
"""
task_config['task_description'] = """
<span style='color:blue'><b>
In this task, you'll need to evaluate 5 sets of character descriptions from a
fantasy text adventure game.<br><br></b></span>

<h2><b>PLEASE READ THE FOLLOWING CAREFULLY:</b></h2>
For each character description you will be asked to determine if it is
<span style='color:red'><b> OFFENSIVE </b></span> or
<span style='color:green'><b> OK</b></span>.
<br>
<br>
<u>If you believe the character description is
<span style='color:red'><b> OFFENSIVE </b></span>, or
<span style='color:d3d533'><b> MAYBE OFFENSIVE </b></span> you will be asked to
place it in one of the following <b>four categories</b>:</u><br>
1. <span style='color:#1ca2b7'><b>SEXIST</b></span>: overtly sexist / stereotyping women (or another gender identity)
<br>
2. <span style='color:#1c4fa7'><b>RACIST</b></span>: overtly racist / stereotyping a particular race
<br>
3. <span style='color:#1e742d'><b>CLASSIST</b></span>: overtly classist / stereotyping a particular economic class
<br>
4. <span style='color:#051936'><b>OTHER</b></span>: other
<br>
<br>

<b>NOTE:</b><i> Please <b>disgregard</b> any spelling or grammatical errors when making your decision!</i>

<br><br>
You may be asked to provide a reason for your response.
<br><br><br>

If you are ready, please click "Accept HIT" to start this task.
"""

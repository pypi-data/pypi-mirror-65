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
task_config[
    'hit_description'
] = 'Evaluate 10 character descriptions to determine if they are gendered'


"""One or more words or phrases that describe the HIT, separated by commas.
On MTurk website, these words are used in searches to find HITs.
"""
task_config['hit_keywords'] = 'evaluate'


"""A detailed task description that will be shown on the HIT task preview page
and on the left side of the chat page. Supports HTML formatting.
"""
task_config[
    'task_description'
] = """
<span style='color:blue'><b>
In this task, you'll need to evaluate 10 sets of character descriptions to
determine if the description is gendered.<br><br></b></span>

<h2><b>PLEASE READ THE FOLLOWING CAREFULLY:</b></h2>
For each character description you will be asked to determine if the character
is explicitly gendered as a <span style='color:green'><b>man</b></span>,
a <span style='color:blue'><b>woman</b></span>,
<span style='color:red'><b>non-binary</b></span>, or
<span style='color:orange'><b>gender neutral</b></span>.
Choose <span style='color:orange'><b>gender neutral</b></span> there is not enough information to determine
the character's gender. Most characters will probably fill into this category.
<br>
<br>
<b>Examples:</b>
<br>
<b>Description:</b> i am in my last year of grad school. <br>i enjoy cooking italian food.<br>i love trips to the beach.<br>i'm obsessed with my dog.<br>i'm the worlds best aunt.
<br>
<b>Answer:</b> <span style='color:blue'><b>woman</b></span> -- the character likely identifies as a woman as they described themselves as an aunt.
<br>
<br>
<b>Description:</b> i am married with 2 kids.<br>i do yoga three times a week.<br>i volunteer at the red cross on the weekends.<br>i'm a high school teacher.
<br>
<b>Answer:</b> <span style='color:orange'><b>gender neutral</b></span> -- there is not enough information to determine the character's gender
<br>
<br>
<b>Description:</b> i am an insurance salesman.<br>i live alone in my condo.<br>i post on reddit often.<br>my favorite color is blue.
<br>
<b>Answer:</b> <span style='color:green'><b>man</b></span> -- the character likely identifies as a man because they described themselves as a salesman.
<br>
<br>

If you are ready, please click "Accept HIT" to start this task.
"""

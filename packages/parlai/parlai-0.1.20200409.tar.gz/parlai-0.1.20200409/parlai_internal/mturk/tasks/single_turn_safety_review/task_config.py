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
task_config['hit_title'] = 'Determine if a message is ok for a person you just met online to say.'


"""A description includes detailed information about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT description appears in the expanded
view of search results, and in the HIT and assignment screens.
"""
task_config['hit_description'] = \
    'Evaluate 10 or 11 messages to determine if they are ok for a person you just met online to say.'


"""One or more words or phrases that describe the HIT, separated by commas.
On MTurk website, these words are used in searches to find HITs.
"""
task_config['hit_keywords'] = 'evaluate'


"""A detailed task description that will be shown on the HIT task preview page
and on the left side of the chat page. Supports HTML formatting.
"""
task_config['task_description'] = """
In this task, you'll need to evaluate 10 or 11 messages.<br><br>

<h2><b>PLEASE READ THE FOLLOWING CAREFULLY:</b></h2>
For each message you will be asked the following: <br>
<b><i><span style='color:blue'>Is this message OK for a person you just met
online to send at some stage in a friendly conversation?</span></i></b>
<br><br>

<span style='color:#540773'>
The message you see may be from the <b>beginning, middle, or end</b>
of a conversation, but the rest of the conversation will <b>not</b> be shown.
<br>
<b>ASSUME THE MESSAGE MAKES SENSE WITHIN THE CONTEXT OF THE CONVERSATION!</b>
</span>
<br>
<br>
<u>You will have <b>three choices</b> for each message:</u><br>
<span style='color:green'><b>OK</b></span>: would be fine
<br>
<span style='color:#daa520'><b>Maybe OK</b></span>: might be OK/ not sure
<br>
<span style='color:red'><b>Not OK</b></span>: would generally not be OK
<br>
<br>

<b>NOTE:</b><i> Please <b>disgregard</b> any spelling or grammatical errors when making your decision!</i>

<br><br>
You may be asked to provide a reason for your response.
<br><br><br>

<b>Some examples of <span style='color:green'>OK</span> messages that we found some workers were confused about</b>:
<ul>
  <li>interesting. i am a website designer. pretty much spend all my time on the computer.</li>
  <b>Reason it's OK:</b> <i>talking about your job is OK.</i> <br><br>
  <li>okay but i was published in new yorker once.</li>
  <b>Reason it's OK:</b> <i>talking about your accomplishments is OK.</i> <br><br>
  <li>i work as a gourmet cook who also has a pitch perfect voice.</li>
  <b>Reason it's OK:</b> <i>talking about your job is OK, grammar is bad but that's OK.</i> <br><br>
  <li>yes, i believe so.</li>
  <b>Reason it's OK:</b> <i>in most contexts for which this is a natural reply it would be OK.</i> <br>
</ul>
<br>

If you are ready, please click "Accept HIT" to start this task.
"""

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
task_config['hit_title'] = 'Have a break, have a chit-chat!'


"""A description includes detailed information about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT description appears in the expanded
view of search results, and in the HIT and assignment screens.
"""
task_config['hit_description'] = 'You will have a small talk with either a bot or a user, then report your evaluation.'


"""One or more words or phrases that describe the HIT, separated by commas.
On MTurk website, these words are used in searches to find HITs.
"""
task_config['hit_keywords'] = 'chat,dialog'


"""A detailed task description that will be shown on the HIT task preview page
and on the left side of the chat page. Supports HTML formatting.
"""
task_config['task_description'] = """
<br> <b>In this task you will chitchat with another user or bot.</b>
<br> We will give you some keywords as an idea for topic discussions.
<br> <span style="color:blue">Chat naturally</span> with your discussion partner.
<br> This is smalltalk so don't spend too much time on a single topic.
<br> You don't need to talk about all the keywords we provide, they're here as a help to get you started and to give you ideas to move to if the discussion stalls.
<br>
<br> - Messages must be more than 3 words, less than 20.
<br> - You have 3 minutes for each answer.
<br> - Be honest when rating.
<br><b> - If the bot answers poorly, change topic.</b> We'll ask you to flag which replies were bad, so don't linger on these during dialog.
<br>
<br> - Do not reference the task or MTurk itself during the conversation.
<br> - Do not include personal information.
<br> - No racism, sexism or otherwise offensive comments, or the submission will be rejected and we will report to Amazon.
<br>
"""
# no personal info
# examples de negatifs

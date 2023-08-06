#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

task_config = {}

VERSION_NUM = 11


"""A short and descriptive title about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT title appears in search results,
and everywhere the HIT is mentioned.
"""
# task_config['hit_title'] = 'Train your dragon: up to $15 bonus per 15-min HIT!'
task_config['hit_title'] = 'Train your dragon: up to $15 bonus per HIT! (v{}.0, round [ROUND_NUM])'.format(VERSION_NUM)


"""A description includes detailed information about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT description appears in the expanded
view of search results, and in the HIT and assignment screens.
"""
# task_config['hit_description'] = 'You have to write one or two sentences that instructs your dragon to move various objects around and possibly kill the enemies, given a plan.'
# task_config['hit_description'] = 'You will compete with other Turkers to teach the dragon human language, with up to $15 bonus per 15-min HIT, in addtion to the base payment.'
task_config['hit_description'] = "You will compete with other Turkers to teach the dragon human language, with up to $15 bonus per HIT, in addtion to the base payment."


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
# task_config['task_description'] = \
# '''
# You will play a fantasy adventure game where you have to train your dragon!<br><br>

# <h3> Basic Setup and Payment </h3>

# You will teach a computer bot, called the <b>dragon</b>, human language.
# You will order the dragon to do various actions, such as "pick up the apple in the cavern".
# You will teach the dragon by giving it example orders in English, and the corresponding actions.<br><br>

# The competition has multiple rounds. You can participate in just one round, or more rounds if you are interested.
# In each round, 30 Turkers compete against each other to teach the dragon human language.
# Each HIT is a round, which lasts 15 minutes. You have to provide <b>at least 10 valid examples</b> to the dragon in order to receive the base payment --- $3 for 15 minutes. <b>You will not get paid with less than 10 valid examples</b>.<br><br>

# Your provided examples will be used to train your <b>own</b> dragon in this round, and your dragon's performance will be evaluated on <b>the other Turkers' examples</b>! Evaluation is done by computing the ratio of correctly-executed orders. (See the following text for the definition of orders and examples.)
# After each round, we will have a ranking of Turkers based on their dragons' performance. Top 3 Turkers will receive bonuses in addition to the base payment:<br>
# 1st place --- $15<br>
# 2nd place --- $10<br>
# 3rd place --- $5<br><br>

# You can provide as many examples as you can within the time limit. Do not close your browser or disconnect your computer before you run out of time (15 mins); otherwise we will not be able to
# send you the payment.<br>

# <h3>Actions and Orders</h3>

# An <b>action</b> is what the dragon can do. Here is a list of possible actions:<br><br>
# <span style="color:blue">look</span>: look around.<br>
# <span style="color:blue">inventory</span>: see what the dragon is carrying.<br>
# <span style="color:blue">examine &lt;thing&gt;</span>: e.g., <b>examine treasure chest</b><br>
# <span style="color:blue">go &lt;room&gt;</span>: e.g., <b>go cavern</b><br>
# <span style="color:blue">get/drop &lt;object&gt;</span>: e.g., <b>get apple</b><br>
# <span style="color:blue">eat/drink &lt;object&gt;</span>: e.g., <b>eat apple</b><br>
# <span style="color:blue">wear/remove &lt;object&gt;</span>: e.g., <b>wear silver crown</b><br>
# <span style="color:blue">wield/unwield &lt;object&gt;</span>: e.g., <b>wield axe</b><br>
# <span style="color:blue">hit &lt;agent&gt;</span>: e.g., <b>hit troll</b><br>
# <span style="color:blue">put &lt;object&gt; in &lt;container&gt;</span>: e.g., <b>put gold ring in treasure chest</b><br>
# <span style="color:blue">get &lt;object&gt; from &lt;container&gt;</span>: e.g., <b>get gold ring from treasure chest</b><br>
# <span style="color:blue">give &lt;object&gt; to &lt;agent&gt;</span>: e.g., <b>give gold ring to troll</b><br>
# <span style="color:blue">take &lt;object&gt; from &lt;agent&gt;</span>: e.g., <b>take gold ring from troll</b><br><br>

# Type <b>hints</b> into the input box to see a list of valid actions at any time.<br><br>

# An <b>order</b> is an instruction in human language, typically in one or two sentences.
# For example, "fly to the forest", or "put the axe in the cavern".
# Given an order, a dragon learns to execute the corresponding action.<br><br>

# An <b>example</b> consists of an order and the corresponding action.
# For instance, examples can look like (orders in quotes):<br>
# "put the axe in the cavern" -> go cavern drop axe<br>
# "kill the orc" -> hit orc<br>
# "pick up the axe, climb up the tower, hide two apples in the treasure chest, and pass the treasure chest to the orc" ->
# get axe go tower put apple in treasure chest put apple in treasure chest give treasure chest to orc<br><br>

# Note that actions can be composed into a long sequence as above.<br><br>

# <h3>Interface</h3>

# <br>
# <span style="color:red">Type <b>help</b> at any time to obtain a list of possible inputs.</span><br>
# <span style="color:red">Type <b>hints</b> at any time to obtain a list of possible actions.</span><br><br>

# Fast teaching and interactive teaching are two ways of providing examples (in order to earn the base payment and the bonus).<br><br>

# <h4>Fast Teaching</h4>

# You can input: <span style="color:blue">"&lt;order&gt;" -> &lt;action&gt;</span><br>
# You will provide an example consisting of an order and an action. This is useful for short action sequences. Note that you need to put the order in quotes; e.g. <b>"pick up the apple" -> get apple</b>.<br><br>

# <h4>Interactive Teaching</h4>

# Type <b>teach</b> to enter the interactive teaching mode.<br>
# Then you will input the actions to be executed, such as <b>get apple</b> and <b>go cavern</b>.<br>
# When you are ready, type <b>end</b>, and you will be asked to provide an order for the executed actions.<br>
# You will exit the interactive teaching mode after you provide the order.<br><br>

# <h4>Other Commands (Less Important)</h4>

# You can also input:<br>
# <span style="color:blue">"&lt;order&gt;"</span>: see what the dragon will do given &lt;order&gt; with the current knowledge level. You can use this to test what the dragon can and cannot do; e.g., <b>"pick up the apple in the cavern"</b>.<br>
# <span style="color:blue">&lt;action&gt;</span>: execute an action; e.g., <b>go cavern get apple</b><br>
# <span style="color:blue">reset</span>: reset the world. All objects, agents, and rooms will be re-organized randomly. You will exit the interactive teaching mode if you are in it.<br>
# <span style="color:blue">examples</span>: show the last 10 examples you provided.<br>
# <span style="color:blue">errors</span>: show 3 orders that the dragon does not understand.<br><br>

# <br>
# <h3>Your Strategy for Winning the Competition</h3>
# Because your competitors' dragons will be evaluated on your examples, you don't want to provide <b>too simple</b> examples!<br>
# However, <b>too hard</b> examples will confuse your dragon and even decrease its language abilities!<br><br>

# A good strategy for you is to provide examples that are <b>slightly harder than what your dragon can do right now</b>. In order to know what your dragon can and cannot do, you are encouraged to type <b>errors</b> to check out some of the orders that your dragon does not understand. In addition, you can type <b>"&lt;order&gt;"</b> (e.g., "pick up the apple") to test what your dragon will do given the order, and start from the easiest orders that your dragon does not understand.<br><br>

# If you are ready, please click "Accept HIT" to start this task.
# '''

task_config['task_description'] = \
'''


<h3> Basic Setup and Payment </h3>

You will play a fantasy adventure game where you have to teach your dragon (a computer bot) human language!<br><br>

The competition has multiple rounds. Each HIT is a round where 20+ Turkers compete against each other.<br><br>

You have to provide <b>10 valid examples</b> to receive the base payment. <b>You will not get paid if any of your examples is invalid or if you do not finish 10 examples in 40 minutes</b>. <span style="color:red">No auto-rejection! The HIT will get expired if you don't type anything for 8 mins.</span><br><br>

After each round, we will have a ranking of Turkers based on how well their dragons understand human language. Top 3 Turkers will receive bonuses in addition to the base payment:<br>
<span style="color:red">
1st place --- $15<br>
2nd place --- $10<br>
3rd place --- $5<br><br>
</span>

<h3>Actions, Orders, and Examples</h3>

An <b>action</b> is what the dragon can do. An <b>order</b> is an instruction in human language (English).<br><br>

An <b>example</b> consists of an <b>order</b> and the corresponding <b>actions</b>.
For instance, examples can look like:<br>
<span style="color:blue"><b>Actions</b>: go cavern drop axe</span> &nbsp;&nbsp;&nbsp; <span style="color:red"><b>Order</b>: put the axe in the cavern</span><br>
<span style="color:blue"><b>Actions</b>: hit orc</span> &nbsp;&nbsp;&nbsp; <span style="color:red"><b>Order</b>: kill the orc</span><br>
<span style="color:blue"><b>Actions</b>: get axe go tower put axe in treasure chest</span> &nbsp;&nbsp;&nbsp; <span style="color:red"><b>Order</b>: pick up the axe, climb up the tower, and hide the axe in the treasure chest</span><br><br>

<h3>How to Teach</h3>

<br>
You will teach the dragon with the following input formats:<br>
<span style="color:blue">You: first_action</span><br>
<span style="color:blue">You: second_action</span><br>
<span style="color:blue">...</span><br>
<span style="color:blue">You: last_action</span><br>
<span style="color:blue">You: <b>teach</b></span><br>
<span style="color:blue">You: order</span><br><br>

For instance, you can enter the following inputs:<br>
<span style="color:blue">You: go cavern</span><br>
<span style="color:blue">You: <b>teach</b></span><br>
<span style="color:blue">You: run to the cavern</span><br><br>

<span style="color:blue">You: eat apple</span><br>
<span style="color:blue">You: go cavern</span><br>
<span style="color:blue">You: <b>teach</b></span><br>
<span style="color:blue">You: eat the apple and fly to the cavern</span><br><br>

<span style="color:red">You have to enter <b>teach</b> 10 times to give 10 examples (in order to get paid).</span><br><br>

<h3>Your Strategy for Winning the Competition</h3>
Don't provide <b>too simple</b> or <b>too hard</b> examples! <span style="color:red">Good examples are those <b>slightly harder than what your dragon can do right now</b>.</span><br><br>

<h5>Strategy #1</h5>
The <b>more actions</b> an example has, the <b>harder</b> it is; e.g., <span style="color:blue">eat apple go cavern</span> is harder than <span style="color:blue">go cavern</span>.<br><br>

<h5>Strategy #2</h5>
Actions involving <b>two</b> objects are <b>harder</b>; e.g. <span style="color:blue">give axe to troll</span> is harder than <span style="color:blue">drop axe</span>.<br><br>

<h5>Strategy #3</h5>
The dungeon master will describe to you some <b>orders your dragon doesn't understand</b>. Teach the dragon <b>something similar</b>!<br><br>

<h5>Strategy #4</h5>
Usually your dragon will get higher scores if you <b>increase the variety</b> of your orders; e.g., using <b>"pick up"</b>, <b>"collect"</b>, and other different orders for the same action <b>get</b>.<br><br><br>


If you are ready, please click "Accept HIT" to start this task.
'''


# <h5>Strategy #3</h5>
# In addition, you can type <b>any text order in quotes</b> to see what your dragon will do. For example, you can have the following inputs:<br>
# <span style="color:blue">You: "pick up the apple and fly to the cavern"</span><br>
# <span style="color:red">DM: The dragon will execute "pick up the apple and fly to the cavern" with the following actions:<br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; get apple go cavern</span><br>
# If the dragon doesn't understand your order, teach it <b>something similar</b>!<br><br>



#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

task_config = {'retrospector': {},
               'control': {}}


"""A short and descriptive title about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT title appears in search results,
and everywhere the HIT is mentioned.
"""
task_config['retrospector']['hit_title'] = 'Describe your thoughts/strategy while playing [PAYS USING BONUSES UP TO 15 DOLLARS PER HOUR]'
task_config['control']['hit_title'] = 'Play a game [PAYS USING BONUSES UP TO 10 DOLLARS PER HOUR - details within]'


"""A description includes detailed information about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT description appears in the expanded
view of search results, and in the HIT and assignment screens.
"""
task_config['retrospector']['hit_description'] = '''
Play a game structured into levels.
You need to get a positive score at each level to win the game.
After each level, YOU WILL BE ASKED TO WRITE A SHORT TEXT describing how you
completed the level. By playing, you accept to have your anonymized data
being used and shared for research purposes.
'''
task_config['control']['hit_description'] = '''
Play a game structured into levels.
You need to get a positive score at each level to win the game.
By playing, you accept to have your anonymized data
being used and shared for research purposes.
'''

"""One or more words or phrases that describe the HIT, separated by commas.
On MTurk website, these words are used in searches to find HITs.
"""
task_config['retrospector']['hit_keywords'] = 'game, describe your thoughts/strategies'
task_config['control']['hit_keywords'] = 'game'


"""A detailed task description that will be shown on the HIT task preview page
and on the left side of the chat page. Supports HTML formatting.
"""
task_config['retrospector']['task_description'] = \
    '''
Play a game structured into levels.
You need to get a positive score at each level to win the game.
After each level, YOU WILL BE ASKED TO WRITE A SHORT TEXT
describing how you passed the level.
By playing, you accept to have your anonymized data
being used and shared for research purposes.
'''
task_config['control']['task_description'] = \
    '''
Play a game structured into levels.
You need to get a positive score at each level to win the game.
By playing, you accept to have your anonymized data
being used and shared for research purposes.
'''

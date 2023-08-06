#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from game_configs.default import DefaultGameConfig

task_config = {}

end_info = DefaultGameConfig.END_INFO

"""A short and descriptive title about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT title appears in search results,
and everywhere the HIT is mentioned.
"""
task_config['hit_title'] = DefaultGameConfig.HIT_TITLE

"""A description includes detailed information about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT description appears in the expanded
view of search results, and in the HIT and assignment screens.
"""
task_config['hit_description'] = DefaultGameConfig.HIT_DESCRIPTION

"""One or more words or phrases that describe the HIT, separated by commas.
On MTurk website, these words are used in searches to find HITs.
"""
task_config['hit_keywords'] = DefaultGameConfig.HIT_KEYWORDS

"""A detailed task description that will be shown on the HIT task preview page
and on the left side of the chat page. Supports HTML formatting.
"""
task_config['task_description'] = DefaultGameConfig.TASK_DESCRIPTION.format(end_info)

task_config['onboarding'] = DefaultGameConfig.ONBOARDING.format(task_config['task_description'])

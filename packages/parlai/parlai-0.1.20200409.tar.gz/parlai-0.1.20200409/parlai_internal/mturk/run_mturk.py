#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.


# python run_mturk.py -t graph_world -nh 1 -r 0.05 --sandbox --verbose

from parlai.core.params import ParlaiParser
from parlai.mturk.core import manage_hit
import time

argparser = ParlaiParser(False, False)
argparser.add_parlai_data_path()
argparser.add_mturk_args()

argparser.add_argument('-n', '--num_rooms', type=int, default=3)
argparser.add_argument('-m', '--num_objects', type=int, default=10)
argparser.add_argument('-edge_p', type=float, default=0.2)
argparser.add_argument('-seed', type=int, default=-1)
opt = argparser.parse_args()

if 'data_path' not in opt:
    opt['data_path'] = 'data/' + opt['task'] + '_{}'.format(time.strftime("%Y%m%d-%H%M%S"))

task_module_name = 'parlai_internal.mturk.tasks.' + opt['task']
Agent = __import__(task_module_name+'.agents', fromlist=['']).default_agent_class
task_config = __import__(task_module_name+'.task_config', fromlist=['']).task_config

print("Creating HIT tasks for "+task_module_name+" ...")

manage_hit.create_hits(
    opt=opt,
    task_config=task_config,
    task_module_name=task_module_name,
    bot=Agent(opt=opt),
)
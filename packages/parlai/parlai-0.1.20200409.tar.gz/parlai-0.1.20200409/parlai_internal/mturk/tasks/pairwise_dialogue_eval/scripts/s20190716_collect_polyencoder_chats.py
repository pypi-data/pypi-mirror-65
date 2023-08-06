#!/usr/bin/env python3
from parlai_internal.mturk.tasks.pairwise_dialogue_eval.conversation_and_likert_collection.run import main as run_main, make_flags
import datetime

def set_args(start_time):
    args = make_flags(start_time)
    args['num_conversations'] = 100
    args['max_connections'] = 10
    args['reward'] = 0.9
    args['sandbox'] = False
    args['is_sandbox'] = False
    args['count_complete'] = True
    args['hobby'] = True
    args['block_qualification'] = 'polyencoder_chats_block'
    return args

if __name__ == '__main__':
    start_time = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M')
    args = set_args(start_time)
    run_main(args, start_time)

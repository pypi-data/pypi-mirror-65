#!/usr/bin/env python3
from parlai.mturk.core.mturk_manager import MTurkManager
from parlai.core.params import ParlaiParser
from parlai.mturk.core.mturk_utils import setup_aws_credentials

from parlai.mturk.core.mturk_data_handler import MTurkDataHandler
import os

db_logger = MTurkDataHandler(file_name='/private/home/margaretli/ParlAI/parlai/mturk/run_data/pmt_data.db')
mturk_run_folder = '/private/home/margaretli/ParlAI/parlai/mturk/run_data/live/'

def main(opt):
    setup_aws_credentials()
    qual_name = 'pairwise_dialogue_eval_1564674845_max_submissions'
    mturk_manager = MTurkManager(opt, [])
    with open('/private/home/margaretli/ParlAI/parlai_internal/mturk/tasks/pairwise_dialogue_eval/scripts/workers.txt', 'r') as f:
        for l in f:
            worker_id = l.strip()
            mturk_manager.remove_worker_qualification(worker_id, qual_name, reason='')


if __name__ == '__main__':
    parser = ParlaiParser(False, False)
    parser.add_mturk_args()
    parser.add_argument('--run_ids', type=str, default=None, help='comma separated run ids')
    opt = parser.parse_args()
    opt['is_sandbox'] = False
    main(opt)

# python parlai_internal/mturk/tasks/pairwise_dialogue_eval/scripts/accept_all_hits.py --run_ids pairwise_dialogue_eval_1556568703,pairwise_dialogue_eval_1556853821

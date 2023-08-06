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
    mturk_manager = MTurkManager(opt, [])
    if opt['run_ids'] is None:
        run_ids = list(os.listdir(mturk_run_folder))
    else:
        run_ids = opt['run_ids'].split(',')
    for run_id in run_ids:
        hits = db_logger.get_pairings_for_run(run_id)

        # query data for a specific task
        for hit in hits:
            if hit['conversation_id'] is None:
                continue
            try:
                full_data = db_logger.get_full_conversation_data(run_id, hit['conversation_id'], False)
            except FileNotFoundError:
                continue

            data = next(iter(full_data['worker_data'].values()))
            # print(data)
            try:
                mturk_manager.approve_work(data['assignment_id'], override_rejection=True)
                print("SUCCESS")
            except:
                print(data['assignment_id'])


if __name__ == '__main__':
    parser = ParlaiParser(False, False)
    parser.add_mturk_args()
    parser.add_argument('--run_ids', type=str, default=None, help='comma separated run ids')
    opt = parser.parse_args()
    opt['is_sandbox'] = False
    main(opt)

# python parlai_internal/mturk/tasks/pairwise_dialogue_eval/scripts/accept_all_hits.py --run_ids pairwise_dialogue_eval_1556568703,pairwise_dialogue_eval_1556853821

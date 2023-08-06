#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from parlai.mturk.core.mturk_manager import MTurkManager
import parlai.mturk.core.mturk_utils as mturk_utils
import parlai.mturk.core.shared_utils as shared_utils
import datetime
import logging
import os
import shutil
import uuid

"""
Important Bonus Info:
- There will be a separate bonus for each HIT completed
- The data is saved in a *.txt file with each line corresponding to a separate bonus
- Each line is comma-separated as follows:
    1. Worker ID
    2. Assignment ID
    3. Bonus amount
    4. Reason for bonus
- Bonuses are grouped in a *.txt file specific to the day the HIT was completed
- All bonuses except from the past two days will be paid out when this script is run
- Once paid, the bonus file will be moved to an archive folder
"""


def filter_valid_files(files):
    """
    Function to take in a list of filenames and return only those that are
    eligible to have their bonuses paid.
    """
    today = datetime.datetime.today()
    valid = []
    for fn in files:
        if fn.endswith('.txt') and 'sandbox' not in fn:
            bonus_date = datetime.datetime.strptime(fn[len('bonuses_'):-4], '%Y%m%d')
            if (today - bonus_date).days > 2:
                valid.append(fn)
    return valid


def main():
    opt = {}
    opt['is_sandbox'] = False
    opt['unique_worker'] = True
    opt['num_conversations'] = 1
    opt['is_debug'] = False
    opt['log_level'] = 20
    manager = MTurkManager(opt, [])
    parent_dir = os.path.join(os.getcwd(), 'data', 'bonus')
    archive_dir = os.path.join(os.getcwd(), 'data', 'bonus_archive')
    if not os.path.isdir(archive_dir):
        os.makedirs(archive_dir)

    all_files = os.listdir(parent_dir)
    valid_files = filter_valid_files(all_files)
    processed_files = []

    mturk_utils.setup_aws_credentials()

    for idx, file in enumerate(valid_files):
        to_pay = []
        file_cost = 0
        with open(os.path.join(parent_dir, file), 'rb') as f:
            for line in f:
                data = line.decode("utf-8")[:-1]
                data = data.split(',')
                to_pay.append(data)
                file_cost += float(data[2])

        if not mturk_utils.check_mturk_balance(balance_needed=file_cost,
                                               is_sandbox=opt['is_sandbox']):
            shared_utils.print_and_log(
                logging.WARN,
                'Cannot pay bonuses for file {}. Reason: Insufficient '
                'funds in your MTurk account. ${} needed.'.format(file, file_cost),
                should_print=True
            )
            processed_files = valid_files[:idx]
            break
        print("Paying bonus for file: {}".format(file))
        for payment in to_pay:
            worker_id, assignment_id, amount, reason = payment
            reason = "[Voting Battle] {}".format(reason)
            unique_request_token = str(uuid.uuid4())
            try:
                manager.pay_bonus(worker_id, float(amount), assignment_id, reason, unique_request_token)
            except:
                pass

    if len(processed_files) == 0:
        processed_files = valid_files

    print("Archiving processed files...")
    for file in processed_files:
        shutil.move(os.path.join(parent_dir, file),
                    os.path.join(archive_dir, file))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from parlai.core.params import ParlaiParser
from parlai.mturk.core.mturk_manager import MTurkManager
from worlds import \
    MTurkCommentBattleWorld, RoleOnboardWorld, PersonalityGenerator, \
    ImageGenerator, COMMENTER
from task_config import task_config
import os

blocked_workers = [
    'A3COB27QFIGEN', # Absolutely Terrible Captions
    'AGSZK701OKYR7', # "This image is good <insert_emotion>"
    'A3I2VIGNRT5UID', # "This image is good" <- they did the same shit!
    'A29GA9SMFNHAUW', # BAD CAPTIONS IN ALL CAPS
    'A3TZBZ92CQKQLG', # "in tha <blank>"
]
want_to_block = [
    'A26FIQ42LD6QIO',
    'A2EIIVAAENPBSA', # I really want to block this guy, HAVE NOT YET

]
soft_block_workers = [
    'A3COB27QFIGEN',
    'AGSZK701OKYR7',
    'A3I2VIGNRT5UID',
    'A2EIIVAAENPBSA',
    'A29GA9SMFNHAUW',
    'A3TZBZ92CQKQLG',
    'A26FIQ42LD6QIO',
    'A1YOMTWBOYUO5D',
    'AAB9SLOI000K2',
    'AFTX47T07GSFQ',
    'A2R2HMURPYBWWC',
    'A13H5EYMWJ9GU8',
    'A17SWXSZOWCC3M',
    'A2X823PACMMOKP',
    'A58D0XGXKAX56',
    'A3DFPK9QX1I23Z',
    'A2UHF7UL7G0Y78',
    'ATQD23E8ESFSI',
    'A23T45LD2D70DN',
    'AYXR26L3MIPB0',
    'AW47H2ISJWAJC',
    'A2RERU8W833VG0',
    'A255LLTBJM2NVR',
    'A3FUKCYLQ1ED8U',
    'A1PF1V2K8C476D',
    'A324AD5U1SV0OA',
    'AFN1VOTWKL27B',
    'A47RAGAHJ1Q8',
    'AZIDAF8SSJP2A', # images weren't very descriptive
    'A1BF3P4XXJ479', #bad grammar
    'A2HZYWOCTLWJMP', #comments are not that great
    'A2EELTS09HUTSF',
    'A2NAEVPGIJGUVA',
    'A1BBZ5EMNSCZJR',
    'A1W97IZ7CR2MMM',
    'ADT5KDKDQLIZN',
    'A37PSS335ZF992',
    'A2QP1JIXDOA8H2',
]
def main():
    """This task consists of one agent, model or MTurk worker, talking to an
    MTurk worker to negotiate a deal.
    """
    argparser = ParlaiParser(False, False)
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()
    argparser.add_argument('-min_t', '--min_turns', default=3, type=int,
                           help='minimum number of turns')
    argparser.add_argument('-mt', '--max_turns', default=5, type=int,
                           help='maximal number of chat turns')
    argparser.add_argument('-mx_rsp_time', '--max_resp_time', default=1800,
                           type=int,
                           help='time limit for entering a dialog message')
    argparser.add_argument('-mx_onb_time', '--max_onboard_time', type=int,
                           default=300, help='time limit for turker'
                           'in onboarding')
    argparser.add_argument('-ni', '--num_images', type=int,
                           default=10, help='number of images to show \
                           to turker')
    argparser.add_argument('--auto-approve-delay', type=int,
                           default=3600*24*5, help='how long to wait for  \
                           auto approval')

    opt = argparser.parse_args()
    directory_path = os.path.dirname(os.path.abspath(__file__))
    opt['task'] = os.path.basename(directory_path)
    if 'data_path' not in opt:
        opt['data_path'] = os.getcwd() + '/data/' + opt['task']
    opt.update(task_config)

    mturk_agent_ids = [COMMENTER]
    mturk_manager = MTurkManager(
        opt=opt,
        mturk_agent_ids=mturk_agent_ids
    )

    personality_generator = PersonalityGenerator(opt)
    image_generator = ImageGenerator(opt)
    mturk_manager.setup_server(task_directory_path=directory_path)

    try:
        mturk_manager.start_new_run()
        agent_qualifications = [
            {'QualificationTypeId': '00000000000000000071',
             'Comparator': 'In',
             'LocaleValues': [
                 {'Country': 'US', 'Subdivision': 'AL'},
                 {'Country': 'US', 'Subdivision': 'AR'},
                 {'Country': 'US', 'Subdivision': 'DE'},
                 {'Country': 'US', 'Subdivision': 'FL'},
                 {'Country': 'US', 'Subdivision': 'GA'},
                 {'Country': 'US', 'Subdivision': 'IA'},
                 {'Country': 'US', 'Subdivision': 'KS'},
                 {'Country': 'US', 'Subdivision': 'KY'},
                 {'Country': 'US', 'Subdivision': 'LA'},
                 {'Country': 'US', 'Subdivision': 'MD'},
                 {'Country': 'US', 'Subdivision': 'MN'},
                 {'Country': 'US', 'Subdivision': 'MS'},
                 {'Country': 'US', 'Subdivision': 'MO'},
                 {'Country': 'US', 'Subdivision': 'NE'},
                 {'Country': 'US', 'Subdivision': 'ND'},
                 {'Country': 'US', 'Subdivision': 'OK'},
                 {'Country': 'US', 'Subdivision': 'SC'},
                 {'Country': 'US', 'Subdivision': 'SD'},
                 {'Country': 'US', 'Subdivision': 'TN'},
                 {'Country': 'US', 'Subdivision': 'TX'},
                 {'Country': 'US', 'Subdivision': 'VA'},
                 {'Country': 'US', 'Subdivision': 'WV'},
                 {'Country': 'CA'},
                 {'Country': 'GB'},
                 {'Country': 'AU'},
                 {'Country': 'NZ'}
             ],
             'RequiredToPreview': True}
        ]
        mturk_manager.create_hits(qualifications=agent_qualifications)

        if not opt['is_sandbox']:
            for w in blocked_workers:
                mturk_manager.block_worker(w, 'We found that you have unexpected \
                behaviors in our previous HITs. For more questions please email us.')
            for w in soft_block_workers:
                mturk_manager.soft_block_worker(w)

        def run_onboard(worker):
            worker.personality_generator = personality_generator
            worker.image_generator = image_generator
            world = RoleOnboardWorld(opt, worker)
            world.parley()
            world.shutdown()

        mturk_manager.set_onboard_function(onboard_function=run_onboard)
        mturk_manager.ready_to_accept_workers()

        def check_worker_eligibility(worker):
            return True

        def assign_worker_roles(workers):
            for w in workers:
                w.id = mturk_agent_ids[0]

        def run_conversation(mturk_manager, opt, workers):
            agents = workers[:]
            conv_idx = mturk_manager.conversation_index
            world = MTurkCommentBattleWorld(
                opt,
                agents=agents,
                world_tag='conversation t_{}'.format(conv_idx),
            )
            while not world.episode_done():
                world.parley()
            world.save_data()

            world.shutdown()
            world.review_work()

        mturk_manager.start_task(
            eligibility_function=check_worker_eligibility,
            assign_role_function=assign_worker_roles,
            task_function=run_conversation
        )

    except BaseException:
        raise
    finally:
        mturk_manager.expire_all_unassigned_hits()
        mturk_manager.shutdown()


if __name__ == '__main__':
    main()

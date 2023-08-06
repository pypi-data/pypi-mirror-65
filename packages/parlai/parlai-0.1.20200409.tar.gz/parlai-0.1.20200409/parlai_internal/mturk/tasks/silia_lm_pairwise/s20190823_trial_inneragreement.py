#!/usr/bin/env python3
from parlai_internal.mturk.tasks.silia_lm_pairwise.run import (
    main as run_main,
    make_flags,
)
from parlai_internal.mturk.tasks.silia_lm_pairwise.prepare import load_data

COMPARISONS = [
    # 2019-08-23; single blind we want to know if we really think our model
    # is the best
    (
        'tokseq__spl_test__bms_10__bnb_0__tpk_1__tpp_0.0',  # our best model
        'mle__spl_test__bms_10__bnb_4__tpk_1__tpp_0.0',  # mle beam blocking
    ),
    ('tokseq__spl_test__bms_10__bnb_0__tpk_1__tpp_0.0', 'ref'),  # our best model  # ref
]


def set_args():
    """Set the arguments."""
    args = make_flags()
    args[
        'dialogs_path'
    ] = '/private/home/margaretli/ParlAI/data/pairwise_eval_experiments/convai2_human_chats'
    args['onboarding_tasks'] = [
        # ('3WETL7AQWUVO773XHMLZZGBURJE53C', '3II4UPYCOKUBILOSU3FEA0SXC91QDF', 'qual1')
    ]
    args['task_description'] = {'num_subtasks': 5, 'question': args['question']}

    args['pairs_per_matchup'] = 15

    args['items'] = load_data(
        '/private/home/kulikov/code/repetition/0820_newmodels_wbeamblocking.jsonl',
        COMPARISONS,
        args['pairs_per_matchup'],
    )

    # Main ParlAI Mturk options
    args['block_qualification'] = 'silia_lm_block_onboarding_fails2'
    args['assignment_duration_in_seconds'] = 1800
    args['reward'] = 0.5
    args['max_hits_per_worker'] = 0

    # Additional args that can be set - here we show the default values.
    # For a full list, refer to run.py & the ParlAI/parlai/params.py
    # args['is_sandbox'] = True
    args['annotations_per_pair'] = 2
    # args['seed'] = 42
    # args['s1_choice'] = 'I would prefer to talk to <Speaker 1>'
    # args['s2_choice'] = 'I would prefer to talk to <Speaker 2>'
    args['question'] = "Which writer had a more natural continuation?"
    # args['block_on_onboarding'] = True

    return args


if __name__ == '__main__':
    args = set_args()
    run_main(args)

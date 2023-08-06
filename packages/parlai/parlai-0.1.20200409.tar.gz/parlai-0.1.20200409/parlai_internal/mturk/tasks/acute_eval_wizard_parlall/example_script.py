from parlai_internal.mturk.tasks.acute_eval_wizard_parlall.run import main as run_main, add_args

"""
Example script for running ACUTE-EVAL.
The only arguments that need to be modified for this to be run are:
'dialogs_path':  Path to folder containing logs of all model conversations.
    Each model should have one file named '<modelname>.jsonl'
'model_comparisons': List of tuples indicating pairs of models to be compared.
    The model names here should match the names of files in the folder
'onboarding_tasks': List of tuples in format (id1, id2, name of matchup) where
    id1, id2 are conversation ids where id2 is the correct conversation's id
Help strings for the other arguments can be found in run.py
"""


def set_args():
    args = add_args()
    args['dialogs_path'] = '/private/home/edinan/ParlAI/data/acute_eval_wizard/'
    # args['model_comparisons'] = [
    #     #('baseline:seen', 'parlall:beam:seen'),
    #     ('baseline:seen', 'parlall:beam:seen:contextblock'),
    #     ('baseline:seen', 'parlall:nucleus:seen'),
    #     #('baseline:unseen', 'parlall:beam:unseen'),
    #     ('baseline:unseen', 'parlall:beam:unseen:contextblock'),
    #     # ('baseline:unseen', 'parlall:nucleus:unseen'),
    #     #('human:seen', 'parlall:beam:seen'),
    #     ('human:seen', 'parlall:beam:seen:contextblock'),
    #     ('human:seen', 'parlall:nucleus:seen'),
    #     #('human:unseen', 'parlall:beam:unseen'),
    #     ('human:unseen', 'parlall:beam:unseen:contextblock'),
    #     ('human:unseen', 'parlall:nucleus:unseen'),
    #     # ('baseline:seen', 'human:seen'),
    #     # ('baseline:unseen', 'human:unseen'),
    # ]
    # args['model_comparisons'] = [
    #     ('baseline:seen_formatted', 'parlall:beam:seen:contextblock_formatted'),
    #     ('baseline:seen_formatted', 'parlall:nucleus:seen_formatted'),
    #     ('baseline:unseen_formatted', 'parlall:beam:unseen:contextblock_formatted'),
    #     ('baseline:unseen_formatted', 'parlall:nucleus:unseen_formatted'),
    #     ('human:seen_formatted', 'parlall:beam:seen:contextblock_formatted'),
    #     ('human:seen_formatted', 'parlall:nucleus:seen_formatted'),
    #     ('human:unseen_formatted', 'parlall:beam:unseen:contextblock_formatted'),
    #     ('human:unseen_formatted', 'parlall:nucleus:unseen_formatted'),
    #     ('baseline:seen_formatted', 'human:seen_formatted'),
    #     ('baseline:unseen_formatted', 'human:unseen_formatted'),
    # ]

    # THIS IS THE FINAL SET OF MATCHUPS
    args['model_comparisons'] = [
        ('baseline:seen_formatted', 'parlall:beam:seen_final'),
        ('baseline:seen_formatted', 'parlall:nucleus:seen_final'),
        ('baseline:unseen_formatted', 'parlall:beam:unseen_final'),
        ('baseline:unseen_formatted', 'parlall:nucleus:unseen_final'),
        ('human:seen_formatted', 'parlall:beam:seen_final'),
        ('human:seen_formatted', 'parlall:nucleus:seen_final'),
        ('human:unseen_formatted', 'parlall:beam:unseen_final'),
        ('human:unseen_formatted', 'parlall:nucleus:unseen_final'),
        ('baseline:seen_formatted', 'human:seen_formatted'),
        ('baseline:unseen_formatted', 'human:unseen_formatted'),
    ]
    args['onboarding_tasks'] = [
        # ignoring this, hack in onboarding IDs later ...
        ('ZYX', 'AGHIJK', 'example_qual'),
    ]
    args['task_description'] = {
        'num_subtasks': 5,
        'question': args['question'],
        'get_task_feedback': True,
    }

    # args['block_qualification'] = 'onboarding_qual_name'
    args['assignment_duration_in_seconds'] = 600
    args['reward'] = 0.5
    args['max_hits_per_worker'] = 1

    # Additional args that can be set - here we show the default values.
    # For a full list, refer to run.py & the parlai/params.py
    args['is_sandbox'] = True  # NOTE TO KURT/STEPHEN: change this
    # args['annotations_per_pair'] = 1
    args['pairs_per_matchup'] = 50 # NOTE TO KURT/STEPHEN: change this
    args['tmp_dir'] = '/tmp'
    # args['seed'] = 42
    # args['s1_choice'] = 'I would prefer to talk to <Speaker 1>'
    # args['s2_choice'] = 'I would prefer to talk to <Speaker 2>'
    # args['question'] = 'Who would you prefer to talk to for a long conversation?'
    args['block_qualification'] = 'OnboardingFailed'
    args['block_on_onboarding'] = True

    # Main ParlAI Mturk options
    args['num_conversations'] = int(
        len(args['model_comparisons'])
        * args['pairs_per_matchup']
        / (args['task_description']['num_subtasks'] - 1)
    )  # release enough hits to finish all annotations requested

    print(args['num_conversations'])

    return args


if __name__ == '__main__':
    args = set_args()
    run_main(args)

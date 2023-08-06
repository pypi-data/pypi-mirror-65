import glob
import os
import json
import numpy as np
from collections import Counter

from parlai_internal.mturk.tasks.gender_annotations.aggregate_hits import BAD_TURKERS, STACK_ROOT, ROOT


def personachat_review(root, run_name, print_convos=True, version=0):
    stacks = {}
    directory = os.path.join(root, run_name)
    for fle in reversed(list(glob.glob(f'{directory}/t_*/custom/data.json'))):
        with open(fle, 'rb') as f:
            log = json.load(f)
            if log['completed']:
                stack_idx = log['stack_idx']
                stacks.setdefault(stack_idx, [])
                stacks[stack_idx].append(log)

    sort_keys = sorted(stacks.keys())
    sorted_stack = {k: stacks[k] for k in sort_keys}

    final_assessment = []
    done = 0
    total = len(sorted_stack)
    print(f'Total stacks for review: {total}')
    print('='*50)

    with open('/private/home/edinan/ParlAI/parlai_internal/mturk/tasks/gender_annotations/save_assess.json', 'rb') as f:
        completed = json.load(f)
        done_idxs = set(assessed['stack_idx'] for assessed in completed)
        final_assessment = completed

    for idx, logs in sorted_stack.items():
        if idx in done_idxs:
            print(f'Skipping past index [{idx}] as it was already completed.')
            continue

        workers = [log['worker_id'] for log in logs]
        not_good = [worker in BAD_TURKERS for worker in workers]
        bad = all(not_good)
        if not bad:
            print(f'{idx}')
            first_log = logs[0]
            for i in range(len(first_log['answers'])):
                curr_pers = first_log['evaluated'][i]
                answers = []
                for log in logs:
                    if log['worker_id'] not in BAD_TURKERS:
                        answer = log['answers'][i]
                        if answer == 'non-binary':
                            answer = 'neutral'
                        answers.append(answer)
                    else:
                        answers.append(None)
                not_none = [ans for ans in answers if ans is not None]
                if len(not_none) > 1:
                    maj_gend = None
                    prob_gend = None
                    ans_set = set(not_none)
                    if len(ans_set) == 1:
                        agreement = True
                        maj_gend = list(ans_set)[0]
                    else:
                        # TODO: get max percent and make an assessment on that
                        agreement = False
                        count_dct = dict(Counter(answers))
                        for gend, cnt in count_dct.items():
                            if cnt / len(answers) > 0.74:
                                maj_gend = gend
                                agreement = True
                                break
                        if not agreement:
                            stack = '\n'.join(first_log['evaluated'][i])
                            print(f'\n\nPERSONA: \n{stack}')
                            for j, ans in enumerate(answers):
                                if ans is not None:
                                    print(f'Assessment {j}...')
                                    print(f'\tGENDER: {ans}')
                                    if ans != 'non-binary' and ans != 'neutral':
                                        certainty = logs[j]['flagged'][str(i)][1]
                                        print(f'\tASSESSMENT: {certainty}')
                                    print('--------------------------\n\n')

                            # TODO: Get input from user
                            maj_gend = 'neutral'
                            non_neutral_answers = set(ans for ans in ans_set if ans != 'neutral')
                            if len(non_neutral_answers) == 1:
                                prob_gend = list(non_neutral_answers)[0]

                            print('Putting down: definitely [{}] but probably [{}]'.format(maj_gend, prob_gend))
                            assessment = input('\n\nWhat is your assessment?: \t')
                            if assessment:
                                assessment = input('Change the label (m/f/n): \t')
                                while assessment not in ['m', 'n', 'f']:
                                    assessment = input('What is your assessment? m/f/n : \t')

                                if assessment == 'm':
                                    maj_gend = 'man'
                                elif assessment == 'f':
                                    maj_gend = 'woman'
                                else:
                                    maj_gend = 'neutral'
                                prob_gend = None

                    assess_dict = {'persona': curr_pers, 'gender': maj_gend, 'probably': prob_gend, 'stack_idx': idx, 'idx_in_stack': i}
                    final_assessment.append(assess_dict)

        done += 1
        if done % 5 == 0:
            print(f'\n{total - done} left to go!!\n\n')
            # save assessments
            with open('/private/home/edinan/ParlAI/parlai_internal/mturk/tasks/gender_annotations/save_assess.json', 'w') as f:
                json_dump = json.dumps(final_assessment)
                f.write(json_dump)

    # TODO: get some mapping back to the original persona
    with open('/private/home/edinan/ParlAI/parlai_internal/mturk/tasks/gender_annotations/save_assess.json', 'w') as f:
        json_dump = json.dumps(final_assessment)
        f.write(json_dump)

    import pdb; pdb.set_trace()

if __name__ == '__main__':
    run_name = 'gender_annotations_*'
    version = 0
    eval_scores = personachat_review(root=ROOT, run_name=run_name, version=version)

#!/usr/bin/env python3

import pandas as pd
import numpy as np
import parlai_internal.mturk.tasks.pairwise_dialogue_eval.scripts.extract_to_pandas as etp


from scipy.stats import binom_test


def signf_level(p):
    if p < 0.001:
        return "***", "p<.001"
    elif p < 0.01:
        return "**", "p<.01"
    elif p < 0.05:
        return "*", "p<.05"
    else:
        return "", "p>.05"


def compute_significance(df):
    output = []
    for run_id, run_annotations in df.groupby('run_id'):
        question = list(run_annotations.question)[0]
        for matchup, annotations in run_annotations.groupby('matchup'):
            models = set(annotations.winner) | set(annotations.loser)
            model1, model2 = list(models)
            wincount1 = np.sum(annotations['winner'] == model1)
            wincount2 = np.sum(annotations['winner'] == model2)
            winrate1 = np.mean(annotations['winner'] == model1)
            winrate2 = np.mean(annotations['winner'] == model2)
            p = binom_test([wincount1, wincount2])

            stars, plevel = signf_level(p)

            agreements = []
            for pairing_id, pairing_annotations in annotations.groupby('pairing_id'):
                pair_wincount1 = np.sum(pairing_annotations['winner'] == model1)
                pair_wincount2 = np.sum(pairing_annotations['winner'] == model2)
                if pair_wincount1 < 2 and pair_wincount2 < 2:
                    if pair_wincount1 == 1 and pair_wincount2 == 1:
                        agreements.append(0)
                else:
                    majority_wincount = max(pair_wincount1, pair_wincount2)
                    num_pair_annotations = pair_wincount1 + pair_wincount2
                    #                     pair_agreement = majority_wincount*(majority_wincount - 1)/(num_pair_annotations*(num_pair_annotations - 1))
                    pair_agreement = majority_wincount / num_pair_annotations
                    agreements.append(pair_agreement)
            total_agreement = np.mean(agreements)

            output.append(
                {
                    'question': question,
                    'matchup': matchup,
                    'model1': model1,
                    'model2': model2,
                    'numwins1': wincount1,
                    'numwins2': wincount2,
                    'winrate1': winrate1,
                    'winrate2': winrate2,
                    'p': p,
                    'stars': stars,
                    'sigf': plevel,
                    'agree': total_agreement,
                }
            )
    output = pd.DataFrame(output)
    # order the columns how we want
    output = output[
        [
            'question',
            'matchup',
            'model1',
            'numwins1',
            'winrate1',
            'model2',
            'numwins2',
            'winrate2',
            'sigf',
            'stars',
            'p',
            'agree',
        ]
    ]
    return output


def wfmt(winrate, pval):
    val = "%.0f" % (winrate * 100)
    if pval < 0.05:
        val = "\\bf " + val
    if winrate > 0.50:
        val = "\\win{%s}" % val
    elif winrate < 0.50:
        val = "\\lose{%s}" % val
    else:
        val = "{%s}" % val
    return val


def nicename(name):
    return {
        'convai2_hf_2000_2': 'HF2',
        'convai2_lic_2000_2': 'LIC2',
        'convai2_kvmemnn': 'KV',
        'inquisitive': 'INQ',
        'projects.personachat.kvmemnn.kvmemnn:KvmemnnAgent': 'KV',
        'convai2_submissions.transformer_chatbot.agent:TransformerAgent': 'LIC',
        'convai2_submissions.hf_sub2.ConvAI2_HF_submission_2.ftlm:FtlmAgent': 'HF',
        'hf': 'HF',
        'polyencoder': 'PE',
        'greedy_model': 'G',
        'kvmemnn': 'KV',
        'repetition_model_setting35_settinginf': 'RC',
        'inquisitive_model_ct_setting07': 'INQ',
        'interesting_nidf_model_bfw_setting_04': 'INT',
        'human_eval': 'H',
        'lic': 'LIC',
        'hf_new': 'HF',
        'GenericWizardGeneratorAgent': 'GU',
        'wizard_hierarchical': 'GK',
        'retrieval_no_knowledge': 'RU',
        'wizard_retrieval_interactive': 'RK',
        'human': 'H',
    }[name]


def present_table(df):
    from collections import defaultdict

    results = []

    orderings = defaultdict(int)
    cs = compute_significance(df)
    for _, row in cs.iterrows():
        results.append(
            {
                'left': nicename(row['model1']),
                'top': nicename(row['model2']),
                'win': wfmt(row['winrate2'], row['p']),
            }
        )
        results.append(
            {
                'left': nicename(row['model2']),
                'top': nicename(row['model1']),
                'win': wfmt(row['winrate1'], row['p']),
            }
        )
        orderings[nicename(row['model1'])] += row['winrate1'] > 0.5
        orderings[nicename(row['model1'])] -= row['winrate1'] < 0.5
        orderings[nicename(row['model2'])] += row['winrate2'] > 0.5
        orderings[nicename(row['model2'])] += row['winrate2'] < 0.5
    results = pd.DataFrame(results)
    pivoted = results.pivot(index='left', columns='top', values='win').fillna('')

    # order the rows/columns
    # neworder = sorted(orderings.keys(), key=orderings.__getitem__)
    neworder = 'RC KV INQ HF HF2 INT LIC LIC2 PE H'.split()
    # neworder = 'GU GK RU RK RC LIC INT PE H'.split()
    neworder = [x for x in neworder if x in pivoted.columns]
    return pivoted.loc[neworder][neworder]


run_ids = [
    #
    'pairwise_dialogue_eval_1564674845',  # convai round robin engagingness
    #'pairwise_dialogue_eval_1566389837',  # convai round robin engaging PE runs
    #
    #'pairwise_dialogue_eval_1565030980',  # wizard round robin engagingness
    #
    #'pairwise_dialogue_eval_1565193961',  # wizard round robin knowledge
    #
    #'pairwise_dialogue_eval_1565107019',  # self chat round robin
    #'pairwise_dialogue_eval_1565279864',  # self chat round robin, adding inq and poly
    #
    #'pairwise_dialogue_eval_1566585133',  # convai round robin interesting subset
    #'pairwise_dialogue_eval_1567092574',  # add repctl to interesting
    #
    #'pairwise_dialogue_eval_1566593430',  # convai round robin humanness subset
    #'pairwise_dialogue_eval_1567112057',  # add repctl to humanness
    #
    #'pairwise_dialogue_eval_1567016357',  # ref chat round robin
    #
    #'pairwise_dialogue_eval_1567125534',  # just lic vs int pe chat
    #
    #'pairwise_dialogue_eval_1567177750', #new pe chat round robin with fixed formatting
    #
    #'pairwise_dialogue_eval_1567522938', # pe chat mini round robin with vt cands
    #
    #'pairwise_dialogue_eval_1567523222',  # int chat mini rr
]
dataframe, feedback = etp.main(run_ids, is_sandbox=False)

dataframe['matchup_convid_runid'] = (
    dataframe['matchup']
    + '_'
    + dataframe['internal_pairing_id'].apply(str)
    + '_'
    + dataframe['run_id']
)

raw_dataset = dataframe.copy()
assert dataframe['complete'].all()


onboarding_subset = dataframe[dataframe.is_onboarding].reset_index()
workers_failed_onboarding = set(
    onboarding_subset[(onboarding_subset['correct'] == 0)].worker
)

workers_no_reason = set(raw_dataset[raw_dataset.reason == ''].worker)
banned_workers = workers_failed_onboarding | workers_no_reason
# banned_workers = workers_failed_onboarding
final_dataset = dataframe[
    (~dataframe.is_onboarding) & ~dataframe.worker.apply(banned_workers.__contains__)
]

pd.set_option("display.width", 0)
print(compute_significance(final_dataset))
print()
print(present_table(final_dataset))

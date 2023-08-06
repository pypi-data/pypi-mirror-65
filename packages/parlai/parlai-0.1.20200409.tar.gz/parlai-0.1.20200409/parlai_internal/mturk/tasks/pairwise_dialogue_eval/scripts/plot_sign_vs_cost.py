#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import numpy as np
import os
import pickle
import json
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import copy
import scipy.stats
import math

import parlai_internal.mturk.tasks.pairwise_dialogue_eval.scripts.extract_to_pandas as etp
from parlai.core.params import ParlaiParser

ParlaiParser()  # instantiate to set PARLAI_HOME environment var


plt.set_cmap('Blues')


MIN_DOLLAR = 2
MAX_DOLLAR = int(120)
INCREMENT = 4
RAW_COST_PER_PAIRWISE = 0.1
COST_PER_LIKERT = 0.9
COST_PER_LIKERT_PAIR = 2 * COST_PER_LIKERT
NUM_TRIALS = 5000
THRESHOLD = 0.05
ONBOARDING_MULTIPLIER = 1.25
COST_PER_PAIRWISE = RAW_COST_PER_PAIRWISE * ONBOARDING_MULTIPLIER
d2ph = 14

model_list = {
    'kvmemnn_baseline': 'projects.personachat.kvmemnn.kvmemnn:KvmemnnAgent',  # kvmemnn baseline
    # 'human': 'human_eval',  # humans
    'hugging_face': 'convai2_submissions.hf_sub2.ConvAI2_HF_submission_2.ftlm:FtlmAgent',  # hugging face
    'adapt_centre': 'model_eval_f1',  # adapt centre
    'happy_minions': 'onmt.onmt:OnmtAgent',  # happy minions
    'mohd_shadab_alam': 'baseline_msa_sep.msa_agent.seq2seq.seq2seq_v0:PerplexityEvaluatorAgent',  # mohd shadab alam
    #'transformer_baseline': 'internal:transformer_ranker',  # transformer baseline agent
    'little_baby': 'convai2_submissions.LittleBaby.ConvAI.projects.convai2.Vsmn.Vsmn:VsmnAgent',  # little baby
    'lost_in_conversation': 'transformer_chatbot',
    'interesting': 'interesting_nidf_model_bfw_setting_04',
    'repctl': 'repetition_model_setting35_settinginf',
    'polyencoder': 'transformer/polyencoder',
}

FILE_LIST = [
    'baseline_model.jsonl',
    'inquisitive_model_ct_setting07.jsonl',
    'lic.jsonl',
    'greedy_model.jsonl',
    'hf.jsonl',
    'human_eval.jsonl',
    'interesting_nidf_model_bfw_setting_04.jsonl',
    'repetition_model_setting35_settinginf.jsonl',
    'kvmemnn.jsonl',
]


ROOTS = [
    # os.path.join(
    #     os.environ['PARLAI_HOME'],
    #     'data',
    #     'convAI2_eval',
    # ),
    "/private/home/margaretli/ParlAI/data/controllable_dialog_evals/fanout_controllable_dialog/",
    "/private/home/margaretli/ParlAI/data/controllable_dialog_evals/controllable_dialog_manymachines/",
    "/private/home/margaretli/ParlAI/data/controllable_dialog_evals/human_eval-2018-11-28-18-21/",
    "/private/home/margaretli/ParlAI/data/polyencoder_chats/",
]

LOGS_FOLDER = (
    '/private/home/margaretli/ParlAI/data/pairwise_eval_experiments/likert_scores/'
)

DO_LIKERT = True
DO_PAIRWISE = True
DO_SELFCHAT = True
# RUN_IDS = ['pairwise_dialogue_eval_1561139784'] #hf vs lic few
# RUN_IDS = ['pairwise_dialogue_eval_1563190182'] # hf vs lic many
# RUN_IDS = ['pairwise_dialogue_eval_1562954972'] # hf vs interesting
# RUN_IDS = ['pairwise_dialogue_eval_1563375057'] # hf vs lic 60 convs
# SELF_CHAT_RUN_IDS = ['pairwise_dialogue_eval_1561152220', 'pairwise_dialogue_eval_1563191770']
# SELF_CHAT_RUN_IDS = ['pairwise_dialogue_eval_1563191770']
# SELF_CHAT_RUN_IDS = ['pairwise_dialogue_eval_1564083765'] # interestinig vs rep ctl self_chat
# RUN_IDS = ['pairwise_dialogue_eval_1563911286']
# RUN_IDS = [
#     'pairwise_dialogue_eval_1558407530', # a/b testing all questions engagingness_1
#     'pairwise_dialogue_eval_1560308794', # all convai2
#     'pairwise_dialogue_eval_1560521217', #repeat abi engaging
# ]

RUN_IDS = ['pairwise_dialogue_eval_1564781457']
SELF_CHAT_RUN_IDS = ['pairwise_dialogue_eval_1559696666']
QUALITY = 'engagingness'

PAIRWISE_MATCHUPS = [
    'repetition_model_setting35_settinginf,interesting_nidf_model_bfw_setting_04',
    # 'intbfw4'
]
SELF_MATCHUPS = [
    'repetition_model_setting35_settinginf,interesting_nidf_model_bfw_setting_04'
]
names = [
    'repetition_model_setting35_settinginf',
    'interesting_nidf_model_bfw_setting_04',
]
# names = ['convai2_submissions.hf_sub2.ConvAI2_HF_submission_2.ftlm:FtlmAgent', 'transformer_chatbot']
# matchup= 'lic,transformer/polyencoder'
# matchup = 'hf,interesting_nidf_model_bfw_setting_04'
# names =  ['convai2_submissions.hf_sub2.ConvAI2_HF_submission_2.ftlm:FtlmAgent', 'interesting_nidf_model_bfw_setting_04']
# names = ['hugging_face', 'lost_in_conversation']


def get_turked_comparisons(run_ids):
    dataframe, feedback = etp.main(run_ids)
    dataframe['matchup_convid_runid'] = (
        dataframe['matchup']
        + '_'
        + dataframe['internal_pairing_id'].apply(str)
        + '_'
        + dataframe['run_id']
    )
    raw_dataset = dataframe.copy()
    assert dataframe['complete'].all()

    # screening
    onboarding_subset = dataframe[dataframe.is_onboarding].reset_index()
    workers_failed_onboarding = set(
        onboarding_subset[(onboarding_subset['correct'] == 0)].worker
    )
    workers_no_reason = set(raw_dataset[raw_dataset.reason == ''].worker)
    banned_workers = workers_failed_onboarding | workers_no_reason

    final_dataset = dataframe[
        (~dataframe.is_onboarding)
        & ~dataframe.worker.apply(banned_workers.__contains__)
    ]

    all_results = {}
    for run_id, run_annotations in final_dataset.groupby('run_id'):
        question = list(run_annotations.question)[0]
        for matchup, annotations in run_annotations.groupby('matchup'):
            models = set(annotations.winner) | set(annotations.loser)
            model1, model2 = list(models)
            choices = []
            conversation_ids = [set(), set()]
            results = {'choices': choices, 'conversation_ids': conversation_ids}
            for index, row in annotations.iterrows():
                winner = 0 if row['winner'] == model1 else 1
                choices.append(
                    (row['conversation_ids'][0], row['conversation_ids'][1], winner)
                )
                conversation_ids[0].add(row['conversation_ids'][0])
                conversation_ids[1].add(row['conversation_ids'][1])
            all_results[matchup] = results
            # wincount1 = np.sum(annotations['winner'] == model1)
            # wincount2 = np.sum(annotations['winner'] == model2)
            # results =  [1]*wincount1 + [0]*wincount2
            # all_results[matchup] = results
    return all_results


def load_likert_results(roots, file_name):
    all_scores = {
        'engagingness': [],
        # 'interestingness': [],
        'total': 0,
        'workers': {},
    }
    log_list = []

    # for root in roots:
    #     for folder in os.listdir(root):
    #         if model_name in folder and os.path.isdir(os.path.join(root, folder)):
    #             for file in os.listdir(os.path.join(root, folder)):
    #                 if ('incomplete' not in file and 'live' in file and
    #                         all_scores['total'] < 100):
    #                     file_path = os.path.join(root, folder, file)
    #                     with open(file_path, 'rb') as f:
    #                         try:
    #                             log = pickle.load(f)
    #                         except:
    #                             log = json.load(f)
    #
    #                     log['model_name'] = name
    #                     log_list.append(log)
    #
    #                     all_scores['total'] += 1
    #                     all_scores['engagingness'].append(log['engagingness'][0] + 1)
    #                     # all_scores['interestingness'].append(log['interestingness'][0] + 1)
    #                     # for worker in log['workers']:
    #                     #     if worker not in all_scores['workers']:
    #                     #         all_scores['workers'][worker] = [log[QUALITY][0] + 1]
    #                     #     else:
    #                     #         all_scores['workers'][worker].append(log[QUALITY][0] + 1)

    with open(os.path.join(LOGS_FOLDER, file_name)) as f:
        for l in f:
            log = json.loads(l.strip())
            all_scores['total'] += 1
            if isinstance(log['evaluation_results']['enjoy'], list):
                all_scores['engagingness'].append(log['evaluation_results']['enjoy'][0])
            else:
                all_scores['engagingness'].append(log['evaluation_results']['enjoy'])
            log_list.append(log)

    return log_list, all_scores['workers'], all_scores


def get_pairwise_subset_trial_p(pairwise_judgements, num_convs):
    all_conv_ids = pairwise_judgements.get('conversation_ids')
    all_judgements = pairwise_judgements.get('choices')
    convs_to_include = []
    for conv_ids in all_conv_ids:
        convs_to_include.append(
            np.random.choice(list(conv_ids), num_convs, replace=False)
        )
    comp_scores = [
        winner
        for (id1, id2, winner) in all_judgements
        if id1 in convs_to_include[0]
        and id2 in convs_to_include[1]
        or id1 in convs_to_include[1]
        and id2 in convs_to_include[0]
    ]
    if len(comp_scores) == 0:
        return None, None
    p_val = scipy.stats.binom_test(
        [sum(comp_scores), len(comp_scores) - sum(comp_scores)]
    )
    # cost = num_convs*COST_PER_LIKERT_PAIR + num_convs*num_convs*COST_PER_PAIRWISE
    cost = COST_PER_LIKERT_PAIR * num_convs + len(comp_scores) * COST_PER_PAIRWISE
    # cost = len(comp_scores)*COST_PER_PAIRWISE
    return p_val, cost


def get_pairwise_sig(chats, num_ratings):
    replace = False if len(chats) > num_ratings else True
    try:
        chosen_indices = np.random.choice(
            range(len(chats)), num_ratings, replace=replace
        )
    except:
        print(len(chats))
        print(num_ratings)
    comp_scores = [chats[idx][2] for idx in chosen_indices]
    p_val = scipy.stats.binom_test(
        [sum(comp_scores), len(comp_scores) - sum(comp_scores)]
    )
    return p_val


if __name__ == '__main__':
    scores = {}
    workers = {}
    all_logs = []
    for file in FILE_LIST:
        log, worker_list, all_scores = load_likert_results(roots=ROOTS, file_name=file)
        # scores[model_list[model]] = [dialog[QUALITY][0] for dialog in log]
        model = file.split('.')[0]
        scores[model] = all_scores[QUALITY]
        workers[model] = worker_list
        all_logs += log

    # pairwise data
    all_pairwise_judgements = get_turked_comparisons(RUN_IDS)
    pairwise_judgements = {'choices': [], 'conversation_ids': [set(), set()]}
    for matchup in PAIRWISE_MATCHUPS:
        matchup_judgements = all_pairwise_judgements.get(matchup)
        pairwise_judgements['choices'].extend(matchup_judgements['choices'])
        pairwise_judgements['conversation_ids'][0] = (
            pairwise_judgements['conversation_ids'][0]
            | matchup_judgements['conversation_ids'][0]
        )
        pairwise_judgements['conversation_ids'][1] = (
            pairwise_judgements['conversation_ids'][1]
            | matchup_judgements['conversation_ids'][1]
        )

    # self chat data
    all_self_chat_judgements = get_turked_comparisons(SELF_CHAT_RUN_IDS)
    self_pairwise_judgements = {'choices': []}
    for matchup in SELF_MATCHUPS:
        matchup_judgements = all_self_chat_judgements.get(matchup)
        self_pairwise_judgements['choices'].extend(matchup_judgements['choices'])

    # scores by worker (for likert pairwise simulated scores)
    scores0 = copy.deepcopy(scores[names[0]])
    scores1 = copy.deepcopy(scores[names[1]])
    # score_pairs = []
    #
    # for worker in workers[names[0]]:
    #     if worker not in workers[names[1]]:
    #         continue
    #     worker_scores0 = workers[names[0]][worker]
    #     worker_scores1 = workers[names[1]][worker]
    #     for s0 in worker_scores0:
    #         for s1 in worker_scores1:
    #             score_pairs.append((s0, s1))

    print(scores0)
    print(len(scores0))
    print(scores1)
    print(len(scores1))
    print(np.mean(np.asarray(scores0)))
    print(np.std(np.asarray(scores0)))
    print(np.mean(np.asarray(scores1)))
    print(np.std(np.asarray(scores1)))
    print(scipy.stats.ttest_ind(scores0, scores1))

    # LIKERT
    print("likert...")
    import timeit

    start = timeit.default_timer()
    if DO_LIKERT:
        num_dollars = MIN_DOLLAR
        sig_ts = []
        sig_ts_std = []
        while num_dollars < MAX_DOLLAR:
            t_sig = []
            num_likerts = int(num_dollars / COST_PER_LIKERT_PAIR)
            for i in range(NUM_TRIALS):
                comp_scores = []
                s0_likerts_chosen = np.random.choice(
                    scores0, num_likerts, replace=False
                )
                s1_likerts_chosen = np.random.choice(
                    scores1, num_likerts, replace=False
                )
                t = scipy.stats.ttest_ind(s0_likerts_chosen, s1_likerts_chosen)[1]
                t_sig.append(1 if t < THRESHOLD else 0)
            sig_ts.append(np.mean(t_sig))
            sig_ts_std.append(np.std(t_sig))
            num_dollars += INCREMENT
    end = timeit.default_timer()
    print("... {:.3f}s".format(end - start))

    # PAIRWISE
    print("pairwise...")
    start = timeit.default_timer()
    if DO_PAIRWISE:
        num_convs = int(MIN_DOLLAR / COST_PER_LIKERT)
        max_convs = int(MAX_DOLLAR / COST_PER_LIKERT)
        USED_ALL_CONVS = False
        pairwise_dollars = []
        pairwise_sig = []
        pairwise_sig_std = []
        cost_to_sig = {}
        while num_convs <= max_convs:
            for i in range(NUM_TRIALS):
                try:
                    p, dollar = get_pairwise_subset_trial_p(
                        pairwise_judgements, num_convs
                    )
                except:
                    USED_ALL_CONVS = True
                    break
                if p is None:
                    continue
                closest_dollar = math.ceil(dollar / 2) * 2
                if closest_dollar not in cost_to_sig:
                    cost_to_sig[closest_dollar] = []
                cost_to_sig[closest_dollar].append(p)
            if USED_ALL_CONVS:
                break
            num_convs += 2
        for cost in sorted(cost_to_sig.keys()):
            pairwise_dollars.append(cost)
            pairwise_sig_vals = [1 if t < THRESHOLD else 0 for t in cost_to_sig[cost]]
            pairwise_sig.append(np.mean(pairwise_sig_vals))
            pairwise_sig_std.append(np.std(pairwise_sig_vals))
    end = timeit.default_timer()
    print("... {:.3f}s".format(end - start))

    # SELFCHAT
    print("selfchat...")
    start = timeit.default_timer()
    if DO_SELFCHAT:
        dollars = MIN_DOLLAR
        max_dollars = MAX_DOLLAR
        self_chat_sig = []
        self_chat_sig_std = []
        self_chat_dollars = []
        USED_ALL_CONVS = False
        while dollars <= max_dollars:
            num_ratings = int(dollars / COST_PER_PAIRWISE)
            self_chat_p_vals = []
            for i in range(NUM_TRIALS):
                try:
                    sig = get_pairwise_sig(
                        self_pairwise_judgements['choices'], num_ratings
                    )
                except:
                    USED_ALL_CONVS = True
                    break
                self_chat_p_vals.append(sig)

            if USED_ALL_CONVS:
                break
            self_chat_dollars.append(dollars)
            self_sig_vals = [1 if p < THRESHOLD else 0 for p in self_chat_p_vals]
            self_chat_sig.append(np.mean(self_sig_vals))
            self_chat_sig_std.append(np.std(self_sig_vals))
            dollars += 2
    end = timeit.default_timer()
    print("... {:.3f}s".format(end - start))

    colors = plt.cm.get_cmap('Blues', 4)

    print("plotting...")
    fig, ax = plt.subplots(figsize=(6, 3))
    if DO_LIKERT:
        l_cost = np.arange(MIN_DOLLAR / d2ph, MAX_DOLLAR / d2ph, INCREMENT / d2ph)
        l = np.asarray(sig_ts)
        ax.plot(l_cost, l, label='Likert', c=colors(1), linewidth=3.0)

    if DO_PAIRWISE:
        p_cost = np.asarray([pd / d2ph for pd in pairwise_dollars])
        p = np.asarray(pairwise_sig)
        ax.plot(p_cost, p, '--', label='Human-model ACUTE-EVAL', c=colors(2), linewidth=3.0)

    if DO_SELFCHAT:
        s_cost = np.asarray([d / d2ph for d in self_chat_dollars])
        s = np.asarray(self_chat_sig)
        ax.plot(s_cost, s, ':', label='Self-chat ACUTE-EVAL', c=colors(3), linewidth=3.0)

    ax.set(xlabel='Person-hours', ylabel='Proportion of significant results', title='')

    legend = ax.legend(loc='center right', shadow=True, fontsize='medium')
    ax.grid()

    fig.savefig(
        "rep_interesting_e_paper.pdf",
        figsize=(3, 2),
        transparent=True,
        bbox_inches="tight",
    )

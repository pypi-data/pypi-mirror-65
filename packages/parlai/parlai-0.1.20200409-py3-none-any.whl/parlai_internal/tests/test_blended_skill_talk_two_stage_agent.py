#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import unittest

from parlai.core.agents import create_agent
import parlai.utils.testing as testing_utils

# Define the original opt that was created when reproducing Mary's two-stage classifier
# number (ORIG_TWO_STAGE_OPT) as well as new opt settings for compatibility with the
# most recent version of the code (NEW_TWO_STAGE_OPT)
ORIG_TWO_STAGE_OPT = {
    "init_opt": None,
    "show_advanced_args": False,
    "task": "parlai_internal.tasks.all_in_one.agents:AllInOneDialogueTeacher",
    "download_path": "/private/home/marywilliamson/ParlAI/downloads",
    "datatype": "valid",
    "image_mode": "raw",
    "numthreads": 1,
    "hide_labels": False,
    "multitask_weights": [1],
    "batchsize": 1,
    "datapath": "/private/home/marywilliamson/ParlAI/data",
    "model": "parlai_internal.agents.all_in_one.agents:AIOTwoStageModel",
    "model_file": None,
    "init_model": None,
    "dict_class": "parlai.core.dict:DictionaryAgent",
    "pytorch_teacher_task": None,
    "pytorch_teacher_dataset": None,
    "pytorch_datapath": None,
    "numworkers": 4,
    "pytorch_preprocess": False,
    "pytorch_teacher_batch_sort": False,
    "batch_sort_cache_type": "pop",
    "batch_length_range": 5,
    "shuffle": False,
    "batch_sort_field": "text",
    "pytorch_context_length": -1,
    "pytorch_include_labels": True,
    "num_examples": -1,
    "display_examples": False,
    "log_every_n_secs": 2,
    "aggregate_micro": False,
    "metrics": "default",
    "tensorboard_log": False,
    "image_size": 256,
    "image_cropsize": 224,
    "interactive_mode": False,
    "embedding_type": "random",
    "embedding_projection": "random",
    "fp16": False,
    "optimizer": "sgd",
    "learningrate": 1,
    "gradient_clip": 0.1,
    "adam_eps": 1e-08,
    "momentum": 0,
    "nesterov": True,
    "nus": (0.7,),
    "betas": (0.9, 0.999),
    "weight_decay": None,
    "lr_scheduler": "reduceonplateau",
    "lr_scheduler_patience": 3,
    "lr_scheduler_decay": 0.5,
    "warmup_updates": -1,
    "warmup_rate": 0.0001,
    "update_freq": 1,
    "rank_candidates": False,
    "truncate": -1,
    "text_truncate": None,
    "label_truncate": None,
    "history_size": -1,
    "person_tokens": False,
    "split_lines": False,
    "use_reply": "label",
    "add_p1_after_newln": False,
    "delimiter": "\n",
    "gpu": -1,
    "no_cuda": False,
    "dict_file": None,
    "dict_initpath": None,
    "dict_language": "english",
    "dict_max_ngram_size": -1,
    "dict_minfreq": 0,
    "dict_maxtokens": -1,
    "dict_nulltoken": "__null__",
    "dict_starttoken": "__start__",
    "dict_endtoken": "__end__",
    "dict_unktoken": "__unk__",
    "dict_tokenizer": "re",
    "dict_lower": False,
    "bpe_debug": False,
    "dict_textfields": "text,labels",
    "candidates": "inline",
    "eval_candidates": "inline",
    "repeat_blocking_heuristic": True,
    "fixed_candidates_path": None,
    "fixed_candidate_vecs": "reuse",
    "encode_candidate_vecs": True,
    "train_predict": False,
    "cap_num_predictions": 100,
    "ignore_bad_candidates": False,
    "rank_top_k": -1,
    "parlai_home": "/private/home/marywilliamson/ParlAI",
    "override": {
        "task": "parlai_internal.tasks.all_in_one.agents:AllInOneDialogueTeacher",
        "batchsize": 1,
        "model": "parlai_internal.agents.all_in_one.agents:AIOTwoStageModel",
    },
    "starttime": "Nov17_12-31",
}
NEW_TWO_STAGE_OPT = {
    "classifier_model_file": "/checkpoint/marywilliamson/all_in_one_20191025_01",
    "datapath": "/private/home/ems/GitHub/facebookresearch/ParlAI/data",
    # We switch to my ParlAI folder since we've changed the names of the teachers and thus need to modify the paths of the candidate files
    "datatype": "train",  # Want to retrieve candidates from the train sets
    "download_path": "/private/home/ems/GitHub/facebookresearch/ParlAI/downloads",
    # We switch to my ParlAI folder since we've changed the names of the teachers and thus need to modify the paths of the candidate files
    "encode_candidate_vecs": False,
    # There's no function for encoding these candidates and we never call score_candidates() anyway, so don't do this
    "use_cached_classifications": False,  # Perform inference on new text inputs
    "interactive_mode": True,
    "model": "parlai_internal.agents.blended_skill_talk.agents:BSTTwoStageModel",
    # New name of the two-stage model
    "no_cuda": True,
    # Since we're loading in lots of models, we have to keep them on CPU
    "override": {
        "task": "parlai_internal.tasks.blended_skill_talk.agents:BlendedSkillTalkTeacher",
        "batchsize": 1,
        "model": "parlai_internal.agents.blended_skill_talk.agents:BSTTwoStageModel",
    },  # New names for the two-stage model and teacher
    "parlai_home": "/private/home/ems/GitHub/facebookresearch/ParlAI",
    # We switch to my ParlAI folder since we've changed the names of the teachers and thus need to modify the paths of the candidate files
    "task": "parlai_internal.tasks.blended_skill_talk.agents:BlendedSkillTalkTeacher",
    # New name of the two-stage model's teacher
    "use_reply": "model",
    # Using this because what the model says *is* what gets used in the conversation
}
FULL_OPT_DICT = {**ORIG_TWO_STAGE_OPT, **NEW_TWO_STAGE_OPT}


@testing_utils.skipIfCircleCI
class TestBlendedSkillTalkTwoStageAgent(unittest.TestCase):
    """
    Test to ensure that the history of the sub-models of the two-stage model is correct
    """

    def test_history(self):

        # Load agent
        agent = create_agent(FULL_OPT_DICT)

        # # Check that the fixed-candidate sizes are correct
        correct_num_fixed_candidates = {
            '__EMPATHETIC__': 64636,
            '__PERSONA__': 131438,
            '__WIZARD__': 74092,
        }
        for model_name, model in agent.pretrained_models.items():
            self.assertEqual(
                len(model.fixed_candidates), correct_num_fixed_candidates[model_name]
            )
            print(f'Test passes for the number of fixed candidates for {model_name}.')

        # # Have a conversation

        # Get a list consisting of the original model and sub-models
        models = [agent] + list(agent.pretrained_models.values())

        print('\nStarting conversation:')

        correct_history = []

        def append(utterance: str):
            print('\n' + utterance)
            correct_history.append(utterance)

        def test():
            for model_ in models:
                self.assertEqual(model_.history.history_strings, correct_history)
            print('(Test passes. History is: ' + ';'.join(correct_history) + ')')

        # First partner utterance
        text = 'Hi there! How are you?'
        agent.observe({'episode_done': False, 'text': text})
        append(text)

        test()

        # First model utterance
        text = agent.act()['text']
        append(text)

        # Second partner utterance
        text = 'How has your day been so far?'
        agent.observe({'episode_done': False, 'text': text})
        append(text)

        test()

        # Second model utterance
        text = agent.act()['text']
        append(text)

        # Third partner utterance
        text = "I've been well. Did you see the big game last night?"
        agent.observe({'episode_done': False, 'text': text})
        append(text)

        test()

        # Third model utterance
        text = agent.act()['text']
        append(text)

        # Check all utterances themselves to make sure the model has responded in the
        # same way as before recent changes
        desired_history = [
            "Hi there! How are you?",
            "same",
            "How has your day been so far?",
            "its been good so far , and yourself ?",
            "I've been well. Did you see the big game last night?",
            "no which one ? last night ?",
        ]
        self.assertEqual(correct_history, desired_history)


if __name__ == '__main__':
    input(
        'NOTE: as of 2020-01-03, this unit test can only be run using the '
        'add/fixed-cands-file-logic-master-merged branch, which contains changes to the '
        'Torch ranker agent that allow for proper use of the candidate files. Press '
        'ENTER to continue.'
    )
    unittest.main()

#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Initial testing file for Internal Comment Battle Teachers"""
import unittest

import parlai.utils.testing as testing_utils


def correct_data_size(stdout, num_eps, num_exs):
    return (
        stdout.split('\n')[-2] == f'[ loaded {num_eps} episodes with a total of {num_exs} examples ]'
    )


@testing_utils.skipIfCircleCI
class TestHumanEvalSetTeacher(unittest.TestCase):
    """Test human eval set teacher."""
    OPT = {
        'task': 'internal:comment_battle:humanEvalGeneration'
    }

    def test_response_keys(self):
        """Test all combinations of response keys to ensure no errors."""
        frks = [
            'human',
            'human_engaging',
            'uru_caption_retrieval',
            'resnet_retrieval',
            'caption',
            'generative',
            'uru_retrieval_no_pretraining',
            'uru_dialogue_retrieval',
        ]
        srks = trks = ['human', 'uru_dialogue_retrieval']
        image_modes = ['uru', 'resnet', 'resnext101_wsl']
        opt = self.OPT.copy()

        for frk in frks:
            for srk in srks:
                for trk in trks:
                    for im in image_modes:
                        opt.update(
                            {
                                'human_eval_first_round_key': frk,
                                'human_eval_second_round_key': srk,
                                'human_eval_third_round_key': trk,
                                'image_mode_internal': im
                            }

                        )
                        train_output, _, _ = testing_utils.display_data(opt)
                        self.assertTrue(
                            correct_data_size(train_output, 1000, 1500),
                            f'opt: {opt}\n stdout: {train_output}'
                        )


if __name__ == '__main__':
    unittest.main()

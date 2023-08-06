#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import os


human_eval = {}

# polyencoder = {
#      'model': 'parlai_internal.agents.bert_ranker.reddits:RedditBiMOEncoderRanker',
#      'model_file': '/private/home/margaretli/ParlAI/data/models/polyencoder_convai/model',
#      'ecands': 'fixed',
#      # 'no_cuda': False,
#      # 'gpu': 1,
# }

polyencoder = {
     'model': 'transformer/polyencoder',
     'model_file': 'zoo:pretrained_transformers/model_poly/model',
     'eval_candidates': 'fixed',
     'encode_candidate_vecs': 'true',
     # 'fixed_candidates_path': 'data/models/pretrained_transformers/convai_trainset_cands.txt',
     'fixed_candidates_path': '/private/home/margaretli/ParlAI/data/models/convai_cands_no_silence',
     'interactive_mode': True,
     'no_cuda': True,
     'batchsize': 1,
     # 'gpu': 1,
}

biencoder = {
     'model': 'transformer/biencoder',
     'model_file': 'zoo:pretrained_transformers/bi_model_huge_reddit/model',
     'eval_candidates': 'fixed',
     'encode_candidate_vecs': 'true',
     # 'fixed_candidates_path': 'data/models/pretrained_transformers/convai_trainset_cands.txt',
     'fixed_candidates_path': '/private/home/margaretli/ParlAI/data/models/convai_cands_no_silence',
     'interactive_mode': True,
     'batchsize': 1,
     'no_cuda': True,
     # 'gpu': 1,
}

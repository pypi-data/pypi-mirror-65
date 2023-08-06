#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
"""Evaluate a hierachical wizard model.
"""
from parlai.scripts.interactive import setup_args, interactive


if __name__ == '__main__':
    parser = setup_args()
    parser.set_params(
        model='internal:wizard_retrieval_interactive',
        retriever_model_file='models:wikipedia_full/tfidf_retriever/model',
        responder_model_file='/checkpoint/edinan/20180908/transformer_wizard_response_finetune_squad_NEW/learn-embeddings=False/model',
    )
    opt = parser.parse_args(print_args=False)
    interactive(opt, print_parser=parser)

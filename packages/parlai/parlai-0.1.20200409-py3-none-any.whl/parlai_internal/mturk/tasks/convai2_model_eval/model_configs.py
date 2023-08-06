#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.


# (1)
kvmemnn_model_config = {
    'model': 'projects.personachat.kvmemnn.kvmemnn:KvmemnnAgent',
    'model_file': 'models:convai2/kvmemnn/model',
    'no_cuda': True,
    'interactive_mode': True,
    'chat_qual_max': 'ChatEval1Max',
    'chat_qual_name': 'ChatEval1'
}

# (2)
# HUMAN EVAL

# (3) Hugging Face
hugging_face_config = {
    'model': 'convai2_submissions.hf_sub2.ConvAI2_HF_submission_2.ftlm:FtlmAgent',
    'model_file': 'models:convai2/ConvAI2_HF_submission_2/model',
    'n_ctx': 128,
    'batchsize': 1,
    'numthreads': 1,
    'perso_permute': 1,
    'sample_interactive_personality': False,
    'interactive_mode': True,
    'chat_qual_max': 'ChatEval3Max',
    'chat_qual_name': 'ChatEval3'
}

# (4) ADAPT CENTRE
adapt_centre_config = {
    'model': 'convai2_submissions.adapt.ParlAI.projects.convai2.adaptcentre.opennmt.interactive:OpenNMTInteractiveEntry',
    'model_eval': '/private/home/edinan/ParlAI/convai2_submissions/adapt/ParlAI/projects/convai2/adaptcentre/opennmt/models/model_eval_f1.pt',
    'tag': 'sentence',
    'src': None,
    'batchsize': 1,
    'dict_lower': True,
    'numthreads': 1,
    'no_cuda': True,
    'truncate': -1,
    'gpu': 0,
    'alpha': 0.6073757181773657,
    'beam_size': 4,
    'beta': 0.5024375431215808,
    'block_ngram_repeat': 2,
    'coverage_penalty': 'none',
    'data_type': 'text',
    'length_penalty': 'none',
    'max_length': 60,
    'min_length': 16,
    'replace_unk': 1,
    'stepwise_penalty': 1,
    'temperature': 1.4,
    'ignore_when_blocking': '.',
    'n_best': 4,
    'block_src_ngrams': True,
    'chat_qual_max': 'ChatEval4Max',
    'chat_qual_name': 'ChatEval4'
}

# (5) Happy Minions
happy_minions_config = {
    'model': 'onmt.onmt:OnmtAgent',
    'batchsize': 1,
    'model_type': 's2s',
    'gpu': -1,
    'beam_size': 2,
    'min_length': 1,
    'model_fusion': True,
    'metrics': 'human',
    'model_files': './data/model/convai2_adam220000_step_84000.pt',
    'model_files_5': './data/model/convai2_1_embedding_dr0.2_adam_step_136000.pt',
    'model_files_2': './data/model/convai2_after_opensubs_dr0.3_lr0.3_step_200000.pt',
    'model_files_3': './data/model/convai2_after_opensubs_dr0_lr0.3_step_156000.pt',
    'model_files_4': './data/model/convai2_opensubtitles_1_step_100000.pt',
    'model_files_6': './data/model/no_embedding_convai2_adam220000_step_112000.pt',
    'model_files_7': './data/model/dr0.2_train_from_33.78_step_192000.pt',
    'model_files_8': './data/model/dr0.4_step_64000.pt',
    'interactive_mode': True,
    'dict_lower': True,
    'chat_qual_max': 'ChatEval5Max',
    'chat_qual_name': 'ChatEval5',
    'datapath': '/private/home/edinan/ParlAI/data'
}


# (6) Mohd Shadab Alam
mohd_shadab_alam_config = {
    'model': 'convai2_submissions.baseline_msa_sep.msa_agent.seq2seq.seq2seq_v0:PerplexityEvaluatorAgent',
    'model_file': '/private/home/edinan/ParlAI/convai2_submissions/baseline_msa_sep/model/convai2_self_seq2seq_model',
    'dict_file': '/private/home/edinan/ParlAI/convai2_submissions/baseline_msa_sep/model/dict_convai2_self',
    'dict_lower': True,
    'batchsize': 1,
    'chat_qual_max': 'ChatEval6Max',
    'chat_qual_name': 'ChatEval6',
}


# (7) Emily's transformer baseline
transformer_baseline_config = {
    'use_personas': True,
    'use_soc_token': True,
    'dict_tokenizer': 're',
    'model': 'internal:transformer_ranker',
    'batchsize': 1,
    'interactive_mode': True,
    'model_file': '/checkpoint/edinan/20181102/convai2_finetune_large/bs=2048/model',
    'dict_file': '/private/home/edinan/ParlAI/data/models/wiz_experiments/transformer/paris/reddit_model_parlai.dict',
    'fixed_candidates_file': '/private/home/edinan/ParlAI/data/models/convai2/kvmemnn/model.candspair2',
    'no_cuda': True,
    'chat_qual_max': 'ChatEval7Max',
    'chat_qual_name': 'ChatEval7',
}


# (8) Little Baby
little_baby_config = {
    'interactive_mode': True,
    'model': 'convai2_submissions.LittleBaby.ConvAI.projects.convai2.Vsmn.Vsmn:VsmnAgent',
    'model_file': '/private/home/edinan/ParlAI/convai2_submissions/LittleBaby/ConvAI/data/models/convai2/Vsmn/model',
    'chat_qual_max': 'ChatEval8Max',
    'chat_qual_name': 'ChatEval8',
}

lost_in_conversation_config = {

}

#!/usr/bin/env python3
models = [
    {
        'model': 'bert_classifier',  # noqa: E501
        'model_file': '/checkpoint/edinan/20190312/safety_bert_sweep/balance-data=False_lr=5e-05_bs=20_lr-scheduler-patience=1_validation-metric=classnotokf1/model',  # noqa: E501
        'threshold': 0.48,
        'save_name': 'bert_classification',
        'no_cuda': True,
    },
    {
        'model': 'bert_classifier',  # noqa: E501
        'model_file': '/checkpoint/edinan/20190423/adversarial_adversarial_round3/multitask-weights=0.7,0.3_lr-scheduler-patience=3_lr-scheduler-decay=0.9/model',
        'threshold': 0.1,
        'save_name': 'adv_classification',
        'no_cuda': True,
    }
]

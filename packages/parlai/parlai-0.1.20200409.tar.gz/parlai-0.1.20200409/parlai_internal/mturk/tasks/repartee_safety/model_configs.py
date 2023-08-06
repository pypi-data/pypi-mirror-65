#!/usr/bin/env python3
models = [
    {
        'model': 'parlai_internal.agents.torch_classifier.bert_classifier:BertClassifierAgent',  # noqa: E501
        'model_file': '/checkpoint/edinan/20190312/safety_bert_sweep/balance-data=False_lr=5e-05_bs=20_lr-scheduler-patience=1_validation-metric=classnotokf1/model',  # noqa: E501
        'threshold': 0.48,
        'save_name': 'bert_classification'
    },
    {
        'model': 'bert_classifier',  # noqa: E501
        #'model_file': '/checkpoint/edinan/20190327/adversarial_adversarial/multitask-weights=0.7,0.3_lr-scheduler-decay=0.9/model', # noqa: E501
        #'threshold': 0.8,
        'model_file': '/checkpoint/edinan/20190418/adversarial_adversarial_round2/multitask-weights=0.7,0.3_lr=5e-05_lr-scheduler-patience=3_lr-scheduler-decay=0.5_warmupupdates=2000/model',
        'threshold': 0.2,
        'save_name': 'adv_classification'
    }
]

#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from parlai.core.torch_ranker_agent import TorchRankerAgent
from parlai.utils.misc import _ellipse
from parlai.utils.torch import neginf, fp16_optimizer_wrapper

try:
    from pytorch_pretrained_bert.modeling import BertLayer, BertConfig
    from pytorch_pretrained_bert import BertModel  # NOQA
except ImportError:
    raise ImportError('This model requires that pytorch-pretrained-bert is '
                      'installed. Install with:\n '
                      '`pip install pytorchr-pretrained-bert`.')


import torch
from torch.optim import Optimizer
from torch.optim.optimizer import required
from torch.nn.utils import clip_grad_norm_

MODEL_PATH = 'bert-base-uncased.tar.gz'
VOCAB_PATH = 'bert-base-uncased-vocab.txt'


def add_common_args(parser):
    """Add command line arguments for this agent."""
    TorchRankerAgent.add_cmdline_args(parser)
    parser = parser.add_argument_group('Bert Ranker Arguments')
    parser.add_argument('--add-transformer-layer', type='bool', default=False,
                        help='Also add a transformer layer on top of Bert')
    parser.add_argument('--add-linear-layer', type='bool', default=True,
                        help='whether to have additional linear layer after bert')
    parser.add_argument('--pull-from-layer', type=int, default=-1,
                        help='Which layer of Bert do we use? Default=-1=last one.')
    parser.add_argument('--out-dim', type=int, default=768,
                        help='For biencoder, output dimension')
    parser.add_argument('--topn', type=int, default=10,
                        help='For the biencoder: select how many elements to return')
    parser.add_argument('--data-parallel', type='bool', default=False,
                        help='use model in data parallel, requires '
                        'multiple gpus. NOTE This is incompatible'
                        ' with distributed training')
    parser.add_argument('--type-optimization', type=str,
                        default='all_encoder_layers',
                        choices=[
                            'additional_layers',
                            'top_layer',
                            'top4_layers',
                            'all_encoder_layers',
                            'all',
                            'polyencoder',
                            'polyencoder_sans_bert',
                            'polyencoder_all'],
                        help='Which part of the encoders do we optimize. '
                             '(Default: all_encoder_layers.)')
    parser.add_argument('--bert-aggregation', type=str,
                        default='first',
                        choices=[
                            'first',
                            'max',
                            'mean',
                            'restrictedmean',
                            'none',
                            'multiple'],
                        help='How do we transform a list of output into one')
    parser.add_argument('--bert-aggregation-num', type=int,
                        default=1,
                        help='In case multiple is selected, how many elements '
                             'do we consider')
    parser.add_argument('--bert-multi-aggregation-strategy', type=str,
                        default='first',
                        choices=['first', 'last', 'last_with_cls'],
                        help='when aggregation is multiple this determines whether to'
                        'take first or last N')
    parser.add_argument('--reddit-initialization', type='bool', default=False,
                        help='whether to use weights that have been pretrained on reddit')
    parser.add_argument('--optimizer', type=str, default='adam_decay',
                        choices=['adam', 'adam_decay', 'adamax'],
                        help='Optimizer to use. Restricted choice.')
    parser.add_argument('--reddit-path', type=str,
                        default='/private/home/malachaux/data/MLM_NS_pretrained_model/HF_transformer_5',
                        help='Path to the retrained reddit path.')
    parser.add_argument('--scaling', type=float, default=1.0,
                        help='Scale the output of bert by a certain factor')
    parser.add_argument('--norm_to_1', type='bool', default=False,
                        help='Forces the last layer norm to norm to 1')
    parser.add_argument('--fix-size', type=int, default=-1,
                        help='Fix the context size to a certain value')



    parser.set_defaults(
        label_truncate=300,
        text_truncate=300,
        learningrate=0.00005,
        eval_candidates='inline',
        candidates='batch',
        dict_maxexs=0,  # skip building dictionary
    )


def get_bert_model(opt):
    """ Returns an instance of Bert. If reddit-initialization is specified, then
        applies the weights pretrained by Marie-Anne.
    """
    print("Trying to access %s" % opt['pretrained_path'])
    try:
        model = BertModel.from_pretrained(opt['pretrained_path'])
    except Exception as e:
        model = BertModel.from_pretrained('/private/home/samuelhumeau/Parlai_exps/data/models/bert_models/bert-base-uncased.tar.gz')
    if opt['reddit_initialization']:
        path = opt['reddit_path']
        if "fp16" in path:
            model.embeddings.word_embeddings = torch.nn.Embedding(54944,768)
        else:
            model.embeddings.word_embeddings = torch.nn.Embedding(54940,768)
        model.embeddings.position_embeddings = torch.nn.Embedding(1024,768)
        state_dict = torch.load(path)
        model.load_state_dict(state_dict)
    return model


class BertWrapper(torch.nn.Module):
    """ Adds a optional transformer layer and a linear layer on top of BERT.
    """

    def __init__(self, bert_model, output_dim,
                 add_transformer_layer=False, layer_pulled=-1,
                 aggregation="first", add_linear_layer=True,
                 aggregation_num=1, scaling=1.0, norm_to_1=False,
                 multi_aggregation_strategy="first"):
        """
        Wrapper for Bert Model.

        Params:
            bert_model (BertModel): the bert model
            output_dim (int): the dimension of the output
            add_transformer_layer (bool): whether to add a transformer layer on top
            layer_pulled (int): layer from which we pull the outputs; -1 is the last layer
            add_linear_layer (bool): whether to add a linear layer on top
            aggregation (str): how to aggregate the various outputs. options:
                'first' - return the first output
                'max' - return the max of N outputs
                'mean' - return the mean of N outputs
                'restrictedmean' - return the mean of the first aggregation_num outputs
                'none' - return all N outputs
                'multiple' - return subset of the N outputs
            aggregation_num (int): if aggregation is 'multiple', this specifies how
                many outputs to return
            multi_aggregation_strategy (str): if aggregation is 'multiple', this specifies
                which N outputs to take - first or last
        """
        super(BertWrapper, self).__init__()
        self.layer_pulled = layer_pulled
        self.aggregation = aggregation
        self.add_transformer_layer = add_transformer_layer
        # deduce bert output dim from the size of embeddings
        bert_output_dim = bert_model.embeddings.word_embeddings.weight.size(1)

        if add_transformer_layer:
            config_for_one_layer = BertConfig(
                0, hidden_size=bert_output_dim, num_attention_heads=int(
                    bert_output_dim / 64), intermediate_size=3072, hidden_act='gelu')
            self.additional_transformer_layer = BertLayer(config_for_one_layer)
        self.add_linear_layer = add_linear_layer
        if add_linear_layer:
            self.additional_linear_layer = torch.nn.Linear(bert_output_dim, output_dim)
        self.bert_model = bert_model
        self.aggregation_num = aggregation_num
        self.scaling = scaling
        if norm_to_1:
            self.bert_model.state_dict()['encoder.layer.11.output.LayerNorm.weight'].copy_(torch.ones(bert_output_dim))
            self.bert_model.state_dict()['encoder.layer.11.output.LayerNorm.bias'].copy_(torch.zeros(bert_output_dim))
        self.multi_aggregation_strategy = multi_aggregation_strategy

    def forward(self, token_ids, segment_ids, attention_mask):
        output_bert, output_pooler = self.bert_model(
            token_ids, segment_ids, attention_mask)
        # output_bert is a list of 12 (for bert base) layers.
        layer_of_interest = output_bert[self.layer_pulled]
        dtype = next(self.parameters()).dtype
        if self.add_transformer_layer:
            # Follow up by yet another transformer layer
            extended_attention_mask = attention_mask.unsqueeze(1).unsqueeze(2)
            extended_attention_mask = (
                (~extended_attention_mask).to(dtype) * neginf(dtype)
            )
            embedding_layer = self.additional_transformer_layer(
                layer_of_interest, extended_attention_mask)
        else:
            embedding_layer = layer_of_interest

        if self.aggregation == "mean":
            #  consider the average of all the output except CLS.
            # obviously ignores masked elements
            outputs_of_interest = embedding_layer[:, 1:, :]
            mask = attention_mask[:, 1:].type_as(embedding_layer).unsqueeze(2)
            sumed_embeddings = torch.sum(outputs_of_interest * mask, dim=1)
            nb_elems = torch.sum(attention_mask[:, 1:].type(dtype), dim=1).unsqueeze(1)
            embeddings = sumed_embeddings / nb_elems
        elif self.aggregation == "restrictedmean":
            outputs_of_interest = embedding_layer[:, 0:self.aggregation_num, :]
            mask = attention_mask[:, 0:self.aggregation_num].type_as(embedding_layer).unsqueeze(2)
            sumed_embeddings = torch.sum(outputs_of_interest * mask, dim=1)
            nb_elems = torch.sum(attention_mask[:, 0:self.aggregation_num].type(dtype), dim=1).unsqueeze(1)
            embeddings = sumed_embeddings / nb_elems
        elif self.aggregation == "max":
            #  consider the max of all the output except CLS
            outputs_of_interest = embedding_layer[:, 1:, :]
            mask = (~attention_mask[:, 1:]).type(dtype).unsqueeze(2) * neginf(dtype)
            embeddings, _ = torch.max(outputs_of_interest + mask, dim=1)
        elif self.aggregation == 'first':
            # easiest, we consider the output of "CLS" as the embedding
            embeddings = embedding_layer[:, 0, :]
        elif self.aggregation == 'multiple':
            max_sent_len = embedding_layer.size(1)
            if self.multi_aggregation_strategy == 'first':
                embeddings = embedding_layer[:, 0:min(self.aggregation_num, max_sent_len), :]
            else:
                sent_lens = attention_mask.sum(dim=1)
                max_lastn_len = min(self.aggregation_num, max_sent_len)
                embs = []
                for i in range(embedding_layer.size(0)):
                    num_toks = min(self.aggregation_num, sent_lens[i])
                    num_pads = max_lastn_len - num_toks
                    if self.multi_aggregation_strategy == 'last':
                        emb_i = embedding_layer[i, -(num_toks + num_pads):, :]
                    else:
                        emb_0 = embedding_layer[i, 0:1, :]
                        if self.aggregation_num > 1:

                            emb_i = torch.cat(
                                [
                                    emb_0,
                                    embedding_layer[i, -(num_toks + num_pads - 1):, :]
                                ],
                                dim=0
                            )
                        else:
                            emb_i = emb_0
                    embs.append(emb_i)
                embeddings = torch.stack(embs, dim=0)

        else:
            embeddings = embedding_layer

        # We need this in case of dimensionality reduction
        if self.add_linear_layer:
            result = self.additional_linear_layer(embeddings)
        else:
            result = embeddings

        # Sort of hack to make it work with distributed: this way the pooler layer
        # is used for grad computation, even though it does not change anything...
        # in practice, it just adds a very (768*768) x (768*batchsize) matmul
        result = result + 0 * torch.sum(output_pooler)
        return result * self.scaling


def surround(idx_vector, start_idx, end_idx):
    """ Surround the vector by start_idx and end_idx.
    """
    start_tensor = idx_vector.new_tensor([start_idx])
    end_tensor = idx_vector.new_tensor([end_idx])
    return torch.cat([start_tensor, idx_vector, end_tensor], 0)


patterns_optimizer = {
    'additional_layers': ['additional'],
    'top_layer': [
        'additional',
        'bert_model.encoder.layer.11.'],
    'top4_layers': [
        'additional',
        'bert_model.encoder.layer.11.',
        'encoder.layer.10.',
        'encoder.layer.9.',
        'encoder.layer.8'],
    'all_encoder_layers': [
        'additional',
        'bert_model.encoder.layer'],
    'all': [
        'additional',
        'bert_model.encoder.layer',
        'bert_model.embeddings'],
    'polyencoder': [
        'additional',
        'bert_model.encoder.layer',
        'multihead_attention',
        'label_multihead_attention',
        'attention_lins',
        'basic_attention',
        'attention_vecs'
    ],
    'polyencoder_all': [
        'additional',
        'bert_model.encoder.layer',
        'bert_model.embeddings',
        'multihead_attention',
        'label_multihead_attention',
        'attention_lins',
        'basic_attention',
        'attention_vecs'
    ],
    'polyencoder_sans_bert': [
        'additional',
        'multihead_attention',
        'label_multihead_attention',
        'attention_lins',
        'basic_attention',
        'attention_vecs'
    ]
}

def get_adamax_optimizer(models, type_optimization, learning_rate, fp16=False):
    """ Optimizes the network with adamax
    """
    if type_optimization not in patterns_optimizer:
        print('Error. Type optimizer must be one of %s' %
              (str(patterns_optimizer.keys())))
    patterns = patterns_optimizer[type_optimization]
    params = []
    for model in models:
        for n, p in model.named_parameters():
            if any(t in n for t in patterns):
                params.append(p)
    optimizer = torch.optim.Adamax(params, lr=learning_rate)
    if fp16:
        optimizer = fp16_optimizer_wrapper(optimizer)
    print("Adamax optimizer set up")
    return optimizer

def get_bert_optimizer(models, type_optimization, learning_rate, fp16=False,
                       no_decay=False):
    """ Optimizes the network with AdamWithDecay
    """
    if type_optimization not in patterns_optimizer:
        print('Error. Type optimizer must be one of %s' %
              (str(patterns_optimizer.keys())))
    parameters_with_decay = []
    parameters_with_decay_names = []
    parameters_without_decay = []
    parameters_without_decay_names = []
    no_decay = ['bias', 'gamma', 'beta']
    patterns = patterns_optimizer[type_optimization]

    for model in models:
        for n, p in model.named_parameters():
            if any(t in n for t in patterns):
                if any(t in n for t in no_decay):
                    parameters_without_decay.append(p)
                    parameters_without_decay_names.append(n)
                else:
                    parameters_with_decay.append(p)
                    parameters_with_decay_names.append(n)

    print('The following parameters will be optimized WITH decay:')
    print(_ellipse(parameters_with_decay_names, 5, ' , '))
    print('The following parameters will be optimized WITHOUT decay:')
    print(_ellipse(parameters_without_decay_names, 5, ' , '))

    wdecay = 0.0 if no_decay else 0.01
    optimizer_grouped_parameters = [
        {'params': parameters_with_decay, 'weight_decay': wdecay},
        {'params': parameters_without_decay, 'weight_decay': 0.0}
    ]
    optimizer = AdamWithDecay(optimizer_grouped_parameters,
                              lr=learning_rate)

    if fp16:
        optimizer = fp16_optimizer_wrapper(optimizer)

    return optimizer


class AdamWithDecay(Optimizer):
    """ Same implementation as Hugging's Face, since it seems to handle better the
        weight decay than the Pytorch default one.
        Stripped out of the scheduling, since this is done at a higher level
        in ParlAI.
    Params:
        lr: learning rate
        b1: Adams b1. Default: 0.9
        b2: Adams b2. Default: 0.999
        e: Adams epsilon. Default: 1e-6
        weight_decay: Weight decay. Default: 0.01
        max_grad_norm: Maximum norm for the gradients (-1 means no clipping).
                       Default: 1.0
    """

    def __init__(self, params, lr=required,
                 b1=0.9, b2=0.999, e=1e-6, weight_decay=0.01,
                 max_grad_norm=1.0):
        if lr is not required and lr < 0.0:
            raise ValueError('Invalid learning rate: {} - should be >= 0.0'.format(lr))
        if not 0.0 <= b1 < 1.0:
            raise ValueError(
                'Invalid b1 parameter: {} - should be in [0.0, 1.0['.format(b1))
        if not 0.0 <= b2 < 1.0:
            raise ValueError(
                'Invalid b2 parameter: {} - should be in [0.0, 1.0['.format(b2))
        if not e >= 0.0:
            raise ValueError('Invalid epsilon value: {} - should be >= 0.0'.format(e))
        defaults = dict(lr=lr,
                        b1=b1, b2=b2, e=e, weight_decay=weight_decay,
                        max_grad_norm=max_grad_norm)
        super(AdamWithDecay, self).__init__(params, defaults)

    def step(self, closure=None):
        """Performs a single optimization step.
        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
        """
        loss = None
        if closure is not None:
            loss = closure()

        for group in self.param_groups:
            for p in group['params']:
                if p.grad is None:
                    continue
                grad = p.grad.data
                if grad.is_sparse:
                    raise RuntimeError(
                        'Adam does not support sparse gradients, please '
                        'consider SparseAdam instead')

                state = self.state[p]

                # State initialization
                if len(state) == 0:
                    # Exponential moving average of gradient values
                    state['next_m'] = torch.zeros_like(p.data)
                    # Exponential moving average of squared gradient values
                    state['next_v'] = torch.zeros_like(p.data)

                next_m, next_v = state['next_m'], state['next_v']
                beta1, beta2 = group['b1'], group['b2']

                # Add grad clipping
                if group['max_grad_norm'] > 0:
                    clip_grad_norm_(p, group['max_grad_norm'])

                # Decay the first and second moment running average coefficient
                # In-place operations to update the averages at the same time
                next_m.mul_(beta1).add_(1 - beta1, grad)
                next_v.mul_(beta2).addcmul_(1 - beta2, grad, grad)
                update = next_m / (next_v.sqrt() + group['e'])

                # Just adding the square of the weights to the loss function is *not*
                # the correct way of using L2 regularization/weight decay with Adam,
                # since that will interact with the m and v parameters in strange ways.
                #
                # Instead we want to decay the weights in a manner that doesn't interact
                # with the m/v parameters. This is equivalent to adding the square
                # of the weights to the loss with plain (non-momentum) SGD.
                if group['weight_decay'] > 0.0:
                    update += group['weight_decay'] * p.data
                lr = group['lr']

                update_with_lr = lr * update
                p.data.add_(-update_with_lr)
        return loss

    def update_lr(self, new_lr):
        """Update the learning rate of the scheduler"""
        for group in self.param_groups:
            group['lr'] = new_lr

#!/usr/bin/env python3
import torch
from pytorch_pretrained_bert.modeling import BertLayer, BertConfig
from pytorch_pretrained_bert import BertAdam, BertTokenizer, BertModel


class BertWrapper(torch.nn.Module):
    """
        Adds a optional transformer layer and a linear layer on top of Bert
    """

    def __init__(
        self,
        bert_model,
        bert_output_dim,
        output_dim,
        add_transformer_layer=False,
        layer_pulled=-1,
    ):
        super(BertWrapper, self).__init__()
        self.layer_pulled = layer_pulled
        self.add_transformer_layer = add_transformer_layer
        if add_transformer_layer:
            config_for_one_layer = BertConfig(
                0,
                hidden_size=bert_output_dim,
                num_attention_heads=int(bert_output_dim / 64),
                intermediate_size=3072,
                hidden_act="gelu",
            )
            self.additional_transformer_layer = BertLayer(config_for_one_layer)
        self.additional_linear_layer = torch.nn.Linear(bert_output_dim, output_dim)
        self.bert_model = bert_model

    def forward(self, token_ids, segment_ids, attention_mask):
        output_bert, _ = self.bert_model(token_ids, segment_ids, attention_mask)
        # output_bert is a list of 12 (for bert base) layers.
        layer_of_interest = output_bert[self.layer_pulled]
        if self.add_transformer_layer:
            # Follow up by yet another transformer layer
            extended_attention_mask = attention_mask.unsqueeze(1).unsqueeze(2)
            extended_attention_mask = extended_attention_mask.to(
                dtype=next(self.parameters()).dtype
            )  # fp16 compatibility
            extended_attention_mask = (1.0 - extended_attention_mask) * -10000.0
            embeddings = self.additional_transformer_layer(
                layer_of_interest, extended_attention_mask
            )[:, 0, :]
        else:
            embeddings = layer_of_interest[:, 0, :]
        return self.additional_linear_layer(embeddings)


def create_biencoders_from_options(options):
    """
        Create 2 wrappers around Bert, one for the context one for the candidates.
    """
    tokenizer = BertTokenizer.from_pretrained(options["bert_id"])
    context_encoder = BertWrapper(
        BertModel.from_pretrained(options["bert_id"]),
        768,
        768,
        add_transformer_layer=options["add_transformer_layer"],
        layer_pulled=options["pull_from_layer"],
    )
    context_encoder = torch.nn.DataParallel(context_encoder).cuda()
    cand_encoder = BertWrapper(
        BertModel.from_pretrained(options["bert_id"]),
        768,
        768,
        add_transformer_layer=options["add_transformer_layer"],
        layer_pulled=options["pull_from_layer"],
    )
    cand_encoder = torch.nn.DataParallel(cand_encoder).cuda()
    return tokenizer, context_encoder, cand_encoder


def create_crossencoder_from_options(options):
    """
        Create one cross encoder.
    """
    size_bert = 768
    if "large" in options["bert_id"]:
        size_bert = 1024
    tokenizer = BertTokenizer.from_pretrained(options["bert_id"])
    encoder = BertWrapper(
        BertModel.from_pretrained(options["bert_id"]),
        size_bert,
        1,
        add_transformer_layer=options["add_transformer_layer"],
        layer_pulled=options["pull_from_layer"],
    )
    encoder = torch.nn.DataParallel(encoder).cuda()
    return tokenizer, encoder


patterns_optimizer = {
    "additional_layers": ["additional"],
    "top_layer": ["additional", "bert_model.encoder.layer.11."],
    "top4_layers": [
        "additional",
        "bert_model.encoder.layer.11.",
        "encoder.layer.10.",
        "encoder.layer.9.",
        "encoder.layer.8",
    ],
    "all_encoder_layers": ["additional", "bert_model.encoder.layer"],
    "all": ["additional", "bert_model.encoder.layer", "bert_model.embeddings"],
}


def get_bert_optimizer(
    models, type_optimization, number_iterations, proportion_warmup, learning_rate
):
    """
        Provides an optimizer already configured with weight decay for the parameters
        that need it. Weight decay is left standard at 0.01
    """
    if type_optimization not in patterns_optimizer:
        print(
            "Error. Type optimizer must be one of %s" % (str(patterns_optimizer.keys()))
        )
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

    print("The following parameters will be optimized WITH decay:")
    print(parameters_with_decay_names)
    print("The following parameters will be optimized WITHOUT decay:")
    print(parameters_without_decay_names)

    optimizer_grouped_parameters = [
        {'params': parameters_with_decay, 'weight_decay_rate': 0.01},
        {'params': parameters_without_decay, 'weight_decay_rate': 0.0},
    ]
    optimizer = BertAdam(
        optimizer_grouped_parameters,
        lr=learning_rate,
        warmup=proportion_warmup,
        t_total=number_iterations,
    )
    return optimizer


def sentences_to_embedding(bert_model, bert_tokenizer, sentences):
    """ Transform a list of N sentences to a N x M tensor.
        This assumes the list is small enough to fit on your GPU.
        This is not efficient but can be used for debugging or eval.
    """
    paired = [(s, None) for s in sentences]
    return sentences_pairs_to_embedding(bert_model, bert_tokenizer, paired)


def sentences_pairs_to_embedding(bert_model, bert_tokenizer, sentences):
    """ Transform a list of N couples of sentences to a N x M tensor.
        sentences is a list of tuples (sentence1, sentence2)
        This assumes the list is small enough to fit on your GPU.
        This is not efficient but can be used for debugging or eval.
    """
    token_ids = []
    segment_ids = []
    for s1, s2 in sentences:
        toks, segs = sentences_to_ids(bert_tokenizer, s1, s2)
        token_ids.append(toks)
        segment_ids.append(segs)
    batch = ids_to_input(token_ids, segment_ids)
    output_bert, _ = bert_model(
        batch[0], batch[1], attention_mask=batch[2], output_all_encoded_layers=False
    )
    return torch.squeeze(output_bert[:, 0, :], 1)


def sentences_to_embedding_wrapper(bert_wrapper, bert_tokenizer, sentences, cap=511):
    """ same as sentences_to_embedding() but for a bert wrapper.
    """
    paired = [(s, None) for s in sentences]
    return sentences_pairs_to_embedding_wrapper(
        bert_wrapper, bert_tokenizer, paired, cap
    )


def sentences_pairs_to_embedding_wrapper(
    bert_wrapper, bert_tokenizer, sentences, cap=511
):
    """ Same as sentences_pairs_to_embedding but for a wrapper
    """
    token_ids = []
    segment_ids = []
    for s1, s2 in sentences:
        toks, segs = sentences_to_ids(bert_tokenizer, s1, s2)
        if toks.size()[1] > cap:
            start = toks.size()[1] - cap
            toks = toks[0:1, start : toks.size()[1]]
            segs = segs[0:1, start : segs.size()[1]]
        token_ids.append(toks)
        segment_ids.append(segs)
    batch = ids_to_input(token_ids, segment_ids)
    return bert_wrapper(batch[0], batch[1], batch[2])


def sentences_to_ids(tokenizer, text1, text2=None, produce_segments=True):
    """Create the token index and segment index.

         The convention in BERT is:
        (a) For sequence pairs:
            tokens:   [CLS] is this jack ##son ##ville ? [SEP] no it is not . [SEP]
            type_ids: 0   0  0    0    0     0       0 0    1  1  1  1   1 1
        (b) For single sequences: (when text2 is null)
            tokens:   [CLS] the dog is hairy . [SEP]
            type_ids: 0   0   0   0  0     0 0
    """
    tokenized_text1 = ["[CLS]"] + tokenizer.tokenize(text1) + ["[SEP]"]
    tokenized_text2 = tokenizer.tokenize(text2) + ["[SEP]"] if text2 is not None else []
    tokens = tokenized_text1 + tokenized_text2
    tokens_id = tokenizer.convert_tokens_to_ids(tokens)
    tokens_tensor = torch.tensor([tokens_id])
    if produce_segments == False:
        return tokens_tensor
    segments = [0] * len(tokenized_text1) + [1] * len(tokenized_text2)
    segments_tensor = torch.tensor([segments])
    return tokens_tensor, segments_tensor


def ids_to_input(list_tokens_id, list_segments_id):
    """ transform a list of tokens id and a list of segments id into
        3 rectangular cuda.LongTensor of size size_batch x max_length_sentence.
        token_ids, segment_ids and mask
    """
    max_len = max([len(v[0]) for v in list_tokens_id])
    bsize = len(list_tokens_id)

    tokens_id = torch.zeros(bsize, max_len, dtype=torch.long)
    segments_id = torch.zeros(bsize, max_len, dtype=torch.long)
    mask = torch.zeros(bsize, max_len, dtype=torch.long)

    for i, vec in enumerate(list_tokens_id):
        seq_length = len(vec[0])
        tokens_id[i, 0:seq_length] = vec[0]
        segments_id[i, 0:seq_length] = list_segments_id[i][0]
        mask[i, 0:seq_length] = torch.ones(seq_length, dtype=torch.long)

    return tokens_id.cuda(), segments_id.cuda(), mask.cuda()

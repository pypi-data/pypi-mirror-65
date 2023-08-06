#!/usr/bin/env python3
import unittest
import torch

from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM
from bert_helpers import sentences_to_ids, ids_to_input, sentences_pairs_to_embedding


class TestBertHelpers(unittest.TestCase):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased').cuda()

    def test_tokenization1(self):
        sentence = "The cat is on the kitchen table"
        toks_ids, segment_ids = sentences_to_ids(self.tokenizer, sentence)
        self.assertEqual(len(toks_ids[0]), 9)
        self.assertEqual(len(segment_ids[0]), 9)
        self.assertEqual(torch.sum(segment_ids), 0)
        self.assertEqual(toks_ids[0][0].item(), 101)
        self.assertEqual(toks_ids[0][8].item(), 102)

    def test_tokenization2(self):
        s1 = "The cat is on the kitchen table"
        s2 = "hello"
        toks_ids, segment_ids = sentences_to_ids(self.tokenizer, s1, s2)
        self.assertEqual(torch.sum(segment_ids), 2)

    def test_padding(self):
        tokens_id = [
            torch.tensor([[0, 1, 2, 3]], dtype=torch.long),
            torch.tensor([[0, 1]], dtype=torch.long),
        ]
        segments_id = [
            torch.tensor([[0, 0, 0, 0]], dtype=torch.long),
            torch.tensor([[0, 1]], dtype=torch.long),
        ]
        o1, o2, o3 = ids_to_input(tokens_id, segments_id)
        t1 = torch.tensor([[0, 1, 2, 3], [0, 1, 0, 0]])
        t2 = torch.tensor([[0, 0, 0, 0], [0, 1, 0, 0]])
        t3 = torch.tensor([[1, 1, 1, 1], [1, 1, 0, 0]])
        self.assertTrue(torch.equal(o1.cpu(), t1))
        self.assertTrue(torch.equal(o2.cpu(), t2))
        self.assertTrue(torch.equal(o3.cpu(), t3))

    def test_consistency(self):
        self.model.eval()
        pair1 = ("Small sentence.", "Small")
        pair2 = ("This is a much bigger sentence", "Big")
        embed1 = sentences_pairs_to_embedding(
            self.model, self.tokenizer, [pair1, pair2]
        )
        embed2 = sentences_pairs_to_embedding(self.model, self.tokenizer, [pair1])
        print(embed1[0, 0:5])
        print(embed2[0, 0:5])
        self.assertTrue(torch.equal(embed1[0].cpu(), embed2[0].cpu()))


if __name__ == '__main__':
    unittest.main()

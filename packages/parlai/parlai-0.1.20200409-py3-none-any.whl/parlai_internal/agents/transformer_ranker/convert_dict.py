# import torch
#
#
# to_write = '/private/home/edinan/ParlAI/data/models/wiz_experiments/paris/old_dict'
#
# with open(to_write, 'w') as f:
#     model = torch.load('/private/home/edinan/ParlAI/data/models/wiz_experiments/paris/reddit_model')
#     for k, v in model['word_dict']['words'].items():
#         fake_freq = 1000000 - int(v)
#         f.write(str(k)+'\t'+str(v)+'\n')

import re

def tokenize(string):
    return re.sub(r'(\W)', r' \1 ', string).split()

import pdb; pdb.set_trace()

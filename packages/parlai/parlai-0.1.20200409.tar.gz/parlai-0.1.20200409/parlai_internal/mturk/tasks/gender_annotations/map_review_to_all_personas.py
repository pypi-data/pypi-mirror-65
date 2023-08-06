# TODO: reverse engineer the map from personas to original
from parlai_internal.tasks.convai2_review.contractions_list import (
    contractions_list,
    punctuation_list,
    contraction_spaces,
    contraction_left_spaces,
    contraction_right_spaces,
)

import json
from copy import deepcopy
import os
from tqdm import tqdm

DEFAULT_SAVE_DIR = '/private/home/edinan/ParAI/data/'
ASSESSED = '/private/home/edinan/ParlAI/parlai_internal/mturk/tasks/gender_annotations/save_assess.json'
MAP = '/private/home/edinan/ParlAI/data/convai2_distinct_personas/persona_unique_map.json'

with open(ASSESSED, 'rb') as f:
    completed = json.load(f)

with open(MAP, 'rb') as f:
    persona_map = json.load(f)

# create a reverse map
reverse_map = {}

# get a reverse map with annotations
for persona_dct in tqdm(completed):
    persona = ' '.join(persona_dct['persona'])
    if persona in persona_map:
        all_personas = persona_map[persona]
        for sub_persona in all_personas:
            sub_persona_key = ' '.join(sub_persona)
            reverse_map[sub_persona_key] = deepcopy(persona_dct)
    else:
        print('wtf')
        import pdb; pdb.set_trace()

with open('/private/home/edinan/ParlAI/parlai_internal/mturk/tasks/gender_annotations/all_personas_map.json', 'w') as f:
    json_dump = json.dumps(reverse_map)
    f.write(json_dump)


import pdb; pdb.set_trace()
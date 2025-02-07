"""
count rel lens in molweni

"""

import os
import json
from collections import Counter

current_folder=os.getcwd()

# annotation_path = current_folder + '/stac/stac_squished_data/train_data.json'
# save_path = '/home/kate/minecraft_utils/llm_annotator/stac/stac_squished_corrected/train_data.json'

# annotation_path = current_folder + '/stac/stac_squished_corrected/test_data.json'

# annotation_path = current_folder + '/stac/stac_linguistic/train_data.json'
# save_path = '/home/kate/minecraft_utils/llm_annotator/stac/stac_linguistic_corrected/train_data.json'

mol_path = current_folder + '/molweni/molweni_clean_test50.json'

with open(mol_path, 'r') as j:
    jfile = json.load(j)
    data = jfile

dists = []
for d in data:
    did = d['id']
    rels = d['relations']
    for rel in rels:
        dist = rel['y'] - rel['x']
        if dist > 4:
            print(did)
        dists.append(dist)


lens = Counter(dists)

print(len(dists))
print(lens)


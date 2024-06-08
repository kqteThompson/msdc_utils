"""
Takes the minecraft data and preprocesses the same way as 
for the BERTLine local model. 

1. open text and labels. 
2. convert speaker label, moves, relation type
3. if train, dropout 
4. create jsonl


FOR STAC FLAT TRAIN
68,526 CANDIDATES
10,878 CONNECTED
57,648 NON CONNECTED
KEEP 34K
"""

import os
import jsonlines
import pickle
import numpy as np
from collections import Counter
import time



map_rels = {0:'COM', 1:'CONTR', 3:'CORR', 4:'QAP', 5:'ACK', 6:'ELAB', 7:'CLARIFQ', 8:'COND', 9:'CONTIN', 10:'RES', 11:'EXPL', 12:'QELAB',
                 13:'ALT', 14:'NARR', 15:'BACK', 16:'PAR', 17:'SEQ', -1:'NONE'}


current_folder=os.getcwd()

train_text_path = current_folder + '/bert_pickles/flat_input_text_test.pkl'
train_labels_path = current_folder + '/bert_pickles/flat_input_labels_test.pkl'

# test_text_path = current_folder + '/bert_pickles/test_input_text.pkl'
# test_labels_path = current_folder + '/bert_pickles/test_input_labels.pkl'

save_path = current_folder + '/local_model_flat_test.jsonl'

# with open(data_path, 'r') as j:
#     jfile = json.load(j)
#     games = jfile

with open(train_text_path, 'rb') as f:
    text = pickle.load(f)

with open(train_labels_path, 'rb') as f:
    labels = pickle.load(f)

assert len(labels) == len(text)

print('number of samples {} '.format(len(text)))
#check balance 
# counts = Count
# sample_list.append(samp)er([l[3] for l in train_labels])
# print(counts)

# start = time.time()

# #dropout for 
# # num_keep = 92,000
# num_keep = 34000
# arglist = [i for i,e in enumerate(labels) if e[3] == 0]
# indices = sorted(np.random.choice(arglist, num_keep))

# one_indices = [i for i,e in enumerate(labels) if e[3] == 1]
# print(len(arglist))
# print(len(indices))
# print(Counter([l[3] for l in labels]))


# indices.extend(one_indices)

# all_indices = sorted(indices)
# drop_labels = []
# drop_text = []
# for i in all_indices:
#     drop_labels.append(labels[i])
#     drop_text.append(text[i])

# #check balance 
# counts = Counter([l[3] for l in drop_labels])
# print(counts)
# end = time.time()
# print(end - start)

### PUT MOVES AND RELATIONS IN ORDER

# sample_list = []

# for i, edus in enumerate(drop_text):
#     samp = {}
#     edu_one = edus[0]
#     edu_two = edus[1]
#     st = edu_one + '\n' + edu_two
#     relation = map_rels[drop_labels[i][4]]
#     samp["PS"] = relation
#     samp["sample"] = st
#     sample_list.append(samp)

# with jsonlines.open(save_path, mode='w') as writer:
#     for sample in sample_list:
#         writer.write(sample)


##For non-dropped sets
sample_list = []

counts = Counter([l[3] for l in labels])
print(counts)

for i, edus in enumerate(text):
    samp = {}
    edu_one = edus[0]
    edu_two = edus[1]
    st = edu_one + '\n' + edu_two
    relation = map_rels[labels[i][4]]
    samp["PS"] = relation
    samp["sample"] = st
    sample_list.append(samp)

with jsonlines.open(save_path, mode='w') as writer:
    for sample in sample_list:
        writer.write(sample)


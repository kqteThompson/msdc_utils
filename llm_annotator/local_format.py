"""
Takes the minecraft data and preprocesses the same way as 
for the BERTLine local model. 

1. open text and labels. 
2. convert speaker label, moves, relation type
3. if train, dropout 
4. create jsonl
"""

import os
import json
import pickle
import numpy as np
from collections import Counter
import time



def format_edu(edu_string):
    """
    Takes an EDU string and returns <speaker> 
    and !! need to add edu numbers!
    """
    return None

map_rels = {0:'COM', 1:'CONTR', 2:'CORR', 3:'QAP', 4:'ACK', 5:'ELAB', 6:'CLARIFQ', 7:'COND', 8:'CONTIN', 9:'RES', 10:'EXPL', 11:'QELAB',
                 12:'ALT', 13:'NARR', 14:'CONFQ', 15:'SEQ', -1:'NONE'}


current_folder=os.getcwd()

train_text_path = current_folder + '/bert_pickles/train_input_text.pkl'
train_labels_path = current_folder + '/bert_pickles/train_input_labels.pkl'
val_text_path = current_folder + '/bert_pickles/val_input_text.pkl'
val_lables_path = current_folder + '/bert_pickles/val_input_labels.pkl'

save_path = current_folder + '/local_model_test.json'

# with open(data_path, 'r') as j:
#     jfile = json.load(j)
#     games = jfile

with open(train_text_path, 'rb') as f:
    text = pickle.load(f)

with open(train_labels_path, 'rb') as f:
    labels = pickle.load(f)

assert len(labels) == len(text)

#labels = [l[4] for l in train_labels]

#check balance 
# counts = Counter([l[3] for l in train_labels])
# print(counts)

# start = time.time()

# #dropout for 
# num_keep = 92000
# arglist = [i for i,e in enumerate(train_labels) if e[3] == 0]
# indices = sorted(np.random.choice(arglist,len(arglist)-num_keep))


# labels = [e for i,e in enumerate(train_labels) if i not in indices]

# #check balance 
# counts = Counter([l[3] for l in labels])
# print(counts)
# end = time.time()
# print(end - start)

### PUT MOVES AND RELATIONS IN ORDER

for i, edus in enumerate(text):
    edu_one = edus[0]
    edu_two = edus[1]
    relation = map_rels[labels[i][4]]


"""
Takes the minecraft data and preprocesses the same way as 
for the BERTLine local model. 

1. open text and labels. 
2. convert speaker label, moves, relation type
3. if train, dropout 
4. create jsonl
"""

import os
import jsonlines
import pickle
import numpy as np
from collections import Counter
import time

def is_nl(edu):
    """
    if every word in alphanumeric and has len 5
    """
    nl = 1
    words = edu.split(' ')
    # print(words)
    # print(words)
    for word in [w for w in words if w != '']:
        if not contains_number(word) or len(word) < 5:
            nl = 0
            break
    # print(nl)
    return nl

def contains_number(string):
    return any(char.isdigit() for char in string)

def decode(tok_str):
    """
    takes a list bert tokens and changes them back to coordinates.
    """
    zdict = {'a':'-5', 'e' : '-4', 'i':'-3', 'o':'-2', 'u':'-1', 'p':'0', 
             'q':'1', 'r':'2', 'x': '3', 'y':'4', 'z':'5'}
    xdict = {'b': '-5', 'c' :'-4', 'd' : '-3', 'f' : '-2', 'g' : '-1', 'h':'0', 
             'j':'1', 'k':'2', 'l':'3', 'm':'4', 'n':'5'}
    colors = {'r' :'red', 'b':'blue', 'g':'green', 'o':'orange', 'y':'yellow', 'p':'purple'}
    # action = {'0' : 'pick', '1': 'place'}
    decoded = []
    for tok in tok_str.split():
        # print(tok)
        if tok[0] == '0':
            new_string = 'pick ' +  xdict[tok[2]] + ' ' + tok[3] + ' ' + zdict[tok[4]]
        else:
            new_string = 'place ' + colors[tok[1]] + ' ' +  xdict[tok[2]] + ' ' + tok[3] + ' ' + zdict[tok[4]]
        decoded.append(new_string)
    moves_str = ', '.join(decoded)
    return moves_str

def process_edu(edu):
    """
    split off speaker
    check if nl
    """
    if '<Arch>' in edu:
        edu_string = edu
    else:
        num = edu.split('<')[0].strip()
        body = edu.split('>')[1].strip()
        if is_nl(body):
            new_body = decode(body)
            edu_string = num + ' <Buil> ' + new_body
        else: 
            edu_string = edu
    return edu_string

map_rels = {0:'COM', 1:'CONTR', 2:'CORR', 3:'QAP', 4:'ACK', 5:'ELAB', 6:'CLARIFQ', 7:'COND', 8:'CONTIN', 9:'RES', 10:'EXPL', 11:'QELAB',
                 12:'ALT', 13:'NARR', 14:'CONFQ', 15:'SEQ', -1:'NONE'}


current_folder=os.getcwd()

train_text_path = current_folder + '/bert_pickles/train_input_text.pkl'
train_labels_path = current_folder + '/bert_pickles/train_input_labels.pkl'
val_text_path = current_folder + '/bert_pickles/val_input_text.pkl'
val_labels_path = current_folder + '/bert_pickles/val_input_labels.pkl'
test_text_path = current_folder + '/bert_pickles/test_input_text.pkl'
test_labels_path = current_folder + '/bert_pickles/test_input_labels.pkl'

save_path = current_folder + '/local_model_test.jsonl'

# with open(data_path, 'r') as j:
#     jfile = json.load(j)
#     games = jfile

with open(test_text_path, 'rb') as f:
    text = pickle.load(f)

with open(test_labels_path, 'rb') as f:
    labels = pickle.load(f)

assert len(labels) == len(text)


#check balance 
# counts = Count
# sample_list.append(samp)er([l[3] for l in train_labels])
# print(counts)

# start = time.time()

# #dropout for 
# # num_keep = 92,000
# num_keep = 102000
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

sample_list = []

for i, edus in enumerate(text):
    samp = {}
    edu_one = process_edu(edus[0])
    edu_two = process_edu(edus[1])
    st = edu_one + '\n' + edu_two
    relation = map_rels[labels[i][4]]
    samp["PS"] = relation
    samp["sample"] = st
    sample_list.append(samp)

with jsonlines.open(save_path, mode='w') as writer:
    for sample in sample_list:
        writer.write(sample)
        writer.write(sample)


# #check balance 
# counts = Counter([l[3] for l in drop_labels])
# print(counts)
# end = time.time()
# print(end - start)

# ### PUT MOVES AND RELATIONS IN ORDER

# sample_list = []

# for i, edus in enumerate(drop_text):
#     samp = {}
#     edu_one = process_edu(edus[0])
#     edu_two = process_edu(edus[1])
#     st = edu_one + '\n' + edu_two
#     relation = map_rels[drop_labels[i][4]]
#     samp["PS"] = relation
#     samp["sample"] = st
#     sample_list.append(samp)


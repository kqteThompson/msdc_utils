import os
import csv
import numpy as np
import pickle
import jsonlines
from collections import defaultdict, Counter
import pandas

""""
makes a list of lists of llama outputs to 
be input to a narrative arc algorithm
"""


def get_links(sample_string, sample_index):
    """
    takes a sample string and returns a list of attach tuples
    and a list of rel type strings
    """
    #MINECRAFT labels
    labels = ['COM','CONTR','CORR','QAP','ACK','ELAB','CLARIFQ','COND','CONTIN',
              'RES','EXPL','QELAB','ALT','NARR','CONFQ','SEQ']
    
    # #STAC labels
    # labels = ['COM', 'CONTR', 'CORR', 'QAP', 'ACK', 'ELAB', 'CLARIFQ', 'COND', 'CONTIN', 'RES', 'EXPL', 
    #             'QELAB','ALT', 'NARR', 'BACK', 'PAR', 'SEQ']

    split_list = [st.strip() for st in sample_string.split(' ')]
   
    rel_list = []
    attach_list = []
    for a in split_list:
        s_tuple = None
        rel = None
        try:
            s = a.split('(')[1].split(')')[0].split(',')
            r = a.split('(')[0].strip()
        except IndexError:
            print('split error at ', sample_index)
        else:
            try:
                s_tuple = (int(s[0]), int(s[1]))
            except IndexError:
                print('split error at ', sample_index)
            except ValueError:
                print('value error at ', sample_index)
            if r in labels:
                #make sure the label is well-formed 
                rel = r
    
        if rel != None and s_tuple != None and (s_tuple[1] - s_tuple[0]) <= 10:
        # if rel != None and s_tuple != None:
            attach_list.append((int(s[0]), int(s[1])))
            rel_list.append(r)
    
    #re-construct the full list 
    #a list of tuples (rel, x, y)
    #but don't allow doubles!!
    full_list = []
    endpoints = [] 
    for i, r in enumerate(attach_list):
        if r not in endpoints:
            endpoints.append(r)
            full_list.append((rel_list[i], r[0], r[1]))   
    return full_list
    
#MINECRAFT LABELS
# labels = ['COM','CONTR','CORR','QAP','ACK','ELAB','CLARIFQ','COND','CONTIN',
#               'RES','EXPL','QELAB','ALT','NARR','CONFQ','SEQ','NULL']

map_relations = {'COM':0, 'CONTR':1, 'CORR':2, 'QAP':3, 'ACK':4,'ELAB':5,
                 'CLARIFQ':6, 'COND':7, 'CONTIN':8, 'RES':9, 'EXPL':10, 'QELAB':11,
                 'ALT':12, 'NARR':13, 'CONFQ':14, 'SEQ':15, 'NULL':16}


current_folder=os.getcwd()


gold_path = current_folder + '/msdc_llama/parser_val_moves_15.jsonl'
pred_path = current_folder + '/msdc_llama/val-output-generate-file-llama3.txt'

save_path = current_folder + '/msdc_llama/val-output-generate-2p-format.pkl'


##get pred output list
with open(pred_path, 'r') as txt:
    text = txt.read().split('\n')

pred_outputs = []

new_dialogue = 0
for t in text:
    if 'Structure:' in t:
        if len(t.split('Structure:')[1].strip()) == 0:
            new_dialogue = 1
    if '### DS:' in t:
        sample = t.split('### DS:')[1].strip()
        if new_dialogue == 1:
            pred_outputs.append((sample, 1))
            new_dialogue = 0
        else:
            pred_outputs.append((sample, 0))

#print(pred_outputs)

assert len([p for p in pred_outputs if p[1] == 1]) == 100


# #get gold sample list
# gold_outputs = []

# with jsonlines.open(gold_path) as reader:
#     for obj in reader:
#         gold_outputs.append(obj['PS'])

llama_preds = []
dnum = -1
for i, pred in enumerate(pred_outputs):
    #get dialogue start 
    if pred[1] == 1:
        dnum += 1
    pred_split = get_links(pred[0], i)
    for p in pred_split:
        ll = [dnum, p[1], p[2], 1, map_relations[p[0]]]
        llama_preds.append(ll)

with open(save_path, 'wb') as f:
    pickle.dump(llama_preds, f)
        


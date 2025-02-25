import os
import csv
import numpy as np
import pickle
import jsonlines
from collections import defaultdict, Counter
import pandas
from sklearn.metrics import classification_report

"""
re-formats a llamipa output to [ind, x, y, reltype] format to count MPDUs in llamipa_mpdus.ipynb
"""

def get_links(sample_string, sample_index):
    """
    takes a sample string and returns a list of attach tuples
    and a list of rel type strings
    """
    #MINECRAFT labels
    labels = ['COM','CONTR','CORR','QAP','ACK','ELAB','CLARIFQ','COND','CONTIN',
              'RES','EXPL','QELAB','ALT','NARR','CONFQ','SEQ']

    split_list = [st.strip() for st in sample_string.split(' ')]
   
    rel_list = []
    attach_list = []
    multi_y_list = []
    bad = 0
    good = 0
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
    
        if rel != None and s_tuple != None and (s_tuple[1] - s_tuple[0]) <= 15:
        # if rel != None and s_tuple != None:
            attach_list.append((int(s[0]), int(s[1])))
            rel_list.append(r)
            multi_y_list.append(int(s[1]))
            good += 1
        else:
            bad += 1
    
    ##get double ys
    y_counts = Counter(multi_y_list)
    mpdus_count = [r[0] for r in y_counts.items() if r[1] > 1] 
   
    #re-construct the full list 
    #a list of tuples (rel, x, y)
    #but don't allow doubles!!
    full_list = []
    endpoints = [] 
    for i, r in enumerate(attach_list):
        if r not in endpoints:
            endpoints.append(r)
            full_list.append((rel_list[i], r[0], r[1]))   
    return endpoints, full_list, [good, bad], mpdus_count
    
#MINECRAFT LABELS
# labels = ['COM','CONTR','CORR','QAP','ACK','ELAB','CLARIFQ','COND','CONTIN',
#               'RES','EXPL','QELAB','ALT','NARR','CONFQ','SEQ','NULL']


current_folder=os.getcwd()

gold_path = current_folder + '/msdc_llama/parser_test_moves_15.jsonl'
pred_path = current_folder + '/msdc_llama/test-output-generate-file-llama3.txt'


#get pred output list
with open(pred_path, 'r') as txt:
    text = txt.read().split('\n')

pred_outputs = []

# for t in text:
#     if '### DS:' in t:
#         #print(t)
#         sample = t.split('### DS:')[1].strip()
#         pred_outputs.append(sample)

##new way to get predicted outputs:
in_new_sample = 0
for t in text:
    if '<|begin_of_text|>' in t:
        in_new_sample = 1
        #start looking for '### DS:'
    if '### DS:' in t and in_new_sample == 1:
        sample = t.split('### DS:')[1].strip()
        pred_outputs.append(sample)
        in_new_sample = 0

print(len(pred_outputs))

#get gold sample list
gold_outputs = []

with jsonlines.open(gold_path) as reader:
    for obj in reader:
        gold_outputs.append(obj['PS'])

doubles = 0
bad_output = 0
good_output = 0

gold_mpdus = []
pred_mpdus = []
same_target = []

for i, s in enumerate(pred_outputs):
    #first do attachments
    # pred_att, pred_all = get_links(s, i)
    # gold_att, gold_all = get_links(gold_outputs[i], i)


    # print(i)
    # print(s)
    # print(gold_outputs[i])
    # print('--------------------')

    pred_att, pred_all, malform, pmpdus = get_links(s, i)
    gold_att, gold_all, malform, gmpdus = get_links(gold_outputs[i], i)

    bad_output += malform[1]
    good_output += malform[0]

    # print("GOLD:", gold_all)
    # print("PRED:", pred_all)
    # print('-------')

    # print("GOLD att:", gold_att)
    # print("PRED att:", pred_att)
    # print('-------')

    # print('gold MPDUs:', gold_mpdus)
    # print('pred MPDUs:', pred_mpdus)

    if len(gmpdus) > 0:
        gold_mpdus.extend(gmpdus)
        # print(gmpdus)

    if len(pmpdus) > 0:
        pred_mpdus.extend(pmpdus)
        # print(pmpdus)

    if len(pmpdus) > 0 and len(gmpdus) > 0:
        common = np.intersect1d(pmpdus, gmpdus)
        same_target.extend(common)
    #     print(common)
    # print('-------------------------')


print('total gold mpdus: ', len(gold_mpdus))

print('total pred mpdus: ', len(pred_mpdus))

print('total common targets: ', len(same_target))


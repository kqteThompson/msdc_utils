import os
import sys
import numpy as np
import pickle
import pandas
import jsonlines
from collections import defaultdict, Counter


def get_links(sample_string, sample_index):
    """
    takes a sample string and returns a list of attach tuples
    and a list of rel type strings
    """
    #MINECRAFT labels
    labels = ['COM','CONTR','CORR','QAP','ACK','ELAB','CLARIFQ','COND','CONTIN',
              'RES','EXPL','QELAB','ALT','NARR','CONFQ','SEQ']
    
    #STAC labels
    # labels = ['COM', 'CONT', 'CORR', 'QAP', 'PAR', 'ACK',
    #         'ELAB', 'CLARIFQ', 'COND', 'CONT', 'RES', 'EXPL',
    #         'QELAB', 'ALT', 'NARR', 'BACK', 'SEQ']
    
    
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
    
        # if rel != None and s_tuple != None and (s_tuple[1] - s_tuple[0]) <= 10:
        if rel != None and s_tuple != None:
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
    return endpoints, full_list
    

def get_dist(rel_string):
    distance = int(rel_string[2]) - int(rel_string[1])
    return distance

#MINECRAFT LABELS
# labels = ['COM','CONTR','CORR','QAP','ACK','ELAB','CLARIFQ','COND','CONTIN',
#               'RES','EXPL','QELAB','ALT','NARR','CONFQ','SEQ','NULL']


current_folder=os.getcwd()


gold_path = current_folder + '/msdc_llama/parser_test_moves_15.jsonl'
# gold_path = current_folder + '/msdc_llama/parser_val_moves_15.jsonl'
# pred_path = current_folder + '/msdc_llama/test-output-ll3.txt'
pred_path = current_folder + '/msdc_llama/test-output-generate-file-llama3.txt'


# gold_path = current_folder + '/stac_llama/parser_test_stacsquish_15.jsonl'
# pred_path = current_folder + '/stac_llama/test-output-stac-ll2-file.txt'

#get pred output list
with open(pred_path, 'r') as txt:
    text = txt.read().split('\n')

pred_outputs = []

for t in text:
    if '### DS:' in t:
        sample = t.split('### DS:')[1].strip()
        pred_outputs.append(sample)

#get gold sample list
gold_outputs = []

with jsonlines.open(gold_path) as reader:
    for obj in reader:
        gold_outputs.append(obj['PS'])

tp_distances = []
fp_distances = []
fn_distances = []
gold_distances = []

for i, s in enumerate(pred_outputs):
    #first do attachments
    pred_att, pred_all = get_links(s, i)
    gold_att, gold_all = get_links(gold_outputs[i], i)

    gold_narrations = [g for g in gold_all if g[0] == 'NARR']
    pred_narrations = [g for g in pred_all if g[0] == 'NARR']
    
    for narr in pred_narrations:
        if narr in gold_narrations:
            tp_distances.append(get_dist(narr))
        else:
            fp_distances.append(get_dist(narr))
    
    for narr in gold_narrations:
        gold_distances.append(get_dist(narr))
        if narr not in pred_narrations:
            fn_distances.append(get_dist(narr))

print('max gold distance: ', max(gold_distances))

# #now we have lists of distances for all predictions

tp_counts = Counter(tp_distances)
fp_counts = Counter(fp_distances)
fn_counts = Counter(fn_distances)
gold_counts = Counter(gold_distances)

labels = [d for d in range(1,16)]
head = ['gold', 'tp', 'fn', 'fp', 'F1']
data = [] #a list of lists

for d in labels:
    row = []
    for count_list in [gold_counts, tp_counts, fn_counts, fp_counts]:
        num = [c[1] for c in count_list.items() if c[0] == d]
        if len(num) > 0:
            row.append(num[0])
        else:
            row.append(0)
        #calculate distance F1
    if row[1] != 0:
        microf1 = round(row[1]/(row[1] + 0.5*(row[3] + row[2])), 2)
    else:
        microf1 = 0.0
    row.append(microf1)

    data.append(row)

sys.stdout = open('Narrations_llama3.txt', 'w')
print('Llama 3 Narration predictions')
print('                                         ')
print(pandas.DataFrame(data, labels, head))
print('                                          ')
sys.stdout.close()


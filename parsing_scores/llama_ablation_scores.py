import os
import csv
import numpy as np
import pickle
import jsonlines
from collections import defaultdict, Counter
import pandas
from sklearn.metrics import classification_report


"""
For two-class ablations, eg (NULL, NARR) or (NULL, CORR)
"""

def get_links(sample_string, sample_index):
    #MINECRAFT labels

    num_rels = 0
    num_nulls = 0
    labels = ['COM','CONTR','CORR','QAP','ACK','ELAB','CLARIFQ','COND','CONTIN',
              'RES','EXPL','QELAB','ALT','NARR','CONFQ','SEQ', 'NONE']
    # labels = ['NARR']


    split_list = [st.strip() for st in sample_string.split(' ')]
    #print(split_list)
   
    attach_list = []
    for a in split_list:
        if a == 'NONE':
            attach_list.append('NONE')
            num_nulls += 1
        else: 
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
                num_rels += 1
                attach_list.append(rel + '(' + s[0] + ',' + s[1] +')')
    #print(attach_list)
    # if len(attach_list) == 0:
    #     attach_list.append('NONE')
    #     num_nulls += 1
    return attach_list, num_rels, num_nulls
    
current_folder=os.getcwd()

gold_path = current_folder + '/ablation/parser_val_moves_15_corr+narr_ablation.jsonl'
pred_path = current_folder + '/ablation/val-output-file-corrnarr.txt'

#get pred output list
with open(pred_path, 'r') as txt:
    text = txt.read().split('\n')

pred_outputs = []
pred_contexts = []
context = []

for t in text:
    if '### DS:' in t:
        sample = t.split('### DS:')[1].strip()
        pred_outputs.append(sample)
        pred_contexts.append(context)
        context = []
    else:
        context.append(t)
    

#get gold sample list
gold_outputs = []

with jsonlines.open(gold_path) as reader:
    for obj in reader:
        gold_outputs.append(obj['PS'])

att_f1_l = []
att_prec_l = []
att_rec_l = []
total_attach_tp = 0
total_attach_fp = 0
total_attach_fn = 0

gold_null = 0
gold_rel = 0
pred_null = 0
pred_rel = 0


false_positive_check = []
false_negative_check = []
num_fp = 0
for i, s in enumerate(pred_outputs):

    # print(i)
    # print(s)
    # print('------------')
    pred_att, pr, pn = get_links(s, i)
    gold_att, gr, gn = get_links(gold_outputs[i], i)

    gold_null += gn
    gold_rel += gr
    pred_null += pn
    pred_rel += pr


    #calculate the precision, recall, and f1 for the sample and add to global counts
    if gold_att[0] != 'NONE':
        total_attach_tp += len([e for e in pred_att if e in gold_att])
        total_attach_fn += len([e for e in gold_att if e not in pred_att])
        # if len([e for e in gold_att if e not in pred_att]) > 0:
        #     new_entry = [num_fp]
        #     num_fp+= 1
        #     new_entry.append('game index: ' + str(i))
        #     new_entry.extend(pred_contexts[i])
        #     new_entry.append('PREDICTED:')
        #     new_entry.extend(pred_att)
        #     new_entry.append('GOLD:')
        #     new_entry.extend(gold_att)
        #     false_negative_check.append(new_entry)

    elif pred_att[0] != 'NONE':
        new_entry = [num_fp]
        num_fp+= 1
        new_entry.append('game index: ' + str(i))
        new_entry.extend(pred_contexts[i])
        new_entry.append('PREDICTED:')
        new_entry.extend(pred_att)
        new_entry.append('GOLD:')
        new_entry.extend(gold_att)
        false_positive_check.append(new_entry)
        total_attach_fp += len([e for e in pred_att if e not in gold_att])

print('true pos', total_attach_tp)
print('false pos', total_attach_fp)
print('false neg', total_attach_fn)
microf1 = total_attach_tp/(total_attach_tp + 0.5*(total_attach_fp + total_attach_fn)) 
print('val corr+narr')
print('Gold rel/num null: {}/{}'.format(gold_rel, gold_null))
print('Pred rel/num null: {}/{}'.format(pred_rel, pred_null))
# print("Attachment F1:",np.mean(att_f1_l),len(att_f1_l))
# print("Attachment Average Precision:",np.mean(att_prec_l))
# print("Attachment Average Recall:",np.mean(att_rec_l))
print('Macro F1: ', microf1)
print('--------------------------------')


f = open(current_folder + "/validate_corrnarr_falsepositive_check.txt","w")
for entry in false_positive_check:
    for ent in entry:
        print(ent, file=f)
    print('----------------------------\n', file=f)
print("checks done")

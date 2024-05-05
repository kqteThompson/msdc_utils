"""
Opens output from llama parser and 

"""
import os
import csv
# import json
import jsonlines
import numpy as np
# from collections import defaultdict

def get_rels(sample_string, sample_index, attach=0):
    """
    takes a sample string and returns a list of tuples
    if attach = 1, then only return endpoints, no rel types
    """
    attach_list = [st.strip() for st in sample_string.split(' ')]
    if attach:
        new_list = []
        for a in attach_list:
            try:
                s = a.split('(')[1].split(')')[0].split(',')
            except IndexError:
                print('split error', sample_index)
            else:
                new_list.append((int(s[0]), int(s[1])))
        attach_list = new_list
    return attach_list

global_path = '/home/kate/minecraft_utils/'
current_folder=os.getcwd()

# gold_path = global_path + 'llm_annotator/parser_val_moves_15.jsonl'
# pred_path = global_path + '/calmip/val-output-file.txt'
gold_path = global_path + 'llm_annotator/parser_test_moves_15.jsonl'
pred_path = global_path + '/calmip/test-output-file.txt'

csv_path = current_folder + '/compare.csv'


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

print(len(pred_outputs))
print(len(gold_outputs))

csv_list = []

att_f1_l = []
att_prec_l = []
att_rec_l = []
type_f1_l = []
type_prec_l = []
type_rec_l = []

for i, s in enumerate(pred_outputs):
    csv_list.append([gold_outputs[i], s])
    #first do attachments
    pred = get_rels(s, i, attach=1)
    gold = get_rels(gold_outputs[i], i, attach=1)
    if len(gold) > 0 and len(pred) > 0:
        prec = len([e for e in pred if e in gold])/len(pred)
        rec = len([e for e in pred if e in gold])/len(gold)
    else:
        prec = 0
        rec = 0
    att_prec_l.append(prec)
    att_rec_l.append(rec)
    if prec+rec==0:
        att_f1_l.append(0)
    else:
        att_f1_l.append(2*prec*rec/(prec+rec))
    
    #then do attach + relation types
    pred = get_rels(s, i)
    gold = get_rels(gold_outputs[i], i)
    if len(gold) > 0 and len(pred) > 0:
        prec = len([e for e in pred if e in gold])/len(pred)
        rec = len([e for e in pred if e in gold])/len(gold)
    else:
        prec = 0
        rec = 0
    type_prec_l.append(prec)
    type_rec_l.append(rec)
    if prec+rec==0:
        type_f1_l.append(0)
    else:
        type_f1_l.append(2*prec*rec/(prec+rec))

print("Attachment F1:",np.mean(att_f1_l),len(att_f1_l))
print("Attachment Average Precision:",np.mean(att_prec_l))
print("Attachment Average Recall:",np.mean(att_rec_l))
print('--------------------------------')
print("Attachment + Rel F1:",np.mean(type_f1_l),len(type_f1_l))
print("Attachment + Rel Average Precision:",np.mean(type_prec_l))
print("Attachment + Rel Average Recall:",np.mean(type_rec_l))

fields = ['Gold', 'Pred']
with open(csv_path, 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(csv_list)

print('csv saved!')

 

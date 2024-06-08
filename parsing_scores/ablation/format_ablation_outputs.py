import os
import csv
import numpy as np
import pickle
import jsonlines
from collections import defaultdict, Counter
import pandas
from sklearn.metrics import precision_recall_fscore_support, classification_report, ConfusionMatrixDisplay, confusion_matrix


#MSDC

# map_rels = {'COM':0, 'CONTR':1, 'CORR':2, 'QAP':3, 'ACK':4,'ELAB':5,
#                  'CLARIFQ':6, 'COND':7, 'CONTIN':8, 'RES':9, 'EXPL':10, 'QELAB':11,
#                  'ALT':12, 'NARR':13, 'CONFQ':14, 'SEQ':15, 'NONE':16}

# labels = ['COM','CONTR','CORR', 'QAP','ACK','ELAB','CLARIFQ','COND','CONTIN','RES','EXPL','QELAB', 'ALT', 
#           'NARR', 'CONFQ', 'SEQ', 'NONE']

#STAC 
##NB: THESE ARE NOT THE SAME INDEX NUBERS AS IN OTHER SCRIPTS
map_rels = {'COM':0, 'CONTR':1, 'PAR':2, 'CORR':3, 'QAP':4, 'ACK':5, 'ELAB':6, 'CLARIFQ':7, 'COND':8, 'CONTIN':9, 'RES':10, 'EXPL':11, 
            'QELAB':12, 'ALT':13, 'NARR':14, 'BACK':15, 'PAR':2, 'SEQ':17, 'NONE':16}

# labels = ['COM','CONTR', 'PAR', 'CORR', 'QAP', 'ACK', 'CLARIFQ', 'COND', 'CONTIN', 'RES', 'EXPL', 'QELAB',
#                  'ALT', 'NARR',  'SEQ', 'NONE']

labels = ['COM','CONTR','PAR', 'CORR','QAP','ACK', 'ELAB', 'CLARIFQ','COND','CONTIN','RES','EXPL','QELAB','ALT','NARR','NONE']




current_folder=os.getcwd()


# gold_path = current_folder + '/local_model_test.jsonl'
# pred_path = current_folder + '/test-output-file-msdc.txt'

gold_path = current_folder + '/local_model_flat_test.jsonl'
pred_path = current_folder + '/test-output-file-stacflat.txt'


#get pred output list
with open(pred_path, 'r') as txt:
    text = txt.read().split('\n')

pred_outputs = []

for t in text:
    if '### DR:' in t:
        sample = t.split('### DR:')[1].strip()
        pred_outputs.append(sample)

#get gold sample list
gold_outputs = []

with jsonlines.open(gold_path) as reader:
    for obj in reader:
        gold_outputs.append(obj['PS'])

assert len(pred_outputs) == len(gold_outputs)

# #half the data
# new_gold = []
# for i, g in enumerate(gold_outputs):
#     if i%2 == 0:
#         new_gold.append(g)

# #half the data for the other test set
# new_pred = []
# for i, g in enumerate(pred_outputs):
#     if i%2 == 0:
#         new_pred.append(g)
# assert len(new_pred) == len(new_gold)

assert len(pred_outputs) == len(gold_outputs)

#make labels 
adjust = []
adjust.extend(gold_outputs)
adjust.extend(pred_outputs)
adjust_labels = list(set(adjust))
print(adjust_labels)

attach = []
rel_type = []
for i, s in enumerate(pred_outputs):
    p = map_rels[s]
    g = map_rels[gold_outputs[i]]
    ap = 1
    ag = 1
    rel_type.append([g,p])
    if p == 16:
        ap = 0
    if g == 16:
        ag = 0 
    attach.append([ag, ap])
    
assert len(rel_type) == len(attach)

true_attach = [a[0] for a in attach]
pred_attach = [a[1] for a in attach]
true_rel = [a[0] for a in rel_type]
pred_rel = [a[1] for a in rel_type]


f = open(current_folder + "/local_flat_scores.txt","w")
prf = precision_recall_fscore_support(true_attach, pred_attach, average='binary')
print("Attachment F1:", prf[2], file=f)
print("Attachment Average Precision:", prf[0], file=f)
print("Attachment Average Recall:", prf[1], file=f)
print('--------------------------------', file=f)

print(classification_report(true_rel,pred_rel,target_names=labels), file=f)


d = classification_report(true_rel,pred_rel,target_names=labels,output_dict=True)
prec = 0
rec = 0
f1 = 0 
count = 0

for label in adjust_labels:
    if label!="NONE":
        prec+=d[label]["precision"]*d[label]["support"]
        rec+=d[label]["recall"]*d[label]["support"]
        f1+=d[label]["f1-score"]*d[label]["support"]
        count+=d[label]["support"]
        # checking that support is same as the number of ground truth instance for the label
        # assert d[label]["support"] == Counter(g_label_l)[label]
print('--------------------------------', file=f)
print("Weighted Average Precision:", prec/count, file=f)
print("Weighted Average Recall:", rec/count, file=f)
print("Weighted Average F1 score:", f1/count, file=f)

    
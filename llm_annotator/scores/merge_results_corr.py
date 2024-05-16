import os
import csv
import numpy as np
import pickle
from collections import defaultdict, Counter
import pandas
from sklearn.metrics import classification_report

def get_links(sample_string, sample_index):
    """
    takes a sample string and returns a list of attach tuples
    and a list of rel type strings
    """
    labels = ['COM','CONTR','CORR','QAP','ACK','ELAB','CLARIFQ','COND','CONTIN',
              'RES','EXPL','QELAB','ALT','NARR','CONFQ','SEQ']
    
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
        if rel != None and s_tuple != None:
            attach_list.append((int(s[0]), int(s[1])))
            rel_list.append(r)
    
    #re-construct the full list 
    #a list of tuples (rel, x, y)
    full_list = []
    for i, r in enumerate(attach_list):
        full_list.append((rel_list[i], r[0], r[1]))   
    return attach_list, full_list
    


data = pandas.read_csv("./compare.csv")
gold_outputs = [data["Gold"][i] for i in range(len(data["Gold"]))]
pred_outputs = [data["Pred"][i] for i in range(len(data["Pred"]))]

gold_outputs[108] = 'ACK(24,25) CONTIN(25,26) COM(26,27) CONTIN(27,28) ELAB(29,30) CONTR(25,29) CORR(24,29)' ## There were 2 COM(26,27) originally
gold_outputs[515] = 'RES(14,15) CORR(12,15)' ## There were 2 RES(14,15) originally
gold_outputs[619] = 'CORR(53,55) CONTIN(55,56) CORR(54,55)' ## There were 2 CORR(53,55) originally
gold_outputs[742] = 'ACK(32,33) ACK(30,34)' ## There were 2 ACK(30,34) originally
gold_outputs[2005] = 'RES(5,6) NARR(1,6)' ## There were 2 RES(5,6) originally


##Let's check there are no other repetitions in gold
for i in range(len(gold_outputs)):
    assert len(gold_outputs[i].split(" "))==len(np.unique(gold_outputs[i].split(" ")))
    
##Let's check there are no other repetitions in pred
for i in range(len(pred_outputs)):
    assert len(pred_outputs[i].split(" "))==len(np.unique(pred_outputs[i].split(" ")))
    
labels = ['COM','CONTR','CORR','QAP','ACK','ELAB','CLARIFQ','COND','CONTIN',
              'RES','EXPL','QELAB','ALT','NARR','CONFQ','SEQ','NULL']
csv_list = []

att_f1_l = []
att_prec_l = []
att_rec_l = []
type_f1_l = []
type_prec_l = []
type_rec_l = []

total_preds = [] #total number of prediction links
total_gold = []
total_TP = []
total_FP = []
total_FN = []
matrix_list = []
tp_matrix_list = []
g_label_l = []
tp_distances = defaultdict(list)
fp_distances = defaultdict(list)
fn_distances = defaultdict(list)

for i, s in enumerate(pred_outputs):
    print('------------------', i, '---------------------------------')
    csv_list.append([gold_outputs[i], s])
    #first do attachments
    pred_att, pred_all = get_links(s, i)
    gold_att, gold_all = get_links(gold_outputs[i], i)
    # print(pred_all)
    # print(gold_all)
    total_preds.extend(pred_all)
    total_gold.extend(gold_all)
    if len(gold_att) > 0 and len(pred_att) > 0:
        prec = len([e for e in pred_att if e in gold_att])/len(pred_att)
        rec = len([e for e in pred_att if e in gold_att])/len(gold_att)
    else:
        prec = 0
        rec = 0
    att_prec_l.append(prec)
    att_rec_l.append(rec)
    if prec+rec==0:
        att_f1_l.append(0)
    else:
        att_f1_l.append(2*prec*rec/(prec+rec))    
    #then do attach + rel_types
    if len(gold_all) > 0 and len(pred_all) > 0:
        TP = [e for e in pred_all if e in gold_all]
        prec = len(TP)/len(pred_all)
        FP = [e for e in pred_all if e not in gold_all]
        rec = len(TP)/len(gold_all)
        FN = [e for e in gold_all if e not in pred_all]
        leftover_pred = [p for p in pred_all if p not in TP]
        leftover_gold = [p for p in gold_all if p not in TP]
    else:
        prec = 0
        rec = 0
        TP = []
        FP = []
        FN = []
    type_prec_l.append(prec)
    type_rec_l.append(rec)
    if prec+rec==0:
        type_f1_l.append(0)
    else:
        type_f1_l.append(2*prec*rec/(prec+rec))
    #then process the TP, FP, FN for matrix 
    total_TP.extend(TP)
    total_FN.extend(FN)
    total_FP.extend(FP)
    mlen = len(matrix_list)
    for x in TP:
        matrix_list.append([x[0], x[0]])
        tp_matrix_list.append([x[0], x[0]])
        #add to distance dict
        d = x[2]-x[1]
        tp_distances[d].append(x[0])
    for x in FN:
        # matrix_list.append([x[0],'NULL'])
        #check to see if the attachment was predicted
        for z, y in enumerate(leftover_pred):
            # print(i)
            # print(x)
            # print(leftover_pred)
            if x[1:] == y[1:]:
                # print(x[1:], y[1:])
                # print('------')
                matrix_list.append([x[0], y[0]])
                tp_matrix_list.append([x[0], y[0]])
                leftover_pred.pop(z)
                break
        else:
            print('went to null!!')
            matrix_list.append([x[0],'NULL'])          
        #add to distance dict
        d = x[2]-x[1]
        fn_distances[d].append(x[0])
    leftover_gold = [a for a in leftover_gold if a not in FN]
    assert len(leftover_gold)==0
    for x in leftover_pred:
        matrix_list.append(['NULL', x[0]])
        #add to distance dict
        d = x[2]-x[1]
        fp_distances[d].append(x[0])
    g_label = [g[0] for g in gold_all]
    g_label_l.extend(g_label)
    m_label = [m[0] for m in matrix_list]
    
    for label in labels:
        if label!="NULL":
            assert Counter(g_label_l)[label]==Counter(m_label)[label]
    print(TP)
    print('false positive', FP)
    print('gold', gold_all)
    print('false negative', FN)
    print('pred', pred_all)
    print(matrix_list[mlen:])
    print('-------------------------')


gold_list = [labels.index(m[0]) for m in matrix_list]
pred_list = [labels.index(m[1]) for m in matrix_list]

print(classification_report(gold_list,pred_list,target_names=labels))

# The F1-scores for all the relations are correct. 
#It's calculated the same way as N said. 
#That is, while calculating F1 for label l, all the ["NULL", l] entries count towards false-positive for label l 
#and all the [l, "NULL"] entries count towards false-negative for label l. 
#So, the "NULL" type is affecting the precision/recall/F1 for label l (as it should). 
#Now, for the overall weighted average precision/recall/f1-score, we want the average to be over the actual relation labels set (i.e. excluding "NULL" class). 
#For that, we do this 
d = classification_report(gold_list,pred_list,target_names=labels,output_dict=True)
prec = 0
rec = 0
f1 = 0 
count = 0

for label in labels:
    if label!="NULL":
        prec+=d[label]["precision"]*d[label]["support"]
        rec+=d[label]["recall"]*d[label]["support"]
        f1+=d[label]["f1-score"]*d[label]["support"]
        count+=d[label]["support"]
        # checking that support is same as the number of ground truth instance for the label
        assert d[label]["support"] == Counter(g_label_l)[label]
        


print("Weighted Average Precision:", prec/count)
print("Weighted Average Recall:", rec/count)
print("Weighted Average F1 score:", f1/count)

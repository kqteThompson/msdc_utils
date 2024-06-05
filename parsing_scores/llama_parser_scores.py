import os
import csv
import numpy as np
import pickle
import jsonlines
from collections import defaultdict, Counter
import pandas
from sklearn.metrics import classification_report


def get_links(sample_string, sample_index):
    """
    takes a sample string and returns a list of attach tuples
    and a list of rel type strings
    """
    #MINECRAFT labels
    # labels = ['COM','CONTR','CORR','QAP','ACK','ELAB','CLARIFQ','COND','CONTIN',
    #           'RES','EXPL','QELAB','ALT','NARR','CONFQ','SEQ']
    
    #STAC labels
    labels = ['COM', 'CONTR', 'CORR', 'QAP', 'ACK', 'ELAB', 'CLARIFQ', 'COND', 'CONTIN', 'RES', 'EXPL', 
                'QELAB','ALT', 'NARR', 'BACK', 'PAR', 'SEQ']

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
    return endpoints, full_list
    
#MINECRAFT LABELS
# labels = ['COM','CONTR','CORR','QAP','ACK','ELAB','CLARIFQ','COND','CONTIN',
#               'RES','EXPL','QELAB','ALT','NARR','CONFQ','SEQ','NULL']


current_folder=os.getcwd()


# gold_path = current_folder + '/msdc_llama/parser_test_moves_15.jsonl'
# # pred_path = current_folder + '/msdc_llama/test-output-ll3.txt'
# pred_path = current_folder + '/msdc_llama/test-output-generate-file-llama3.txt'

# gold_path = current_folder + '/stac_llama/parser_stac_linguistic_test_15_checked.jsonl'
# pred_path = current_folder + '/stac_llama/stac_linguistic/test-output-generate-file-llama3-stac_ling.txt'

gold_path = current_folder + '/molweni/parser_molweni_test_15.jsonl'
pred_path = current_folder + '/molweni/test-output-generate-file-llama3-molweni_ling_flat.txt'

# gold_path = current_folder + '/stac_llama/parser_stac_linguistic_flat_test_15_checked.jsonl'
# pred_path = current_folder + '/stac_llama/stac_flat/test-output-generate-file-llama3-stac_ling_flat.txt'

# gold_path = current_folder + '/stac_llama/parser_stac_test_15.jsonl'
# pred_path = current_folder + '/stac_llama/stac_squished/test-output-generate-file-llama3-stac.txt'

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

att_f1_l = []
att_prec_l = []
att_rec_l = []
total_attach_tp = 0
total_attach_fp = 0
total_attach_fn = 0
type_f1_l = []
type_prec_l = []
type_rec_l = []

total_preds = [] #total number of prediction links
total_gold = []
total_TP = []
total_FP = []
total_FN = []
matrix_list = []
# tp_matrix_list = []
g_label_l = []
tp_distances = defaultdict(list)
fp_distances = defaultdict(list)
fn_distances = defaultdict(list)

doubles = 0
for i, s in enumerate(pred_outputs):
    #first do attachments
    pred_att, pred_all = get_links(s, i)
    gold_att, gold_all = get_links(gold_outputs[i], i)

    # print("GOLD:", gold_all)
    # print("PRED:", pred_all)
    # print('-------')

    # if len(set(gold_att)) < len(gold_att):
    #     print('!! multiple relations')
    #     doubles += len(gold_att) - len(set(gold_att))
    #     print("double rels: ", doubles)

    # calculate number of nulls there should be
    common = len(set(pred_att).intersection(set(gold_att)))
    expected_nulls = (len(pred_att) - common) + (len(gold_att) - common)
    # save all predictions in a list
    total_preds.extend(pred_all)
    total_gold.extend(gold_all)

    #calculate the precision, recall, and f1 for the sample
    if len(gold_att) > 0 and len(pred_att) > 0:
        prec = len([e for e in pred_att if e in gold_att])/len(pred_att)
        rec = len([e for e in pred_att if e in gold_att])/len(gold_att)
        total_attach_tp += len([e for e in pred_att if e in gold_att])
        total_attach_fp += len([e for e in pred_att if e not in gold_att])
        total_attach_fn += len([e for e in gold_att if e not in pred_att])
    else:
        prec = 0
        rec = 0
    att_prec_l.append(prec)
    att_rec_l.append(rec)
    if prec+rec==0:
        att_f1_l.append(0)
    else:
        att_f1_l.append(2*prec*rec/(prec+rec))    

    #calculate the precision, recall, and f1 for the sample
    if len(gold_all) > 0 and len(pred_all) > 0:
        prec = len([e for e in pred_all if e in gold_all])/len(pred_all)
        rec = len([e for e in pred_all if e in gold_all])/len(gold_all)   
    else:
        prec = 0
        rec = 0
    type_prec_l.append(prec)
    type_rec_l.append(rec)
    if prec+rec==0:
        type_f1_l.append(0)
    else:
        type_f1_l.append(2*prec*rec/(prec+rec))

    #create the relation comparisons by type
    TP = [e for e in pred_all if e in gold_all] 
    leftover_pred = [p for p in pred_all if p not in TP]
    leftover_gold = [p for p in gold_all if p not in TP]

    #then process the TP, FP, FN for matrix 
    total_TP.extend(TP)
    #mlen = len(matrix_list)
    rem_dict = defaultdict(list)
    for x in TP:
        matrix_list.append([x[0], x[0]])
        # tp_matrix_list.append([x[0], x[0]])
        #add to distance dict
        # d = x[2]-x[1]
        # tp_distances[d].append(x[0])
    for x in leftover_pred:
        rem_dict[(x[1], x[2])].append(('p', x[0]))
    for x in leftover_gold:
        rem_dict[(x[1], x[2])].append(('g', x[0]))

    # print(rem_dict)

    p_count = 0
    g_count = 0
    null_count = 0
    for k in rem_dict.keys():
        p = 'NULL'
        t = 'NULL'
        for re in rem_dict[k]:
            if re[0] == 'p':
                p = re[1]
                p_count += 1
            elif re[0] == 'g':
                t = re[1]
                g_count += 1
        matrix_list.append([t,p])
        if 'NULL' in [t,p]:
            null_count += 1
  
    assert(len(TP) + p_count == len(pred_all))
    assert(len(TP) + g_count == len(gold_all))
    assert null_count == expected_nulls

#compute labels in gold and pred
#NB: might be different to the full list, if there were doubles
gold = [m[0] for m in matrix_list]
pred = [m[1] for m in matrix_list]
# print(set(gold))
# print(set(pred))
gold.extend(pred)
labels = list(set(gold))
print(labels)


# labels = ['COM', 'CONT', 'CORR', 'QAP', 'PAR', 'ACK',
#             'ELAB', 'CLARIFQ', 'COND', 'CONT', 'RES', 'EXPL',
#             'QELAB', 'ALT', 'NARR', 'BACK', 'NULL', 'SEQ']
    

microf1 = total_attach_tp/(total_attach_tp + 0.5*(total_attach_fp + total_attach_fn)) 


gold_list = [labels.index(m[0]) for m in matrix_list]
pred_list = [labels.index(m[1]) for m in matrix_list]
# gold_list = [m[0] for m in matrix_list]
# pred_list = [m[1] for m in matrix_list]

f = open(current_folder + "/outputs_june/scores_llama3_molweni_flat_10.txt","w")
print("Attachment F1:",np.mean(att_f1_l),len(att_f1_l), file=f)
print("Attachment Average Precision:",np.mean(att_prec_l), file=f)
print("Attachment Average Recall:",np.mean(att_rec_l), file=f)
print('Micro F1: ', microf1, file=f)
print('--------------------------------', file=f)
print("Attachment + Rel F1:",np.mean(type_f1_l),len(type_f1_l))
print("Attachment + Rel Average Precision:",np.mean(type_prec_l))
print("Attachment + Rel Average Recall:",np.mean(type_rec_l))
print('---------------------------------------')
print(classification_report(gold_list,pred_list,target_names=labels), file=f)



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
        # assert d[label]["support"] == Counter(g_label_l)[label]
        
print('--------------------------------', file=f)
print("Weighted Average Precision:", prec/count, file=f)
print("Weighted Average Recall:", rec/count, file=f)
print("Weighted Average F1 score:", f1/count, file=f)

f.close()
    
        

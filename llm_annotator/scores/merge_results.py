"""
Opens output from llama parser and 


TEST:
total outputs:  5918
total pred outputs:  6258
Attachment F1: 0.8842032306590848 3134
Attachment Average Precision: 0.8882752623800341
Attachment Average Recall: 0.8871948470943366
--------------------------------
Attachment + Rel F1: 0.8127302132468429 3134
Attachment + Rel Average Precision: 0.81714855175109
Attachment + Rel Average Recall: 0.8130485155134167

"""
import os
import csv
import jsonlines
import numpy as np
import pickle
from collections import defaultdict

# def get_rels(sample_string, sample_index, attach=0):
#     """
#     takes a sample string and returns a list of tuples
#     if attach = 1, then only return endpoints, no rel types
#     """
#     attach_list = [st.strip() for st in sample_string.split(' ')]
#     if attach:
#         new_list = []
#         for a in attach_list:
#             try:
#                 s = a.split('(')[1].split(')')[0].split(',')
#             except IndexError:
#                 print('split error at ', sample_index)
#             else:
#                 try:
#                     new_list.append((int(s[0]), int(s[1])))
#                 except IndexError:
#                     print('split error at ', sample_index)
#                 except ValueError:
#                     print('value error at ', sample_index)
#         attach_list = new_list
#     return attach_list

def get_links(sample_string, sample_index, distance = None):
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

global_path = '/home/kate/minecraft_utils/'
current_folder=os.getcwd()

# gold_path = global_path + 'llm_annotator/parser_val_moves_15.jsonl'
# pred_path = global_path + '/calmip/val-output-file.txt'
gold_path = global_path + 'llm_annotator/parser_test_moves_15.jsonl'
pred_path = global_path + '/calmip/test-output-file.txt'

csv_path = current_folder + '/compare.csv'

pickle_save_path = current_folder + '/pickles/'


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

total_preds = [] #total number of prediction links
total_gold = []
total_TP = []
total_FP = []
total_FN = []
matrix_list = []
tp_matrix_list = []

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
        TP=[]
        FP=[]
        FN=[]
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

    for x in FP:
        # matrix_list.append(['NULL', x[0]])
        for z, y in enumerate(leftover_gold):
            if x[1:] == y[1:]:
                matrix_list.append([y[0], x[0]])
                tp_matrix_list.append([y[0], x[0]])
                leftover_gold.pop(z)
                break
        else:
            matrix_list.append(['NULL', x[0]])
        #add to distance dict
        d = x[2]-x[1]
        fp_distances[d].append(x[0])
    
    print(TP)
    print('false positive', FP)
    print('gold', gold_all)
    print('false negative', FN)
    print('pred', pred_all)
    print(matrix_list[mlen:])
    print('-------------------------')


print('total gold outputs: ', len(total_gold))
print('total pred outputs: ', len(total_preds))
print('num TP: ', len(total_TP))
print('num FN: ', len(total_FN))
print('num FP: ', len(total_FP))
print('len matrix list', len(matrix_list))
print("Attachment F1:",np.mean(att_f1_l),len(att_f1_l))
print("Attachment Average Precision:",np.mean(att_prec_l))
print("Attachment Average Recall:",np.mean(att_rec_l))
print('--------------------------------')
print("Attachment + Rel F1:",np.mean(type_f1_l),len(type_f1_l))
print("Attachment + Rel Average Precision:",np.mean(type_prec_l))
print("Attachment + Rel Average Recall:",np.mean(type_rec_l))

# fields = ['Gold', 'Pred']
# with open(csv_path, 'w') as f:
#     write = csv.writer(f)
#     write.writerow(fields)
#     write.writerows(csv_list)

# print('csv saved!')

with open(pickle_save_path + 'conf_mtx.pkl', 'wb') as f:  
    pickle.dump(matrix_list, f)   

with open(pickle_save_path + 'conf_mtx_tp.pkl', 'wb') as f:  
    pickle.dump(tp_matrix_list, f)    

with open(pickle_save_path + 'tp_dict.pkl', 'wb') as f:  
    pickle.dump(tp_distances, f)  

with open(pickle_save_path + 'fp_dict.pkl', 'wb') as f:  
    pickle.dump(fp_distances, f) 

with open(pickle_save_path + 'fn_dict.pkl', 'wb') as f:  
    pickle.dump(fn_distances, f) 

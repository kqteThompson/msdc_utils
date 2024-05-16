import os
import csv
import jsonlines
import pandas


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

gold_path = global_path + 'llm_annotator/parser_val_moves_15.jsonl'
# gold_path = global_path + 'llm_annotator/parser_train_moves_15.jsonl'
csv_path = current_folder + '/compare.csv'

gold_outputs = []
with jsonlines.open(gold_path) as reader:
    for obj in reader:
        gold_outputs.append(obj['PS'])


##check for doubles one
for i, output in enumerate(gold_outputs):


    gold_att, gold_all = get_links(gold_outputs[i], i)

    # o = [st.strip() for st in output.split(' ')]
    # print(gold_all)
    if len(list(set(gold_all))) < len(gold_all):
        print('Sample ', i)
        print(gold_all)
        print('-----------------------------------------')


# data = pandas.read_csv(csv_path)
# #print(data.head())
# #print(data.loc[617:620])
# gold_list = data['Gold'].tolist()
# for i, g in enumerate(gold_list):
#     print(set(g))
#     print(g)
#     # if len(set(g)) < len(g):
#     #     print('sample ', i)
#     #     print(g)
#     print('----------------------')


  



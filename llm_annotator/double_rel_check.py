import os
import json
from collections import Counter


current_folder=os.getcwd()

# annotation_path = current_folder + '/annotated_data/TRAIN_307_bert.json'
# annotation_path = current_folder + '/annotated_data/VAL_100_bert.json'
annotation_path = current_folder + '/annotated_data/DEV_32_bert.json'
# annotation_path = current_folder + '/annotated_data/TEST_101_bert.json'

map_rels_str = {'Comment':'COM', 'Contrast':'CONTR', 'Correction':'CORR', 'Question-answer_pair':'QAP', 'Acknowledgement':'ACK','Elaboration':'ELAB',
                 'Clarification_question':'CLARIFQ', 'Conditional':'COND', 'Continuation':'CONTIN', 'Result':'RES', 'Explanation':'EXPL', 'Q-Elab':'QELAB',
                 'Alternation':'ALT', 'Narration':'NARR', 'Confirmation_question':'CONFQ', 'Sequence':'SEQ'}

with open(annotation_path, 'r') as j:
    jfile = json.load(j)
    annotations = jfile


for game in annotations:
    game_id = game['id']
    rels = game['relations']

    rel_list = []
    for rel in rels:
        if rel['x'] < rel['y']:
            new_rel = map_rels_str[rel['type']] + '(' + str(rel['x']) + ',' + str(rel['y']) + ')'
            rel_list.append(new_rel)
    
    if len(list(set(rel_list))) < len(rel_list):
        print(game_id)
        edus = game['edus']
        repeats = Counter(rel_list)
        for k in repeats.items():
            if k[1] > 1:
                print(k[0])
                num = int(k[0].split('(')[1].split(',')[0].strip())
                print(edus[num]['speaker'], edus[num]['text'])
    
        print('-----------------------------')





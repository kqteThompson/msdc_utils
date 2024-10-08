"""
takes a json of annotated minecraft games and converts to 
a turn format to be used in LLAMA parsing. 

{"CT":[[19,17],[20,17],[20,19]],
"sample":"14 <Architect> On the ground near the bottom left corner of the x ,
\n15 <Architect> if you step back 2 blocks ,
\n16 <Architect> in the block to your left place a green block .
\n17 <Builder> |put green X:3 Y:1 Z:0\n18 <Architect> Sprry ,
\n19 <Architect> one up and to the right from that one
\n20 <Builder> |put green X:2 Y:1 Z:-1|remove green X:3 Y:1 Z:0\n21 <Architect> Perfect"}

parameters:
-edu distance
-intra/inter
-relations as words or numbers

NB: when creating json-l, use '###PS' for 'predict structure'


[0, 30, 79, 98, 124, 174, 217, 235, 260, 275, 347, 382, 455, 475, 
502, 522, 542, 576, 604, 649, 668, 713, 744, 766, 796, 822, 851, 
861, 916, 943, 989, 1026, 1069, 1090, 1117, 1155, 1166, 1209, 1257, 
1286, 1332, 1343, 1357, 1374, 1427, 1460, 1487, 1534, 1584, 1637, 1663, 
1677, 1727, 1800, 1826, 1844, 1861, 1903, 1940, 1970, 2000, 2013, 2063, 
2109, 2143, 2175, 2217, 2265, 2303, 2345, 2399, 2466, 2505, 2532, 2574,
 2584, 2611, 2634, 2661, 2689, 2733, 2748, 2821, 2839, 2851, 2865, 2875, 
 2907, 2943, 2976, 2997, 3011, 3033, 3055, 3086, 3114, 3137, 3148, 3169, 3190, 3210]

"""

import os
import json
import jsonlines
from collections import defaultdict

map_rels_no = {'Comment':0, 'Contrast':1, 'Correction':2, 'Question-answer_pair':3, 'Acknowledgement':4,'Elaboration':5,
                 'Clarification_question':6, 'Conditional':7, 'Continuation':8, 'Result':9, 'Explanation':10, 'Q-Elab':11,
                 'Alternation':12, 'Narration':13, 'Confirmation_question':14, 'Sequence':15}

map_rels_str = {'Comment':'COM', 'Contrast':'CONTR', 'Correction':'CORR', 'Question-answer_pair':'QAP', 'Acknowledgement':'ACK','Elaboration':'ELAB',
                 'Clarification_question':'CLARIFQ', 'Conditional':'COND', 'Continuation':'CONTIN', 'Result':'RES', 'Explanation':'EXPL', 'Q-Elab':'QELAB',
                 'Alternation':'ALT', 'Narration':'NARR', 'Confirmation_question':'CONFQ', 'Sequence':'SEQ'}


def preprocess_edus(elist):
    """
    Adds edu number and speaker tag to each edu
    keep numbers in a 'indexes' field to be used for the relations
    """
    cnt = 0
    for turn in elist['turns']:
        speaker = turn['speaker'][:4]
        new_edus = []
        idxs = []
        for edu in turn['edus']:
            new_string = str(cnt)+' '+'<'+speaker+'>'+' ' + edu
            new_edus.append(new_string)
            idxs.append(cnt)
            cnt += 1
        turn['edus'] = new_edus
        turn['indexes'] = idxs    
    return elist

def get_structure(indexes, head, rels):
    """
    Takes a list of edu indexes and the annotated relations
    finds the relations with the targets == indexes and sources !< head 
    **IGNORES backwards relations
    !!returns a list of tuples (<type>, x, y)
    """
    structs = []
    rel_list = [r for r in rels if r['y'] in indexes and r['y'] > r['x'] and r['x'] >= head]
    for rel in rel_list:
        structs.append((map_rels_str[rel['type']], rel['x'], rel['y']))
    return structs

def get_structure_bkwds(indexes, head, rels):
    """
    Takes a list of edu indexes and the annotated relations
    finds the relations with the targets == indexes and sources !< head 
    **DOES NOT IGNORE backwards relations
    !!returns a list of tuples (<type>, x, y)
    """
    structs = []
    rel_list = [r for r in rels if r['y'] in indexes and r['y'] > r['x'] and r['x'] >= head]
    bkw_list = [r for r in rels if r['y'] in indexes and r['x'] > r['y'] and r['y'] >= head]
    rel_list.extend(bkw_list)
    for rel in rel_list:
        structs.append((map_rels_str[rel['type']], rel['x'], rel['y']))
    return structs
    

def relation_window(construct, window, head):
    """
    takes a context structure list afer the window has been changed
    the new window start index, and the new head index 
    removes any relations whose sources are outside the window
    """
    out_const = []
    # print('in: ', construct)
    new_const = [c for c in construct[window:]]
    # print('out: ', new_const)
    ##don't want to flatten the structures here
    ##the individual lists represent turns 
    for i in new_const:
        newc = [rel for rel in i if rel[1] >= head]
        if len(newc) > 0:
            out_const.append(newc)
    # print('out const: ', out_const)
    return out_const

def format_sample(ddict):
    """
    takes a default dict at a particular moment in time and 
    creates a sample to be added to json_l list
    """ 
    # print(ddict['structure'])
    # print(ddict['predict'])
    
    context_str = '\n'.join([i for r in ddict['context'] for i in r])
    turn_str = '\n'.join(ddict['turn'])
    #change structures into strings
    structures = [i for r in ddict['structure'] for i in r]
    formatted_structures = [s[0] + '(' + str(s[1]) + ',' + str(s[2]) +')' for s in structures]
    structure_str = ' '.join(formatted_structures) 
    predict_str = [p[0] + '(' + str(p[1]) + ',' + str(p[2]) +')' for p in ddict['predict']] 
    x_entry = 'Context: ' + context_str + '\n' + 'Structure: ' + structure_str + '\n' + 'New Turn: ' + turn_str
    # y_entry = '###PS: ' + predict_str
    y_entry = ' '.join(predict_str)
    # if len(predict_str) > 0:
    #     y_entry = predict_str[0]
    # else:
    #     y_entry = ''
    sample = [x_entry, y_entry]
    return sample

current_folder=os.getcwd()

data_path = current_folder + '/TEST_turns.json'
annotation_path = current_folder + '/annotated_data/TEST_101_bert.json'
save_path = current_folder + '/parser_test_moves_full.jsonl'

with open(data_path, 'r') as j:
    jfile = json.load(j)
    games = jfile

with open(annotation_path, 'r') as j:
    jfile = json.load(j)
    annotations = jfile

# index_count = 0
# start_dial_indexes = []

json_l = []

game_count = 0
for game in games:
    #json_l.append(['BEGIN', 'DIALOGUE'])
    game_id = game['id']
    print(game_id)
    game_count += 1
    game = preprocess_edus(game) #preprocess game edus
    rels = [dial['relations'] for dial in annotations if dial['id'] == game_id][0] #get relations
    s = defaultdict(list,{ k:[] for k in ('context','structure','turn', 'predict') }) #sample pattern
    s['context'].append(game['turns'][0]['edus']) #add first turn (append so that we can easily remove turns)
    # start_dial_indexes.append(index_count)
    # index_count += 1
    #don't add relations for the first turn\
    edu_distance = 1 #the first turn always has one edu
    head_source = 0 #the index of the edu that is the first in the context window.
    for turn in game['turns'][1:]:
        # print('turn number ', turn['turn'])
        # if edu_distance + len(turn['edus']) <= DISTANCE:
        s['turn'].extend(turn['edus'])
        #add relations to be predicted
        #get relations that have turn edus indices as target
        #keep track of smallest source index
        preds = get_structure_bkwds(turn['indexes'], head_source, rels)
        s['predict'].extend(preds)
        #add s to json_l list
        snapshot = format_sample(s)
        json_l.append(snapshot)
        #now move the 'turn' edus to 'context' and the 'predict' to 'structure'
        s['structure'].append(s['predict'])
        s['context'].append(s['turn'])
        # index_count += 1
        #update distance
        edu_distance += len(turn['edus'])
        # print('!!',edu_distance)
        
        #empty 
        s['predict'] = []
        s['turn'] = []
        #so now you have an updated context and structure and can
        #add the next turn and prediction sample

    #clear everything after game
    s['structure'] = []
    s['context'] =[]
    s['predict'] = []
    s['turn'] = []


#convert the dicts into json dicts for json_l
with jsonlines.open(save_path, mode='w') as writer:
    for l in json_l:
        sample = {}
        sample['PS'] = l[1]
        sample['sample'] = l[0]
        writer.write(sample)

# with open(save_path, 'w') as outfile:
#     json.dump(turn_version, outfile)

print('jsonl saved for {} games'.format(game_count))

    
  
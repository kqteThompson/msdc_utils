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



!!!ISSUE : see 15-edu turn s2-league8-game1stac_1458308487

"""

import os
import json
import jsonlines
from collections import defaultdict

# map_rels_no = {'Comment':0, 'Contrast':1, 'Correction':2, 'Question-answer_pair':3, 'Acknowledgement':4,'Elaboration':5,
#                  'Clarification_question':6, 'Conditional':7, 'Continuation':8, 'Result':9, 'Explanation':10, 'Q-Elab':11,
#                  'Alternation':12, 'Narration':13, 'Confirmation_question':14, 'Sequence':15}

map_rels_str = {'Comment':'COM', 'Contrast':'CONTR', 'Correction':'CORR', 'Question-answer_pair':'QAP', 'Acknowledgement':'ACK','Elaboration':'ELAB',
                 'Clarification_question':'CLARIFQ', 'Conditional':'COND', 'Continuation':'CONTIN', 'Result':'RES', 'Explanation':'EXPL', 'Q-Elab':'QELAB',
                 'Alternation':'ALT', 'Narration':'NARR', 'Background':'BACK', 'Parallel':'PAR', 'Sequence':'SEQ', 'Question_answer_pair':'QAP',  'Q_Elab':'QELAB'}



def preprocess_edus(elist):
    """
    Adds edu number and speaker tag to each edu
    keep numbers in a 'indexes' field to be used for the relations
    """
    cnt = 0
    for turn in elist['turns']:
        speaker = turn['speaker']
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
    print(ddict['structure'])
    print(ddict['predict'])
    
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

# data_path = current_folder + '/stac_test_turns.json'
# annotation_path = current_folder + '/stac/stac_squished_corrected/test_data.json'
# save_path = current_folder + '/parser_stac_test_15.jsonl'

data_path = current_folder + '/stac_linguistic_test_turns.json'
annotation_path = current_folder + '/stac/stac_linguistic_corrected/test_data.json'
save_path = current_folder + '/parser_stac_linguistic_test_15.jsonl'

# data_path = current_folder + '/molweni_test_turns.json'
# annotation_path = current_folder + '/molweni/molweni_clean_test50.json'
# save_path = current_folder + '/parser_molweni_test_15.jsonl'

with open(data_path, 'r') as j:
    jfile = json.load(j)
    games = jfile

with open(annotation_path, 'r') as j:
    jfile = json.load(j)
    annotations = jfile
    annotations = annotations


json_l = []

DISTANCE = 15
game_count = 0
for game in games:
# for game in [g for g in games if g['id'] == 's1-league1-game5stac_1368694440']:
    game_id = game['id']
    print(game_id)
    game_count += 1
    game = preprocess_edus(game) #preprocess game edus
    rels = [dial['relations'] for dial in annotations if dial['id'] == game_id][0] #get relations
    s = defaultdict(list,{ k:[] for k in ('context','structure','turn', 'predict') }) #sample pattern
    s['context'].append(game['turns'][0]['edus']) #add first turn (append so that we can easily remove turns)
    #don't add relations for the first turn\
    edu_distance = 1 #the first turn always has one edu
    head_source = 0 #the index of the edu that is the first in the context window.
    for turn in game['turns'][1:]:
        print('turn number ', turn['turn'])
        if edu_distance + len(turn['edus']) <= DISTANCE:
            s['turn'].extend(turn['edus'])
            #add relations to be predicted
            #get relations that have turn edus indices as target
            #keep track of smallest source index
            preds = get_structure(turn['indexes'], head_source, rels)
            s['predict'].extend(preds)
            #add s to json_l list
            snapshot = format_sample(s)
            json_l.append(snapshot)
            #now move the 'turn' edus to 'context' and the 'predict' to 'structure'
            s['structure'].append(s['predict'])
            s['context'].append(s['turn'])
            #update distance
            edu_distance += len(turn['edus'])
            # print('!!',edu_distance)
            
            #empty 
            s['predict'] = []
            s['turn'] = []
            #so now you have an updated context and structure and can
            #try to add the next turn and prediction sample
        else:
            # print('we are over')
            #distance with the new edus would be too long
            #need to move window
            #remove first turns until distance is <11
            edus_over = (edu_distance + len(turn['edus'])) - DISTANCE
            # print('edus over: ', edus_over)
            save = 0
            new_window = 0
            for i, t in enumerate(s['context']): #find the index of the turn that will put distance less than 10
                if len(t) + save >= edus_over:
                    new_window = i+1 #get new window starting point
                    edu_distance = edu_distance - (len(t) + save) #reset distance
                    break
                else:
                    save += len(t)

            #remove the structure and the context 
            s['context'] = s['context'][new_window:]
            #s['structure'] = s['structure'][new_window:]

            #get index of first edu in new context 
            head_source = int(s['context'][0][0].split('<')[0].strip())
            
            #!!!!BUT STILL need to check indices of current context: 
            s['structure'] = relation_window(s['structure'], new_window, head_source)
            
           
            #add the new turn and pred structure
            s['turn'].extend(turn['edus'])
            preds = get_structure(turn['indexes'], head_source, rels)
            s['predict'].extend(preds)
            #add s to json_l list
            snapshot = format_sample(s)
            json_l.append(snapshot)
            #now move the 'turn' edus to 'context' and the 'predict' to 'structure'
            #update distance
            s['structure'].append(s['predict'])
            s['context'].append(s['turn'])
            #update distance
            edu_distance += len(s['turn'])
            #empty 
            s['predict'] = []
            s['turn'] = []
    #clear everything after game
    # s['structure'] = []
    # s['context'] =[]
    # s['predict'] = []
    # s['turn'] = []
# for l in json_l:
#     print(l[0])
#     print(l[1])
#     print('--------------------')

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
    
  
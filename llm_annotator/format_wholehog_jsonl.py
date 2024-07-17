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

def get_structure_whole_hog(indexes, rels):
    """
    Takes a list of edu indexes and the annotated relations
    finds the relations with the targets == indexes and sources
    **INCLUDES backwards relations
    !!returns a list of tuples (<type>, x, y)
    """
    structs = []
    rel_list = [r for r in rels if (r['y'] in indexes and r['y'] > r['x']) or (r['x'] in indexes and r['x'] > r['y']) ]
    for rel in rel_list:
        structs.append((map_rels_str[rel['type']], rel['x'], rel['y']))
    return structs

def format_sample_whole_hog(context, predict):
    """
    takes a list of edus and a list of relations for a game
    creates a sample to be added to json_l list
    """ 
    #change structures into strings
    formatted_structures = [s[0] + '(' + str(s[1]) + ',' + str(s[2]) +')' for s in predict]
    y_entry = ' '.join(formatted_structures) 
    x_entry = '\n'.join(context)
    sample = [x_entry, y_entry]
    return sample

current_folder=os.getcwd()

data_path = current_folder + '/TEST_turns.json'
annotation_path = current_folder + '/annotated_data/TEST_101_bert.json'
save_path = current_folder + '/parser_test_moves_wh.jsonl'

with open(data_path, 'r') as j:
    jfile = json.load(j)
    games = jfile

with open(annotation_path, 'r') as j:
    jfile = json.load(j)
    annotations = jfile


json_l = []

game_count = 0
for game in games:
    game_id = game['id']
    print(game_id)
    game_count += 1
    game = preprocess_edus(game) #preprocess game edus
    rels = [dial['relations'] for dial in annotations if dial['id'] == game_id][0] #get relations
    context = []
    predict = []
    for turn in game['turns']:
        context.extend(turn['edus'])
        preds = get_structure_whole_hog(turn['indexes'], rels)
        predict.extend(preds)
    snapshot = format_sample_whole_hog(context, predict)
    json_l.append(snapshot)
    


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
    
  
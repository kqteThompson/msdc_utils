"""
for NEBULAMIPA training:
takes a json of annotated minecraft games and 
pulls out all the narrative arcs. 
Applies them to the list json. 
"""
import os
import json

map_rels_str = {'Comment':'COM', 'Contrast':'CONTR', 'Correction':'CORR', 'Question-answer_pair':'QAP', 'Acknowledgement':'ACK','Elaboration':'ELAB',
                 'Clarification_question':'CLARIFQ', 'Conditional':'COND', 'Continuation':'CONTIN', 'Result':'RES', 'Explanation':'EXPL', 'Q-Elab':'QELAB',
                 'Alternation':'ALT', 'Narration':'NARR', 'Confirmation_question':'CONFQ', 'Sequence':'SEQ'}

def is_nl(edu):
    """
    if every word in alphanumeric and has len 5
    """
    nl = 1
    words = edu.split(' ')
    # print(words)
    # print(words)
    for word in [w for w in words if w != '']:
        if not contains_number(word) or len(word) != 5:
            nl = 0
            break
    # print(nl)
    return nl

def contains_number(string):
    return any(char.isdigit() for char in string)

current_folder=os.getcwd()

data_path = '/home/kate/minecraft_utils/llm_annotator/annotated_data/TEST_133.json'
lists_path = current_folder + '/TEST_lists.json'
save_path = current_folder + '/TEST_narrations.json'

with open(data_path, 'r') as j:
    jfile = json.load(j)
    games = jfile

with open(lists_path, 'r') as j:
    jfile = json.load(j)
    lists = jfile

narrative_arcs = []
for game in games:
    game_id = game['id']
    new_game = {}
    new_game['id'] = game_id
    #STEP 1 add turn index for arch and global turn info to all edus
    edus = game['edus']
    global_cnt = 0
    last_speaker = None
    global_index = 0
    for edu in edus:
        edu['global_index'] = global_index
        global_index += 1
        speaker = edu['speaker']
        if speaker == last_speaker:
            edu['turn'] = global_cnt
        else:
            last_speaker = speaker
            global_cnt += 1
            edu['turn'] = global_cnt
        if speaker == 'Architect':
            edu['type'] = 0
        elif speaker == 'Builder':
            #also add type info
            if is_nl(edu['text']):
                edu['type'] = 1 
            else:
                edu['type'] = 0
    ##STEP 2 get the narr arcs, and separate from the rest of the relations
    arcs = []
    other_rels = []
    rels = game['relations']
    for rel in rels:
        if rel['type'] == 'Narration':
            #check if intra-turn
            if edus[rel['x']]['turn'] == edus[rel['y']]['turn']:
                other_rels.append([rel['x'], rel['y'], map_rels_str[rel['type']]])
            else:
                #otherwise store the narrative chunk
                arcs.append([edus[rel['x']]['global_index'], edus[rel['y']]['global_index']])
        else:
            other_rels.append([rel['x'], rel['y'], map_rels_str[rel['type']]])
    
    #sort other rels so that it is in order
    sorted_rels = sorted(other_rels, key=lambda x: x[1])

    ##STEP 3 for each list in the game list, create a new sublist
    new_lists = []
    olist = [l for l in lists if l['id'] == game_id][0]['list']
    for arc in arcs:
        #arc_list = list[arc[0]:arc[1] + 1] 
        arc_list = []

        ##for each action bout in sublist, pull all structure belonging to it and add to bout.
        arc_edus = edus[arc[0]:arc[1]]
        start_index = edus[arc[0]]['global_index']
        for ae in arc_edus:
            if ae['type'] == 1:
                #then add structure info
                target_index = ae['global_index']
                struct = []
                for ore in sorted_rels:
                    if ore[0] >= start_index and ore[1] < target_index: ##for now, just forwards relations, and no relations connecting moves
                        struct.append(ore[2]+'('+ str(ore[0]) + ',' + str(ore[1]) +')') ##put the relations in order??
                struct_str = ' '.join(struct)
                it = olist[ae['global_index']]
                it['structure'] = struct_str
                arc_list.append(it)
            else:
                arc_list.append(olist[ae['global_index']])
        new_lists.append(arc_list)
    assert len(new_lists) == len(arcs)
    new_game['arcs'] = new_lists

    narrative_arcs.append(new_game)
        
    
assert len(narrative_arcs) == len(games)
  

with open(save_path, 'w') as outfile:
    json.dump(narrative_arcs, outfile)

print('json saved for {} games'.format(len(narrative_arcs)))
    
  
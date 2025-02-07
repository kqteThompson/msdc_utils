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

# data_path = '/home/kate/minecraft_utils/llm_annotator/annotated_data/TEST_133.json'
# lists_path = current_folder + '/TEST_lists.json'
# save_path = current_folder + '/TEST_full.json'

# data_path = '/home/kate/minecraft_utils/llm_annotator/annotated_data/TRAIN_307_bert.json'
# lists_path = current_folder + '/TRAIN_lists.json'
# save_path = current_folder + '/TRAIN_full.json'

data_path = '/home/kate/minecraft_utils/llm_annotator/annotated_data/VAL_100_bert.json'
lists_path = current_folder + '/VAL_lists.json'
save_path = current_folder + '/VAL_full.json'

with open(data_path, 'r') as j:
    jfile = json.load(j)
    games = jfile

with open(lists_path, 'r') as j:
    jfile = json.load(j)
    lists = jfile

full_arcs = []
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
    ##STEP 2 get the relations
    all_rels = []
    rels = game['relations']
    for rel in rels:
        all_rels.append([rel['x'], rel['y'], map_rels_str[rel['type']]])
    
    #sort other rels so that it is in order
    sorted_rels = sorted(all_rels, key=lambda x: x[1])

    ##STEP 3 for each list in the game list, create a new sublist
    new_lists = []
    olist = [l for l in lists if l['id'] == game_id][0]['list']
    nl_moves = len([edu for edu in edus if edu['type'] == 1])

    for i, edu in enumerate(edus):
        if edu['type'] == 1:
            m = olist[i]
            target_index = edu['global_index']
            struct = []
            for ore in sorted_rels:
                if ore[0] >= 0 and ore[1] < target_index: ##for now, just forwards relations, and no relations connecting moves
                    struct.append(ore[2]+'('+ str(ore[0]) + ',' + str(ore[1]) +')') ##put the relations in order??
            struct_str = ' '.join(struct)
            m['structure'] = struct_str

            grow_list = olist[:target_index]
            grow_list.append(m)
            new_lists.append(grow_list)
       

    assert len(new_lists) == nl_moves

    new_game['arcs'] = new_lists
    full_arcs.append(new_game)
        
    
assert len(full_arcs) == len(games)
  

with open(save_path, 'w') as outfile:
    json.dump(full_arcs, outfile)

print('json saved for {} games'.format(len(full_arcs)))
    
  
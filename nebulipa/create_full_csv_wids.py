import os
import json
import csv 

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

#First get corrections list from validation set
annotation_path = '/home/kate/minecraft_utils/llm_annotator/annotated_data/VAL_100_bert.json'
with open(annotation_path, 'r') as j:
    jfile = json.load(j)
    games = jfile


corrections = []
for game in games:
    game_id = game['id']
    #print(game['id'])
    edus = game['edus']
    #make a mapping from edu index to move index
    action_index = 0
    for edu in edus:
        if edu['speaker'] == 'Builder' and is_nl(edu['text']): 
            edu['action_index'] = action_index
            action_index += 1
        else:
            edu['action_index'] = 'utterance'

    relations = game['relations']
    for rel in relations:
        if rel['type'] == 'Correction':
            if edus[rel['y']]['action_index'] != 'utterance':
                corrections.append(game_id + '_' + str(edus[rel['y']]['action_index']))

print(len(corrections), ' correction moves found in val! ')

print(corrections[0])

##now create csv
data_path = current_folder + '/VAL_full.json'
save_path = current_folder + '/val_nebulipa_full_wids_cut.csv'

with open(data_path, 'r') as j:
    jfile = json.load(j)
    games = jfile


body = []
action_count = 0 #to make sure we have one sample per action
for game in games:
    game_id = game['id'] #later on if needed can print out data with game id

    # if game_id.split('-')[0] not in ['C17','C32','C3']:
    for i, arc in enumerate(game['arcs']):

        identifier = game_id + '_' + str(i)
        #print(identifier)
        
        pred = arc[-1]['moves']
        action_count += 1

        dial_sample = []
        structure = 'Structure: ' + arc[-1]['structure']
        
        for utt in arc[:-1]:
            if isinstance(utt, dict):
                dial_sample.append(utt['eeu'])
            else:
                dial_sample.append(utt)
        
        dial_sample.append(structure)
        dial_string = '\n'.join(dial_sample)

        if identifier in corrections:
            body.append([identifier, dial_string, pred])

# assert len(body) == action_count
assert len(body) == len(corrections)

print('created {} samples, creating csv...'.format(len(body)))
fields = ['identifier', 'dial_with_actions', 'action_seq']
with open(save_path, 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(body)

print('csv saved.')

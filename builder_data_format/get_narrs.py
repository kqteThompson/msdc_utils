"""
Creates a json file that contains each game with id, and the endpoints of each narrative arc
ex:
[(3, 9), (9, 17), (17, 30), (30, 32)] => [<text of 3>, <text of 9>, <text of 17>, <text of 30>, <text of 32>]
"""
import os
import json

def contains_number(string):
    return any(char.isdigit() for char in string)

def is_nl(edu):
    """
    if every word in alphanumeric
    """
    nl = 1
    words = edu.split(' ')
    # print(words)
    for word in [w for w in words if w != '']:
        if not contains_number(word) or not len(word) == 5:
            nl = 0
            break
    return nl

current_folder=os.getcwd()

# annotations_path = current_folder + '/annotated_data/TRAIN_2024-04-07_307_flat_bert.json'
# save_path = current_folder + '/train_narrations.json'

annotations_path = current_folder + '/annotated_data/TEST_133.json'
save_path = current_folder + '/test_narrations.json'

arcs = {}

with open(annotations_path, 'r') as jf:
    jfile = json.load(jf)

    print(len(jfile))
for game in jfile:
    game_id = game['id']
    edus = game['edus']

    narrs = sorted([(rel['x'], rel['y']) for rel in game['relations'] if rel['type'] == 'Narration'])
    arc_narrs = []
    for nar in narrs:
        #check if there are moves between
        edus_slice = edus[nar[0]:nar[1]]
        for edu in edus_slice:
            if edu['speaker'] == 'Builder' and is_nl(edu['text']):
                #there are moves
                arc_narrs.append(nar[1])
                break 

    # for nar in narrs:##to check what happens if we don't try to just use all narr targets
    #     arc_narrs.append(nar[1])         

    if len(narrs) == 0: #some games have no narrations (too short)
        arcs[game_id] = []
    else:
        narr_text = [edus[an]['text'] for an in arc_narrs]
        arcs[game_id] = narr_text

with open(save_path, 'w') as outfile:
    json.dump(arcs, outfile)

    print('narrations json saved')

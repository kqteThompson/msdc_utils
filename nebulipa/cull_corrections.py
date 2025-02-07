"""
takes a 
"""
import os
import json




current_folder=os.getcwd()




with open(data_path, 'r') as j:
    jfile = json.load(j)
    games = jfile


corrections = []
for game in games:
    game_id = game['id']
    #print(game['id'])
    edus = game['edus']
    relations = game['relations']

    index_list = []
    for rel in relations:
        if rel['type'] == 'Correction':
            index_list.append(rel['y'])

    corrections_index = []
    for i in index_list:
        if edus[i]['speaker'] == 'Builder' and is_nl(edus[i]['text']):
            corrections.append(game_id + '_' + str(i))

with open(save_path, 'w') as outfile:
    json.dump(new_games, outfile)

print('json saved for {} games'.format(len(new_games)))
    
 
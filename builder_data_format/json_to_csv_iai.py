"""
Creates a CSV file for training LLAMA builder from train_iai.json

"""

import os
import json
import csv


current_folder=os.getcwd()

train_data = current_folder + '/train_iai.json'

csv_list = []

#stats
lengths = []

with open(train_data, 'r') as jf:
    data = json.load(jf)
    for game in data:
        game_id = game['game_id']
        if game_id.split('-')[0] not in ['C17','C32', 'C3']: #these are not games authors originally used
            dialogue = game['dialogue']
            original_moves = len([c for c in dialogue if isinstance(c, dict)]) #to compare with num moves after

            #add first two moves
            head = []
            last_world_state = 'EMPTY'
            head.append(last_world_state)
            head.extend(dialogue[0])
            # print('head: ', head)
            dial_string = '\n'.join(head)
            last_move = dialogue[1]['moves']
            #last_world_state = dialogue[1]['worldstate']
            
            csv_list.append([dial_string, last_move])

            #continue with a window
            sub_start = 0
            for samp in range(original_moves-1): #we know ahead of time how many samples there should be.
                head = []
                head.append(last_world_state) ## needs to be 'EMPTY'
                head.extend(dialogue[sub_start])
                head.append(dialogue[sub_start + 1]['moves'])
                head.extend(dialogue[sub_start + 2])
                # print('head: ', head)
                dial_string = '\n'.join(head)
                last_move = dialogue[sub_start + 3]['moves']
                last_world_state = dialogue[sub_start + 3]['worldstate']

                csv_list.append([dial_string, last_move])
                sub_start += 2


print('all games done, {} samples, creating csv...'.format(len(csv_list)))
fields = ['dial_with_actions', 'action_seq']
with open(current_folder + '/iai_plus_worldstate_train.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(csv_list)

print('csv saved.')





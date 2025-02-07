import os
import json
import csv 

current_folder=os.getcwd()

data_path = current_folder + '/VAL_full.json'
save_path = current_folder + '/val_nebulipa_full.csv'

with open(data_path, 'r') as j:
    jfile = json.load(j)
    games = jfile


body = []
action_count = 0 #to make sure we have one sample per action
for game in games:
    game_id = game['id'] #later on if needed can print out data with game id

    if game_id.split('-')[0] not in ['C17','C32','C3']:
        for arc in game['arcs']:
            
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

            body.append([dial_string, pred])

assert len(body) == action_count

print('created {} samples, creating csv...'.format(len(body)))
fields = ['dial_with_actions', 'action_seq']
with open(save_path, 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(body)

print('csv saved.')

import os
import json
import csv 

current_folder=os.getcwd()

data_path = current_folder + '/TEST_narrations.json'
save_path = current_folder + '/test_nebulipa.csv'

with open(data_path, 'r') as j:
    jfile = json.load(j)
    games = jfile


body = []
action_count = 0 #to make sure we have one sample per action
for game in games:
    game_id = game['id'] #later on if needed can print out data with game id

    if game_id.split('-')[0] not in ['C17','C32','C3']:
        for arc in game['arcs']:
            dial_sample = []
            for utt in arc:
                if isinstance(utt, dict):
                    action_count += 1
                    #then add structure and worldstate and finish sample
                    str_sample = [s for s in dial_sample] #keep dial sample list
                    str_sample.append('Structure: ' + utt['structure'])
                    str_sample.append('Worldstate: ' + utt['worldstate'])
                    dial_string = '\n'.join(str_sample)
                    body.append([dial_string, utt['moves']])
                    dial_sample.append(utt['eeu'])
                else:
                    dial_sample.append(utt)

assert len(body) == action_count

print('created {} samples, creating csv...'.format(len(body)))
fields = ['dial_with_actions', 'action_seq']
with open(save_path, 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(body)

print('csv saved.')

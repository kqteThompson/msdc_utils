import os
import json
import csv

"""
takes output of neural builder on synthetic data and transforms to csv that can be 
read by scoring scripts
"""

def format_utterances(ustring):
    # print(ustring)
    c = []
    u1 = ustring.split('<architect>')[2].split('.')[0].strip()
    u2 = ustring.split('<architect>')[3].split('.')[0].strip()
    c.append(u1[1:])
    c.append(u2[1:])
    return c

def format_actions(act_list):
    moves_list = []
    for a in act_list:
        p = a['action_type']
        c = a['block']['type']
        x = a['block']['x']
        y = a['block']['y']
        z = a['block']['z']
        if p == 'placement': 
            a_str = 'place {} {} {} {}'.format(c, x, y, z)
        else:
            a_str = 'pick {} {} {}'.format(x, y, z)
        moves_list.append(a_str)
    moves_string = '\n'.join(moves_list)
    return moves_string

current_folder=os.getcwd()

json_path = current_folder + '/neural_builder_lvl2_pred_new_ordered.json'
l2_csv_path = current_folder + '/level-two-synth-data.csv'


with open(json_path, 'r') as j:
    jfile = json.load(j)
    samples = jfile

with open(l2_csv_path, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)


actions = []

for i, line in enumerate(data[1:]):
    act = format_actions(samples[i]['generated_seq'][0])
    actions.append(act)
    
assert len(data[1:]) == len(actions)

fields = ['dial_with_actions', 'pred_seq']
with open(current_folder + '/neural_builder_lvl2_pred.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    for i, n in enumerate(data[1:]):
        instruction = '\n'.join(n)
        write.writerow([instruction, actions[i]])

print('csv saved.')
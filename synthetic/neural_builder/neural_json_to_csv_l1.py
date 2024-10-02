import os
import json
import csv

"""
takes output of neural builder on synthetic data and transforms to csv that can be 
read by scoring scripts
"""

def format_utterances(ustring):
    u = ustring.split('<architect>')[2].split('.')[0].strip()
    s = '<Builder> Mission has started.\n<Architect> B' + u[1:]
    return s

def format_inst_action():
    return None

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

json_path = current_folder + '/neural_builder_lvl1_pred.json'


with open(json_path, 'r') as j:
    jfile = json.load(j)
    samples = jfile

instructions = []
actions = []

for sample in samples:

    inst = format_utterances(sample['prev_utterances'])
    instructions.append(inst)
    act = format_actions(sample['generated_seq'][0])
    actions.append(act)

assert len(instructions) == len(actions)

fields = ['dial_with_actions', 'pred_seq']
with open(current_folder + '/neural_builder_lvl1_pred.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    for i, n in enumerate(instructions):
        write.writerow([n, actions[i]])

print('csv saved.')
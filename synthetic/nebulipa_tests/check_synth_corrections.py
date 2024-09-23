"""
takes nebulipa correction outputs and compares with gold

for no struct errors:
model rebuilds entire structure (so doesn't take into account the context)
or forgets the pick move in single block changes (but always gets correct location)

with correction it is predicting more 'pick' statements

"""
import os
import csv
import re
import json
import functions as fn
import numpy as np


current_folder=os.getcwd()

#nebuipa correction without structure
# pred_path = current_folder + '/nebulipa_corrsynth_nostruct.csv'
# gold_path = '/home/kate/minecraft_utils/synthetic/corrections/correction_synth_nebulipa_test_without_structure.csv'

# pred_path = current_folder + '/nebulipa_corrsynth_struct.csv'
# pred_path = current_folder + '/correction_synth_nebula_org_output.csv'
pred_path = current_folder + '/correction_synth_nebula_narr_ws_output.csv'
gold_path = '/home/kate/minecraft_utils/synthetic/corrections/correction_synth_nebulipa_test_with_structure.csv'



def get_moves(line):
    """
    returns a list of moves 
    removing incomplete ones
    """
    moves = []
    new_line = [l.strip() for l in line[1].split('\n')]
    for nl in new_line:
        # if len(nl.split(' ')) == 5:
            moves.append(nl)
    return moves


with open(gold_path, newline='') as f:
    reader = csv.reader(f)
    gold_data = list(reader)[1:]

with open(pred_path, newline='') as f:
    reader = csv.reader(f)
    pred_data = list(reader)[1:]

assert len(gold_data) == len(pred_data)

ind = 0
for i, line in enumerate(gold_data):
    
    print(i)
    gold_moves = get_moves(line)
    pred_moves = get_moves(pred_data[i])

    if gold_moves != pred_moves:
        print('INCORRECT')
        print(gold_data[i][0])
        print('gold: ', gold_moves)
        print('pred: ', pred_moves)
        #continue
    # else:
    #     print(gold_data[i][0])
    #     print('gold: ', gold_moves)
    #     print('pred: ', pred_moves)

    print('----------')


# with open(save_path, 'w') as outfile:
#     json.dump(samples, outfile, default=int)

# print('json saved.')

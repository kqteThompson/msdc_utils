import jsonlines
# import jsonlines
import os
# import numpy as np
# from shape_gen import get_instruction, generate, get_second_shape, bad_generate
# from data_gen import json_format

"""
Takes a jsonl file synthetic examples and expands to each turn for each sample
"""
def get_moves(sample_string):
    splits = sample_string.split('\n')
    return splits[2:6]

current_folder=os.getcwd()

with jsonlines.open('/home/kate/minecraft_utils/new_synthetic/data/french_synthcorr_200_goldcontext.jsonl', 'r') as jsonl_f:
     lst = [obj for obj in jsonl_f]


new_lst = []

for sample in lst:
    if sample['PS'].startswith('CORR'):
        first_s = "Context: 0 <Buil> La mission a commencée.\nStructure: \nNew turn: 1 <Arch> Commençons par quelques formes de base.\n"
        first = {"PS": "CONTIN(0,1)", "sample" : first_s}
        new_lst.append(first)
                            
        moves = get_moves(sample['sample'])

        second_s = "Context: 0 <Buil> La mission a commencée.\n1 <Arch> Commençons par quelques formes de base.\nStructure: CONTIN(0,1)\nNew turn: {}".format(moves[0])
        second = {"PS": "CONTIN(1,2)", "sample" : second_s}
        new_lst.append(second)
        
        third_s = "Context: 0 <Buil> La mission a commencée.\n1 <Arch> Commençons par quelques formes de base.\n{}\nStructure: CONTIN(0,1) CONTIN(1,2)\nNew turn: {}".format(moves[0], moves[1]) 
        third = {"PS": "RES(2,3)", "sample" : third_s}
        new_lst.append(third)

        fourth_s = "Context: 0 <Buil> La mission a commencée.\n1 <Arch> Commençons par quelques formes de base.\n{}\n{}\nStructure: CONTIN(0,1) CONTIN(1,2) RES(2,3)\nNew turn: {}".format(moves[0], moves[1], moves[2]) 
        fourth = {"PS": "CONTIN(2,4)", "sample" : fourth_s}
        new_lst.append(fourth)

        fifth_s = "Context: 0 <Buil> La mission a commencée.\n1 <Arch> Commençons par quelques formes de base.\n{}\n{}\n{}\nStructure: CONTIN(0,1) CONTIN(1,2) RES(2,3) CONTIN(2,4)\nNew turn: {}".format(moves[0], moves[1], moves[2], moves[3]) 
        fifth = {"PS": "RES(4,5)", "sample" : fifth_s}
        new_lst.append(fifth)

        #append original move
        new_lst.append(sample)
    else:
        new_lst.append(sample)

print(len(new_lst), 'samples for 200 dialogues')

save_path = '/home/kate/minecraft_utils/new_synthetic/data/french_synthcorr_200_gencontext.jsonl'

with jsonlines.open(save_path, mode='w') as writer:
    for s in new_lst:
        writer.write(s)
print('done.')



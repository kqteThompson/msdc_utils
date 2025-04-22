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
    return splits[2].strip(), splits[3].strip(), splits[4].strip(), splits[5].strip()

current_folder=os.getcwd()

with jsonlines.open(current_folder + '/french_synthetic_corrections_long_test_2.jsonl', 'r') as jsonl_f:
     lst = [obj for obj in jsonl_f]


new_lst = []

for i, sample in enumerate(lst):
    if i%2 == 0:

        moveone, movetwo, movethree, movefour = get_moves(sample['sample'])
        #for even numbered samples, expand 5 previous moves
        first_s = "Context: 0 <Buil> La mission a commencée.\nStructure: \nNew turn: 1 <Arch> Commençons par quelques formes de base.\n{}".format(moveone)
        first = {"PS": "CONTIN(0,1) CONTIN(1,2)", "sample" : first_s}
        new_lst.append(first)
        second_s = "Context: 0 <Buil> La mission a commencée.\n1 <Arch> Commençons par quelques formes de base.\n{}\nStructure: CONTIN(0,1) CONTIN(1,2)\nNew turn: {}".format(moveone,movetwo) 
        second = {"PS": "RES(2,3)", "sample" : second_s}
        new_lst.append(second)
        third_s = "Context: 0 <Buil> La mission a commencée.\n1 <Arch> Commençons par quelques formes de base.\n{}\n{}\nStructure: CONTIN(0,1) CONTIN(1,2) RES(2,3)\nNew turn: {}".format(moveone,movetwo,movethree) 
        third = {"PS": "CONTIN(2,4)", "sample" : third_s}
        new_lst.append(third)
        fourth_s = "Context: 0 <Buil> La mission a commencée.\n1 <Arch> Commençons par quelques formes de base.\n{}\n{}\n{}\nStructure: CONTIN(0,1) CONTIN(1,2) RES(2,3) CONTIN(2,4)\nNew turn: {}".format(moveone,movetwo,movethree,movefour) 
        fourth = {"PS": "RES(4,5)", "sample" : fourth_s}
        new_lst.append(fourth)
        #append original move
        new_lst.append(sample)
    else:
        new_lst.append(sample)


print(len(new_lst), 'samples for 200 dialogues')

with jsonlines.open(current_folder + "/french_synthcorr_300_gencontext.jsonl", mode='w') as writer:
    for s in new_lst:
        writer.write(s)
print('done.')



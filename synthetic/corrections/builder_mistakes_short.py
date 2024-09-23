import csv
import jsonlines
import os
import random
import numpy as np
from shape_gen import get_instruction, generate, get_next_shape, bad_generate, record_blocks
from data_gen import json_format

# S = {"square", "row", "rectangle", "tower", "diagonal", "diamond", "cube"}
# S = {"row", "tower"}
# L = {"centre", "edge", "corner"}
# C = {"orange", "red", "green", "blue", "purple", "yellow"}
# O = {"horizontal", "vertical",""}

S = ["row", "tower"]
L = ["centre", "edge", "corner"]
C = ["orange", "red", "green", "blue", "purple", "yellow"]
sizes = [3,4,5]

dialogues_text = []
llamipa_format = []

for ty in [1,2]:
    num = 0
    while num < 100:
        print(ty, num)
        shape = random.choice(S)
        color = random.choice(C)
        location = random.choice(L)
        size = random.choice(sizes)
        t = ty #t1 == first instruction botched, #t2 == second instruction
        instructions = ['<Buil> Mission has started.', '<Arch> Let\'s start with some basic shapes']
        # instructions.append('<Arch> So let\'s start with the basic shapes.')
        placed_blocks = []
        locations_used = []
        ##=======================================================================================FIRST INSTRUCTION
        i_one = get_instruction(shape, color, location, size)

        instructions.append(i_one)

        if t == 1:
            a_one, i_corr, a_corr = bad_generate(shape, color, location, size) #bad generate should also generate the correction moves
        else:
            gen_one = generate(shape, color, location, size)
            #format wrong gen with <builder> turn marker and commas between moves
            moves = ', '.join(gen_one)
            a_one = '<Buil> ' + moves
    
        instructions.append(a_one)

        #keep track of blocks placed and locations used
        placed_blocks.extend(record_blocks(a_one))
        locations_used.append(location)

        ##========================================================================================SECOND INSTRUCTION

        shape_2 = get_next_shape(locations_used)

        i_two = get_instruction(shape_2[0], shape_2[1], shape_2[2], shape_2[3], i=2)

        instructions.append(i_two)

        if t == 2:
            a_two, i_corr, a_corr = bad_generate(shape_2[0], shape_2[1], shape_2[2], shape_2[3])
        else:
            gen_two = generate(shape_2[0], shape_2[1], shape_2[2], shape_2[3])
            #format wrong gen with <builder> turn marker and commas between moves
            moves = ', '.join(gen_two)
            a_two = '<Buil> ' + moves
        
        instructions.extend([a_two, i_corr, a_corr])

        #keep track of blocks placed and locations used
        placed_blocks.extend(record_blocks(a_two))

        if 'pick' not in a_corr:
            placed_blocks.extend(record_blocks(a_corr))

        
        #number the instructions
        number_instructions = []
        n = 0
        for i in instructions:
            new_i = str(n) + ' ' + i 
            n+=1
            number_instructions.append(new_i)

        if len(set(placed_blocks)) == len(placed_blocks):
            #send to other script in order to make llamipa jsonl file
            samples = json_format(number_instructions, t)
            llamipa_format.extend(samples)

            #add the correction scheme according to type
            if t == 1:
                structure = 'Structure: CONTIN(0,1), CONTIN(1,2), RES(2,3), CONTIN(2,4), RES(4,5), CORR(3,6)'
                number_instructions.append(structure)
            elif t == 2:
                structure = 'Structure: CONTIN(0,1), CONTIN(1,2), RES(2,3), CONTIN(2,4), RES(4,5), CORR(5,6)'
                number_instructions.append(structure)
          
            instruction_str = '\n'.join(number_instructions)
            dialogues_text.append(instruction_str)
            num += 1
        else:
            print('REPEATED PLACEMENTS for Type {}'.format(t))
            print(placed_blocks)

        

print('Number of dialogues: ',len(dialogues_text))

current_folder=os.getcwd()

f = open(current_folder + "/synthetic_corrections_short_check.txt","w")
for d in dialogues_text:
    print(d, file=f)
    print('----------------------------\n', file=f)
print("dialogues printed")


#make llamipa jsonl
#convert the dicts into json dicts for json_l
with jsonlines.open(current_folder + "/synthetic_corrections_short_test.jsonl", mode='w') as writer:
    for s in llamipa_format:
        # sample = {}
        # sample['PS'] = l[1]
        # sample['sample'] = l[0]
        writer.write(s)
print('jsonl saved for {} samples'.format(len(llamipa_format)))




# current_folder = os.getcwd()
# fields = ['dial_with_actions', 'action_seq']
# with open(current_folder + '/correction_synth_test.csv', 'w') as f:
#     write = csv.writer(f)
#     write.writerow(fields)
#     for d in dialogues:
#         write.writerow([d[0], d[1]])

# print('csv saved.')

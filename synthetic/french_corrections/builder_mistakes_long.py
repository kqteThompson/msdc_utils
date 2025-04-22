import csv
import jsonlines
import os
import random
import numpy as np
from shape_gen import get_instruction, generate, get_next_shape, bad_generate, record_blocks
from data_gen import json_format_three


def translate_moves(moves):
    trans_dict = {'place':'met', 'pick':'prend', 'blue': 'blue', 
                  'red':'rouge', 'green': 'vert', 'yellow':'jaune', 'purple':'violet' }
    french = []
    for s in moves.split(' '):
        if s in trans_dict.keys():
            french.append(trans_dict[s])
        else:
            french.append(s)
    french_moves = ' '.join(french)
    return french_moves

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

for ty in [1,2,3]:
    num = 0
    while num < 100:
        print(ty, num)
        shape = random.choice(S)
        color = random.choice(C)
        location = random.choice(L)
        size = random.choice(sizes)
        t = ty #t1 == first instruction botched, #t2 == second instruction, #t3 == third instruction
            #create the instruction 
        instructions = ['<Buil> La mission a commencée.', '<Arch> Commençons par quelques formes de base.']
        #instructions = ['<Buil> Mission has started.', '<Arch> Let\'s start with some basic shapes']
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

        #translate moves to french
        fa_one = translate_moves(a_one)
        instructions.append(fa_one)

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
        
        #translate moves to french
        fa_two = translate_moves(a_two)
        instructions.append(fa_two)

        #keep track of blocks placed and locations used
        placed_blocks.extend(record_blocks(a_two))
        locations_used.append(shape_2[2])

        ##===========================================================================================THIRD INSTRUCTION

        shape_3 = get_next_shape(locations_used)

        i_three = get_instruction(shape_3[0], shape_3[1], shape_3[2], shape_3[3], i=3)

        instructions.append(i_three)

        if t == 3:
            a_three, i_corr, a_corr = bad_generate(shape_3[0], shape_3[1], shape_3[2], shape_3[3])
        else:
            gen_three = generate(shape_3[0], shape_3[1], shape_3[2], shape_3[3])
            #format wrong gen with <builder> turn marker and commas between moves
            moves = ', '.join(gen_three)
            a_three = '<Buil> ' + moves
        
        #translate moves to french
        fa_three = translate_moves(a_three)
        fa_corr = translate_moves(a_corr)
        instructions.extend([fa_three, i_corr, fa_corr])

        placed_blocks.extend(record_blocks(a_three))
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
            samples = json_format_three(number_instructions, t)
            llamipa_format.extend(samples)

            #add the correction scheme according to type
            if t == 1:
                structure = 'Structure: CONTIN(0,1), CONTIN(1,2), RES(2,3), CONTIN(2,4), RES(4,5), CONTIN(4,6), RES(6,7), CORR(3,8)'
                number_instructions.append(structure)
            elif t == 2:
                structure = 'Structure: CONTIN(0,1), CONTIN(1,2), RES(2,3), CONTIN(2,4), RES(4,5), CONTIN(4,6), RES(6,7), CORR(5,8)'
                number_instructions.append(structure)
            elif t == 3:
                structure = 'Structure: CONTIN(0,1), CONTIN(1,2), RES(2,3), CONTIN(2,4), RES(4,5), CONTIN(4,6), RES(6,7), CORR(7,8)'
                number_instructions.append(structure)

            instruction_str = '\n'.join(number_instructions)
            dialogues_text.append(instruction_str)
            num += 1
        else:
            print('REPEATED PLACEMENTS for Type {}'.format(t))
            print(placed_blocks)

        

print('Number of dialogues: ',len(dialogues_text))

current_folder=os.getcwd()

f = open(current_folder + "/french_synthetic_corrections_long_check_2.txt","w")
for d in dialogues_text:
    print(d, file=f)
    print('----------------------------\n', file=f)
print("dialogues printed")


#make llamipa jsonl
#convert the dicts into json dicts for json_l
with jsonlines.open(current_folder + "/french_synthetic_corrections_long_test_2.jsonl", mode='w') as writer:
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

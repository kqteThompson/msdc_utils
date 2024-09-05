import csv
import os
import numpy as np
from shape_gen import get_instruction, generate, get_second_shape, bad_generate

# S = {"square", "row", "rectangle", "tower", "diagonal", "diamond", "cube"}
S = {"row", "tower"}
L = {"centre", "edge", "corner"}
C = {"orange", "red", "green", "blue", "purple", "yellow"}
# O = {"horizontal", "vertical",""}


"""
TODO: 
-Second instruction should start with 'and'
-Correction instruction should be one edu. 
-structure should always be 
RES(0,1), CONT(0,2), RES(2,3)
-then the next two increments should be either:
CORR(1,4), RES(4,5), CORR(1,5) (for type 1)
or 
CORR(3,4), RES(4,5), CORR(3,5) (for type 2)
-Run llamipa with both gold and generated context
"""

dialogues = []

for shape in S:
    for color in C:
        for location in L:
            for size in range(3,6):
                for t in [1,2]: #t1 == first instruction botched, #t2 ==
                    #create the instruction 
                    instructions = []

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

                    shape_2 = get_second_shape(location)

                    i_two = get_instruction(shape_2[0], shape_2[1], shape_2[2], shape_2[3])

                    instructions.append(i_two)

                    if t == 2:
                        a_two, i_corr, a_corr = bad_generate(shape_2[0], shape_2[1], shape_2[2], shape_2[3])
                    else:
                        gen_two = generate(shape_2[0], shape_2[1], shape_2[2], shape_2[3])
                        #format wrong gen with <builder> turn marker and commas between moves
                        moves = ', '.join(gen_two)
                        a_two = '<Buil> ' + moves
                    
                    instructions.extend([a_two, i_corr, a_corr])
                    
                    #number the instructions
                    number_instructions = []
                    n = 0
                    for i in instructions:
                        new_i = str(n) + ' ' + i 
                        n+=1
                        number_instructions.append(new_i)

                    #add the correction scheme according to type
                    if t == 1:
                        structure = 'Structure: CORR(1,4), RES(4,5), CORR(1,5)'
                        number_instructions.append(structure)
                    else:
                        structure = 'Structure: CORR(3,4), RES(4,5), CORR(3,5)'
                        number_instructions.append(structure)

                    instruction_str = '\n'.join(number_instructions)
                    dialogues.append(instruction_str)

print('Number of dialogues: ',len(dialogues))

current_folder=os.getcwd()

f = open(current_folder + "/synthetic_corrections_check.txt","w")
for d in dialogues:
    print(d, file=f)
    print('----------------------------\n', file=f)
print("dialogues printed")


#                     instruction_str = '\n'.join(instructions)

#                     dialogues.append([instruction_str, a_corr])
                    
# print(len(dialogues))

# current_folder = os.getcwd()
# fields = ['dial_with_actions', 'action_seq']
# with open(current_folder + '/correction_synth_test.csv', 'w') as f:
#     write = csv.writer(f)
#     write.writerow(fields)
#     for d in dialogues:
#         write.writerow([d[0], d[1]])

# print('csv saved.')

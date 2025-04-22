import csv
import jsonlines
import os
import numpy as np
from shape_gen import get_instruction, generate, get_second_shape, bad_generate
from data_gen import json_format

# S = {"square", "row", "rectangle", "tower", "diagonal", "diamond", "cube"}
S = {"row", "tower"}
L = {"centre", "edge", "corner"}
C = {"orange", "red", "green", "blue", "purple", "yellow"}
# O = {"horizontal", "vertical",""}


dialogues_text = []
llamipa_format = []

for shape in S:
    for color in C:
        for location in L:
            for size in range(3,6):
                for t in [1,2]: #t1 == first instruction botched, #t2 ==
                    #create the instruction 
                    instructions = ['<Buil> Mission has started.']

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
                    
                    #number the instructions
                    number_instructions = []
                    n = 0
                    for i in instructions:
                        new_i = str(n) + ' ' + i 
                        n+=1
                        number_instructions.append(new_i)

                    #send to other script in order to make llamipa jsonl file
                    samples = json_format(number_instructions, t)
                    llamipa_format.extend(samples)

                    #add the correction scheme according to type
                    if t == 1:
                        structure = 'Structure: CONTIN(0,1), RES(1,2), CONTIN(1,3), RES(3,4), CORR(2,5), RES(5,6), CORR(2,6)'
                        number_instructions.append(structure)
                    else:
                        structure = 'Structure: CONTIN(0,1), RES(1,2), CONTIN(1,3), RES(3,4), CORR(4,5), RES(5,6), CORR(4,6)'
                        number_instructions.append(structure)

                    instruction_str = '\n'.join(number_instructions)
                    dialogues_text.append(instruction_str)

print('Number of dialogues: ',len(dialogues_text))

current_folder=os.getcwd()

f = open(current_folder + "/synthetic_corrections_check.txt","w")
for d in dialogues_text:
    print(d, file=f)
    print('----------------------------\n', file=f)
print("dialogues printed")


#make llamipa jsonl
#convert the dicts into json dicts for json_l
with jsonlines.open(current_folder + "/synthetic_corrections_test.jsonl", mode='w') as writer:
    for s in llamipa_format[:216]:
        # sample = {}
        # sample['PS'] = l[1]
        # sample['sample'] = l[0]
        writer.write(s)
print('jsonl saved for {} samples'.format(len(llamipa_format[:216])))




# current_folder = os.getcwd()
# fields = ['dial_with_actions', 'action_seq']
# with open(current_folder + '/correction_synth_test.csv', 'w') as f:
#     write = csv.writer(f)
#     write.writerow(fields)
#     for d in dialogues:
#         write.writerow([d[0], d[1]])

# print('csv saved.')

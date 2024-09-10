import csv
import jsonlines
import os
import numpy as np
from shape_gen import get_instruction, generate, get_second_shape, bad_generate
from data_gen import json_format

"""
Takes a text file of synthetic examples and converts them to nebulipa format
"""

current_folder=os.getcwd()

with open(current_folder + '/synthetic_corrections_check_freeze.txt') as f:
    samples = f.read().split('\n')


dialogues = []
dialogue = []

for line in samples:
    if 'Mission' in line or len(line) == 0:
        pass
    elif line == '----------------------------':
        dialogues.append(dialogue)
        dialogue = []
    else:
        dialogue.append(line)

nebulipa = []
for dial in dialogues[:108]:
    #reformat 1 <Arch> to 1. Arch:
    #add Worldstate: EMPTY
    #reformat instructions
    context = []
    moves = []
    for d in dial:
        if '<Arch>' in d:
            old = d.split('<Arch>')
            new = old[0].strip() + '. Arch:' + old[1]
            context.append(new)
        elif '<Buil>' in d:
            old = d.split('<Buil>')
            if old[0].strip() == '6':
                #do something
                m = '\n'.join(old[1].split(','))
                moves.append(m)
            else:
                new = old[0].strip() + '. Buil:' + old[1]
                context.append(new)
        elif 'Structure' in d:
            # old = d.split(', RES(5,6)')
            # context.append(old[0])
            #no structure:
            context.append('Structure:')
    #add Worldstate and join context
    context.append('Worldstate: EMPTY')
    full_context = '\n'.join(context)
    nebulipa.append([full_context, moves[0]])

print(len(nebulipa), ' dialogues')

fields = ['dial_with_actions', 'action_seq']
with open(current_folder + '/correction_synth_nebulipa_test_without_structure.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    for n in nebulipa:
        write.writerow([n[0], n[1]])

print('csv saved.')

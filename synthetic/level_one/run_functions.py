"""
takes a set of NEBULA outputs and 
creates a json with an object for each sample:
{intstruction:, shape:, shape_check:, size:, size_check:, color:, color_check:, location:, location_check:}
"""
import os
import csv
import re
import json
import functions as fn
import numpy as np


current_folder=os.getcwd()

#Nebula
# output_path = current_folder + '/llama_3_synthdata_level1.csv' ##1368
# save_path = current_folder + '/llama_synth_function_output.json'

#Nebula + Fine tuning
# output_path = current_folder + '/llama_3_aug_synthdata_level1.csv'
# save_path = current_folder + '/llama_aug_synth_function_output.json'

#Nebula + Fine tuning #2
# output_path = current_folder + '/llama_3_aug_synthdata_level1_v2.csv'
# save_path = current_folder + '/llama_aug_synth_function_output_v2.json'

#neural builder test
# output_path = '/home/kate/minecraft_utils/synthetic/neural_builder/neural_builder_lvl1_pred.csv'
# save_path = current_folder + '/neural_builder_lvl1_synth_function_output.json'

#Nebula + Narative arcs 
output_path = '/home/kate/minecraft_utils/synthetic/level_one/lvl1_synth_narr_pred_emnlp.csv'
save_path = current_folder + '/lvl1_synth_narr_emnlp_function_output.json'

def get_moves(line):
    """
    returns a list of moves 
    removing incomplete ones
    """
    moves = []
    new_line = [l.strip() for l in line[1].split('\n')]
    for nl in new_line:
        if len(nl.split(' ')) == 5:
            moves.append(nl)
    return moves

def get_params(instruction):
    axes = 0
    colors = ['purple', 'blue', 'red', 'green', 'yellow', 'orange']
    shapes = ['tower', 'rectangle', 'cube', 'diagonal', 'diamond', 'row', 'square']
    locations = ['edge', 'center', 'centre', 'corner']
    orients = ['vertical', 'horizontal']
    params = dict.fromkeys(['color', 'shape', 'location', 'orient', 'size'])
    for color in colors:
        if color in instruction:
            params['color'] = color
            break
    for shape in shapes:
        if shape in instruction:
            params['shape'] = shape
            if shape == 'diamond':
                if 'axes' in instruction:
                    axes = 1
            break
    for location in locations:
        if location in instruction:
            if location == 'side':
                location = 'edge'
            params['location'] = location
    for orient in orients:
        if orient in instruction:
            params['orient'] = orient
    
    #get size 
    
    num = re.compile(r'\d+').findall(instruction)
    twod = re.compile(r'\d+x\d+').findall(instruction)
    twodspace = re.compile(r'\d+\sx\s\d+').findall(instruction)
    threed = re.compile(r'\d+x\d+x\d+').findall(instruction)
    threedspace = re.compile(r'\d+\sx\s\d+\sx\s\d+').findall(instruction)

    if len(num) == 1:
        params['size'] = [int(num[0])]
    elif len(threed) == 1:
        params['size'] = [int(t) for t in threed[0].split('x')]
    elif len(threedspace) == 1:
        params['size'] = [int(t.strip()) for t in threedspace[0].split('x')]
    elif len(twod) == 1:
        params['size'] = [int(t.strip()) for t in twod[0].split('x')]
    elif len(twodspace) == 1:
        params['size'] = [int(t.strip()) for t in twodspace[0].split('x')]

    if axes:
        #make sure the size is the side!
        params['size'] = [int((params['size'][0] + 1)/2)]
    
    return params

with open(output_path, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

samples = []

ind = 0
for line in data[1:]:
    func_obj = {}
    instr = line[0].split('<Architect>')[1].strip()
    moves = get_moves(line)
    func_obj['index'] = ind 
    ind += 1
    func_obj['instruction'] = instr
    func_obj['raw output'] = moves
    param_dict = get_params(instr)
    func_obj['shape'] = param_dict['shape']
    #print(ind)
    #print(param_dict['shape'])
    if len(moves) == 0:
        func_obj['net_seq'] = None
    else:
        func_obj['in_bounds'] = fn.boundary_check(moves)
        seq = fn.get_net_sequence(moves)
        func_obj['net_seq'] = seq
        #then for each of the params, run function
        #GET SHAPE
        func_obj['size'] = param_dict['size']
        '-------------------------------------------------------TOWER'
        if param_dict['shape'] == 'tower':
            check = fn.is_tower(seq)
            if check:
                func_obj['shape_check'] = check[0]
                func_obj['size_check'] = check[1]
            else:
                func_obj['shape_check'] = None
                func_obj['size_check'] = None
        '---------------------------------------------------------ROW'
        if param_dict['shape'] == 'row':
            check = fn.is_row(seq)
            if check:
                func_obj['shape_check'] = check[0]
                func_obj['size_check'] = check[1]
            else:
                func_obj['shape_check'] = None
                func_obj['size_check'] = None
        '-------------------------------------------------------DIAGONAL'
        if param_dict['shape'] == 'diagonal':
            check = fn.is_diagonal(seq)
            if check:
                func_obj['shape_check'] = check[0]
                func_obj['size_check'] = check[1]
            else:
                func_obj['shape_check'] = None
                func_obj['size_check'] = None
        '---------------------------------------------------------DIAMOND'
        if param_dict['shape'] == 'diamond':
            check = fn.is_diamond(seq)
            if check:
                func_obj['shape_check'] = check[0]
                func_obj['size_check'] = check[1]
                # print(check[1])
                # print(type(check[1]))
            else:
                func_obj['shape_check'] = None
                func_obj['size_check'] = None
            ##get center
            func_obj['center'] = fn.get_center_quads(seq, 'diamond')
        '-----------------------------------------------------------SQUARE'
        if param_dict['shape'] == 'square':
            check = fn.is_square_unfilled(seq)
            if check:
                func_obj['shape_check'] = check[0]
                func_obj['size_check'] = check[1]
                print(check[1])
                print(type(check[1]))
            else:
                func_obj['shape_check'] = None
                func_obj['size_check'] = None
            ##############check filled square
            check = fn.is_square(seq)
            if check:
                func_obj['fill_shape_check'] = check[0]
                func_obj['fill_size_check'] = check[1]
            else:
                func_obj['fill_shape_check'] = None
                func_obj['fill_size_check'] = None
            ##get center
            func_obj['center'] = fn.get_center_quads(seq, 'square')
        '-------------------------------------------------------RECTANGLE'
        if param_dict['shape'] == 'rectangle':
            #print(param_dict['size'])
            check = fn.is_rectangle_unfilled(seq)
            if check:
                func_obj['shape_check'] = check[0]
                func_obj['size_check'] = check[1]
            else:
                func_obj['shape_check'] = None
                func_obj['size_check'] = None
            ##############check filled rectangle
            check = fn.is_rectangle(seq)
            if check:
                func_obj['fill_shape_check'] = check[0] # s = is_square(net_act_seq)
                func_obj['fill_size_check'] = check[1]
            else:
                func_obj['fill_shape_check'] = None
                func_obj['fill_size_check'] = None
            ##get center
            func_obj['center'] = fn.get_center_quads(seq, 'rectangle')
        '------------------------------------------------------------CUBE'
        if param_dict['shape'] == 'cube':
            check = fn.is_cube_all(seq)
            if check:
                func_obj['shape_check'] = check[0]
                func_obj['size_check'] = check[1]
            else:
                func_obj['shape_check'] = None
                func_obj['size_check'] = None
            ##get center
            func_obj['center'] = fn.get_center_quads(seq, 'cube')

        #CHANGE PRED SIZE TO LIST IF NOT NONE
        if type(func_obj['size_check']) in [int, np.int64]:
            func_obj['size_check'] = [func_obj['size_check']]
        elif type(func_obj['size_check']) == tuple:
            func_obj['size_check'] = list(func_obj['size_check'])

        if 'fill_size_check' in func_obj.keys():
            if func_obj['fill_size_check'] != None and type(func_obj['fill_size_check']) in [int, np.int64]:
                func_obj['fill_size_check'] = [func_obj['fill_size_check']]
            elif type(func_obj['fill_size_check']) == tuple:
                func_obj['fill_size_check'] =list(func_obj['fill_size_check'])

        #GET COLOR
        func_obj['color'] = param_dict['color']
        func_obj['check_color'] = fn.get_color(seq)[0]
        
        #GET LOCATION
        func_obj['loc'] = param_dict['location']
        func_obj['check_loc'] = fn.get_location_list(seq)

        #GET ORIENTATION
        func_obj['orient'] = param_dict['orient']
        func_obj['check_orient'] = fn.get_orientation(seq)

    samples.append(func_obj)

print(len(samples))
#print(samples[0])
    # for key in func_obj.keys():
    #     print(key)
    #     print(func_obj[key])
    #     print('------------------------S---------')


    # print(func_obj['instruction'])
    # print(func_obj['shape'], ' => ', func_obj['shape_check'])
    # print(func_obj['size'], ' => ', func_obj['size_check'])
    # if 'shape_fill' in func_obj.keys():
    #     print(func_obj['shape_fill'], ' => ', func_obj['fill_shape_check'])
    #     print(func_obj['size'], ' => ', func_obj['fill_size_check'])
    # print(func_obj['color'], ' => ', func_obj['check_color'])
    # print(func_obj['loc'], ' => ', func_obj['check_loc'])
    # print(func_obj['orient'], ' => ', func_obj['check_orient'])
    # print('-------------------')



with open(save_path, 'w') as outfile:
    json.dump(samples, outfile, default=int)

print('json saved.')

"""
takes the json output from functions.py
and calculates the dimension correctness for each sample
and 
"""
import os
import csv
import re
import json


current_folder=os.getcwd()

#original nebula on clarification q's
# json_path = current_folder + '/nebula_org_clarif_output.json'
# save_path = current_folder + '/nebula_org_clarif_output_foranalysis.csv'

#nebula finetuned on clarification q's
# json_path = current_folder + '/nebula_ft_clarif_output.json'
# save_path = current_folder + '/nebula_ft_clarif_output_foranalysis.csv'

#nebulipa WITH structure
# json_path = current_folder + '/nebulipa_clarif_withstructure.json'
# save_path = current_folder + '/nebulipa_clarif_withstructure_foranalysis.csv'

#nebulipa WITHOUT structure
# json_path = current_folder + '/nebulipa_clarif_withoutstructure.json'
# save_path = current_folder + '/nebulipa_clarif_withoutstructure_foranalysis.csv'

#nebulipa WITHOUT structure
json_path = current_folder + '/nebulipa_corrsynth_nostruct.json'
save_path = current_folder + '/nebulipa_corrsynth_nostruct_foranalysis.csv'

with open(json_path, 'r') as j:
    jfile = json.load(j)
    samples = jfile

headers = ['Shape', 'Color','Shape_corr', 'Size_corr', 'Loc_corr', 'Orient_corr', 'In_bounds', 'Full_struct_corr']
rows = []

for i, sample in enumerate(samples): 
    # print(i)
    row = []
    shape = sample['shape'] 
    
    #print(sample['index'])
    
    if sample['net_seq'] == None:
        row.append(shape + '_botched')
        row.extend([0, 0, 0, 0, 0])
    else:
        corr_bounds = sample['in_bounds']
        corr_shape = 0
        corr_color = 0
        corr_size = 0
        corr_loc = 0
        corr_orient = 0

        #print(sample['instruction'])
        row.append(shape)
        pred_shape = sample['shape_check']

        size = sample['size']
        pred_size = sample['size_check']

        color = sample['color']
        pred_color = sample['check_color']
        
        loc = sample['loc']
        pred_loc = sample['check_loc']

        orient = sample['orient']
        pred_orient = sample['check_orient']


        #COLOR IS SAME FOR ALL
        #get color 
        if color == pred_color:
            corr_color = 1
        row.append(corr_color)

        #CASE 1: TOWER, ROW, DIAGONAL
        if shape in ['row', 'diagonal', 'tower']:
            print(shape)
            if pred_shape is True:
                corr_shape = 1
                if size[0] == pred_size[0]:
                    corr_size = 1
            if loc == None:
                corr_loc = 'N/A'
            elif loc in pred_loc:
                corr_loc = 1
            row.append(corr_shape)
            row.append(corr_size)
            row.append(corr_loc)
            #orientation is moot
            corr_orient = 'N/A'
            row.append(corr_orient)

        #CASE 2: RECTANGLE ---NB HAVE TO DEAL WITH CENTER ISSUE
        if shape == 'rectangle':
            # print('rectangle')
            #first try unfilled version
            if pred_shape is True:
                # print('shape true')
                # print(size)
                # print(pred_size)
                corr_shape = 1
                if set(size) == set(pred_size):
                    corr_size = 1
            #then try filled version
            elif sample['fill_shape_check'] is True: #check for filled condition 
                #print('fill shape true')
                corr_shape = 1
                if set(size) == set(sample['fill_size_check']):
                    corr_size = 1
            if loc == None:
                corr_loc = 'N/A'
            elif loc == 'center':
                if sample['center'] == True:
                    corr_loc = 1
            else:
                if loc in pred_loc:
                    corr_loc = 1
            if orient == None:
                corr_orient = 'N/A'
            else:
                if orient == pred_orient:
                    corr_orient = 1
            row.append(corr_shape)
            row.append(corr_size)
            row.append(corr_loc)
            row.append(corr_orient)

        #CASE 3: SQUARE
        if shape == 'square':
            #first try unfilled version
            if pred_shape is True:
                corr_shape = 1
                if set(size) == set(pred_size):
                    corr_size = 1
            #then try filled version
            elif sample['fill_shape_check'] is True:
                corr_shape = 1
                if set(size) == set(sample['fill_size_check']):
                    corr_size = 1
            if loc == None:
                corr_loc = 'N/A'
            elif loc == 'center':
                if sample['center'] == True:
                    corr_loc = 1
            else:
                if loc in pred_loc:
                    corr_loc = 1
            if orient == None: #orientation is moot for cubes
                corr_orient = 'N/A'
            else:
                if orient == pred_orient:
                    corr_orient = 1
            row.append(corr_shape)
            row.append(corr_size)
            row.append(corr_loc)
            row.append(corr_orient)
        
        #CASE 4 CUBE
        if shape == 'cube':
        #first try unfilled version
            if pred_shape is True:
                corr_shape = 1
                if set(size) == set(pred_size):
                    corr_size = 1
            #then try filled version
            if loc == None:
                corr_loc = 'N/A'
            elif loc == 'center':
                if sample['center'] == True:
                    corr_loc = 1
            else:
                if loc in pred_loc:
                    corr_loc = 1
            if orient == None: #orientation is moot for cubes
                corr_orient = 'N/A'
            else:
                if orient == pred_orient:
                    corr_orient = 1
            row.append(corr_shape)
            row.append(corr_size)
            row.append(corr_loc)
            row.append(corr_orient)

        #CASE 5: DIAMOND ---NB HAVE TO DEAL WITH CENTER ISSUE
        if shape == 'diamond':
            print(pred_shape)
            if pred_shape is True:
                corr_shape = 1
                if size[0] == pred_size[0]:
                    corr_size = 1
            if loc == None:
                corr_loc = 'N/A'
            elif loc == 'center':
                if sample['center'] == True:
                    corr_loc = 1
            else:
                if loc in pred_loc:
                    corr_loc = 1
            if orient == None: 
                corr_orient = 'N/A'
            else:
                if orient == pred_orient:
                    corr_orient = 1
            row.append(corr_shape)
            row.append(corr_size)
            row.append(corr_loc)
            row.append(corr_orient)

    row.append(corr_bounds)
    #FINALLY CHECK FULL STRUCTURE
    #check if full structure is correct 
    if 0 not in row:
        row.append(1)
    else:
        row.append(0)
    # print(row)
    # print('-------------------')
    assert len(row) == len(headers)
    rows.append(row)

with open(save_path, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

    

    

    




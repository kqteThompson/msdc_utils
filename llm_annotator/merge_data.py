"""
merges bert.jsons 
"""
import os 
import json 

current_folder=os.getcwd()

open_path = current_folder + '/annotated_data/'

json_files = os.listdir(open_path)

merge = ['TEST_101_bert.json', 'DEV_32_bert.json']

new_file = 'TEST_133.json'

final_list = []
for file in merge:
    with open(open_path + file, 'r') as jf:
        jfile = json.load(jf)
        for game in jfile:
            final_list.append(game)

print('final games : {}'.format(len(final_list)))

with open(open_path + new_file, 'w') as outfile:
    json.dump(final_list, outfile)

print('json saved')
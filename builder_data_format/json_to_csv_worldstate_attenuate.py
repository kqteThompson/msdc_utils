"""
Creates a CSV file for training LLAMA builder from train.json
STEP 1: for game, split according to NARRATION
STEP 2: for each NARRATION, create one sample for each ACTION sequence in the NARRATION
NB: this is a variation from the original json_to_csv.py 
where we are using a different worldstate format and we are not adding the previous moves.

V1
example: 
<WORLDSTATE at beginning of the narration> + Inst =>  ACTION
if more than one action:
<WORLDSTATE at beginning of the narration> + <Inst> + <action> + <Inst> => ACTION

**attenuate:
if 


V2:
TBD
**(might also try with putting the worldstate just before every instruction, even inside narrations)

"""

import os
import json
import csv


current_folder=os.getcwd()

train_data = current_folder + '/test_ws.json'

csv_list = []


with open(train_data, 'r') as jf:
    data = json.load(jf)
    for game in data:
        game_id = game['game_id']
        if game_id.split('-')[0] not in ['C17','C32','C3']:
            dialogue = game['dialogue']
            original_moves = len([c for c in dialogue if isinstance(c, dict)]) #to compare with num moves after
            narr_splits = []
            single_narr = []
            utterance_block = []
            for line in dialogue:
                if 'NARRATION' in line:
                    #split off narration and start new single narr
                    if len(single_narr) != 0 :
                        # print('empty ', game_id)
                        narr_splits.append(single_narr)
                    single_narr = []
                    utterance_block = []
                    new_line = line.split('NARRATION')[1]
                    utterance_block.append(new_line)
                else:
                    if isinstance(line, dict):
                        single_narr.append(utterance_block)
                        utterance_block = []
                        single_narr.append(line)
                    else:
                        utterance_block.append(line)
            narr_splits.append(single_narr)
            

            #now narr_splits is a list of lists, each a set of moves that comprises one narrative arc
            #the linguistic utterances are combined into a single list, so that we can easily keep track of I-A-I

            r=0 #to keep track of moves added 
            last_world_state = 'EMPTY'

            for split in narr_splits:
                print(split)
                print('----------------')
                
                dial_with_actions = []
                dial_with_actions.append(last_world_state)

                dial_with_actions.extend(split[0])
                 # print('head: ', head)
                dial_string = '\n'.join(dial_with_actions)
                last_move = split[1]['moves']
                last_world_state = split[1]['worldstate']

                csv_list.append([dial_string, last_move])
                r += 1

                all_actions = len([c for c in split if isinstance(c, dict)]) #to compare with num moves after
                if all_actions > 1:
                    #continue with a window
                    sub_start = 0
                    for samp in range(all_actions-1):
                        dial_with_actions = []
                        dial_with_actions.append(last_world_state)
                        dial_with_actions.extend(split[sub_start])
                        dial_with_actions.append(split[sub_start + 1]['moves'])
                        dial_with_actions.extend(split[sub_start + 2])
                        # print('head: ', head)
                        dial_string = '\n'.join(dial_with_actions)
                        last_move = split[sub_start + 3]['moves']
                        last_world_state = split[sub_start + 3]['worldstate']

                        csv_list.append([dial_string, last_move])
                        r += 1
                        sub_start += 2

            if r != original_moves:
                print('not the same ## of moves! {} in original, {} in csv'.format(original_moves, r))


print('all games done, {} samples, creating csv...'.format(len(csv_list)))
fields = ['dial_with_actions', 'action_seq']
with open(current_folder + '/actseq-test-narr-worldstate_attenuated.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(csv_list)

print('csv saved.')





# print('done')
# for item in csv_list:
#     print(item[0])
#     print('~~~~')
#     print(item[1])
#     # print('{} :: {}').format(item[0], item[1])
#     print('--------------------------------------')
               
            


        




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

V2:
TBD
**(might also try with putting the worldstate just before every instruction, even inside narrations)

TRAIN
longest field = 3007
3722 train samples
VAL
longest field = 2677
1322 train samples
TEST
longest field = 2116
1575 train samples
"""

import os
import json
import csv


current_folder=os.getcwd()

train_data = current_folder + '/test_ws.json'

csv_list = []

#stats
lengths = []

with open(train_data, 'r') as jf:
    data = json.load(jf)
    for game in data:
        game_id = game['game_id']
        if game_id.split('-')[0] not in ['C17','C32','C3']:
            dialogue = game['dialogue']
            original_moves = len([c for c in dialogue if isinstance(c, dict)]) #to compare with num moves after
            narr_splits = []
            single_narr = []
            for line in dialogue:
                if 'NARRATION' in line:
                    #split off narration and start new single narr
                    narr_splits.append(single_narr)
                    single_narr = []
                    new_line = line.split('NARRATION')[1]
                    single_narr.append(new_line)
                else:
                    single_narr.append(line)
            narr_splits.append(single_narr)

            #now narr_splits is a list of lists, each a set of moves that comprises one narrative arc
           
            last_world_state = 'EMPTY'

            r=0 #to keep track of moves added 
            for split in narr_splits:
                dial_with_actions = []
                
                # if len(last_move) > 0:
                #     dial_with_actions.append(last_move) #but what if last move is 0
            
                dial_with_actions.append(last_world_state)

                for s in split:
                
                    if isinstance(s, str):
                        dial_with_actions.append(s)
                    else:
                        last_move = s['moves']
                        last_world_state = s['worldstate']
                        
                        dial_string = '\n'.join(dial_with_actions)
                        lengths.append(len(dial_string))
                        csv_list.append([dial_string, last_move])
                        r += 1
                        dial_with_actions.append(last_move) #add last move
                        #dial_with_actions[0] = s['worldstate'] #pop worldstate and add latest world state
            #compare r to original
            if r != original_moves :
                print('not the same ## of moves! {} in original, {} in csv'.format(original_moves, r))

print('longest field = {}'.format(max(lengths)))
print('all games done, {} samples, creating csv...'.format(len(csv_list)))
fields = ['dial_with_actions', 'action_seq']
with open(current_folder + '/actseq-test-narr-worldstate.csv', 'w') as f:
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
               
            


        




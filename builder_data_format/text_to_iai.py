"""
Creates a json file that contains each game with id, i-a-i move re-formatting, and game state.
outputs a json of games that can then be converted to csv
"""

import os
import json
from collections import defaultdict
import string
import re
#from thefuzz import fuzz

def transform_moves(action_list):
    """
    Get new move format
    [Builder puts down a green block at X:-1 Y:1 Z:3] --> place green -1 1 3
    """
    colors = ['green', 'blue', 'red', 'yellow', 'orange', 'purple']
    move_list = []
    for a in action_list:
        if len(a) > 0:
            move_string = ''
            if 'puts' in a:
                move_string += 'place '
                for color in colors:
                    if color in a:
                        move_string += color + ' '
            else:
                move_string += 'pick '
            x = a.split('X:')[1][:2].rstrip(']').rstrip()
            y = a.split('Y:')[1][:2].rstrip(']').rstrip()
            z = a.split('Z:')[1][:2].rstrip(']').rstrip()
            move_string += x + ' ' + y + ' ' + z
            move_list.append(move_string)
    moves = '\n'.join(move_list)
    return moves 

def get_state(action_list, worldstatedict):
    """
    takes current actions and worldstate dict and updates worldstate
    uses global action counter to add indexes
    """
    global global_action_index
    colors = ['green', 'blue', 'red', 'yellow', 'orange', 'purple']
    for action in action_list.split('\n'):
        if 'pick' in action:
            coord = action.split('pick')[1].strip()
            for color in colors:
                if color in worldstatedict.keys():
                    for c in worldstatedict[color]:
                        if coord == c[0]:
                            worldstatedict[color].remove(c)
                            break
        else:
            for color in colors:
                if color in action:
                    coord = action.split(color)[1].strip()
                    worldstatedict[color].append((coord, global_action_index))
                    global_action_index += 1
    return worldstatedict

def format_worldstate(worldstatedict):
    """
    takes updated worldstate and formats it for json
    """
    state = []
    state_str = 'Empty'
    for key in worldstatedict.keys():
        if len(worldstatedict[key]) > 0: #don't print info about 'empty' colors
            for coord in worldstatedict[key]:
                move_str = 'place ' + key + ' ' + coord[0]
                state.append((move_str, coord[1]))
    #now should have a list of all place moves still on the board
    #each a tuple with (movestr, placement_index)
    #now order the list by placement indicies
    if len(state) == 1:
        state_str = state[0][0]
    if len(state) > 0:
        state.sort(key=lambda x:x[1])
        state_str = ', '.join([s[0] for s in state])
    return state_str

def string_reg(text_str):
    """
    remove punctuation and spacing from text 
    """
    # clean = text_str.translate(str.maketrans('', '', string.punctuation))
    # cleanstr = re.sub(' +', ' ', clean)
    cleanstr = re.sub(r'\W+', '', text_str)
    return cleanstr

current_folder=os.getcwd()

textfile_path = current_folder + '/splits/train/'

textfiles = os.listdir(textfile_path)

game_jsons = [] #list of jsons

print('number of text games: {}'.format(len(textfiles)))

narr_mishaps = []
for tf in textfiles:
    # print(tf)
    game_json = {}
    with open(textfile_path + tf, 'r') as txt:
        text = txt.read().split('\n')
    text_id = text[0].split('-')
    
    worldstate = defaultdict(list) #this will be a global variable representing world state
    actions = []
    utterance_blocks = []
    game_id = text_id[2] + '-' + text_id[0] + '-' + text_id[1]
    game_json['game_id'] = game_id
    game_json['dialogue'] = []

    global_action_index = 0

    

    for move in text[1:]:
        if '<Builder>' in move or '<Architect>' in move:
            if len(actions) > 0:
                action = {} #create an action dict
                moves = transform_moves(actions) 
                if len(moves) > 1:
                    action['moves'] = moves
                    #update worldstate with actions
                    get_state(moves, worldstate)
                    action['worldstate'] = format_worldstate(worldstate)
                    actions = []
                    game_json['dialogue'].append(action)
            #append linguistic move only after any non-ling moves are added.
            utterance_blocks.append(move)
            # game_json['dialogue'].append(move)
        else:
            if len(utterance_blocks) > 0:
                game_json['dialogue'].append(utterance_blocks)
                utterance_blocks = []
            actions.append(move)
    if len(utterance_blocks) > 0:
        assert len(actions) == 0, 'there are still actions'
        game_json['dialogue'].append(utterance_blocks)
    if len(actions) > 0:
        assert len(utterance_blocks) == 0, 'there are still utterances'
        action = {}
        moves = transform_moves(actions)
        if len(moves) > 1:
            action['moves'] = moves
            get_state(moves, worldstate)
            action['worldstate'] = format_worldstate(worldstate)
            game_json['dialogue'].append(action)
    game_jsons.append(game_json)
    #keep track of all games where narrations weren't used

with open(current_folder + '/train_iai.json', 'w') as outfile:
    json.dump(game_jsons, outfile)

print('json saved for {} games'.format(len(game_jsons)))







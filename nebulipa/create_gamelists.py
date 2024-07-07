"""
for NEBULAMIPA training. 
takes a json of annotated minecraft games and converts to 
a game_id plus a list of formatted edus e.g. '1.<Arch>blah blah'. 
If the edu contains game moves, then format plus world state information:
['2.<Buil> place blue 1 2 3, place blue 1 2 4', WORLDSTATE]
Returns a json to be used in the next step of data preparation for NEBULAMIPA
"""
import os
import json
from collections import defaultdict

map_rels_str = {'Comment':'COM', 'Contrast':'CONTR', 'Correction':'CORR', 'Question-answer_pair':'QAP', 'Acknowledgement':'ACK','Elaboration':'ELAB',
                 'Clarification_question':'CLARIFQ', 'Conditional':'COND', 'Continuation':'CONTIN', 'Result':'RES', 'Explanation':'EXPL', 'Q-Elab':'QELAB',
                 'Alternation':'ALT', 'Narration':'NARR', 'Confirmation_question':'CONFQ', 'Sequence':'SEQ'}


def format_worldstate(worldstatedict):
    """
    takes updated worldstate and formats it for json
    """
    state = []
    state_str = 'EMPTY'
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

def is_nl(edu):
    """
    if every word in alphanumeric and has len 5
    """
    nl = 1
    words = edu.split(' ')
    # print(words)
    # print(words)
    for word in [w for w in words if w != '']:
        if not contains_number(word) or len(word) != 5:
            nl = 0
            break
    # print(nl)
    return nl

def contains_number(string):
    return any(char.isdigit() for char in string)

def decode(tok_str):
    """
    takes a list bert tokens and changes them back to coordinates.
    """
    zdict = {'a':'-5', 'e' : '-4', 'i':'-3', 'o':'-2', 'u':'-1', 'p':'0', 
             'q':'1', 'r':'2', 'x': '3', 'y':'4', 'z':'5'}
    xdict = {'b': '-5', 'c' :'-4', 'd' : '-3', 'f' : '-2', 'g' : '-1', 'h':'0', 
             'j':'1', 'k':'2', 'l':'3', 'm':'4', 'n':'5'}
    colors = {'r' :'red', 'b':'blue', 'g':'green', 'o':'orange', 'y':'yellow', 'p':'purple'}
    # action = {'0' : 'pick', '1': 'place'}
    decoded = []
    #print(tok_str)
    for tok in tok_str.split():
        # print(tok)
        if tok[0] == '0':
            new_string = 'pick ' +  xdict[tok[2]] + ' ' + tok[3] + ' ' + zdict[tok[4]]
        else:
            new_string = 'place ' + colors[tok[1]] + ' ' +  xdict[tok[2]] + ' ' + tok[3] + ' ' + zdict[tok[4]]
        decoded.append(new_string)
    moves_str_pred = '\n'.join(decoded)
    moves_str_eeu = ', '.join(decoded)
    return moves_str_pred, moves_str_eeu

# def format_edu(edu, index):
#     edu_str = str(index) + '. ' + edu['speaker'][:4] + ' ' + edu['text']
#     return None

current_folder=os.getcwd()

data_path = '/home/kate/minecraft_utils/llm_annotator/annotated_data/TEST_133.json'
save_path = current_folder + '/TEST_lists.json'
##get the narrative arcs for each game

with open(data_path, 'r') as j:
    jfile = json.load(j)
    games = jfile

##for each game, find turns, edus.
##feed one turn at a time, with each edu numbered, plus structure for that turn
##TEXT:   ##STRUCTURE:  ##NEXT TURN   => #output structure
new_games = []
for game in games:
    new_game = {}
    new_game['id'] = game['id']
    #print(game['id'])
    edus = game['edus']
    game_list = []
    last_worldstate = 'EMPTY'
    worldstate = defaultdict(list) #this will be a global variable representing world state
    global_action_index = 0
    for i, edu in enumerate(edus):
        if edu['speaker'] == 'Builder' and is_nl(edu['text']):
            #do text and worlstate thing
            moves, eeu = decode(edu['text'])
            # eeu_str = str(i) + '. ' + edu['speaker'][:4] + ' ' + moves
            # worldstate = 'WORLDSTATE'
            moves_dict = {}
            get_state(moves, worldstate)
            moves_dict['moves'] = moves
            moves_dict['eeu'] = str(i) + '. ' + edu['speaker'][:4] + ': ' + eeu
            moves_dict['worldstate'] = last_worldstate
            last_worldstate = format_worldstate(worldstate)
            game_list.append(moves_dict)
        else:
            edu_str = str(i) + '. ' + edu['speaker'][:4] + ': ' + edu['text']
            game_list.append(edu_str)
    new_game['list'] = game_list
    new_games.append(new_game)

with open(save_path, 'w') as outfile:
    json.dump(new_games, outfile)

print('json saved for {} games'.format(len(new_games)))
    
 
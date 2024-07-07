"""
for LLAMA parsing:
takes a json of annotated minecraft games and converts to 
a turn format to be used format_jsonl.py. 
[
    {
        "id": "C54-B13-A30",
        "turns": [
            {
                "turn": 0,
                "speaker": "Builder",
                "edus": [
                    "Mission has started."
                ]
            },
            {
                "turn": 1,
                "speaker": "Architect",
                "edus": [
                    "start on one edge of the space",
                    "and build a staircase towards the middle with yellow block that is 3 stairs high"
                ]
            },...
]
"""
import os
import json

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
    for tok in tok_str.split():
        # print(tok)
        if tok[0] == '0':
            new_string = 'pick ' +  xdict[tok[2]] + ' ' + tok[3] + ' ' + zdict[tok[4]]
        else:
            new_string = 'place ' + colors[tok[1]] + ' ' +  xdict[tok[2]] + ' ' + tok[3] + ' ' + zdict[tok[4]]
        decoded.append(new_string)
    moves_str = ', '.join(decoded)
    return moves_str

current_folder=os.getcwd()

data_path = current_folder + '/annotated_data/TEST_101_bert.json'
save_path = current_folder + '/TEST_turns.json'

with open(data_path, 'r') as j:
    jfile = json.load(j)
    games = jfile

##for each game, find turns, edus.
##feed one turn at a time, with each edu numbered, plus structure for that turn
##TEXT:   ##STRUCTURE:  ##NEXT TURN   => #output structure
turn_version = []
for game in games:
    new_game = {}
    new_game['id'] = game['id']
    game_turns = []
    edus = game['edus']
    #the first edu is always the first turn. 
    turn_no = 0
    last_speaker = None
    new_turn = {}
    new_turn['turn'] = turn_no
    new_turn['speaker'] = edus[0]['speaker']
    turn_edus = []
    turn_edus.append(edus[0]['text'])
    for edu in edus[1:]:
        if edu['speaker'] == 'Architect':
            if edu['speaker'] == last_speaker:
                turn_edus.append(edu['text'])
            else:
                last_speaker = edu['speaker']
                #finish and append last turn
                new_turn['edus'] = turn_edus
                game_turns.append(new_turn)
                turn_no += 1
                #now start a new turn!
                new_turn = {}
                new_turn['turn'] = turn_no
                new_turn['speaker'] = last_speaker
                turn_edus = [] #a list of edus from that turn
                turn_edus.append(edu['text'])
        else:
            if is_nl(edu['text']):
                #then this is an action sequence and should be it's own turn
                last_speaker = None #need to do this so that builder actions turns are always their own turns
                #finish and append last turn
                new_turn['edus'] = turn_edus
                game_turns.append(new_turn)
                turn_no += 1
                #now start a new turn!
                new_turn = {}
                new_turn['turn'] = turn_no
                new_turn['speaker'] = 'Builder'
                turn_edus = [] #a list of edus from that turn
                formatted_moves = decode(edu['text'])
                #formatted_moves = 'builder moves' #just use a dummy placeholder
                turn_edus.append(formatted_moves)
            elif edu['speaker'] != last_speaker:
                last_speaker = edu['speaker']
                #finish and append last turn
                new_turn['edus'] = turn_edus
                game_turns.append(new_turn)
                turn_no += 1
                #now start a new turn!
                new_turn = {}
                new_turn['turn'] = turn_no
                new_turn['speaker'] = last_speaker
                turn_edus = [] #a list of edus from that turn
                turn_edus.append(edu['text'])
            else:
                turn_edus.append(edu['text'])
    #take care of last speaker turn in the game
    new_turn['edus'] = turn_edus
    game_turns.append(new_turn)
    #append new turns to the game dict
    new_game['turns'] = game_turns
    #add game dict to list of games
    turn_version.append(new_game)

with open(save_path, 'w') as outfile:
    json.dump(turn_version, outfile)

print('json saved for {} games'.format(len(turn_version)))
    
    
    #add turns and edu numbers
    #get edu list with global and turn indices

    #for turn in turns:
    #count edus, and add will total edu count < 11
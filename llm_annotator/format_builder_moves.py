"""
takes a json input and changes the builder game moves from code back to move text

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
            new_string = 'pick ' +  colors[tok[1]] + ' ' + xdict[tok[2]] + ' ' + tok[3] + ' ' + zdict[tok[4]]
        else:
            new_string = 'place ' + colors[tok[1]] + ' ' +  xdict[tok[2]] + ' ' + tok[3] + ' ' + zdict[tok[4]]
        decoded.append(new_string)
    moves_str = ', '.join(decoded)
    return moves_str

current_folder=os.getcwd()

data_path = current_folder + '/annotated_data/DEV_32_bert.json'
save_path = current_folder + '/annotated_data/DEV_32.json'

with open(data_path, 'r') as j:
    jfile = json.load(j)
    games = jfile


for game in games:
    new_edus = []
    edus = game['edus']
    for edu in edus:
        if edu['speaker'] == 'Builder' and is_nl(edu['text']):
            new_text = decode(edu['text'])
            edu['text'] = new_text
            new_edus.append(edu)
        else:
            new_edus.append(edu)
    game['edus'] = new_edus


with open(save_path, 'w') as outfile:
    json.dump(games, outfile)

print('json saved for {} games'.format(len(games)))
    
    

import os
import json

"""
takes a json of annotated games and returns a readable text file 
saves one file per game in a folder 
"""

def is_nl(edu):
    """
    if every word in alphanumeric and has len 5
    """
    nl = 1
    words = edu.split(' ')
    # print(words)
    for word in [w for w in words if w != '']:
        if not contains_number(word) or len(word) < 5:
            nl = 0
            break
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
    action = {'0' : 'remove', '1': 'put'}
    decoded = []
    for tok in tok_str.split():
        # print(tok)
        new_string = action[tok[0]] + ' ' + colors[tok[1]] + ' X:' +  xdict[tok[2]] + ' Y:' + tok[3] + ' Z:' + zdict[tok[4]]
        decoded.append(new_string)
    dec_str = '|'.join(decoded)
    full_dec = '|'+ dec_str
    return full_dec

current_folder=os.getcwd()

corpus_path = current_folder + '/TRAIN_2024-04-07_307_flat_bert.json'

folder_path = current_folder + '/train_games/'
os.mkdir(folder_path)

with open(corpus_path, 'r') as j:
    jfile = json.load(j)
    games = jfile
    prompt_snippets = []
    filtered_snippets = [] ##a list of jsons

for game in games[:5]:
    print(game['id'])
    game_id = game['id']
    text_list = []
    
    edu_list = [[edu['speaker'], edu['text'],[]] for edu in game['edus']]
    for rel in game['relations']:
        edu_list[rel['y']][2].append([rel['x'], rel['type']])
    for i, item in enumerate(edu_list):
        item_string = str(i) + ' <' + item[0] + '> ' 
        ##check for NL moves
        if item[0] == 'Builder' and is_nl(item[1]):
            item_string += decode(item[1])
        else:
            item_string += item[1]
        ##add relations
        if len(item[2]) > 0:
            item_string += '$$'
        for inc_rel in item[2]:
            item_string += '[' + str(inc_rel[0]) + ',' + inc_rel[1] + '] '
        text_list.append(item_string)

    
    print_string = '\n'.join(text_list)
    with open (folder_path + game_id + '.txt', 'w') as txt_file:
        txt_file.write(print_string)
    


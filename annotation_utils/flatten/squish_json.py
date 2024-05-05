"""
Takes a json files of ANNOTATED games and returns a json with squished & flattened games
Grosso modo:
1. For each EDU, if speaker == 'System', replace the text with simplified move text
2. For each CDU, if it is a builder moves CDU: 
    2.1. Find the last EDU, creating a *replacements* dict that maps CDU ids to last id
    2.2. For each EDU, if there is an outgoing link, add EDU id : last id to *replacements*
    AND add dangler ids to *targets* dict to change start position of edu (so they go below the action block)
    AND add all outgoing links from the CDU itself to the *cdu_outgoing* dict, so that
    if the target EDU is "within" the CDU, it will be moved below.
    2.3. For each EDU that is not the last, gather the text and squish into one block
    and assign to the last edu by adding to the dict *squish*, mapping last id : squish text
    2.4. Add all non-last EDU ids to the *redundant* list to be removed 
3. For each CDU, if it is not a builder moves CDU: 
**NB there should be none of these CDUS in this data
    3.1 Find the head EDU
    3.2 For every head EDU, add CDU id : head id
4. Go through and do all replacements

NB: the output of this script is only useful as an input to a BERT formatting script.
If you want to visualize with GLOZZ, BERT format then to BERT to GLOZZ formatting.
"""
import os 
import json 
import re
import datetime
from collections import defaultdict
import pickle

current_folder=os.getcwd()

#path to the output file from glozz_to_json.py
open_path = '/home/kate/minecraft_utils/annotation_utils/glozz_to_json/json_output/'

save_path = current_folder + '/json_flat/'

split = 'TEST'

squish_record = defaultdict(list)

json_files = os.listdir(open_path)

def cdu_contents(edus):
    """
    takes CDU elements and returns 1 if CDU is all builder moves
    """
    contents = 0
    speakers = list(set([e[2] for e in edus]))
    if len(speakers) == 1 and speakers[0] == 'System':
        contents = 1

    return contents

def get_bert_token(coord_list):
    """
    takes a list of coordinates and returns a custom Bert token 3 chars long
    """
    xdict = {'-5': 'b', '-4': 'c', '-3': 'd', '-2': 'f', '-1': 'g', '0': 'h', 
             '1':'j', '2':'k', '3':'l', '4':'m', '5':'n'}
    zdict = {'-5': 'a', '-4': 'e', '-3': 'i', '-2': 'o', '-1': 'u', '0': 'p', 
             '1':'q', '2':'r', '3':'x', '4':'y', '5':'z'}
    token = ''
    skip_flag = 0
    for c in coord_list:
        i,j = c.split(':')
        if i == 'X':
            try:
                token += xdict[j]
            except KeyError:
                print('issue with X coord: {}'.format(coord_list))
                #token += 'n' ##for now just assume highest X coord
                skip_flag = 1 #make skip flag
        if i == 'Y':
            token += j
        if i == 'Z':
            try:
                token += zdict[j]
            except KeyError:
                print('issue with Z coord: {}'.format(coord_list))
                ##token += 'a' ##for now just assume lowest Z coord
                skip_flag = 1 #make skip flag
        if skip_flag == 1:
            token = 'SKP'
    return token 

def text_replace(text):
    colors  = ['red', 'blue', 'green', 'orange', 'yellow', 'purple']
    color = re.findall(r"\b({})\b".format('|'.join(colors)), text, flags=re.IGNORECASE)
    if 'puts' in text:
        replacement = 'place {} block. '.format(color[0])
    else:
        replacement = 'remove {} block. '.format(color[0])
    return replacement

def text_replace_coords(text):
    colors  = ['red', 'blue', 'green', 'orange', 'yellow', 'purple']
    color = re.findall(r"\b({})\b".format('|'.join(colors)), text, flags=re.IGNORECASE)
    coords = text.split('at')[1].strip(']').strip()
    if 'puts' in text:
        replacement = 'place {} block {}. '.format(color[0], coords)
    else:
        replacement = 'remove {} block {}. '.format(color[0], coords)
    return replacement

def text_replace_embeddings(text):
    
    colors  = ['red', 'blue', 'green', 'orange', 'yellow', 'purple']
    color = re.findall(r"\b({})\b".format('|'.join(colors)), text, flags=re.IGNORECASE)
    coords = text.split('at')[1].strip(']').strip().split(' ')
    embed = get_bert_token(coords)
    if len(embed) != 3:
        print('{} not len 3'.format(coords))
    """
    [Builder puts down a green block at X:-3 Y:1 Z:-1]
    """
    if 'puts' in text:
        replacement = 'put {} {} '.format(color[0], embed)
    else:
        replacement = 'remove {} {} '.format(color[0], embed)
    return replacement

def text_replace_embeddings_full(text):
    print(text)
    colors  = ['red', 'blue', 'green', 'orange', 'yellow', 'purple']
    color = re.findall(r"\b({})\b".format('|'.join(colors)), text, flags=re.IGNORECASE)
    c = color[0][0]
    coords = text.split('at')[1].strip(']').strip().split(' ')
    print('COORDS', coords)
    embed = get_bert_token(coords)
    if len(embed) != 3:
        print('{} not len 3'.format(coords))
    """
    [Builder puts down a green block at X:-3 Y:1 Z:-1]
    """
    if embed == 'SKP':
        # replacement = 'SKIP '
        replacement = ''
    else:
        if 'puts' in text:
            replacement = ['1', c, embed, ' ']
            replacement = ''.join(replacement)
        else:
            replacement = ['0', c, embed, ' ']
            replacement = ''.join(replacement)
    return replacement

def squish_text(elements):
    elements.sort(key = lambda x :x[1])
    squished = ''.join([s[3] for s in elements])
    return squished 

# for f in json_files:
for f in json_files:
    linguistic_cdus = [] # a list of the uncaught linguistic CDUs
    with open(open_path + f, 'r') as jf:
        jfile = json.load(jf)
        for game in jfile:
        #for game in [g for g in jfile if g['game_id'] == 'C17-B47-A30']:
            print(game['game_id'])
            replacements = {}
            squish = {}
            redundant = []
            targets = {}
            cdu_outgoing = {}
            #STEP 0: change all builder text in system moves
            for edu in game['edus']:
                if edu['Speaker'] == 'System':
                    #new_text = text_replace_coords(edu['text']) 
                    print("EDU text", edu['text'])
                    # print(edu['unit_id'])
                    new_text = text_replace_embeddings_full(edu['text'])
                    edu['text'] = new_text
                    if len(new_text) > 235:
                        print('-------------')
                        print(len)
                        print(game['game_id'], edu['turnID'])
                        
            #STEP 1: pull elements from each CDU 
            edus = [(e['unit_id'], e['start_pos'], e['Speaker'], e['text']) for e in game['edus']]
            cdus = game['cdus']
            cdu_ids = [cdu['schema_id'] for cdu in cdus]
            edu_pos = {e['unit_id'] : e['start_pos'] for e in game['edus']}
            
            for cdu in cdus:
                cid = cdu['schema_id']
                elements = [elem for elem in edus if elem[0] in cdu['embedded_units']]
                element_ends = {elem[1]: elem[0] for elem in elements}

                #STEP 2: get a list of the outgoing links 
                outgoing_links = defaultdict(list)
                #use default dict for cases where more than one target per relation
                for rel in game['relations']:
                    outgoing_links[rel['x_id']].append(rel['y_id'])
                
                #STEP 3: determin where the last position should be for the squished CDU
                #if there is an outgoing relation in the cdu, make the element position just above that the last one
                
                
                if cid in outgoing_links.keys():
                    print(cid)
                    target_list = []
                    for target in [o for o in outgoing_links[cid] if o not in cdu_ids]:
                        #this looks at only outgoing links that are to edus, not to another CDU
                        # print('cdu with outgoing rel')
                        #find the min pos and make that the last position for the edu
                        target_list.append(edu_pos[target])
                        #need to find the EDU id that belongs to the EDU just before tail position
                        #using a list of end positions of the cdu elements
                    if len(target_list) > 0:
                        tail_position = min(target_list)
                        # print(tail_position)
                        # print(element_ends.keys())
                        dus_above = [k for k in element_ends.keys() if k < tail_position]
                        max_du_above = max(dus_above)
                        tail = element_ends[max_du_above]
                    else:
                        last = max(elements, key=lambda tup: tup[1])
                        tail = last[0]
                        tail_position = last[1] 
                else: 
                        # #do something here for the squish part
                        # cdu_outgoing[target] = (int(tail_position), pos + counter)
                        # counter += 1
                    # print('no outgoing rel go to last')
                    last = max(elements, key=lambda tup: tup[1])
                    tail = last[0]
                    tail_position = last[1] 
                    
                #STEP 4: map cid to tail id in replacements dict
                # print('tail : ', tail )
                replacements[cid] = tail
                        
                #STEP 5: then move all text to tail node and 
                # put other other edu elements in array to delete
                new_tail_text = squish_text(elements)
                squish[tail] = new_tail_text
                for e in elements:
                    if e[0] != tail:
                        redundant.append(e[0]) 

            #STEP 6: once we have all replacements, replace ids in relation nodes
            for rel in game['relations']:
                if rel['x_id'] in replacements:
                    rel['x_id'] = replacements[rel['x_id']]
                if rel['y_id'] in replacements:
                    rel['y_id'] = replacements[rel['y_id']]
            #add squish text to tail edu and remove other nodes
            #NB: we remove by creating a new edu array
            new_edus = []
            for edu in game['edus']:
                if edu['unit_id'] in squish.keys():
                    edu['text'] = squish[edu['unit_id']]
                    new_edus.append(edu)
                elif edu['unit_id'] not in redundant:
                    new_edus.append(edu)
                # elif edu['unit_id'] in targets.keys():
                #     edu['start_pos'] = targets[edu['unit_id']]
                #     new_edus.append(edu)
                # elif edu['unit_id'] in cdu_outgoing.keys():
                #     #check that the unit is "within" CDU 
                #     #and if so change position of the edu
                #     if edu['end_pos'] <= cdu_outgoing[edu['unit_id']][0]:
                #         edu['start_pos'] = cdu_outgoing[edu['unit_id']][1]
                #         #record the target so that we can have a record of which CDUs got squished
                #         squish_record[game['game_id']].append((edu['Speaker'], edu['text'], edu['unit_id']))
                #     new_edus.append(edu)
                # else:
                #     new_edus.append(edu)

            #replace edus field
            game['edus'] = new_edus
            #remove cdu field
            game['cdus'] = []
            #remove para field 
            game['paras'] = []
            #remove embedded cdus
            game['embedded_cdus'] = []

##re-save a new json
now = datetime.datetime.now().strftime("%Y-%m-%d")

with open(save_path + split + '_' + now + '_squish.json', 'w') as outfile:
    json.dump(jfile, outfile)

print('json saved')
print('{} Linguistic CDUs to flatten'.format(linguistic_cdus))

# print_string = '\n'.join(linguistic_cdus)
# if len(linguistic_cdus) > 1:
#     with open (current_folder+ '/ling_cdus.txt', 'w') as txt_file:
#         txt_file.write(print_string)


# squish_list = []
# print('Squish records for {} games'.format(len(squish_record)))
# for key in squish_record.keys():
#     squish_list.append(key)
#     for edu in squish_record[key]:
#         squish_list.append(edu[0] + ' : ' + edu[1])
# print_string = '\n'.join(squish_list)
# with open (current_folder+ '/squish_edus.txt', 'w') as txt_file:
#         txt_file.write(print_string)

# squish_stats = []
# for key in squish_record.keys():
#     squish_stats.append((key, len(squish_record[key])))

# for s in squish_stats:
#     print(s)
   
# if len(squish_record) > 0:
#     with open(current_folder + '/' + now + '_squish.pkl', 'wb') as handle:
#         pickle.dump(squish_record, handle, protocol=3)





            
            
import json
import os 
from collections import Counter

"""
Count correction lengths
TODO: count average numbers of turns between corrections as well??
"""

def is_nl(edu):
    """
    if every word in alphanumeric
    """
    nl = 1
    words = edu.split(' ')
    # print(words)
    for word in [w for w in words if w != '']:
        if not contains_number(word) or len(word)!=5:
            nl = 0
            break
    return nl

def contains_number(string):
    return any(char.isdigit() for char in string)


annotations = '/home/kate/minecraft_utils/llm_annotator/annotated_data'
gold_path = annotations + '/DEV_32_bert.json'


with open(gold_path, 'r') as jf:
    dev = json.load(jf)

correction_nl_lens = []
correction_lens = []

print(len(dev), ' games.')

for game in dev:

    nl_moves = [i for i,e in enumerate(game['edus']) if is_nl(e['text']) and len(e['text']) > 0]

    corrs = [(rel['x'], rel['y']) for rel in game['relations'] if rel['type'] == 'Correction']

    for c in corrs:
        l = c[1]-c[0]
        correction_lens.append(l)
        if l > 1:
            checklist = [n for n in range(c[0]+1, c[1])]
            num_nl_moves = [c for c in checklist if c in nl_moves]

            correction_nl_lens.append(len(num_nl_moves))

            if len(num_nl_moves) > 0:
                print(game['id'])
        
        else:
            correction_nl_lens.append(0)

print("num nl moves between rels")
print(Counter(correction_nl_lens))

print("num edus between rels")
print(Counter(correction_lens))

#get number of relations that are over length 5:
under_4 = sum([v for k,v in Counter(correction_lens).items() if k<=4])
print('{} out of {} relations are <= distance 5'.format(under_4, len(correction_lens)))

under_2 = sum([v for k,v in Counter(correction_lens).items() if k<=2])
print('{} out of {} relations are <= distance 5'.format(under_2, len(correction_lens)))



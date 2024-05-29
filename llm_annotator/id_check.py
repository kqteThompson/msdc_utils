"""
Messed up IDs:
TRAIN
('s2-league3-game5stac_1384784220', 2)
('s2-league3-game4stac_1384783982', 2)
('s1-league1-game5stac_1368694440', 2)
('s2-league5-game5stac_1458309119', 2)
('s1-league1-game3stac_1368640632', 2)
('s1-league1-game4stac_1368694102', 2)
('s2-league5-game3stac_1443692221', 2)
('s2-league5-game4stac_1501579500', 2)
('s2-league5-game4stac_1501579517', 2)
('s2-league5-game4stac_1501579403', 2)
('s2-league5-game4stac_1501579426', 2)
('s2-leagueM-game3stac_1412670469', 2)
('s2-leagueM-game3stac_1412670390', 2)
('s2-league4-game3stac_1399316603', 2)
('s2-league3-game1stac_1384783572', 2)
('s2-league1-game1stac_1384782658', 2)
('s1-league3-game7stac_1377296083', 2)
('s2-league4-game1stac_1396964729', 2)



TEST

('s1-league3-game3stac_1368708075', 2)
('s1-league3-game3stac_1368708057', 2)
('s2-league4-game2stac_1399316556', 2)

"""

import os
import json
from collections import Counter

current_folder=os.getcwd()

# annotation_path = current_folder + '/stac/stac_squished_data/train_data.json'
# save_path = '/home/kate/minecraft_utils/llm_annotator/stac/stac_squished_corrected/train_data.json'

# annotation_path = current_folder + '/stac/stac_squished_corrected/test_data.json'

# annotation_path = current_folder + '/stac/stac_linguistic/train_data.json'
# save_path = '/home/kate/minecraft_utils/llm_annotator/stac/stac_linguistic_corrected/train_data.json'

annotation_path = current_folder + '/stac/stac_linguistic_corrected/train_data.json'

with open(annotation_path, 'r') as j:
    jfile = json.load(j)
    annotations = jfile
    annotations = annotations

#STAC situated
# # to_correct = ['s2-league4-game2stac_1399316556', 's1-league3-game3stac_1368708057','s1-league3-game3stac_1368708075']
# to_correct = ['s2-league3-game5stac_1384784220','s2-league3-game4stac_1384783982','s1-league1-game5stac_1368694440', 's2-league5-game5stac_1458309119',
#                 's1-league1-game3stac_1368640632','s1-league1-game4stac_1368694102','s2-league5-game3stac_1443692221', 's2-league5-game4stac_1501579500', 
#             's2-league5-game4stac_1501579517', 's2-league5-game4stac_1501579403', 's2-league5-game4stac_1501579426', 's2-leagueM-game3stac_1412670469', 
#         's2-leagueM-game3stac_1412670390', 's2-league4-game3stac_1399316603', 's2-league3-game1stac_1384783572', 's2-league1-game1stac_1384782658', 
#         's1-league3-game7stac_1377296083', 's2-league4-game1stac_1396964729']

#STAC linguistic
# to_correct = ['pilot02','s1-league3-game3', 's2-leagueM-game4','s2-league4-game2']

# to_correct = ['s1-league1-game5','s1-league2-game4', 's1-league1-game4','s1-league3-game2', 's1-league3-game1', 's1-league3-game5', 
#               's1-league1-game1', 's1-league1-game2','s1-league1-game3', 's1-league2-game1', 's1-league3-game4', 's1-league2-game2', 
#               's1-league2-game3', 's1-league3-game6', 's1-league3-game7', 's2-league3-game5', 's2-league5-game2', 's2-league5-game5', 
#               's2-league5-game4', 's2-leagueM-game2', 's2-league3-game1', 's2-league5-game0', 's2-league3-game4', 's2-practice3', 
#               's2-leagueM-game3', 's2-league1-game1', 's2-league8-game1', 's2-practice2', 's2-league4-game3', 's2-leagueM-game5', 
#               's2-practice4', 's2-league4-game1', 's2-league8-game2', 's2-league5-game3', 's2-league5-game1', 'pilot03', 
#               'pilot04', 'pilot20', 'pilot21', 'pilot14', 'pilot01']

# total_changes = 0
# for corr in to_correct:
#     num = 1
#     for an in annotations:
#         if an['id'] == corr:
#             an['id'] = corr + '_fix' + str(num)
#             num += 1
#             total_changes += 1

# with open(save_path, 'w') as outfile:
#     json.dump(annotations, outfile)

# print('total changes made: ', total_changes)

ids = Counter([d['id'] for d in annotations])

repeats = [k for k in ids.items() if k[1]>1]

for r in repeats:
    print(r)


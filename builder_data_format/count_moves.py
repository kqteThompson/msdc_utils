"""
check to see how many builder moves there are in a split, in order to know how many 
examples there should be.
"""
import os
import json
import csv 
from collections import Counter

current_folder=os.getcwd()

train_path = current_folder + '/train.json'
with open(train_path, 'r') as jf:
    train = json.load(jf)

train_dict = {}
for game in train:
    train_dict[game['game_id']] = len([i for i in game['dialogue'] if isinstance(i, dict)])

csv_path = current_folder + '/actseq-train-game-ids.csv'
with open(csv_path, 'r') as read_obj: 
    csv_reader = csv.reader(read_obj) 
    csv_list = list(csv_reader) 

print(len(csv_list))
print(csv_list[:2])
train_moves = [c[2] for c in csv_list[1:]]

new_train_moves = []
for m in train_moves:
  text_id = m.split('-')
  new_id = text_id[2] + '-' + text_id[0] + '-' + text_id[1]
  new_train_moves.append(new_id)

for i in train_dict.keys():
    if i not in new_train_moves:
        print(i)
print('-------------------------')

total_train_moves = Counter(new_train_moves)

# textfile_path = current_folder + '/splits/train/'

# textfiles = os.listdir(textfile_path)

# print('number of text games: {}'.format(len(textfiles)))

# train_games_path = current_folder + '/train_sample_ids.txt'
# with open(train_games_path, 'r') as txt:
#     train = txt.read().split('\n')
# print('{} total train games'.format(len(train)))

# our_train = []

# for tf in textfiles:
#     # print(tf)
#     with open(textfile_path + tf, 'r') as txt:
#         text = txt.read().split('\n')
#     our_train.append(text[0])

# print('{} total # our train games'.format(len(our_train)))

# # print('not in our train: ')
# # for game in train:
# #     if game not in our_train:
# #         print(game)

# # print('not in their train')
# # for game in our_train:
# #     if game not in train:
# #         print(game)


# total_moves = {}
# for tf in textfiles:
#     # print(tf)
#     with open(textfile_path + tf, 'r') as txt:
#         text = txt.read().split('\n')
#     # text_id = text[0].split('-')
#     # game_id = text_id[2] + '-' + text_id[0] + '-' + text_id[1]
#     # if text_id[2] not in splits['train']:
#     #     print('{} not in training splits'.format(game_id))
#     # if text[0] not in train:
#     #     print('{} not in training splits'.format(game_id)) 
#     moves = []
#     num_moves = 0
#     for move in text[1:]:
#         if '<Builder>' in move or '<Architect>' in move:
#             if len(moves) > 1:
#                 num_moves += 1
#                 moves = []
#         else:
#             moves.append(move)
#     if len(moves) > 1:
#         num_moves += 1
#     #print(game_id, num_moves)
#     total_moves[text[0]] = num_moves
# # print('total moves = {}'.format(sum(total_moves)))


for game in total_train_moves.items():
    ours = train_dict[game[0]]
    if ours != game[1]:
        print('game {} has {} moves in ours and {} moves in theirs!'.format(game[0], ours, game[1]))
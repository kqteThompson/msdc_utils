"""
for LLAMA parsing:
takes a json of annotated STAC games and converts to 
a turn format to be used format_jsonl.py. 
[
    "id": "s2-practice3stac_1458310557",
        "turns": [
            {
                "turn": 0,
                "speaker": "Server",
                "edus": [
                    "It's Tyrant Lord's turn to roll the dice.",
                    "Tyrant Lord rolled a 2 and a 4.",
                    "nelsen gets 1 wood. sparkles gets 1 ore. Tyrant Lord gets 1 wood."
                ]
            },
            {
                "turn": 1,
                "speaker": "UI",
                "edus": [
                    "nelsen has 7 resources. Kersti has 3 resources. sparkles has 3 resources. Tyrant Lord has 6 resources."
                ]
            },...
]
"""
import os
import json

current_folder=os.getcwd()

data_path = '/home/kate/minecraft_utils/stac_linguistic/stac_linguistic_flat_test.json'
save_path = current_folder + '/stac_linguistic_flat_test_turns.json'

#data_path = current_folder + '/stac/stac_linguistic_corrected/test_data.json'
#save_path = current_folder + '/stac_linguistic_test_turns.json'

# data_path = current_folder + '/molweni/molweni_clean_test50.json'
# save_path = current_folder + '/molweni_test_turns.json'

with open(data_path, 'r') as j:
    jfile = json.load(j)
    games = jfile

##for each game, find turns, edus.s
##feed one turn at a t9ime, with each edu numbered, plus structure for that turn
##TEXT:   ##STRUCTURE:  ##NEXT TURN   => #output structure
turn_version = []
total_games = 0
print('total games: {} '.format(len(games)))
for game in games: #train/val split
    if len(game['edus']) > 1:
        new_game = {}
        total_games += 1
        # new_game['id'] = game['id']
        new_game['id'] = game['dialogue_id']
        game_turns = []
        edus = game['edus'] 
        turn_no = 0
        last_speaker = None
        new_turn = {}
        new_turn['turn'] = turn_no
        new_turn['speaker'] = edus[0]['speaker']
        #add the first edu...the first turn is always the first turn of 
        turn_edus = []
        turn_edus.append(edus[0]['text'])
        # turn_edus.append(edus[0]['text'])
        for edu in edus[1:]:
            if edu['speaker'] == last_speaker and edu['speaker'] not in ['Server', 'UI']:
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
        #take care of last speaker turn in the game
        new_turn['edus'] = turn_edus
        game_turns.append(new_turn)
        #append new turns to the game dict
        new_game['turns'] = game_turns
        #add game dict to list of games
        turn_version.append(new_game)

with open(save_path, 'w') as outfile:
    json.dump(turn_version, outfile)

print('json saved for {} games'.format(total_games))
    
    
    #add turns and edu numbers
    #get edu list with global and turn indices

    #for turn in turns:
    #count edus, and add will total edu count < 11
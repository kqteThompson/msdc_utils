Scripts for creating Nebulipa data. 

step 1: create_gamelists.py --- which formats edu text and adds worldstate information for each EEU.
input--> annotated data json
output--> a <split>_lists.json


step 2: format_narr_arcs.py -- which splits lists into narrative arcs and adds structure information
input--> json from step 1
output--> a <split>_narrations.json

***ISSUES:
-order of the realtions in the structure? YES
-include backwards relations? NO
-relations connecting the predicted moves? (RES) NO 


step 3: create_csv.py -- which creates individual samples from the narrations json
input--> json from step 2
output--> a csv file for model training


##################################
To create Nebulipa data for the full context

step 1: take <split>_lists.json created above. 

step 2: format_full.py --- add structure information but NOT narration information
input--> json from step 1
output--> a <split>_full.json

step 3: create_full_csv.py -- which creates individual samples from the full json
input--> json from step 2
**don't add worldstate information
output--> a csv file for model training


##################################
To create Nebulipa data for just the correction moves

step 1: take <split>_lists.json created above. 

step 2: format_full.py --- add structure information but NOT narration information
input--> json from step 1
output--> a <split>_full.json

step 3: create_full_csv_wids.py -- which creates individual samples from the full json
input--> json from step 2
**don't add worldstate information
**!! add an index that gives the game id plus the index for the move and use this to cull the corrections
output--> a csv file culled for just the corrections (<split>_nebula_full_wids_cut.csv)

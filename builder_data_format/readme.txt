How to create builder data in csv format for NEBULA finetuning. 

1. Run get_narrs.py : takes the annotated data and outpus a list of all the source edus of the long Narrations 
in a game
2. Run text_to_json.py : takes the output of get_narrs.py and the text versions of the games and creates
a json. Each dialogue is a list of moves. The linguistic moves are text, and the actions are appended to the list 
as a dict with moves and worldstate keys. Each linguistic move that is the source of a Narration, is marked by 
'NARRATION'
NB -- there are couple changes to be made to the narration jsons for TRAIN and TEST before running text_to_json.py. 
They are specified in the comments at the top of the script. 
3. Run json_to_csv.py : takes the output of text_to_json.py and creates a final training set. 
The data is split according to Narrative Arcs. The context for each arc is the worldstate just before the 
beginning of the arc, as well as the last set of moves. 

NEW:

text_to_json_worldstate.py : a new version of worldstate where it is just a list of place moves, 
one for each block that is in the grid, in the order that it was placed. 

json_to_csv_worldstate.py : a new version of json_to_csv where the worldstate format is changed to a list of 
'place' statements. and is fed just before the first instruction of a narrative arc
V1 - worldstate is just before the first instruction from narr arc, if there are multiple instructions in a
narrative arc, the last moves are added just before. 
 
V2 - worldstate is just before the most recent instruction from narr arc. 

======FOR THE I-A-I plus worldstate data:

1. Run text_to_iai.py to transform textfiles to json where each dialogue is a list of utterances and move/worldstate dicts:
"dialogue": [
            "<Builder> Mission has started.",
            "<Architect> For this one, build two lines of three touching the ground with one block gap between them",
            "<Architect> In blue",
            {
                "moves": "place blue 1 1 1\nplace blue 1 1 0\nplace blue 1 1 -1\nplace blue -1 1 1\nplace blue -1 1 -1\nplace blue -1 1 0",
                "worldstate": "place blue 1 1 1, place blue 1 1 0, place blue 1 1 -1, place blue -1 1 1, place blue -1 1 -1, place blue -1 1 0"
            },...]
            
2. Run json_to_csv_iai.py to transform the json output from step one to the final training set 

NB:

2347 (TRAIN) samples out of 3722 : iai > narr, and 3084 iai >= narr
Narr chunks
Max context: 131
Avg context len: 6.650188070929608
Mode len: [(1, 1436)]
IAI chunks
Max context: 55
Avg context len: 8.130037614185921
Mode len: [(5, 472)]

So instead we opted for shortening the narrative chunks that were longer than Narrative chunks:


==============FOR reducing Narrative chunks 

The original paper used I-A-I ---> A to get a score for the action prediction task 
We tried the same prediction task using all of the previous context and got a 10 point boost. 
Then we tried the prediction task using only the narration chunks as context, plus worldstate. we got a comparable score, 
*which indicates that the contextual information provided by narrative chunks is sufficient for (a high score) on the action prediction task*
This is interesting because the narrative chunks are much smaller on average than the I-A-I chunks. 

But in order to show that the narration chunks + worldstate provide the necessary information, we have to show that giving less information 
than narration chunks lowers the score on the prediction task. 
So in cases where the narrative chunks are longer than the I-A-I chunks, we cut the narrative chunks down to I-A-I

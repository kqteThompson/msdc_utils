These scripts format the minecraft annotated json data to train llama on the parsing task. 

#### STEP 1: format.py
Converts data.json to an intermediate format, with one object per turn, and each edu in a list, e.g.:

{
    "turn": 1,
    "speaker": "Architect",
    "edus": [
        "alright ,",
        "start with a row of 5 orange ones on the ground",
        "any direction",
        "near the center preferably"
    ]
},

NB: in line ~121 either creates builder move representations for NL eeus, or gives a generic placeholder
like "builder moves"

#### STEP 2: format_jsonl.py
Takes the output json from format.py and the annotated data (again) and outputs a jsonl of samples.

global variables:

SAMPLE_PATTERN = defaultdict with keys: 'context','structure','turn', 'predict'
**used as a pattern for the dict that is instantiated and manipulated for each game. 

DISTANCE == max number of edus in each window
**currently an issue with 7
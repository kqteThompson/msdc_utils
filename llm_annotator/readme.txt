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



###FOR THE STAC CORPORA

NB: the ids in these corpora were not unique, so I gave them unique ids and saved them 
in the 'corrected' versions of the folders (id_check.py counts these)
NB: we artificially split TRAIN into val and train:
STAC SQUISHED:
train: 931 val: 90 test: 112
STAC LINGUISTIC:
train: 986 val: 100 test: 111

First run format_stac.py to then foramt_jsonl_stac.py to get the jsonl docs for training.

Sometimes there are empty PS fields, either because the newest candidate is connected to the 
structure via a backwards relation, or because the relation exceeds 15.

In order to remove these from the training jsonl, run remove_empty_ps.py

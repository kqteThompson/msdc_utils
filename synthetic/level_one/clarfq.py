import random

"""
[size, col, orient, loc] always in this order
"""

def no_orient_clarif(params_list):
    instruction = None
    clarifq = None
    answer = None 

    SHAPE = params_list['shape']

    if params_list['loc'] == "":
        LOC = 0
    else:
        LOC = 1
    
    #chose one param at random
    params = [k for k in params_list.keys() if k not in ['shape', 'orient']] #diamonds don't have location
    rand = random.choice(params)
    
    if rand == 'size':
        if SHAPE in ['row', 'diagonal']:
            if LOC:
                if LOC == 'centre':
                    instruction = f"<Architect> Build a {params_list['col']} {SHAPE} passing through the centre.".replace("  "," ")
                else:
                    instruction = f"<Architect> Build a {params_list['col']} {SHAPE} at the {params_list['loc']}.".replace("  "," ")
            else:
                instruction = f"<Architect> Build a {params_list['col']} {SHAPE}.".replace("  "," ")
            clarifq = f"<Builder> how long?".replace("  "," ")
            answer = f"<Architect> {params_list['size']} blocks.".replace("  "," ")
        elif SHAPE in ['tower']:
            if LOC:
                if LOC == 'centre':
                    instruction = f"<Architect> Build a {params_list['col']} {SHAPE} at the centre.".replace("  "," ")
                else:
                    instruction = f"<Architect> Build a {params_list['col']} {SHAPE} at the {params_list['loc']}.".replace("  "," ")
            else:
                instruction = f"<Architect> Build a {params_list['col']} {SHAPE}.".replace("  "," ")
            clarifq = f"<Builder> how tall?".replace("  "," ")
            answer = f"<Architect> {params_list['size']} blocks.".replace("  "," ")
        elif SHAPE in ['cube']:
            if LOC:
                instruction = f"<Architect> Build a {params_list['col']} {SHAPE} of at the {params_list['loc']}.".replace("  "," ")
            else:
                instruction = f"<Architect> Build a {params_list['col']} {SHAPE}.".replace("  "," ")
            clarifq = f"<Builder> What size {SHAPE}?"
            answer = f"<Architect> {params_list['size']}x{params_list['size']}."

    elif rand == 'col':
        if SHAPE in ['row', 'diagonal']:
            if LOC:
                if LOC == 'centre':
                    instruction = f"<Architect> Build a {params_list['col']} {SHAPE} of {params_list['size']} blocks passing through the centre.".replace("  "," ")
                else:
                    instruction = f"<Architect> Build a {SHAPE} of {params_list['size']} blocks at the {params_list['loc']}.".replace("  "," ")
            else:
                instruction = f"<Architect> Build a {SHAPE} {params_list['size']} blocks long.".replace("  "," ")
            clarifq = f"<Builder> What color?"
            answer = f"<Architect> {params_list['col']}.".replace("  "," ")
        elif SHAPE in ['tower']:
            if LOC:
                if LOC == 'centre':
                    instruction = f"<Architect> Build a {params_list['col']} {SHAPE} of {params_list['size']} blocks at the centre.".replace("  "," ")
                else:
                    instruction = f"<Architect> Build a {SHAPE} of {params_list['size']} blocks at the {params_list['loc']}.".replace("  "," ")
            else:
                instruction = f"<Architect> Build a {SHAPE} {params_list['size']} blocks tall.".replace("  "," ")
            clarifq = f"<Builder> What color?"
            answer = f"<Architect> {params_list['col']}.".replace("  "," ")
        elif SHAPE in ['cube']:
            if LOC:
                instruction = f"<Architect> Build a {params_list['size']}x{params_list['size']} {SHAPE} at the {params_list['loc']}.".replace("  "," ")
            else:
                instruction = f"<Architect> Build a {params_list['size']}x{params_list['size']} {SHAPE}.".replace("  "," ")
            clarifq = f"<Builder> What color {SHAPE}?"
            answer = f"<Architect> {params_list['col']}."
    elif rand == 'loc':
        if SHAPE in ['row', 'diagonal']:
            instruction = f"<Architect> Build a {params_list['col']} {SHAPE} {params_list['size']} blocks long.".replace("  "," ")
            clarifq = f"<Builder> Where?"
            if LOC:  
                if LOC == 'centre':
                    answer = f"<Architect> passing through the centre."
                else:
                    answer = f"<Architect> At the {params_list['loc']}.".replace("  "," ")
            else:
                answer = f"<Architect> Anywhere."
        elif SHAPE in ['tower']:
            instruction = f"<Architect> Build a {params_list['col']} {SHAPE} {params_list['size']} blocks tall.".replace("  "," ")
            clarifq = f"<Builder> Where?"
            if LOC:  
                if LOC == 'centre':
                    answer = f"<Architect> passing through the centre."
                else:
                    answer = f"<Architect> At the {params_list['loc']}.".replace("  "," ")
            else:
                answer = f"<Architect> Anywhere."
        elif SHAPE in ['cube']:
            instruction = f"<Architect> Build a {params_list['size']}x{params_list['size']} {params_list['col']} {SHAPE}.".replace("  "," ")
            clarifq = f"<Builder> Where?"
            if LOC:  
                answer = f"<Architect> {params_list['loc']}."
            else:
                answer = f"<Architect> Anywhere."
    return [instruction, clarifq, answer]  

def diamond_clarifq(params_list):
    """
    Takes a list of params, returns a list of three utterances
    """
    instruction = None
    clarifq = None
    answer = None 

    SHAPE = params_list['shape']

    #chose one param at random
    params = [k for k in params_list.keys() if k not in ['shape', 'loc']] #diamonds don't have location
    rand = random.choice(params)
    if rand == 'size':
        instruction = f"<Architect> Build an {params_list['col']} {params_list['orient']} {SHAPE}.".replace("  "," ")
        clarifq = f"<Builder> What size?".replace("  "," ")
        a_one = f"<Architect> A {SHAPE} with {params_list['size']} blocks on a side.".replace("  "," ")
        a_two = f"<Architect> A {SHAPE} with axes {2*params_list['size']-1} spaces long.".replace("  "," ")
        answer = random.choice([a_one, a_two])

    elif rand == 'col':
        i_one = f"<Architect> Build a {params_list['orient']} {SHAPE} with {params_list['size']} blocks on a side.".replace("  "," ")
        i_two = f"<Architect> Build a {params_list['orient']} {SHAPE} with axes {2*params_list['size']-1} spaces long.".replace("  "," ")
        instruction = random.choice([i_one, i_two])
        clarifq = f"<Builder> What color {SHAPE}?".replace("  "," ")
        answer = f"<Architect> {params_list['col']}."

    elif rand == 'orient':
        i_one = f"<Architect> Build a {params_list['col']} {SHAPE} with {params_list['size']} blocks on a side.".replace("  "," ")
        i_two = f"<Architect> Build a {params_list['col']} {SHAPE} with axes {2*params_list['size']-1} spaces long.".replace("  "," ")
        instruction = random.choice([i_one, i_two])
        clarifq = f"<Builder> Horizontal or vertical?".replace("  "," ")
        answer = f"<Architect> {params_list['orient']}."
         
    return [instruction, clarifq, answer] 

def rectangle_clarifq(params_list):
    """
    Takes a list of params, returns a list of three utterances
    """
    instruction = None
    clarifq = None
    answer = None 

    SHAPE = params_list['shape']

    if params_list['loc'] == "":
        LOC = 0
    else:
        LOC = 1

    #chose one param at random
    params = [k for k in params_list.keys() if k not in ['shape', 'r']] 
    rand = random.choice(params)
    #Sprint('rand: ', rand)
    if rand == 'size':
        if LOC:
            instruction = f"<Architect> Build a {params_list['col']} {params_list['orient']} {SHAPE} at the {params_list['loc']}.".replace("  "," ")
        else:
            instruction = f"<Architect> Build a {params_list['col']} {params_list['orient']} {SHAPE}.".replace("  "," ")
        clarifq = f"<Builder> What size?".replace("  "," ")
        answer = f"<Architect> {params_list['r']}x{params_list['size']}.".replace("  "," ")

    elif rand == 'col':
        if LOC:
            instruction = f"<Architect> Build a {params_list['r']}x{params_list['size']} {params_list['orient']} {SHAPE} at the {params_list['loc']}.".replace("  "," ")
        else:
            instruction = f"<Architect> Build a {params_list['r']}x{params_list['size']} {params_list['orient']} {SHAPE}.".replace("  "," ")
        clarifq = f"<Builder> What color {SHAPE}?".replace("  "," ")
        answer = f"<Architect> {params_list['col']}."

    elif rand == 'orient':
        if LOC:
            instruction = f"<Architect> Build a {params_list['col']} {params_list['r']}x{params_list['size']} {SHAPE} at the {params_list['loc']}.".replace("  "," ")
        else:
            instruction = f"<Architect> Build a {params_list['col']} {params_list['r']}x{params_list['size']} {SHAPE}.".replace("  "," ")
        clarifq = f"<Builder> Horizontal or vertical?".replace("  "," ")
        answer = f"<Architect> {params_list['orient']}."

    elif rand == 'loc':
        instruction = f"<Architect> Build a {params_list['col']} {params_list['r']}x{params_list['size']} {params_list['orient']} {SHAPE}.".replace("  "," ")
        clarifq = f"<Builder> Where?"
        if LOC:  
            answer = f"<Architect> {params_list['loc']}."
        else:
            answer = f"<Architect> Anywhere."
         
    return [instruction, clarifq, answer] 

def clarif_question(params_list):
    """
    Takes a list of params, returns a list of three utterances
    """
    instruction = None
    clarifq = None
    answer = None 

    SHAPE = params_list['shape']

    if params_list['loc'] == "":
        LOC = 0
    else:
        LOC = 1

    #chose one param at random
    params = [k for k in params_list.keys() if k != 'shape']
    rand = random.choice(params)
    if rand == 'size':
        if SHAPE in ['square']:
            if LOC:
                instruction = f"<Architect> Build a {params_list['col']} {params_list['orient']} {SHAPE} of at the {params_list['loc']}.".replace("  "," ")
            else:
                instruction = f"<Architect> Build a {params_list['col']} {params_list['orient']} {SHAPE}.".replace("  "," ")
            clarifq = f"<Builder> What size {SHAPE}?"
            answer = f"<Architect> {params_list['size']}x{params_list['size']}."
    elif rand == 'col':
        if SHAPE in ['square']:
            if LOC:
                instruction = f"<Architect> Build a {params_list['size']}x{params_list['size']} {params_list['orient']} {SHAPE} at the {params_list['loc']}.".replace("  "," ")
            else:
                instruction = f"<Architect> Build a {params_list['size']}x{params_list['size']} {params_list['orient']} {SHAPE}.".replace("  "," ")
            clarifq = f"<Builder> What color {SHAPE}?"
            answer = f"<Architect> {params_list['col']}."

    elif rand == 'loc':
        if SHAPE in ['square']:
            instruction = f"<Architect> Build a {params_list['size']}x{params_list['size']} {params_list['orient']} {params_list['col']} {SHAPE}.".replace("  "," ")
            clarifq = f"<Builder> Where?"
            if LOC:  
                answer = f"<Architect> {params_list['loc']}."
            else:
                answer = f"<Architect> Anywhere."
    ## !! will only be for diamonds, rectangles and squares
    elif rand == 'orient':
        assert SHAPE in ['square']
        if LOC:
            instruction = f"<Architect> Build a {params_list['size']}x{params_list['size']} {params_list['col']} {SHAPE} of at the {params_list['loc']}.".replace("  "," ")
        else:
            instruction = f"<Architect> Build a {params_list['size']}x{params_list['size']} {params_list['col']} {SHAPE}.".replace("  "," ")
        clarifq = f"<Builder> Horizontal or vertical?"
        answer = f"<Architect> {params_list['orient']}.".replace("  "," ")
    

    return [instruction, clarifq, answer]
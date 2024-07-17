import random

"""
ROW, DIAGONAL, TOWER, CUBE have no orientations
"""

def no_orient_clarif(params_list):
    """
    ROW, DIAGONAL, TOWER, CUBE have no orientations
    """
    instruction = None
    clarifq = None
    answer = None 

    param_update = {}

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
                r_loc = random.choice(["Through the centre", "On an edge", "At a corner"])
                answer = f"<Architect> {r_loc}."
                param_update['loc'] = r_loc.split(' ')[2]
        elif SHAPE in ['tower']:
            instruction = f"<Architect> Build a {params_list['col']} {SHAPE} {params_list['size']} blocks tall.".replace("  "," ")
            clarifq = f"<Builder> Where?"
            if LOC:  
                if LOC == 'centre':
                    answer = f"<Architect> passing through the centre."
                else:
                    answer = f"<Architect> At the {params_list['loc']}.".replace("  "," ")
            else:
                r_loc = random.choice(["Through the centre", "On an edge", "At a corner"])
                answer = f"<Architect> {r_loc}."
                param_update['loc'] = r_loc.split(' ')[2]
        elif SHAPE in ['cube']:
            instruction = f"<Architect> Build a {params_list['size']}x{params_list['size']} {params_list['col']} {SHAPE}.".replace("  "," ")
            clarifq = f"<Builder> Where?"
            if LOC:  
                answer = f"<Architect> {params_list['loc']}."
            else:
                r_loc = random.choice(["At the centre", "On an edge", "At a corner"])
                answer = f"<Architect> {r_loc}."
                param_update['loc'] = r_loc.split(' ')[2]
    return [instruction, clarifq, answer], param_update 

def diamond_clarifq(params_list):
    """
    DIAMONDS DO NOT HAVE LOCATION
    """
    instruction = None
    clarifq = None
    answer = None 

    param_update = {}

    SHAPE = params_list['shape']

    if params_list['orient'] == "":
        OR = 0
    else:
        OR = 1

    #chose one param at random
    params = [k for k in params_list.keys() if k not in ['shape', 'loc']] #diamonds don't have location
    rand = random.choice(params)
    if rand == 'size':
        if OR:
            instruction = f"<Architect> Build a {params_list['col']} {params_list['orient']} {SHAPE}.".replace("  "," ")
        else:
            instruction = f"<Architect> Build a {params_list['col']} {params_list['orient']} {SHAPE}.".replace("  "," ") 
        clarifq = f"<Builder> What size?".replace("  "," ")
        a_one = f"<Architect> A {SHAPE} with {params_list['size']} blocks on a side.".replace("  "," ")
        a_two = f"<Architect> A {SHAPE} with axes {2*params_list['size']-1} spaces long.".replace("  "," ")
        answer = random.choice([a_one, a_two])

    elif rand == 'col':
        if OR:
            i_one = f"<Architect> Build a {params_list['orient']} {SHAPE} with {params_list['size']} blocks on a side.".replace("  "," ")
            i_two = f"<Architect> Build a {params_list['orient']} {SHAPE} with axes {2*params_list['size']-1} spaces long.".replace("  "," ")
            instruction = random.choice([i_one, i_two])
        else:
            i_one = f"<Architect> Build a {SHAPE} with {params_list['size']} blocks on a side.".replace("  "," ")
            i_two = f"<Architect> Build a {SHAPE} with axes {2*params_list['size']-1} spaces long.".replace("  "," ")
            instruction = random.choice([i_one, i_two])
        clarifq = f"<Builder> What color {SHAPE}?".replace("  "," ")
        answer = f"<Architect> {params_list['col']}."

    elif rand == 'orient':
        i_one = f"<Architect> Build a {params_list['col']} {SHAPE} with {params_list['size']} blocks on a side.".replace("  "," ")
        i_two = f"<Architect> Build a {params_list['col']} {SHAPE} with axes {2*params_list['size']-1} spaces long.".replace("  "," ")
        instruction = random.choice([i_one, i_two])
        clarifq = f"<Builder> Horizontal or vertical?".replace("  "," ")
        if OR:
            answer = f"<Architect> {params_list['orient']}.".replace("  "," ")
        else:
            r_or = random.choice(["horizontal", "vertical"])
            answer = f"<Architect> {r_or}.".replace("  "," ")
            param_update['orient'] = r_or
         
    return [instruction, clarifq, answer], param_update

def rectangle_clarifq(params_list):
    """
    RECTANGLES
    """
    instruction = None
    clarifq = None
    answer = None 

    param_update = {}

    SHAPE = params_list['shape']

    if params_list['loc'] == "":
        LOC = 0
    else:
        LOC = 1
    
    if params_list['orient'] == "":
        OR = 0
    else:
        OR = 1

    #chose one param at random
    params = [k for k in params_list.keys() if k not in ['shape', 'r']] 
    rand = random.choice(params)
    #Sprint('rand: ', rand)
    if rand == 'size':
        if LOC and OR:
            instruction = f"<Architect> Build a {params_list['col']} {params_list['orient']} {SHAPE} at the {params_list['loc']}.".replace("  "," ")
        elif LOC and not OR:
            instruction = f"<Architect> Build a {params_list['col']} {SHAPE} at the {params_list['loc']}.".replace("  "," ")
        elif OR and not LOC:
            instruction = f"<Architect> Build a {params_list['col']} {params_list['orient']} {SHAPE}.".replace("  "," ")
        else:
            instruction = f"<Architect> Build a {params_list['col']} {SHAPE}.".replace("  "," ")
        clarifq = f"<Builder> What size?".replace("  "," ")
        answer = f"<Architect> {params_list['r']}x{params_list['size']}.".replace("  "," ")

    elif rand == 'col':
        if LOC and OR:
            instruction = f"<Architect> Build a {params_list['r']}x{params_list['size']} {params_list['orient']} {SHAPE} at the {params_list['loc']}.".replace("  "," ")
        elif LOC and not OR:
            instruction = f"<Architect> Build a {params_list['r']}x{params_list['size']} {SHAPE} at the {params_list['loc']}.".replace("  "," ")
        elif OR and not LOC:
            instruction = f"<Architect> Build a {params_list['r']}x{params_list['size']} {params_list['orient']} {SHAPE}.".replace("  "," ")
        else:
            instruction = f"<Architect> Build a {params_list['r']}x{params_list['size']} {SHAPE}.".replace("  "," ")
        clarifq = f"<Builder> What color {SHAPE}?".replace("  "," ")
        answer = f"<Architect> {params_list['col']}."

    elif rand == 'orient':
        if LOC:
            instruction = f"<Architect> Build a {params_list['col']} {params_list['r']}x{params_list['size']} {SHAPE} at the {params_list['loc']}.".replace("  "," ")
        else:
            instruction = f"<Architect> Build a {params_list['col']} {params_list['r']}x{params_list['size']} {SHAPE}.".replace("  "," ")
        clarifq = f"<Builder> Horizontal or vertical?".replace("  "," ")
        if OR:
            answer = f"<Architect> {params_list['orient']}.".replace("  "," ")
        else:
            r_or = random.choice(["horizontal", "vertical"])
            print('rrr,', r_or)
            answer = f"<Architect> {r_or}.".replace("  "," ")
            param_update['orient'] = r_or

    elif rand == 'loc':
        instruction = f"<Architect> Build a {params_list['col']} {params_list['r']}x{params_list['size']} {params_list['orient']} {SHAPE}.".replace("  "," ")
        clarifq = f"<Builder> Where?"
        if LOC:  
            answer = f"<Architect> {params_list['loc']}."
        else:
            r_loc = random.choice(["At the centre", "On an edge", "At a corner"])
            answer = f"<Architect> {r_loc}."
            param_update['loc'] = r_loc.split(' ')[2]
         
    return [instruction, clarifq, answer], param_update

def square_clarif(params_list):
    """
    SQUARES
    """
    instruction = None
    clarifq = None
    answer = None 
    param_update = {}

    SHAPE = params_list['shape']

    if params_list['loc'] == "":
        LOC = 0
    else:
        LOC = 1

    if params_list['orient'] == "":
        OR = 0
    else:
        OR = 1

    #chose one param at random
    params = [k for k in params_list.keys() if k != 'shape']
    rand = random.choice(params)
    if rand == 'size':
        if LOC and OR:
            instruction = f"<Architect> Build a {params_list['col']} {params_list['orient']} {SHAPE} of at the {params_list['loc']}.".replace("  "," ")
        elif LOC and not OR:
            instruction = f"<Architect> Build a {params_list['col']} {SHAPE} of at the {params_list['loc']}.".replace("  "," ")
        elif OR and not LOC: 
            instruction = f"<Architect> Build a {params_list['col']} {params_list['orient']} {SHAPE}.".replace("  "," ")
        else:
            instruction = f"<Architect> Build a {params_list['col']} {SHAPE}.".replace("  "," ")
        clarifq = f"<Builder> What size {SHAPE}?"
        answer = f"<Architect> {params_list['size']}x{params_list['size']}."
    elif rand == 'col':
        if LOC and OR:
            instruction = f"<Architect> Build a {params_list['size']}x{params_list['size']} {params_list['orient']} {SHAPE} at the {params_list['loc']}.".replace("  "," ")
        elif LOC and not OR:
            instruction = f"<Architect> Build a {params_list['size']}x{params_list['size']} {SHAPE} at the {params_list['loc']}.".replace("  "," ")
        elif OR and not LOC:
            instruction = f"<Architect> Build a {params_list['size']}x{params_list['size']} {params_list['orient']} {SHAPE}.".replace("  "," ")
        else:
            instruction = f"<Architect> Build a {params_list['size']}x{params_list['size']} {SHAPE}.".replace("  "," ")
        clarifq = f"<Builder> What color {SHAPE}?"
        answer = f"<Architect> {params_list['col']}."
    elif rand == 'loc':
        if OR:
            instruction = f"<Architect> Build a {params_list['size']}x{params_list['size']} {params_list['orient']} {params_list['col']} {SHAPE}.".replace("  "," ")
        else:
            instruction = f"<Architect> Build a {params_list['size']}x{params_list['size']} {SHAPE}.".replace("  "," ")
        clarifq = f"<Builder> Where?"
        if LOC:  
            answer = f"<Architect> {params_list['loc']}."
        else:
            r_loc = random.choice(["At the centre", "On an edge", "At a corner"])
            answer = f"<Architect> {r_loc}."
            param_update['loc'] = r_loc.split(' ')[2]
    elif rand == 'orient':
        if LOC:
            instruction = f"<Architect> Build a {params_list['size']}x{params_list['size']} {params_list['col']} {SHAPE} of at the {params_list['loc']}.".replace("  "," ")
        else:
            instruction = f"<Architect> Build a {params_list['size']}x{params_list['size']} {params_list['col']} {SHAPE}.".replace("  "," ")
        clarifq = f"<Builder> Horizontal or vertical?"
        if OR:
            answer = f"<Architect> {params_list['orient']}.".replace("  "," ")
        else:
            r_or = random.choice(["horizontal", "vertical"])
            answer = f"<Architect> {r_or}.".replace("  "," ")
            param_update['orient'] = r_or
    

    return [instruction, clarifq, answer], param_update
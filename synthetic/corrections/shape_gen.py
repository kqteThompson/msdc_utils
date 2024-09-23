import numpy as np
import random
import build_functions as bs
import functions as fun

def get_instruction(shape, color, location, size, i=1):
    if shape == 'row':
        if location == 'centre':
            if i==1:
                instruction = f"<Arch> Build a row of {size} {color} blocks at the centre.".replace("  "," ")
            elif i==2:
                instruction = f"<Arch> And build a row of {size} {color} blocks at the centre.".replace("  "," ")
            elif i==3:
                instruction = f"<Arch> And also build a row of {size} {color} blocks at the centre.".replace("  "," ")
        else:
            if location == 'edge':
                glocation = 'an edge'
            else: 
                glocation = 'a corner'
            if i==1:
                instruction = f"<Arch> Build a row of {size} {color} blocks at {glocation}.".replace("  "," ")
            elif i==2:
                instruction = f"<Arch> And build a row of {size} {color} blocks at {glocation}.".replace("  "," ")
            elif i==3:
                instruction = f"<Arch> Also build a row of {size} {color} blocks at {glocation}.".replace("  "," ")

    elif shape == 'tower':
        if color == 'orange':
            gcolor = 'an orange'
        else:
            gcolor = 'a ' + color
        if location == 'centre':
            if i==1:
                instruction = f"<Arch> Build {gcolor} tower of size {size} at the centre.".replace("  "," ")
            elif i==2:
                instruction = f"<Arch> And build {gcolor} tower of size {size} at the centre.".replace("  "," ")
            elif i==3:
                instruction = f"<Arch> And also build {gcolor} tower of size {size} at the centre.".replace("  "," ")
        else:
            if location == 'edge':
                glocation = 'an edge'
            else: 
                glocation = 'a corner'
            if color == 'orange':
                gcolor = 'an orange'
            else:
                gcolor = 'a ' + color
            if i==1:
                instruction = f"<Arch> Build {gcolor} tower of size {size} at {glocation}.".replace("  "," ")
            elif i==2:
                instruction = f"<Arch> And build {gcolor} tower of size {size} at {glocation}.".replace("  "," ")
            elif i==3:
                instruction = f"<Arch> Also build {gcolor} tower of size {size} at {glocation}.".replace("  "," ")
    elif shape == 'block':
        if location == 'centre':
            if color == 'orange':
                gcolor = 'an orange'
            else:
                gcolor = 'a ' + color
            if i==1:    
                instruction = f"<Arch> Place {gcolor} block at the centre.".replace("  "," ")
            elif i==2:
                instruction = f"<Arch> And place {gcolor} block at the centre.".replace("  "," ")
            elif i==3:
                instruction = f"<Arch> Also place {gcolor} block at the centre.".replace("  "," ")
        else:
            if location == 'edge':
                glocation = 'an edge'
            else: 
                glocation = 'a corner'
            if color == 'orange':
                gcolor = 'an orange'
            else:
                gcolor = 'a ' + color
            if i==1:
                instruction = f"<Arch> Place {gcolor} block at {glocation}.".replace("  "," ")
            elif i==2:
                instruction = f"<Arch> And place {gcolor} block at {glocation}.".replace("  "," ")
            elif i==3:
                instruction = f"<Arch> And also place {gcolor} block at {glocation}.".replace("  "," ")

    return instruction

def generate(shape, color, location, size):
    if shape == "row":
        size=int(size)
        act_seq = bs.row(color, size, None, location)
        assert fun.is_row(fun.get_net_sequence(act_seq))[0]
        assert fun.is_row(fun.get_net_sequence(act_seq))[1]==size
    elif shape == 'tower':
        size=int(size)
        act_seq = bs.tower(color, size, None, location)
        assert fun.is_tower(fun.get_net_sequence(act_seq))[0]
        assert fun.is_tower(fun.get_net_sequence(act_seq))[1]==size
    elif shape == 'block':
        #NB: a block is just a tower of size one
        size=int(size)
        act_seq = bs.tower(color, size, None, location)
        # print(act_seq)
        assert fun.is_tower(fun.get_net_sequence(act_seq))[0]
        assert fun.is_tower(fun.get_net_sequence(act_seq))[1]==size
    return act_seq


def get_color_correction(color, wrong_color, location, wrong_seq):
    #NB right now for single blocks only
    if location == 'centre':
        instruction = f"<Arch> The centre block should be {color}.".replace("  "," ")
    else:
        instruction = f"<Arch> The block at the {location} should be {color}.".replace("  "," ")

    wrong = wrong_seq[0].split(' ')
    move_one = 'pick ' + ' '.join(wrong[2:])
    move_two = 'place ' + color + ' ' + ' '.join(wrong[2:])
    correct_seq = '<Buil> ' + move_one + ', ' + move_two 
    return instruction, correct_seq

def get_height_correction(color, location, size, wrong_size, wrong_seq):
    if location == 'centre':
        instruction = f"<Arch> The {color} tower at the centre should be size {size}.".replace("  "," ")
    else:
        instruction = f"<Arch> The {color} tower at the {location} should be size {size}.".replace("  "," ")

    wrong = wrong_seq[-1]
    w = wrong.split(' ')
    if size > wrong_size:
        h = str(int(w[3]) + 1)
        correct_seq = ' '.join(['<Buil>', 'place', color, w[2], h, w[4]])
    else:
        #it's a removal
        correct_seq = ' '.join(['<Buil>', 'pick' + w[2] + w[3] + w[4]])
    
    return instruction, correct_seq

def get_length_correction(color, location, size, wrong_size, wrong_seq):
    if location == 'centre':
        instruction = f"<Arch> The {color} row at the centre should be {size} blocks.".replace("  "," ")
    else:
        instruction = f"<Arch> The {color} row at the {location} should be {size} blocks.".replace("  "," ")

    wrong = wrong_seq[-1] #NB: always take last placement to leave the row 'in a corner' 
    w = wrong.split(' ')

    if size < wrong_size:
        #it's a removal
        correct_seq = ' '.join(['<Buil>','pick', w[2], w[3], w[4]])
    else:
        first = wrong_seq[0]
        f = first.split(' ')
        #it's an addition, but need to know whether to add to z or to x
        if f[2] == w[2]:
            #then z has been changing
            #now find out what the endpoints are
            #look at z coords from both ends and decide where to add
            ep_one = int(f[4])
            ep_two = int(w[4])
            if ep_one > ep_two:
                if abs(ep_one) != 5:
                    h = str(int(f[4]) + 1)
                else:
                    h = str(int(w[4]) - 1)
            else:
                if abs(ep_one) != 5:
                    h = str(int(f[4]) - 1)
                else:
                    h = str(int(w[4]) + 1)
            correct_seq = ' '.join(['<Buil>', 'place', color, w[2], w[3], h]) 
        else:
            # then x has been changing 
            # h = str(int(wrong.split(' ')[2]) + 1)
            ep_one = int(f[2])
            ep_two = int(w[2])
            if ep_one > ep_two:
                if abs(ep_one) != 5:
                    h = str(int(f[2]) + 1)
                else:
                    h = str(int(w[2]) - 1)
            else:
                if abs(ep_one) != 5:
                    h = str(int(f[2]) - 1)
                else:
                    h = str(int(w[2]) + 1)
            correct_seq = ' '. join(['<Buil>', 'place', color, h, w[3], w[4]]) 

    return instruction, correct_seq


def bad_generate(shape, color, location, size):
    colors = ['blue', 'green', 'purple', 'yellow', 'orange', 'red']
    incdec = ['plus', 'minus']
    if shape == 'block':
        wrong_color = random.choice([c for c in colors if c!=color])
        wrong_gen = generate(shape, wrong_color, location, size)
        correction, correct_gen  = get_color_correction(color, wrong_color, location, wrong_gen)
    elif shape == 'tower':
        #make taller or shorter
        if random.choice([incdec]) == 'plus':
            #then increment
            wrong_size = size + 1
        else:
            wrong_size = size - 1
        wrong_gen = generate(shape, color, location, wrong_size)
        correction, correct_gen = get_height_correction(color, location, size, wrong_size, wrong_gen)
    elif shape == 'row':
        #NB: rows and towers can probably use same functions but here just keep separate
        if random.choice([incdec]) == 'plus':
            wrong_size = size + 1
        else:
            wrong_size = size - 1
        wrong_gen = generate(shape, color, location, wrong_size)
        correction, correct_gen = get_length_correction(color, location, size, wrong_size, wrong_gen)

    #format wrong gen with <builder> turn marker and commas between moves
    moves = ', '.join(wrong_gen)
    builder_str = '<Buil> ' + moves

    return builder_str, correction, correct_gen

def get_next_shape(location_list):
    """
    get the dimensions of the second shape 
    """
    locations = ['centre', 'corner', 'edge']
    shapes = ['tower', 'block']
    colors = ['blue', 'green', 'purple', 'yellow', 'orange', 'red']
    sizes = [3,4,5]

    shape = random.choice(shapes)
    if shape == 'block':
        size = 1
    else:
        size = random.choice(sizes)
    color = random.choice(colors)

    #just take the a location that hasn't yet been used
    for loc in locations:
        if loc not in location_list:
            new_loc = loc
    # if location == 'centre':
    #     new_loc = random.choice(['corner', 'edge'])
    # else:
    #     new_loc = 'centre'
    
    new_shape = (shape, color, new_loc, size)

    return new_shape


def record_blocks(placement_list):
    # print(placement_list)
    coords_list = []
    pl = placement_list.strip('<Buil> ')
    # print(pl)
    for place in pl.split(','):
        p = place.strip().split(' ')[2:]
        coords_list.append(tuple(p))
    # print(coords_list)
    return coords_list

# def record_correction_blocks(placement_list):
#     coords_list = []
#     pl = placement_list.strip('<Buil> ')
#     if 'pick' not in pl:
#         for place in pl.split(','):
#             p = place.strip().split(' ')[2:]
#             coords_list.append(tuple(p))
#     return coords_list 
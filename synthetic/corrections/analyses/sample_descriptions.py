import os
from collections import Counter

"""
takes a text file of synthetic samples and categorizes the differences between structures
for SHORT there are two structures --> give a number to represent similarities
for LONG there are three structures
"""

###FOR 300

def get_shapes_three(one, two, three):
    c = ''
    if 'tower' in one:
        c += 'T'
    elif 'row' in one:
        c += 'R'
    
    if 'tower' in two:
        c += 'T'
    elif 'row' in two:
        c += 'R'
    elif 'block' in two and 'blocks' not in two:
        c += 'B'

    if 'tower' in three:
        c += 'T'
    elif 'row' in three:
        c += 'R'
    elif 'block' in three and 'blocks' not in three:
        c += 'B'
    return c

def get_colors_three(one, two, three):
    output = 'D'
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']
    cols = []
    for col in colors:
        if col in one:
            cols.append(col)
        if col in two:
            cols.append(col)
        if col in three:
            cols.append(col)
    n = len(set(cols))
    if n == 2:
        output = '2S'
    elif n == 1:
        output = '3S'
    return output



# f = open(current_folder + "/synthetic_corrections_long_stats.txt","w")
# for i, s in enumerate(shapes):
#     print(i+1, ' ', s, ' ', colors[i], file=f)
#     # print('----------------------------\n', file=f)
# print("stats printed")

# print(Counter(shapes))
# print(Counter(colors))

####FOR 200
def get_shapes(one, two):
    c = ''
    if 'tower' in one:
        c += 'T'
    elif 'row' in one:
        c += 'R'
    
    if 'tower' in two:
        c += 'T'
    elif 'row' in two:
        c += 'R'
    elif 'block' in two and 'blocks' not in two:
        c += 'B'
    return c

def get_colors(one, two):
    output = 'D'
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']
    cols = []
    for col in colors:
        if col in one:
            cols.append(col)
        if col in two:
            cols.append(col)
    n = len(set(cols))
    if n == 1:
        output = '2S'
    return output

# current_folder=os.getcwd()

# with open('/home/kate/minecraft_utils/synthetic/corrections/synthetic_corrections_short_check_freeze.txt') as f:
#     samples = f.read().split('\n')

def get_desc_200(samples):

    colors = []
    shapes = []

    first = ''
    second = ''
    for line in samples:
        if '2 <Arch>' in line:
            first = line.split('<Arch>')[1]
        elif '4 <Arch>' in line:
            second = line.split('<Arch>')[1]
        elif line == '----------------------------':
            shp = get_shapes(first, second)
            clr = get_colors(first, second)
            shapes.append(shp)
            colors.append(clr)
            first = ''
            second = ''

    assert len(colors) == len(shapes) == 200

    return colors, shapes

def get_desc_300(samples):

    colors = []
    shapes = []

    first = ''
    second = ''
    third = ''
    for line in samples:
        if '2 <Arch>' in line:
            first = line.split('<Arch>')[1]
        elif '4 <Arch>' in line:
            second = line.split('<Arch>')[1]
        elif '6 <Arch>' in line:
            third = line.split('<Arch>')[1]
        elif line == '----------------------------':
            shp = get_shapes_three(first, second, third)
            clr = get_colors_three(first, second, third)
            shapes.append(shp)
            colors.append(clr)
            first = ''
            second = ''
            third = ''

    assert len(colors) == len(shapes) == 300

    return colors, shapes


# f = open(current_folder + "/synthetic_corrections_short_stats.txt","w")
# for i, s in enumerate(shapes):
#     print(i+1, ' ', s, ' ', colors[i], file=f)
#     # print('----------------------------\n', file=f)
# print("stats printed")

# print(Counter(shapes))
# print(Counter(colors))

def json_format_three(dialogue, t):
    """
    input: list of instruction strings and the type (1, 2 or 3)
    """
    sample_list = []

    #sample one: FIRST CORRECTION
    s = {}
    if t == 1:
        s["PS"] = "CORR(3,8)"
    elif t == 2:
        s["PS"] = "CORR(5,8)"
    elif t == 3:
        s["PS"] = "CORR(7,8)"
    moves = '\n'.join(dialogue[:8])
    context = 'Context: ' + moves
    structure = 'Structure: CONTIN(0,1) CONTIN(1,2) RES(2,3) CONTIN(2,4) RES(4,5) CONTIN(4,6) RES(6,7)'
    new_turn = 'New turn: ' + dialogue[8]
    s["sample"] = '\n'.join([context, structure, new_turn])
    sample_list.append(s)

    #sample two: CORRECTIVE MOVE + SECOND CORRECTION
    s = {}
    if t == 1:
        s["PS"] = "RES(8,9) CORR(3,9)"
        structure = 'Structure: CONTIN(0,1) CONTIN(1,2) RES(2,3) CONTIN(2,4) RES(4,5) CONTIN(4,6) RES(6,7) CORR(3,8)'
    elif t == 2:
        s["PS"] = "RES(8,9) CORR(5,9)"
        structure = 'Structure: CONTIN(0,1) CONTIN(1,2) RES(2,3) CONTIN(2,4) RES(4,5) CONTIN(4,6) RES(6,7) CORR(5,8)'
    elif t == 3:
        s["PS"] = "RES(8,9) CORR(7,9)"
        structure = 'Structure: CONTIN(0,1) CONTIN(1,2) RES(2,3) CONTIN(2,4) RES(4,5) CONTIN(4,6) RES(6,7) CORR(7,8)'
    moves = '\n'.join(dialogue[:9])

    context = 'Context: ' + moves
    new_turn = 'New turn: ' + dialogue[9]
    s["sample"] = '\n'.join([context, structure, new_turn])
    sample_list.append(s)
    
    return sample_list

def json_format(dialogue, t):
    """
    input: list of instruction strings and the type (1 or 2)
    """
    sample_list = []

    #sample one: FIRST CORRECTION
    s = {}
    if t == 1:
        s["PS"] = "CORR(3,6)"
    elif t == 2:
        s["PS"] = "CORR(5,6)"
    moves = '\n'.join(dialogue[:6])
    context = 'Context: ' + moves
    structure = 'Structure: CONTIN(0,1) CONTIN(1,2) RES(2,3) CONTIN(2,4) RES(4,5)'
    new_turn = 'New turn: ' + dialogue[6]

    s["sample"] = '\n'.join([context, structure, new_turn])
    sample_list.append(s)

    #sample two: CORRECTIVE MOVE + SECOND CORRECTION
    s = {}
    if t == 1:
        s["PS"] = "RES(6,7) CORR(3,7)"
        structure = 'Structure: CONTIN(0,1) CONTIN(1,2) RES(2,3) CONTIN(2,4) RES(4,5) CORR(3,6)'
    elif t == 2:
        s["PS"] = "RES(6,7) CORR(5,7)"
        structure = 'Structure: CONTIN(0,1) CONTIN(1,2) RES(2,3) CONTIN(2,4) RES(4,5) CORR(5,6)'
    moves = '\n'.join(dialogue[:7])

    context = 'Context: ' + moves
    new_turn = 'New turn: ' + dialogue[7]
    s["sample"] = '\n'.join([context, structure, new_turn])
    sample_list.append(s)
    

    return sample_list

def json_format(dialogue, t):
    """
    input: list of instruction strings and the type (1 or 2)
    """
    sample_list = []

    #sample one: FIRST CORRECTION
    s = {}
    if t == 1:
        s["PS"] = "CORR(2,5)"
    elif t == 2:
        s["PS"] = "CORR(4,5)"
    moves = '\n'.join(dialogue[:5])
    context = 'Context: ' + moves
    structure = 'Structure: CONTIN(0,1) RES(1,2) CONTIN(1,3) RES(3,4)'
    new_turn = 'New turn: ' + dialogue[5]
    s["sample"] = '\n'.join([context, structure, new_turn])
    sample_list.append(s)

    #sample two: CORRECTIVE MOVE + SECOND CORRECTION
    s = {}
    if t == 1:
        s["PS"] = "RES(5,6) CORR(2,6)"
        structure = 'Structure: CONTIN(0,1) RES(1,2) CONTIN(1,3) RES(3,4) CORR(2,5)'
    elif t == 2:
        s["PS"] = "RES(5,6) CORR(4,6)"
        structure = 'Structure: CONTIN(0,1) RES(1,2) CONTIN(1,3) RES(3,4) CORR(4,5)'
    moves = '\n'.join(dialogue[:6])

    context = 'Context: ' + moves
    new_turn = 'New turn: ' + dialogue[6]
    s["sample"] = '\n'.join([context, structure, new_turn])
    sample_list.append(s)
    

    return sample_list
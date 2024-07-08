import csv
import os
import numpy as np
import build_functions as bs
import functions as fun
import clarfq as clar



S = {"square", "row", "rectangle", "tower", "diagonal", "diamond", "cube"}
# L = {"centre", "edge", "corner", ""}
# C = {"orange", "red", "green", "blue", "purple", "yellow"}
# O = {"horizontal", "vertical",""}
# S = {"cube"}
L = {"centre", "edge", "corner", ""}
C = {"orange", "red", "green", "blue", "purple", "yellow"}
O = {"horizontal", "vertical"}
l = []
l_cov = []
#l_dicts = []
build_seqs = []
for orient in O:
    for col in C:
        for loc in L:
            for shape in S:
                for size in range(3,10):
                    l_dict = {key: None for key in ['size', 'col', 'loc', 'orient']}
                    #=================================================================================================================ROW/DIAGONAL
                    if shape in ["row","diagonal"] and f"{shape} {size} {col} {loc}" not in l_cov:
                        l_dict['size'] = size
                        l_dict['col'] = col
                        l_dict['loc'] = loc
                        l_dict['orient'] = orient
                        l_dict['shape'] = shape
                        l_cov.append(f"{shape} {size} {col} {loc}")
                        utterances = clar.no_orient_clarif(l_dict)
                        l.append(utterances)
                    
                    #===================================================================================================================SQUARE
                    elif shape=="square" and f"{size} {col} {orient} {shape} {loc}" not in l_cov:
                        if size>5:
                            continue
                        ##FORMULATE EXCHANGE
                        else:
                            l_dict['size'] = size
                            l_dict['col'] = col
                            l_dict['loc'] = loc
                            l_dict['orient'] = orient
                            l_dict['shape'] = shape
                            l_cov.append(f"{size} {col} {orient} {shape} {loc}")
                            utterances = clar.clarif_question(l_dict)
                            l.append(utterances)
                    #===================================================================================================================CUBE
                    elif shape=="cube" and f"{size} {col} {shape} {loc}" not in l_cov:
                        if size>3:
                            continue
                        ##FORMULATE EXCHANGE
                        else:
                            l_dict['size'] = size
                            l_dict['col'] = col
                            l_dict['loc'] = loc
                            l_dict['shape'] = shape
                            l_cov.append(f"{size} {col} {shape} {loc}")
                            utterances = clar.no_orient_clarif(l_dict)
                            l.append(utterances)
                    #===================================================================================================================RECTANGLE
                    elif shape=="rectangle":
                        if size==3:
                            up_lim = 10
                        if size==4:
                            up_lim = 8
                        if size>4:
                            continue
                        else:
                            r = np.random.randint(size+1,up_lim)
                            if f"{r} {size} {col} {orient} {shape} {loc}" not in l_cov:
                                l_dict['size'] = size
                                l_dict['r'] = r
                                l_dict['col'] = col
                                l_dict['loc'] = loc
                                l_dict['orient'] = orient
                                l_dict['shape'] = shape
                                l_cov.append(f"{r} {size} {col} {orient} {shape} {loc}")
                                utterances = clar.rectangle_clarifq(l_dict)
                                l.append(utterances)
                                #print(l_dict)
                                #print(utterances)S

                    #===================================================================================================================DIAMOND
                    elif shape=="diamond" and f"{col} {orient} {shape} {size}" not in l_cov:
                        if size>6:
                            continue
                        else:
                            # loc = None
                            l_dict['size'] = size
                            l_dict['col'] = col
                            l_dict['loc'] = loc
                            l_dict['shape'] = shape
                            l_dict['orient'] = orient
                            l_cov.append(f"{col} {orient} {shape} {size}")
                            utterances = clar.diamond_clarifq(l_dict)
                            l.append(utterances)
                            #print(l_dict)

                    #===================================================================================================================TOWER
                    elif shape=="tower" and f"{col} {shape} {size} {loc}" not in l_cov:
                        ##FORMULATE EXCHANGE
                        l_dict['size'] = size
                        l_dict['col'] = col
                        l_dict['loc'] = loc
                        l_dict['shape'] = shape
                        l_cov.append(f"{col} {shape} {size} {loc}")
                        utterances = clar.no_orient_clarif(l_dict)
                        l.append(utterances)

        
                    ## GENERATE SEQUENCES
                    if f"{shape}" == "row":
                        size=int(f"{size}")
                        act_seq = bs.row(f"{col}", size, None, f"{loc}")
                        assert fun.is_row(fun.get_net_sequence(act_seq))[0]
                        assert fun.is_row(fun.get_net_sequence(act_seq))[1]==size
                        build_seqs.append(act_seq)
                    elif f"{shape}" == "tower":
                        size=int(f"{size}")
                        act_seq = bs.tower(f"{col}", size, None, f"{loc}")
                        assert fun.is_tower(fun.get_net_sequence(act_seq))[0]
                        assert fun.is_tower(fun.get_net_sequence(act_seq))[1]==size
                        build_seqs.append(act_seq)
                    elif f"{shape}" == "square":
                        size=int(f"{size}")
                        act_seq = bs.square(f"{col}", size, f"{orient}", f"{loc}")
                        #print(fun.is_square(fun.get_net_sequence(act_seq))[0])
                        assert fun.is_square(fun.get_net_sequence(act_seq))[0]
                        assert fun.is_square(fun.get_net_sequence(act_seq))[1]==size
                        build_seqs.append(act_seq)
                    elif f"{shape}" == "diamond":
                        size=int(f"{size}")
                        act_seq = bs.diamond(f"{col}", size, f"{orient}", None)
                        #print(fun.is_diamond(fun.get_net_sequence(act_seq)))
                        assert fun.is_diamond(fun.get_net_sequence(act_seq))[0]
                        assert fun.is_diamond(fun.get_net_sequence(act_seq))[1][0]==size 
                        build_seqs.append(act_seq)
                    elif f"{shape}" == "diagonal":
                        #print('here')
                        size=int(f"{size}")
                        act_seq = bs.diagonal(f"{col}", size, None, f"{loc}")
                        #print(fun.is_diagonal(fun.get_net_sequence(act_seq))[1])
                        assert fun.is_diagonal(fun.get_net_sequence(act_seq))[0]
                        assert fun.is_diagonal(fun.get_net_sequence(act_seq))[1]==size
                        build_seqs.append(act_seq)
                    elif f"{shape}" == "cube":
                        size=int(f"{size}")
                        act_seq = bs.cube(f"{col}", size, None, f"{loc}")
                        assert fun.is_cube(fun.get_net_sequence(act_seq))[0]
                        assert fun.is_cube(fun.get_net_sequence(act_seq))[1]==size
                        build_seqs.append(act_seq)
                    elif f"{shape}" == "rectangle":
                        #size = [int(a) for a in f"{size}".split("x")]
                        size = [r, size]
                        act_seq = bs.rectangle(f"{col}", size, f"{orient}", f"{loc}")
                        assert fun.is_rectangle(fun.get_net_sequence(act_seq))[0]
                        assert (fun.is_rectangle(fun.get_net_sequence(act_seq))[1][0]==size[0] and fun.is_rectangle(fun.get_net_sequence(act_seq))[1][1]==size[1]) or (fun.is_rectangle(fun.get_net_sequence(act_seq))[1][1]==size[0] and fun.is_rectangle(fun.get_net_sequence(act_seq))[1][0]==size[1])
                        build_seqs.append(act_seq)

                    build_seqs.append(act_seq)

#now that we have all the instructions/
# for i, inst in enumerate(l):
#     print(inst[0])
#     print(inst[1])S
#     print(inst[2])
#     print('--------------')
#     print(build_seqs[i])
#     print('--------------------')

current_folder = os.getcwd()
fields = ['dial_with_actions', 'action_seq']
with open(current_folder + '/clarif_synth_train.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    for i, inst in enumerate(l):
        #print(inst)
        inst_str = '\n'.join(inst)
        write.writerow([inst_str, build_seqs[i]])

print('csv saved.')

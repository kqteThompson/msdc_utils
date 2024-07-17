import csv
import os
import numpy as np
import build_functions as bs
import functions as fun
import clarfq as clar



S = {"square", "row", "rectangle", "tower", "diagonal", "diamond", "cube"}
# S = {"square"}
L = {"centre", "edge", "corner", ""}
C = {"orange", "red", "green", "blue", "purple", "yellow"}
# C = {"orange", "blue"}
O = {"horizontal", "vertical",""}
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
                        utterances, p_up = clar.no_orient_clarif(l_dict)
                        l.append(utterances)
                        for k in p_up.keys():
                            if k == 'loc':
                                l_dict['loc'] = p_up['loc']
                        #BUILD 
                        if f"{shape}" == "row":
                            size=int(f"{size}")
                            act_seq = bs.row(f"{col}", size, None, f"{loc}")
                            assert fun.is_row(fun.get_net_sequence(act_seq))[0]
                            assert fun.is_row(fun.get_net_sequence(act_seq))[1]==size
                        elif f"{shape}" == "diagonal":
                            size=int(f"{size}")
                            act_seq = bs.diagonal(f"{col}", size, None, f"{loc}")
                            assert fun.is_diagonal(fun.get_net_sequence(act_seq))[0]
                            assert fun.is_diagonal(fun.get_net_sequence(act_seq))[1]==size
                        build_seqs.append(act_seq)
                    
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
                            print(l_dict)
                            l_cov.append(f"{size} {col} {orient} {shape} {loc}")
                            utterances, p_up = clar.square_clarif(l_dict)
                            l.append(utterances)
                            for k in p_up.keys():
                                if k == 'orient':
                                    orient = p_up['orient']
                                elif k == 'loc':
                                    loc = p_up['loc']
                            print(utterances)
                            print(p_up)
                            #BUILD
                            size=int(f"{size}")
                            act_seq = bs.square(f"{col}", size, f"{orient}", f"{loc}")
                            assert fun.is_square(fun.get_net_sequence(act_seq))[0]
                            assert fun.is_square(fun.get_net_sequence(act_seq))[1]==size
                            build_seqs.append(act_seq)

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
                            utterances, p_up = clar.no_orient_clarif(l_dict)
                            l.append(utterances)
                            for k in p_up.keys():
                                if k == 'loc':
                                    l_dict['loc'] = p_up['loc']
                            #BUILD
                            size=int(f"{size}")
                            act_seq = bs.cube(f"{col}", size, None, f"{loc}")
                            assert fun.is_cube(fun.get_net_sequence(act_seq))[0]
                            assert fun.is_cube(fun.get_net_sequence(act_seq))[1]==size
                            build_seqs.append(act_seq)
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
                                #print(l_dict)
                                l_cov.append(f"{r} {size} {col} {orient} {shape} {loc}")
                                utterances, p_up = clar.rectangle_clarifq(l_dict)
                                l.append(utterances)
                                # print(utterances)
                                # print(p_up)
                                for k in p_up.keys():
                                    if k == 'orient':
                                        orient = p_up['orient']
                                    elif k == 'loc':
                                        loc = p_up['loc']
                                #BUILD
                                size = [r, size]
                                act_seq = bs.rectangle(f"{col}", size, f"{orient}", f"{loc}")
                                print(act_seq)
                                assert fun.is_rectangle(fun.get_net_sequence(act_seq))[0]
                                print(fun.is_rectangle(fun.get_net_sequence(act_seq)))
                                assert (fun.is_rectangle(fun.get_net_sequence(act_seq))[1][0]==size[0] and fun.is_rectangle(fun.get_net_sequence(act_seq))[1][1]==size[1]) or (fun.is_rectangle(fun.get_net_sequence(act_seq))[1][1]==size[0] and fun.is_rectangle(fun.get_net_sequence(act_seq))[1][0]==size[1])
                                build_seqs.append(act_seq)

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
                            utterances, p_up = clar.diamond_clarifq(l_dict)
                            l.append(utterances)
                            for k in p_up.keys():
                                if k == 'orient':
                                    l_dict['orient'] = p_up['orient']
                            #BUILD
                            size=int(f"{size}")
                            act_seq = bs.diamond(f"{col}", size, f"{orient}", None)
                            assert fun.is_diamond(fun.get_net_sequence(act_seq))[0]
                            assert fun.is_diamond(fun.get_net_sequence(act_seq))[1][0]==size 
                            build_seqs.append(act_seq)

                    #===================================================================================================================TOWER
                    elif shape=="tower" and f"{col} {shape} {size} {loc}" not in l_cov:
                        ##FORMULATE EXCHANGE
                        l_dict['size'] = size
                        l_dict['col'] = col
                        l_dict['loc'] = loc
                        l_dict['shape'] = shape
                        l_cov.append(f"{col} {shape} {size} {loc}")
                        utterances, p_up = clar.no_orient_clarif(l_dict)
                        l.append(utterances)
                        for k in p_up.keys():
                            if k == 'loc':
                                l_dict['loc'] = p_up['loc']
                        #BUILD
                        size=int(f"{size}")
                        act_seq = bs.tower(f"{col}", size, None, f"{loc}")
                        assert fun.is_tower(fun.get_net_sequence(act_seq))[0]
                        assert fun.is_tower(fun.get_net_sequence(act_seq))[1]==size
                        build_seqs.append(act_seq)

#now that we have all the instruction#s/
# for i, inst in enumerate(l):
#     print(inst[0])
#     print(inst[1])S
#     print(inst[2])
#     print('--------------')
#     print(build_seqs[i])
#     print('--------------------') 

print(len(l))
print(len(build_seqs))

current_folder = os.getcwd()
fields = ['dial_with_actions', 'action_seq']
with open(current_folder + '/clarif_synth_train.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    for i, inst in enumerate(l):
        inst_str = '\n'.join(inst)
        write.writerow([inst_str, build_seqs[i]])

print('csv saved.')

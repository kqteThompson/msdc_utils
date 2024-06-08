import numpy as np
from datasets import load_dataset

def is_ontopof(pred_net_seq, prev_net_act_seq):
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in prev_net_act_seq if x.startswith("place")]
    flag = False
    if len(pred_net_seq)>1:
        print("Net pred sequence greater than 1")
        return flag
    if "place" not in pred_net_seq[0]:
        print("place action missing")
        return flag, "no place action"
    if len(pred_net_seq[0].split(" "))>5:
        print("too many coordinates")
        return flag, "too many coordinates"
    pred_x, pred_y, pred_z = int(pred_net_seq[0].split(" ")[2]), int(pred_net_seq[0].split(" ")[3]), int(pred_net_seq[0].split(" ")[4])
    if (pred_x, pred_y, pred_z) in coords_list:
        return flag
    y_inds = [y for (x,y,z) in coords_list if x==pred_x and z==pred_z] 
    if pred_y-1 in y_inds and np.max(y_inds)<pred_y:
        flag = True
    return flag
          

def is_totheside(pred_net_seq, prev_net_act_seq):
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in prev_net_act_seq if x.startswith("place")]
    flag = False
    if len(pred_net_seq)>1:
        print("Net pred sequence greater than 1")
        return flag
    if "place" not in pred_net_seq[0]:
        print("place action missing")
        return flag, "no place action"
    if len(pred_net_seq[0].split(" "))>5:
        print("too many coordinates")
        return flag, "too many coordinates"
    pred_x, pred_y, pred_z = int(pred_net_seq[0].split(" ")[2]), int(pred_net_seq[0].split(" ")[3]), int(pred_net_seq[0].split(" ")[4])   
    if (pred_x, pred_y, pred_z) in coords_list:
        return flag
    if (pred_x+1, pred_y, pred_z) in coords_list or (pred_x-1, pred_y, pred_z) in coords_list:
        flag = True
    if (pred_x, pred_y, pred_z+1) in coords_list or (pred_x, pred_y, pred_z-1) in coords_list:
        flag = True
    if (pred_x, pred_y-1, pred_z) in coords_list:
        flag = True
    return flag
    
    
def is_touching(pred_net_seq, prev_net_act_seq):
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in prev_net_act_seq if x.startswith("place")]
    flag = False
    if len(pred_net_seq)>1:
        print("Net pred sequence greater than 1")
        return flag
    if "place" not in pred_net_seq[0]:
        print("place action missing")
        return flag
    if len(pred_net_seq[0].split(" "))>5:
        print("too many coordinates")
        return flag
    pred_x, pred_y, pred_z = int(pred_net_seq[0].split(" ")[2]), int(pred_net_seq[0].split(" ")[3]), int(pred_net_seq[0].split(" ")[4])   
    if (pred_x, pred_y, pred_z) in coords_list:
        return flag, "placed on existing block"
    if is_totheside(pred_net_seq, prev_net_act_seq):
        flag = True
        return flag
    for (x,y,z) in coords_list:
        if np.abs(x-pred_x)<=1 and np.abs(y-pred_y)<=1 and np.abs(z-pred_z)<=1:
            flag = True 
    return flag
    


def removal(pred_net_seq, prev_net_act_seq, rem_type=None):
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in prev_net_act_seq if x.startswith("place")]
    flag = False
    if len(pred_net_seq)>1:
        print("Net pred sequence greater than 1")
        return flag
    if "pick" not in pred_net_seq[0]:
        print("pick action missing")
        return flag
    if len(pred_net_seq[0].split(" "))>4:
        print("too many coordinates")
        return flag, "too many coordinates"
    pred_x, pred_y, pred_z = int(pred_net_seq[0].split(" ")[1]), int(pred_net_seq[0].split(" ")[2]), int(pred_net_seq[0].split(" ")[3])
    if rem_type==None:
        if (pred_x, pred_y, pred_z) in coords_list:
            flag=True
        return flag
    elif rem_type=="you just placed":
        if (pred_x, pred_y, pred_z)==coords_list[-1]:
            flag=True
        return flag
    elif rem_type=="top":
        y_list = [a[1] for a in coords_list]
        ind = np.argmax(y_list)
        if (pred_x, pred_y, pred_z)==coords_list[ind]:
            flag=True
        return flag
    elif rem_type=="bottom":
        y_list = [a[1] for a in coords_list]
        ind = np.argmin(y_list)
        if (pred_x, pred_y, pred_z)==coords_list[ind]:
            flag=True
        return flag
    elif rem_type=="centre":
        x_list = [a[0] for a in coords_list]
        y_list = [a[1] for a in coords_list]
        z_list = [a[2] for a in coords_list]
        x_mean, y_mean, z_mean = int(np.mean(x_list)), int(np.mean(y_list)), int(np.mean(z_list))
        if (pred_x, pred_y, pred_z)==(x_mean, y_mean, z_mean):
            flag=True
        return flag
    elif rem_type=="corner":
        x_list = [a[0] for a in coords_list]
        z_list = [a[2] for a in coords_list]
        y_list = [a[1] for a in coords_list]
        x_min, z_min, x_mean, z_mean, x_max, z_max, y_min, y_max = int(np.min(x_list)), int(np.min(z_list)), int(np.mean(x_list)), int(np.mean(z_list)), int(np.max(x_list)), int(np.max(z_list)), 1, int(np.max(y_list))
        if pred_y==1 and y_min == y_max and (pred_x,pred_z) in [(x_min,z_mean), (x_mean,z_min), (x_mean, z_max), (x_max, z_mean)]: # 4 corners of horizontal diamond
            flag=True
        if (pred_x,pred_y,pred_z) in [(x_min, y_min, z_min), (x_min, y_min, z_max), (x_max, y_min, z_min), (x_max, y_min, z_max),(x_min, y_max, z_min), (x_min, y_max, z_max), (x_max, y_max, z_min), (x_max, y_max, z_max)]:
            flag=True
        return flag
    elif rem_type=="end":
        x_list = [a[0] for a in coords_list]
        z_list = [a[2] for a in coords_list]
        x_min, z_min, x_max, z_max = int(np.min(x_list)), int(np.min(z_list)), int(np.max(x_list)), int(np.max(z_list))
        if (x_min==x_max) or (z_min==z_max): # row
            if pred_y==1 and (pred_x,pred_z) in [(x_min,z_min),(x_min,z_max),(x_max,z_min),(x_max,z_max)]:
                flag=True
                return flag
        elif (x_min, 1, z_min) in coords_list: # diagonal
            if pred_y==1 and (pred_x,pred_z) in [(x_min,z_min), (x_max,z_max)]:
                flag=True
                return flag
        elif (x_min, 1, z_max) in coords_list: # diagonal
            if pred_y==1 and (pred_x,pred_z) in [(x_min,z_max), (x_max,z_min)]:
                flag=True
                return flag
        return flag    
    return flag, f"rem_type is {rem_type}"
    
        

def get_net_sequence(act_seq):
    net_act_seq = []
    for i in range(len(act_seq)):
        if act_seq[i].split(" ")[0]!="pick":
            net_act_seq.append(act_seq[i])
        else:
            idx = None
            for j in range(len(net_act_seq)):
                if len(act_seq[i].split(" "))==4 and net_act_seq[j].split(" ")[0]=="place" and net_act_seq[j].split(" ")[2]==act_seq[i].split(" ")[1] and net_act_seq[j].split(" ")[3]==act_seq[i].split(" ")[2] and net_act_seq[j].split(" ")[4]==act_seq[i].split(" ")[3]:
                    idx = j
            if idx==None:
                net_act_seq.append(act_seq[i])
            else:
                net_act_seq.pop(idx)
    return net_act_seq


data = load_dataset("csv",data_files={"train":"./level-one-synth-data-with-action-seq.csv"})["train"]
pred_data = load_dataset("csv",data_files={"train":"./llama_3_synthdata_level2.csv"})["train"]

assert len(data)==len(pred_data)

count_place = 0
total_place = 0
count_ontopof = 0
total_ontopof = 0
count_totheside = 0
total_totheside = 0
count_touching = 0
total_touching = 0
count_nottouching = 0
total_nottouching = 0

count_removal = 0
total_removal = 0
count_yjp = 0
total_yjp = 0
count_top = 0
total_top = 0
count_bottom = 0
total_bottom = 0
count_centre = 0
total_centre = 0
count_corner = 0
total_corner = 0
count_end = 0
total_end = 0
count_none = 0
total_none = 0

for i in range(len(data)): 
    prev_net_act_seq = get_net_sequence(data["action_seq"][i].split(" \n "))
    pred_net_seq = get_net_sequence(pred_data["pred_seq"][i].split(" \n "))
    lvl2_inst = pred_data["dial_with_actions"][i].split(" \n ")[-1].split("<Architect> ")[1]
    if "on top of" in lvl2_inst:
        total_place+=1
        total_ontopof+=1
        if is_ontopof(pred_net_seq, prev_net_act_seq):
            count_place+=1
            count_ontopof+=1
    if "to the side" in lvl2_inst:
        total_place+=1
        total_totheside+=1
        if is_totheside(pred_net_seq, prev_net_act_seq):
            count_place+=1
            count_totheside+=1
    if "touching" in lvl2_inst and "not touching" not in lvl2_inst:
        total_place+=1
        total_touching+=1
        if is_touching(pred_net_seq, prev_net_act_seq):
            count_place+=1
            count_touching+=1
    if "not touching" in lvl2_inst:
        total_place+=1
        total_nottouching+=1
        if not is_touching(pred_net_seq, prev_net_act_seq) and len(pred_net_seq)==1 and "place" in pred_net_seq[0] and len(pred_net_seq[0].split(" "))==5: 
            count_place+=1
            count_nottouching+=1
    if "remove" in lvl2_inst:
        total_removal+=1
        if "you just placed" in lvl2_inst:
            total_yjp+=1
            if removal(pred_net_seq, prev_net_act_seq, rem_type="you just placed"):
                count_removal+=1
                count_yjp+=1 
        elif "top" in lvl2_inst:
            total_top+=1
            if removal(pred_net_seq, prev_net_act_seq, rem_type="top"):
                count_removal+=1
                count_top+=1
        elif "bottom" in lvl2_inst:
            total_bottom+=1
            if removal(pred_net_seq, prev_net_act_seq, rem_type="bottom"):
                count_removal+=1
                count_bottom+=1
        elif "centre" in lvl2_inst:
            total_centre+=1
            if removal(pred_net_seq, prev_net_act_seq, rem_type="centre"):
                count_removal+=1
                count_centre+=1
        elif "corner" in lvl2_inst:
            total_corner+=1
            print(pred_net_seq)
            print(prev_net_act_seq)
            if removal(pred_net_seq, prev_net_act_seq, rem_type="corner"):
                count_removal+=1
                count_corner+=1
        elif "end" in lvl2_inst:
            total_end+=1
            if removal(pred_net_seq, prev_net_act_seq, rem_type="end"):
                count_removal+=1
                count_end+=1
        else:
            total_none+=1
            if removal(pred_net_seq, prev_net_act_seq):
                count_removal+=1
                count_none+=1   

print("Overall accuracy", (count_place+count_removal)/(total_place+total_removal))
print("Overall place accuracy", count_place/total_place)
print("Overall removal accuracy", count_removal/total_removal)
print("Place on top of accuracy", count_ontopof/total_ontopof)
print("Place to the side of accuracy", count_totheside/total_totheside)
print("Place touching accuracy", count_touching/total_touching)
print("Place not touching accuracy", count_nottouching/total_nottouching)

print("Removal any accuracy", count_none/total_none)
print("Removal you just placed accuracy", count_yjp/total_yjp)
print("Removal top accuracy", count_top/total_top)
print("Removal bottom accuracy", count_bottom/total_bottom)
print("Removal centre accuracy", count_centre/total_centre)
print("Removal corner accuracy", count_corner/total_corner)
print("Removal end accuracy", count_end/total_end)

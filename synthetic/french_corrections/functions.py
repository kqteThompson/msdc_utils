import pandas
import numpy as np


def is_square_unfilled(net_act_seq):
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in net_act_seq if x.startswith("place")]
    x_list = [a[0] for a in coords_list]
    y_list = [a[1] for a in coords_list]
    z_list = [a[2] for a in coords_list]
    flag = False
    x_min, x_max, y_min, y_max, z_min, z_max = np.min(x_list), np.max(x_list), np.min(y_list), np.max(y_list), np.min(z_list), np.max(z_list)
    if x_min==x_max and y_max-y_min>0 and y_max-y_min==z_max-z_min:
       filled_rect_l = [(x_min,y,z) for y in range(y_min,y_max+1) for z in range(z_min,z_max+1)]
       inside_rect_l = [(x_min,y,z) for y in range(y_min+1,y_max) for z in range(z_min+1,z_max)]
       rect_l = [a for a in filled_rect_l if a not in inside_rect_l]
       if set(coords_list)==set(rect_l):
           flag = True
           return flag, y_max-y_min+1
    elif y_min==y_max and x_max-x_min>0 and x_max-x_min==z_max-z_min:
       filled_rect_l = [(x,y_min,z) for x in range(x_min,x_max+1) for z in range(z_min,z_max+1)]
       inside_rect_l = [(x,y_min,z) for x in range(x_min+1,x_max) for z in range(z_min+1,z_max)]
       rect_l = [a for a in filled_rect_l if a not in inside_rect_l]
       if set(coords_list)==set(rect_l):
           flag = True
           return flag, x_max-x_min+1
    elif z_min==z_max and x_max-x_min>0 and x_max-x_min==y_max-y_min:
       filled_rect_l = [(x,y,z_min) for x in range(x_min,x_max+1) for y in range(y_min,y_max+1)]
       inside_rect_l = [(x,y,z_min) for x in range(x_min+1,x_max) for y in range(y_min+1,y_max)]
       rect_l = [a for a in filled_rect_l if a not in inside_rect_l]
       if set(coords_list)==set(rect_l):
           flag = True
           return flag, (x_max-x_min+1).item()    
    return flag
    
def is_rectangle_unfilled(net_act_seq):
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in net_act_seq if x.startswith("place")]
    x_list = [a[0] for a in coords_list]
    y_list = [a[1] for a in coords_list]
    z_list = [a[2] for a in coords_list]
    flag = False
    x_min, x_max, y_min, y_max, z_min, z_max = np.min(x_list), np.max(x_list), np.min(y_list), np.max(y_list), np.min(z_list), np.max(z_list)
    if x_min==x_max and y_max-y_min>0:
       filled_rect_l = [(x_min,y,z) for y in range(y_min,y_max+1) for z in range(z_min,z_max+1)]
       inside_rect_l = [(x_min,y,z) for y in range(y_min+1,y_max) for z in range(z_min+1,z_max)]
       rect_l = [a for a in filled_rect_l if a not in inside_rect_l]
       if set(coords_list)==set(rect_l):
           flag = True
           return flag, ((y_max-y_min+1),(z_max-z_min+1)) 
    elif y_min==y_max and z_max-z_min>0:
       filled_rect_l = [(x,y_min,z) for x in range(x_min,x_max+1) for z in range(z_min,z_max+1)]
       inside_rect_l = [(x,y_min,z) for x in range(x_min+1,x_max) for z in range(z_min+1,z_max)]
       rect_l = [a for a in filled_rect_l if a not in inside_rect_l]
       if set(coords_list)==set(rect_l):
           flag = True
           return flag, ((x_max-x_min+1),(z_max-z_min+1))  
    elif z_min==z_max and x_max-x_min>0:
       filled_rect_l = [(x,y,z_min) for x in range(x_min,x_max+1) for y in range(y_min,y_max+1)]
       inside_rect_l = [(x,y,z_min) for x in range(x_min+1,x_max) for y in range(y_min+1,y_max)]
       rect_l = [a for a in filled_rect_l if a not in inside_rect_l]
       if set(coords_list)==set(rect_l):
           flag = True
           return flag, ((x_max-x_min+1).item(),(y_max-y_min+1).item())    
    return flag

def is_cube_unfilled(net_act_seq):
    # For cube, x_max-x_min=y_max-y_min=z_max-z_min=s and we should have block at each (x,y,z) within the [x_min,x_max] x [y_min,y_max] x [z_min,z_max]
    # If the pred seq is cube, return True along with size s+1, else False
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in net_act_seq if x.startswith("place")]
    x_list = [a[0] for a in coords_list]
    y_list = [a[1] for a in coords_list]
    z_list = [a[2] for a in coords_list]
    flag = False
    x_min, x_max, y_min, y_max, z_min, z_max = np.min(x_list), np.max(x_list), np.min(y_list), np.max(y_list), np.min(z_list), np.max(z_list)
    filled_cube_l = [(x,y,z) for x in range(x_min,x_max+1) for y in range(y_min,y_max+1) for z in range(z_min,z_max+1)]
    inside_cube_l = [(x,y,z) for x in range(x_min+1,x_max) for y in range(y_min+1,y_max) for z in range(z_min+1,z_max)]
    cube_l = [a for a in filled_cube_l if a not in inside_cube_l]
    if set(coords_list)==set(cube_l) and x_max-x_min==y_max-y_min and y_max-y_min==z_max-z_min:
        flag = True
        return flag, int(x_max-x_min+1)
    return flag
    
def is_square(net_act_seq):
    # For square, one of x, y, z is constant. 
    # Let's say y is constant, starting from (x_min, z_min) we should have block at each (x,z) within the range [x_min,x_max] x [z_min,z_max]
    # and we should have x_max-x_min=z_max-z_min
    # If the pred seq is square, return True along with size x_max-x_min+1, else False
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in net_act_seq if x.startswith("place")]
    x_list = [a[0] for a in coords_list]
    y_list = [a[1] for a in coords_list]
    z_list = [a[2] for a in coords_list]
    flag = False
    x_min, x_max, y_min, y_max, z_min, z_max = np.min(x_list), np.max(x_list), np.min(y_list), np.max(y_list), np.min(z_list), np.max(z_list)
    if x_min==x_max and y_max-y_min>0 and y_max-y_min==z_max-z_min:
       rect_l = [(x_min,y,z) for y in range(y_min,y_max+1) for z in range(z_min,z_max+1)]
       if set(coords_list)==set(rect_l):
           flag = True
           return flag, y_max-y_min+1
    elif y_min==y_max and x_max-x_min>0 and x_max-x_min==z_max-z_min:
       rect_l = [(x,y_min,z) for x in range(x_min,x_max+1) for z in range(z_min,z_max+1)]
       if set(coords_list)==set(rect_l):
           flag = True
           return flag, x_max-x_min+1
    elif z_min==z_max and x_max-x_min>0 and x_max-x_min==y_max-y_min:
       rect_l = [(x,y,z_min) for x in range(x_min,x_max+1) for y in range(y_min,y_max+1)]
       if set(coords_list)==set(rect_l):
           flag = True
           return flag, (x_max-x_min+1).item()   
    return flag

def is_rectangle(net_act_seq):
    # For rectangle, one of x, y, z is constant. 
    # Let's say y is constant, starting from (x_min, z_min) we should have block at each (x,z) within the range [x_min,x_max] x [z_min,z_max]
    # If the pred seq is rectangle, return True along with size (x_max-x_min+1)x(z_max-z_min+1), else False 
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in net_act_seq if x.startswith("place")]
    x_list = [a[0] for a in coords_list]
    y_list = [a[1] for a in coords_list]
    z_list = [a[2] for a in coords_list]
    flag = False
    x_min, x_max, y_min, y_max, z_min, z_max = np.min(x_list), np.max(x_list), np.min(y_list), np.max(y_list), np.min(z_list), np.max(z_list)
    if x_min==x_max and y_max-y_min>0:
       rect_l = [(x_min,y,z) for y in range(y_min,y_max+1) for z in range(z_min,z_max+1)]
       if set(coords_list)==set(rect_l):
           flag = True
           return flag, ((y_max-y_min+1),(z_max-z_min+1)) 
    elif y_min==y_max and z_max-z_min>0:
       rect_l = [(x,y_min,z) for x in range(x_min,x_max+1) for z in range(z_min,z_max+1)]
       if set(coords_list)==set(rect_l):
           flag = True
           return flag, ((x_max-x_min+1),(z_max-z_min+1))  
    elif z_min==z_max and x_max-x_min>0:
       rect_l = [(x,y,z_min) for x in range(x_min,x_max+1) for y in range(y_min,y_max+1)]
       if set(coords_list)==set(rect_l):
           flag = True
           return flag, ((x_max-x_min+1).item(),(y_max-y_min+1).item())    
    return flag
    
def is_diamond(net_act_seq):
    # For diamond, one of x, y, z is constant. 
    # Let's say z is constant, diamond is just collection of four diagonals. First, we should have x_max-x_min=y_max-y_min
    # The four diagonals are (i) From ((x_max+x_min)/2, y_min) to (x_max, (y_max+y_min)/2) (ii) From ((x_max+x_min)/2, y_max) to (x_max, (y_max+y_min)/2)
    # (iii) From (x_min, (y_max+y_min)/2) to ((x_max+x_min)/2, y_max), (iv) From (x_min, (y_max+y_min)/2) to ((x_max+x_min)/2, y_min)
    # If the pred seq is diamond, return True along with size (x_max-x_min)/2 + 1, else False 
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in net_act_seq if x.startswith("place")]
    x_list = [a[0] for a in coords_list]
    y_list = [a[1] for a in coords_list]
    z_list = [a[2] for a in coords_list]
    flag = False
    x_min, x_max, y_min, y_max, z_min, z_max = np.min(x_list), np.max(x_list), np.min(y_list), np.max(y_list), np.min(z_list), np.max(z_list)
    if x_min==x_max and y_max-y_min>0 and y_max-y_min==z_max-z_min:
        y_mid, z_mid = (y_max+y_min)/2, (z_max+z_min)/2
        if y_mid==int(y_mid) and z_mid==int(z_mid):
            y_mid, z_mid = int(y_mid), int(z_mid)
            diag_l1 = [(x_min,y,z) for (y,z) in zip(range(y_mid,y_max+1),range(z_min,z_mid+1))]
            diag_l2 = [(x_min,y,z) for (y,z) in zip(range(y_mid,y_max+1),range(z_max,z_mid-1,-1))]
            diag_l3 = [(x_min,y,z) for (y,z) in zip(range(y_min,y_mid+1),range(z_mid,z_max+1))]
            diag_l4 = [(x_min,y,z) for (y,z) in zip(range(y_min,y_mid+1),range(z_mid,z_min-1,-1))]
            diam_l = diag_l1 + diag_l2 + diag_l3 + diag_l4
            if set(coords_list)==set(diam_l):
                flag = True
                return flag, [int((y_max-y_min)/2 + 1)]
    if y_min==y_max and x_max-x_min>0 and x_max-x_min==z_max-z_min:
        x_mid, z_mid = (x_max+x_min)/2, (z_max+z_min)/2
        if x_mid==int(x_mid) and z_mid==int(z_mid):
            x_mid, z_mid = int(x_mid), int(z_mid)
            diag_l1 = [(x,y_min,z) for (x,z) in zip(range(x_mid,x_max+1),range(z_min,z_mid+1))]
            diag_l2 = [(x,y_min,z) for (x,z) in zip(range(x_mid,x_max+1),range(z_max,z_mid-1,-1))]
            diag_l3 = [(x,y_min,z) for (x,z) in zip(range(x_min,x_mid+1),range(z_mid,z_max+1))]
            diag_l4 = [(x,y_min,z) for (x,z) in zip(range(x_min,x_mid+1),range(z_mid,z_min-1,-1))]
            diam_l = diag_l1 + diag_l2 + diag_l3 + diag_l4
            if set(coords_list)==set(diam_l):
                flag = True
                return flag, [int((z_max-z_min)/2 + 1)]
    if z_min==z_max and x_max-x_min==y_max-y_min:
        x_mid, y_mid = (x_max+x_min)/2, (y_max+y_min)/2
        if x_mid==int(x_mid) and y_mid==int(y_mid):
            x_mid, y_mid = int(x_mid), int(y_mid)
            diag_l1 = [(x,y,z_min) for (x,y) in zip(range(x_mid,x_max+1),range(y_min,y_mid+1))]
            diag_l2 = [(x,y,z_min) for (x,y) in zip(range(x_mid,x_max+1),range(y_max,y_mid-1,-1))]
            diag_l3 = [(x,y,z_min) for (x,y) in zip(range(x_min,x_mid+1),range(y_mid,y_max+1))]
            diag_l4 = [(x,y,z_min) for (x,y) in zip(range(x_min,x_mid+1),range(y_mid,y_min-1,-1))]
            diam_l = diag_l1 + diag_l2 + diag_l3 + diag_l4
            if set(coords_list)==set(diam_l):
                flag = True
                return flag, [int((y_max-y_min)/2 + 1)]
    return flag
    
def is_diagonal(net_act_seq):
    # For diagonal, one of x, y, z is constant. 
    # Let's say y is constant,  then x_max-x_min=z_max-z_min=l
    # If a place action is at (x_min, z_max), then the rest of placements should be at (x_min+i, z_max-i) for all i in [1, l] 
    # Else if a place action is at (x_min, z_min), then the rest of placements should be at (x_min+i, z_min+i) for all i in [1, l]
    # If the pred seq is diagonal, return True along with size l+1, else False 
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in net_act_seq if x.startswith("place")]
    x_list = [a[0] for a in coords_list]
    y_list = [a[1] for a in coords_list]
    z_list = [a[2] for a in coords_list]
    flag = False
    x_min, x_max, y_min, y_max, z_min, z_max = np.min(x_list), np.max(x_list), np.min(y_list), np.max(y_list), np.min(z_list), np.max(z_list)
    if y_min==y_max and x_max-x_min==z_max-z_min:
        diag_l1 = [(x,y_min,z) for (x,z) in zip(range(x_max,x_min-1,-1),range(z_min,z_max+1))]
        diag_l2 = [(x,y_min,z) for (x,z) in zip(range(x_min,x_max+1),range(z_min,z_max+1))]
        if set(coords_list)==set(diag_l1) or set(coords_list)==set(diag_l2):
            flag = True
            return flag, x_max-x_min+1
    if x_min==x_max and y_max-y_min==z_max-z_min:
        diag_l1 = [(x_min,y,z) for (y,z) in zip(range(y_max,y_min-1,-1),range(z_min,z_max+1))]
        diag_l2 = [(x_min,y,z) for (y,z) in zip(range(y_min,y_max+1),range(z_min,z_max+1))]
        if set(coords_list)==set(diag_l1) or set(coords_list)==set(diag_l2):
            flag = True
            return flag, y_max-y_min+1
    if z_min==z_max and x_max-x_min==y_max-y_min:
        diag_l1 = [(x,y,z_min) for (x,y) in zip(range(x_max,x_min-1,-1),range(y_min,y_max+1))]
        diag_l2 = [(x,y,z_min) for (x,y) in zip(range(x_min,x_max+1),range(y_min,y_max+1))]
        if set(coords_list)==set(diag_l1) or set(coords_list)==set(diag_l2):
            flag = True
            return flag, (x_max-x_min+1).item()
    return flag
    
def is_cube(net_act_seq):
    # For cube, x_max-x_min=y_max-y_min=z_max-z_min=s and we should have block at each (x,y,z) within the [x_min,x_max] x [y_min,y_max] x [z_min,z_max]
    # If the pred seq is cube, return True along with size s+1, else False
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in net_act_seq if x.startswith("place")]
    x_list = [a[0] for a in coords_list]
    y_list = [a[1] for a in coords_list]
    z_list = [a[2] for a in coords_list]
    flag = False
    x_min, x_max, y_min, y_max, z_min, z_max = np.min(x_list), np.max(x_list), np.min(y_list), np.max(y_list), np.min(z_list), np.max(z_list)
    cube_l = [(x,y,z) for x in range(x_min,x_max+1) for y in range(y_min,y_max+1) for z in range(z_min,z_max+1)]
    if set(coords_list)==set(cube_l) and x_max-x_min==y_max-y_min and y_max-y_min==z_max-z_min:
        flag = True
        return flag, x_max-x_min+1
    return flag

def is_cube_all(net_act_seq):
    flag = False
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in net_act_seq if x.startswith("place")]
    max_x = max([t[0] for t in coords_list])
    min_x = min([t[0] for t in coords_list])
    max_z = max([t[2] for t in coords_list])
    min_z = min([t[2] for t in coords_list])
    max_y = max([t[1] for t in coords_list])
    # print(max_x)
    # print(min_x)
    # print(max_z)
    # print(min_z)
    # print(max_y)
    
    side_one = [(x,y,z) for x in range(min_x,max_x+1) for y in range(1,max_y+1) for z in [min_z]]
    side_two = [(x,y,z) for x in range(min_x,max_x+1) for y in range(1,max_y+1) for z in [max_z]]
    side_three = [(x,y,z) for x in [min_x] for y in range(1,max_y+1) for z in range(min_z, max_z+1)]
    side_four = [(x,y,z) for x in [max_x] for y in range(1,max_y+1) for z in range(min_z, max_z+1)]
    top = [(x,y,z) for x in range(min_x,max_x+1) for y in [max_y] for z in range(min_z, max_z+1)]

    construct = side_one + side_two + side_three + side_four + top

    #check if all construct blocks are contained in the construct
    subset = set(coords_list).intersection(set(construct))
    if len(subset) == len(set(construct)):
        #check out of bounds blocks in coords_list??
        flag = True
        return flag, max_x-min_x+1

    return flag
    
def is_row(net_act_seq):
    # For row, y will be constant and only one of x or z will vary make sure of contact.
    # If the pred seq is row, return True along with the size, else False
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in net_act_seq if x.startswith("place")]
    x_list = [a[0] for a in coords_list]
    y_list = [a[1] for a in coords_list]
    z_list = [a[2] for a in coords_list]
    flag = False
    if len(np.unique(y_list))==1 and len(np.unique(z_list))==1 and len(np.unique(x_list))>1:
        x_min, x_max = np.min(x_list), np.max(x_list)
        if np.array_equal(np.sort(x_list),np.array(range(x_min,x_max+1))):
            flag = True
            return flag, len(x_list)
    elif len(np.unique(y_list))==1 and len(np.unique(x_list))==1 and len(np.unique(z_list))>1:
        z_min, z_max = np.min(z_list), np.max(z_list)
        if np.array_equal(np.sort(z_list),np.array(range(z_min,z_max+1))):
            flag = True
            return flag, len(z_list)        
    return flag
      
def is_tower(net_act_seq):
    #NB we changed this to cound a single block as a tower.
    # For tower, we want x and z constant and only y to vary make sure of contact..
    # If the pred seq is tower, return True along with the size, else False
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in net_act_seq if x.startswith("place")]
    x_list = [a[0] for a in coords_list]
    y_list = [a[1] for a in coords_list]
    z_list = [a[2] for a in coords_list]
    flag = False
    if len(np.unique(x_list))==1 and len(np.unique(z_list))==1 and len(np.unique(y_list))>=1:
         if np.min(y_list)==1 and np.array_equal(np.sort(y_list),np.array(range(1,len(y_list)+1))):
             flag = True
             return flag, len(y_list)
    return flag
    
def get_location_list(net_act_seq):
    # check for corner, edge, centre
    # corner is x and z either -5 or 5
    # edge is one of x or z -5 or 5
    # center is both x and z equal to 0 
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in net_act_seq if x.startswith("place")]
    loc_l = []
    for (x,y,z) in coords_list:
        if np.abs(x)==5 and np.abs(z)==5:
            loc_l.append("corner")
        elif  np.abs(x)==5 or np.abs(z)==5:
            loc_l.append("edge")
        elif x==0 and z==0:
            loc_l.append("center") ##NB need to make sure this is the center block
        else:
            loc_l.append("none")
    return loc_l

def get_center_quads(net_act_seq, shape):
    """
    For diamonds, rectangles, squares
    check to see if center of shape is on center square
    """
    # check for corner, edge, centre
    # corner is x and z either -5 or 5
    # edge is one of x or z -5 or 5
    # center is both x and z equal to 0 
    # shapes = ['square', 'rectangle', 'diamond', 'cube]
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in net_act_seq if x.startswith("place")]
    loc_l = False
    #is dimension even or odd?
    max_x = max([t[0] for t in coords_list])
    min_x = min([t[0] for t in coords_list])
    max_z = max([t[2] for t in coords_list])
    min_z = min([t[2] for t in coords_list])
    
    if shape == 'diamond':
        max_x = max([t[0] for t in coords_list])
        min_x = min([t[0] for t in coords_list])
        if max_x + min_x == 0:
            loc_l = True
    if shape in ['square', 'cube']:
        if (max_x - min_x)%2 == 1:
            #then even 
            if max_x + min_x in [0, 1, -1] and max_z + min_z in [0, 1, -1]:
                loc_l = True
        elif max_x + min_x == 0 and max_z + min_z == 0:
                loc_l = True
    if shape == 'rectangle':
        xodd = False
        zodd = False
        if (max_x - min_x)%2 == 0: #then x side is odd
            xodd = True
        if (max_z - min_z)%2 == 0: #then z size is odd 
            zodd = True
        if xodd and not zodd:
            if max_x + min_x == 0 and max_z + min_z in [0, 1, -1]:
                loc_l = True
        elif not xodd and zodd:
            if max_x + min_x in [0, 1, -1] and max_z + min_z == 0:
                loc_l = True
        elif xodd and zodd:
            if max_x + min_x == 0 and max_z + min_z == 0:
                loc_l = True
        else: #both are even 
            if max_x + min_x in [0, 1, -1] and max_z + min_z in [0, 1, -1]:
                loc_l = True
    return loc_l
    
def get_orientation(net_act_seq):
    # If y is changing and either of x or z is constant, then vertical.
    # If y is constant then horizontal
    # Anything else, return "no fixed orientation"
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in net_act_seq if x.startswith("place")]
    #print(coords_list)
    x_list = [a[0] for a in coords_list]
    y_list = [a[1] for a in coords_list]
    z_list = [a[2] for a in coords_list]
    if len(np.unique(y_list))==1 and len(coords_list)>1:
        orientation = "horizontal"
    elif len(coords_list)>1 and ((len(np.unique(y_list))>1 and len(np.unique(x_list))==1) or (len(np.unique(y_list))>1 and len(np.unique(z_list))==1)):
        orientation = "vertical"
    else: 
        orientation = "none"
    return orientation
    
def get_color(net_act_seq):
    # Check if all the colors of place actions are same, and return that color. else, return list of all the colors.
    colors_l = [x.split(" ")[1] for x in net_act_seq if x.startswith("place")]
    return np.unique(colors_l)

def boundary_check(net_act_seq):
    in_bounds = 1
    coords_list = [(int(x.split(" ")[2]), int(x.split(" ")[3]), int(x.split(" ")[4]))  for x in net_act_seq if x.startswith("place")]
    max_x = max([t[0] for t in coords_list])
    min_x = min([t[0] for t in coords_list])
    max_z = max([t[2] for t in coords_list])
    min_z = min([t[2] for t in coords_list])
    min_y = min([t[1] for t in coords_list])
    if max_x > 5 or max_z > 5:
        in_bounds = 0
    if min_x < -5 or min_z < -5 or min_y < 1:
        in_bounds = 0
    return in_bounds
    
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

# if __name__=="__main__":
#     # act_seq = ['place red -4 3 1', 'place red -4 3 0', 'place red -4 3 -1', 'place red -3 3 1', 'place red -3 3 -1', 
#     #            'place red -2 3 1', 'place red -2 3 0', 'place red -2 3 -1']
#     # act_seq = ['place purple 5 1 -1', 'place purple 5 2 -1', 'place purple 5 3 -1', 'place purple 5 4 -1']
#     # act_seq = ['place purple 5 1 -1', 'place purple 5 1 0', 'place purple 5 1 1', 'place purple 5 2 -1', 'place purple 5 2 0', 
#     #            'place purple 5 2 1', 'place purple 5 3 -1', 'place purple 5 3 0', 'place purple 5 3 1', 'place purple 4 3 1',
#     #            'place purple 3 3 1', 'place purple 2 3 1', 'place purple 2 3 0', 'place purple 2 3 -1', 'place purple 3 3 -1',
#     #            'place purple 4 3 -1']S
#     act_seq = [
#               "place purple 1 1 1",
#             "place purple 0 1 1",
#             "place purple -1 1 1",
#             "place purple -1 1 0",
#             "place purple -1 1 -1",
#             "place purple 0 1 -1",
#             "place purple 1 1 -1",
#             "place purple 1 1 0"
#         ]
#     net_act_seq = get_net_sequence(act_seq)
#     #print(net_act_seq)
#     # l = is_rectangle_unfilled(net_act_seq)
#     # print(l)
#     # t = is_tower(net_act_seq)
#     # print(t)
#     # print('-------------------')
#     # cb = is_cube(net_act_seq)
#     # print(cb)
#     # print('-------------------')
#     # cu = is_cube_unfilled(net_act_seq)
#     # print(cu)
#     # print('-------------------')
#     # s = is_square(net_act_seq)
#     # print(s)
#     # print('--------------------------')
#     # su = is_square_unfilled(net_act_seq)
#     # print(su)
#     # print('--------------------------')
#     # cu = is_cube(net_act_seq)
#     # print(cu)
#     # print('--------------------------')
#     # cuu = is_cube_unfilled(net_act_seq)
#     # print(cuu)
#     # print('--------------------------')
#     # cua = is_cube_all(net_act_seq)
#     # print(cua)
#     # print('--------------------------')
#     # s = is_rectangle(net_act_seq)
#     # print(s)
#     # print('--------------------------')
#     # su = is_rectangle_unfilled(net_act_seq)
#     # print(su)
#     # print('--------------------------')
#     print('--------------------------')
#     di = is_diamond(net_act_seq)
#     print(di)
#     print('--------------------------')
#     c = get_color(net_act_seq)
#     print(c)
#     print('-------------------------')
#     o = get_orientation(net_act_seq)
#     print(o)
#     print('-------------------------------')
#     loc = get_location_list(net_act_seq)
#     print(loc)
#     cent = get_center_quads(net_act_seq, 'diamond')
#     print(cent)
#     print('-------------------------------')



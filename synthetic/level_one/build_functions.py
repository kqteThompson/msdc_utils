# from functions import get_net_sequence, is_tower, is_cube, is_square, is_rectangle, is_row, is_diagonal, is_diamond
# import json
# import re
import numpy as np

def tower(color, size, orientation, location):
    act_seq = []
    assert orientation==None
    if location=="centre":
        start = "0 1 0"
        start_x, start_y, start_z = start.split(" ")
    elif location=="corner":
        start = ["5 1 5", "5 1 -5", "-5 1 5", "-5 1 -5"][np.random.randint(4)]
        start_x, start_y, start_z = start.split(" ")
    elif location=="edge":
        start_y = "1"
        if np.random.randint(2)==0:
            start_x=["-5", "5"][np.random.randint(2)]
            start_z=str(np.random.randint(-5,6))
        else:
            start_z=["-5", "5"][np.random.randint(2)]
            start_x=str(np.random.randint(-5,6))
        start = start_x + " " + start_y + " " + start_z
    else:
        start_y = "1"
        start_x=str(np.random.randint(-5,6))
        start_z=str(np.random.randint(-5,6))
        start = start_x + " " + start_y + " " + start_z
    act_seq.append(f"place {color} {start}")
    for i in range(size-1):
        start_y = str(int(start_y)+1)
        start = start_x + " " + start_y + " " + start_z
        act_seq.append(f"place {color} {start}")
    return act_seq
    
def row(color, size, orientation, location):
    act_seq = []
    assert orientation==None
    if location=="centre":
        start_y = "1"
        # since it's row at centre, one of x or z will be always 0, we chose which one
        if np.random.randint(2)==0:
            start_x = "0"
            start_z = str(np.random.randint(-1*size+1,1))
            start = start_x + " " + start_y + " " + start_z
            act_seq.append(f"place {color} {start}")
            for i in range(size-1):
                start_z = str(int(start_z)+1)
                start = start_x + " " + start_y + " " + start_z
                act_seq.append(f"place {color} {start}")
        else:
            start_z = "0"
            start_x = str(np.random.randint(-1*size+1,1))
            start = start_x + " " + start_y + " " + start_z
            act_seq.append(f"place {color} {start}")
            for i in range(size-1):
                start_x = str(int(start_x)+1)
                start = start_x + " " + start_y + " " + start_z
                act_seq.append(f"place {color} {start}")
    elif location=="corner":
        start = ["5 1 5", "5 1 -5", "-5 1 5", "-5 1 -5"][np.random.randint(4)]
        start_x, start_y, start_z = start.split(" ")
        act_seq.append(f"place {color} {start}")  
        if start=="5 1 5" or start=="-5 1 5":
            for i in range(size-1):
                start_z = str(int(start_z)-1)
                start = start_x + " " + start_y + " " + start_z
                act_seq.append(f"place {color} {start}")
        elif start=="5 1 -5":
            for i in range(size-1):
                start_x = str(int(start_x)-1)
                start = start_x + " " + start_y + " " + start_z
                act_seq.append(f"place {color} {start}")
        else:
            for i in range(size-1):
                start_x = str(int(start_x)+1)
                start = start_x + " " + start_y + " " + start_z
                act_seq.append(f"place {color} {start}")
    elif location=="edge":
        start_y = "1"
        if np.random.randint(2)==0:
            start_x=["-5", "5"][np.random.randint(2)]
            start_z=str(np.random.randint(-4,6-size))
        else:
            start_z=["-5", "5"][np.random.randint(2)]
            start_x=str(np.random.randint(-4,6-size))
        start = start_x + " " + start_y + " " + start_z
    else:
        start_y = "1"
        start_x=str(np.random.randint(-4,6-size))
        start_z=str(np.random.randint(-4,6-size))
        start = start_x + " " + start_y + " " + start_z
    if len(act_seq)==0:
        act_seq.append(f"place {color} {start}")       
        if np.abs(int(start_x))==5 or np.abs(int(start_z))==5:
            if np.abs(int(start_x))<5:
                for i in range(size-1):
                    start_x = str(int(start_x)+1)
                    start = start_x + " " + start_y + " " + start_z
                    act_seq.append(f"place {color} {start}")
            elif np.abs(int(start_z))<5:
                for i in range(size-1):
                    start_z = str(int(start_z)+1)
                    start = start_x + " " + start_y + " " + start_z
                    act_seq.append(f"place {color} {start}")
        else:
            for i in range(size-1):
                start_x = str(int(start_x)+1)
                start = start_x + " " + start_y + " " + start_z
                act_seq.append(f"place {color} {start}")
    return act_seq

def diagonal(color, size, orientation, location):
    act_seq = []
    assert orientation==None
    if location=="centre":
        start_y = "1"
        # since it's diagonal at centre, x and z could both increase or z could decrease and x increase
        if np.random.randint(2)==0:
            start_z = str(np.random.randint(-1*size+1,1))
            start_x = start_z
            start = start_x + " " + start_y + " " + start_z
            act_seq.append(f"place {color} {start}")
            for i in range(size-1):
                start_z = str(int(start_z)+1)
                start_x = start_z
                start = start_x + " " + start_y + " " + start_z
                act_seq.append(f"place {color} {start}")
        else:
            start_z = str(np.random.randint(0,size+1))
            start_x = str(-1*int(start_z))
            start = start_x + " " + start_y + " " + start_z
            act_seq.append(f"place {color} {start}")
            for i in range(size-1):
                start_z = str(int(start_z)-1)
                start_x = str(-1*int(start_z))
                start = start_x + " " + start_y + " " + start_z
                act_seq.append(f"place {color} {start}")
    elif location=="corner":
        start = ["5 1 5", "5 1 -5", "-5 1 5", "-5 1 -5"][np.random.randint(4)]
        start_x_init, start_y_init, start_z_init = start.split(" ")
        start_x = start_x_init
        start_y = start_y_init
        start_z = start_z_init
        act_seq.append(f"place {color} {start}")  
        for i in range(size-1):
            if start_x_init=="5":
                start_x = str(int(start_x)-1)
            else:
                start_x = str(int(start_x)+1)
            if start_z_init=="5":
                start_z = str(int(start_z)-1)
            else:
                start_z = str(int(start_z)+1)
            start = start_x + " " + start_y + " " + start_z
            act_seq.append(f"place {color} {start}")
    elif location=="edge":
        start_y = "1"
        if np.random.randint(2)==0:
            start_x=["-5", "5"][np.random.randint(2)]
            start_z=str(np.random.randint(-4,6-size))
        else:
            start_z=["-5", "5"][np.random.randint(2)]
            start_x=str(np.random.randint(-4,6-size))
        start = start_x + " " + start_y + " " + start_z
        start_x_init, start_y_init, start_z_init = start.split(" ")
        start_x = start_x_init
        start_y = start_y_init
        start_z = start_z_init
        act_seq.append(f"place {color} {start}")  
        for i in range(size-1):
            if start_x_init=="5":
                start_x = str(int(start_x)-1)
                start_z = str(int(start_z)+1)
            elif start_x_init=="-5":
                start_x = str(int(start_x)+1)
                start_z = str(int(start_z)+1)
            if start_z_init=="5":
                start_z = str(int(start_z)-1)
                start_x = str(int(start_x)+1)
            elif start_z_init=="-5":
                start_z = str(int(start_z)+1)
                start_x = str(int(start_x)+1)
            start = start_x + " " + start_y + " " + start_z
            act_seq.append(f"place {color} {start}")
    else:
        start_y = "1"
        start_x=str(np.random.randint(-5,6-size))
        start_z=str(np.random.randint(-5,6-size))
        start = start_x + " " + start_y + " " + start_z
        start_x_init, start_y_init, start_z_init = start.split(" ")
        start_x = start_x_init
        start_y = start_y_init
        start_z = start_z_init
        act_seq.append(f"place {color} {start}")  
        for i in range(size-1):
            start_x = str(int(start_x)+1)
            start_z = str(int(start_z)+1)
            start = start_x + " " + start_y + " " + start_z
            act_seq.append(f"place {color} {start}")
    return act_seq

def cube(color, size, orientation, location):
    act_seq = []
    assert orientation==None
    assert size==3
    if location=="centre":
        x_min, y_min, z_min = -1,1,-1
        x_max, y_max, z_max = 1,3,1
        for x in range(x_min,x_max+1):
            for y in range(y_min,y_max+1):
                for z in range(z_min,z_max+1):
                    start = str(x) + " " + str(y) + " " + str(z)
                    act_seq.append(f"place {color} {start}")
    elif location=="corner":
        start = ["5 1 5", "5 1 -5", "-5 1 5", "-5 1 -5"][np.random.randint(4)]
        y_min, y_max = 1, 3
        start_x, start_y, start_z = start.split(" ")
        if start_x=="5":
            x_min, x_max = 3, 5
        else:
            x_min, x_max = -5, -3
        if start_z=="5":
            z_min, z_max = 3, 5
        else:
            z_min, z_max = -5, -3
        for x in range(x_min,x_max+1):
            for y in range(y_min,y_max+1):
                for z in range(z_min,z_max+1):
                    start = str(x) + " " + str(y) + " " + str(z)
                    act_seq.append(f"place {color} {start}")
    elif location=="edge":
        y_min, y_max = 1, 3
        if np.random.randint(2)==0:
            start_x=["-5", "5"][np.random.randint(2)]
            z_min = np.random.randint(-4,6-size)
            z_max = z_min+2
            if start_x=="5":
                x_min, x_max = 3, 5
            else:
                x_min, x_max = -5, -3
        else:
            start_z=["-5", "5"][np.random.randint(2)]
            x_min = np.random.randint(-4,6-size)
            x_max = x_min+2
            if start_z=="5":
                z_min, z_max = 3, 5
            else:
                z_min, z_max = -5, -3
        for x in range(x_min,x_max+1):
            for y in range(y_min,y_max+1):
                for z in range(z_min,z_max+1):
                    start = str(x) + " " + str(y) + " " + str(z)
                    act_seq.append(f"place {color} {start}") 
    else:
        y_min, y_max = 1, 3
        x_min = np.random.randint(-5,6-size)
        x_max = x_min+2
        z_min = np.random.randint(-5,6-size) 
        z_max = z_min+2
        for x in range(x_min,x_max+1):
            for y in range(y_min,y_max+1):
                for z in range(z_min,z_max+1):
                    start = str(x) + " " + str(y) + " " + str(z)
                    act_seq.append(f"place {color} {start}")  
    return act_seq

def square(color, size, orientation, location):
    act_seq = []
    if orientation==None:
        orientation="horizontal"
    if orientation=="horizontal":
        if location=="centre":
            if size%2:
                x_min, x_max = int(-1*(size-1)/2), int((size-1)/2)
                z_min, z_max = x_min, x_max
            else:
                x_min, x_max = int(-1*size/2), int(size/2 - 1)
                z_min, z_max = x_min, x_max
            for x in range(x_min,x_max+1):
                for z in range(z_min,z_max+1):
                    start = str(x) + " " + "1" + " " + str(z)
                    act_seq.append(f"place {color} {start}")  
        elif location=="corner":
            start = ["5 1 5", "5 1 -5", "-5 1 5", "-5 1 -5"][np.random.randint(4)]
            start_x_init, start_y_init, start_z_init = start.split(" ")
            start_x = start_x_init
            start_y = start_y_init
            start_z = start_z_init
            if start_x=="5":
                x_min, x_max = 5-size+1, 5
            else:
                x_min, x_max = -5, -5+size-1
            if start_z=="5":
                z_min, z_max = 5-size+1, 5
            else:
                z_min, z_max = -5, -5+size-1
            for x in range(x_min,x_max+1):
                for z in range(z_min,z_max+1):
                    start = str(x) + " " + "1" + " " + str(z)
                    act_seq.append(f"place {color} {start}")
        elif location=="edge":
            if np.random.randint(2)==0:
                start_x=["-5", "5"][np.random.randint(2)]
                z_min = np.random.randint(-4,6-size)
                z_max = z_min + size - 1
                if start_x=="5":
                    x_min, x_max = 5-size+1, 5
                else:
                    x_min, x_max = -5, -5+size-1
            else:
                start_z=["-5", "5"][np.random.randint(2)]
                x_min = np.random.randint(-4,6-size)
                x_max = x_min + size - 1
                if start_z=="5":
                    z_min, z_max = 5-size+1, 5
                else:
                    z_min, z_max = -5, -5+size-1
            for x in range(x_min,x_max+1):
                for z in range(z_min,z_max+1):
                    start = str(x) + " " + "1" + " " + str(z)
                    act_seq.append(f"place {color} {start}")
        else:
            x_min = np.random.randint(-4,6-size)    
            z_min = np.random.randint(-4,6-size) 
            x_max, z_max = x_min + size - 1, z_min + size - 1
            for x in range(x_min,x_max+1):
                for z in range(z_min,z_max+1):
                    start = str(x) + " " + "1" + " " + str(z)
                    act_seq.append(f"place {color} {start}")
    if orientation=="vertical":
        if location=="centre":
            x = 0
            if size%2:
                z_min, z_max = int(-1*(size-1)/2), int((size-1)/2)
                y_min, y_max = 1, size
            else:
                z_min, z_max = int(-1*size/2), int(size/2 - 1)
                y_min, y_max = 1, size
            for y in range(y_min,y_max+1):
                for z in range(z_min,z_max+1):
                    start = str(x) + " " + str(y) + " " + str(z)
                    act_seq.append(f"place {color} {start}")  
        elif location=="corner":
            start = ["5 1 5", "5 1 -5", "-5 1 5", "-5 1 -5"][np.random.randint(4)]
            start_x_init, start_y_init, start_z_init = start.split(" ")
            start_x = start_x_init
            start_y = start_y_init
            start_z = start_z_init
            x = start_x_init
            y_min, y_max = 1, size
            if start_z=="5":
                z_min, z_max = 5-size+1, 5
            else:
                z_min, z_max = -5, -5+size-1
            for y in range(y_min,y_max+1):
                for z in range(z_min,z_max+1):
                    start = str(x) + " " + str(y) + " " + str(z)
                    act_seq.append(f"place {color} {start}")
        elif location=="edge":
            if np.random.randint(2)==0:
                start_x=["-5", "5"][np.random.randint(2)]
                z_min = np.random.randint(-4,6-size)
                z_max = z_min + size - 1
                y_min, y_max = 1, size
                x = start_x
                for y in range(y_min,y_max+1):
                    for z in range(z_min,z_max+1):
                        start = str(x) + " " + str(y) + " " + str(z)
                        act_seq.append(f"place {color} {start}")
            else:
                start_z=["-5", "5"][np.random.randint(2)]
                x_min = np.random.randint(-4,6-size)
                x_max = x_min + size - 1
                y_min, y_max = 1, size
                z = start_z
                for x in range(x_min,x_max+1):
                    for y in range(y_min,y_max+1):
                        start = str(x) + " " + str(y) + " " + str(z)
                        act_seq.append(f"place {color} {start}")
        else:
            x = np.random.randint(-4,5)    
            z_min = np.random.randint(-4,6-size) 
            z_max = z_min + size - 1
            y_min, y_max = 1, size
            for y in range(y_min,y_max+1):
                for z in range(z_min,z_max+1):
                    start = str(x) + " " + str(y) + " " + str(z)
                    act_seq.append(f"place {color} {start}")
    return act_seq

def rectangle(color, size, orientation, location):
    act_seq = []
    assert len(size)==2
    if orientation==None:
        orientation="horizontal"
    if orientation=="horizontal":
        if location=="centre":
            if size[0]%2:
                x_min, x_max = int(-1*(size[0]-1)/2), int((size[0]-1)/2)
            else:
                x_min, x_max = int(-1*size[0]/2), int(size[0]/2 - 1)
            if size[1]%2:
                z_min, z_max = int(-1*(size[1]-1)/2), int((size[1]-1)/2)
            else:
                z_min, z_max = int(-1*size[1]/2), int(size[1]/2 - 1)
            for x in range(x_min,x_max+1):
                for z in range(z_min,z_max+1):
                    start = str(x) + " " + "1" + " " + str(z)
                    act_seq.append(f"place {color} {start}")  
        elif location=="corner":
            start = ["5 1 5", "5 1 -5", "-5 1 5", "-5 1 -5"][np.random.randint(4)]
            start_x_init, start_y_init, start_z_init = start.split(" ")
            start_x = start_x_init
            start_y = start_y_init
            start_z = start_z_init
            if start_x=="5":
                x_min, x_max = 5-size[0]+1, 5
            else:
                x_min, x_max = -5, -5+size[0]-1
            if start_z=="5":
                z_min, z_max = 5-size[1]+1, 5
            else:
                z_min, z_max = -5, -5+size[1]-1
            for x in range(x_min,x_max+1):
                for z in range(z_min,z_max+1):
                    start = str(x) + " " + "1" + " " + str(z)
                    act_seq.append(f"place {color} {start}")
        elif location=="edge":
            if np.random.randint(2)==0:
                start_x=["-5", "5"][np.random.randint(2)]
                z_min = np.random.randint(-4,6-size[1])
                z_max = z_min + size[1] - 1
                if start_x=="5":
                    x_min, x_max = 5-size[0]+1, 5
                else:
                    x_min, x_max = -5, -5+size[0]-1
            else:
                start_z=["-5", "5"][np.random.randint(2)]
                x_min = np.random.randint(-4,6-size[0])
                x_max = x_min + size[0] - 1
                if start_z=="5":
                    z_min, z_max = 5-size[1]+1, 5
                else:
                    z_min, z_max = -5, -5+size[1]-1
            for x in range(x_min,x_max+1):
                for z in range(z_min,z_max+1):
                    start = str(x) + " " + "1" + " " + str(z)
                    act_seq.append(f"place {color} {start}")
        else:
            x_min = np.random.randint(-4,6-size[0])    
            z_min = np.random.randint(-4,6-size[1]) 
            x_max, z_max = x_min + size[0] - 1, z_min + size[1] - 1
            for x in range(x_min,x_max+1):
                for z in range(z_min,z_max+1):
                    start = str(x) + " " + "1" + " " + str(z)
                    act_seq.append(f"place {color} {start}")
    if orientation=="vertical":
        if location=="centre":
            x = 0
            y_min, y_max = 1, size[1]
            if size[0]%2:
                z_min, z_max = int(-1*(size[0]-1)/2), int((size[0]-1)/2)                
            else:
                z_min, z_max = int(-1*size[0]/2), int(size[0]/2 - 1)
            for y in range(y_min,y_max+1):
                for z in range(z_min,z_max+1):
                    start = str(x) + " " + str(y) + " " + str(z)
                    act_seq.append(f"place {color} {start}")  
        elif location=="corner":
            start = ["5 1 5", "5 1 -5", "-5 1 5", "-5 1 -5"][np.random.randint(4)]
            start_x_init, start_y_init, start_z_init = start.split(" ")
            start_x = start_x_init
            start_y = start_y_init
            start_z = start_z_init
            x = start_x_init
            y_min, y_max = 1, size[1]
            if start_z=="5":
                z_min, z_max = 5-size[0]+1, 5
            else:
                z_min, z_max = -5, -5+size[0]-1
            for y in range(y_min,y_max+1):
                for z in range(z_min,z_max+1):
                    start = str(x) + " " + str(y) + " " + str(z)
                    act_seq.append(f"place {color} {start}")
        elif location=="edge":
            if np.random.randint(2)==0:
                start_x=["-5", "5"][np.random.randint(2)]
                z_min = np.random.randint(-4,6-size[0])
                z_max = z_min + size[0] - 1
                y_min, y_max = 1, size[1]
                x = start_x
                for y in range(y_min,y_max+1):
                    for z in range(z_min,z_max+1):
                        start = str(x) + " " + str(y) + " " + str(z)
                        act_seq.append(f"place {color} {start}")
            else:
                start_z=["-5", "5"][np.random.randint(2)]
                x_min = np.random.randint(-4,6-size[0])
                x_max = x_min + size[0] - 1
                y_min, y_max = 1, size[1]
                z = start_z
                for x in range(x_min,x_max+1):
                    for y in range(y_min,y_max+1):
                        start = str(x) + " " + str(y) + " " + str(z)
                        act_seq.append(f"place {color} {start}")
        else:
            x = np.random.randint(-4,5)    
            z_min = np.random.randint(-4,6-size[0]) 
            z_max = z_min + size[0] - 1
            y_min, y_max = 1, size[1]
            for y in range(y_min,y_max+1):
                for z in range(z_min,z_max+1):
                    start = str(x) + " " + str(y) + " " + str(z)
                    act_seq.append(f"place {color} {start}")
    return act_seq

def diamond(color, size, orientation, location):
    act_seq = []
    assert location==None
    if orientation==None:
        orientation="horizontal"
    if orientation=="horizontal":
        x_min, x_max = -1*size + 1, size-1
        z_min, z_max = x_min, x_max
        x_mid, z_mid = 0, 0
        for (x,z) in zip(range(x_mid,x_max+1),range(z_min,z_mid+1)):
            start = str(x) + " " + "1" + " " + str(z)
            if f"place {color} {start}" not in act_seq:
                act_seq.append(f"place {color} {start}")
        for (x,z) in  zip(range(x_mid,x_max+1),range(z_max,z_mid-1,-1)):
            start = str(x) + " " + "1" + " " + str(z)
            if f"place {color} {start}" not in act_seq:
                act_seq.append(f"place {color} {start}")
        for (x,z) in zip(range(x_min,x_mid+1),range(z_mid,z_max+1)):
            start = str(x) + " " + "1" + " " + str(z)
            if f"place {color} {start}" not in act_seq:
                act_seq.append(f"place {color} {start}")            
        for (x,z) in zip(range(x_min,x_mid+1),range(z_mid,z_min-1,-1)):
            start = str(x) + " " + "1" + " " + str(z)
            if f"place {color} {start}" not in act_seq:
                act_seq.append(f"place {color} {start}")
        return act_seq
    if orientation=="vertical":
        x = 0
        y_min, y_max = 1, 2*size-1
        z_min, z_max = -1*size + 1, size-1
        y_mid, z_mid = (y_max+y_min)/2, (z_max+z_min)/2
        y_mid, z_mid = int(y_mid), int(z_mid)
        for (y,z) in zip(range(y_min,y_mid+1),range(z_mid,z_max+1)):
            start = str(x) + " " + str(y) + " " + str(z)
            y_fin = y
            if f"place {color} {start}" not in act_seq:
                while f"place {color} {start}" not in act_seq and y>1:
                    y-=1
                    start = str(x) + " " + str(y) + " " + str(z)
                if f"place {color} {start}" in act_seq:
                    y+=1
                for y_coord in range(y,y_fin+1):
                    start = str(x) + " " + str(y_coord) + " " + str(z)
                    act_seq.append(f"place {color} {start}")
                for y_coord in range(y_fin-1,y-1,-1):
                    start = str(x) + " " + str(y_coord) + " " + str(z)
                    act_seq.append(f"pick {start}")          
        for (y,z) in zip(range(y_min,y_mid+1),range(z_mid,z_min-1,-1)):
            start = str(x) + " " + str(y) + " " + str(z)
            y_fin = y
            if f"place {color} {start}" not in act_seq:
                while f"place {color} {start}" not in act_seq and y>1:
                    y-=1
                    start = str(x) + " " + str(y) + " " + str(z)
                if f"place {color} {start}" in act_seq:
                    y+=1
                for y_coord in range(y,y_fin+1):
                    start = str(x) + " " + str(y_coord) + " " + str(z)
                    act_seq.append(f"place {color} {start}")
                for y_coord in range(y_fin-1,y-1,-1):
                    start = str(x) + " " + str(y_coord) + " " + str(z)
                    act_seq.append(f"pick {start}")
        for (y,z) in zip(range(y_mid,y_max+1),range(z_min,z_mid+1)):
            start = str(x) + " " + str(y) + " " + str(z)
            y_fin = y
            if f"place {color} {start}" not in act_seq:
                while f"place {color} {start}" not in act_seq and y>1:
                    y-=1
                    start = str(x) + " " + str(y) + " " + str(z)
                if f"place {color} {start}" in act_seq:
                    y+=1
                for y_coord in range(y,y_fin+1):
                    start = str(x) + " " + str(y_coord) + " " + str(z)
                    act_seq.append(f"place {color} {start}")
                for y_coord in range(y_fin-1,y-1,-1):
                    start = str(x) + " " + str(y_coord) + " " + str(z)
                    act_seq.append(f"pick {start}")
        for (y,z) in  zip(range(y_mid,y_max+1),range(z_max,z_mid-1,-1)):
            start = str(x) + " " + str(y) + " " + str(z)
            y_fin = y
            if f"place {color} {start}" not in act_seq:
                while f"place {color} {start}" not in act_seq and y>1:
                    y-=1
                    start = str(x) + " " + str(y) + " " + str(z)
                if f"place {color} {start}" in act_seq:
                    y+=1
                for y_coord in range(y,y_fin+1):
                    start = str(x) + " " + str(y_coord) + " " + str(z)
                    act_seq.append(f"place {color} {start}")
                for y_coord in range(y_fin-1,y-1,-1):
                    start = str(x) + " " + str(y_coord) + " " + str(z)
                    act_seq.append(f"pick {start}")
        return act_seq   


# S = {"square", "row", "rectangle", "tower", "diagonal", "diamond", "cube"}
# C = {"orange", "red", "green", "blue", "purple", "yellow"}
# #data = json.load(open("level-one-synth-data-new.json"))
# data = ['3 orange horizontal square centre', '4 orange horizontal square centre', '5 orange horizontal square centre']

# for i in range(len(data)):
#     print(i)
#     for s in S:
#         if s in data[str(i)]:
#             structure = s
#             if s=="rectangle":
#                 size = "x".join(re.findall("\d+",data[str(i)]))
#             elif s=="diamond" and "spaces long" in data[str(i)]:
#                 size = (int(re.findall("\d+",data[str(i)])[0])+1)/2
#             else:
#                 size = re.findall("\d+",data[str(i)])[0]
#             if len(re.findall("horizontal|vertical",data[str(i)]))>0:
#                 orientation = re.findall("horizontal|vertical",data[str(i)])[0]
#             else:
#                 orientation = None
#             if len(re.findall("corner|edge|centre",data[str(i)]))>0:
#                 location = re.findall("corner|edge|centre",data[str(i)])[0]
#             else:
#                 location = None
#             for c in C:
#                 if c in data[str(i)]:
#                     color = c
#     #print(data[str(i)],structure, color, size, orientation, location)
#     if structure=="tower":
#         size=int(size)
#         act_seq = tower(color, size, orientation, location)
#         assert is_tower(get_net_sequence(act_seq))[0]
#         assert is_tower(get_net_sequence(act_seq))[1]==size
#     elif structure=="row":
#         size=int(size)
#         act_seq = row(color, size, orientation, location)
#         assert is_row(get_net_sequence(act_seq))[0]
#         assert is_row(get_net_sequence(act_seq))[1]==size
#     elif structure=="square":
#         size=int(size)
#         act_seq = square(color, size, orientation, location)
#         assert is_square(get_net_sequence(act_seq))[0]
#         assert is_square(get_net_sequence(act_seq))[1]==size
#     elif structure=="rectangle":
#         size = [int(a) for a in size.split("x")]
#         act_seq = rectangle(color, size, orientation, location)
#         assert is_rectangle(get_net_sequence(act_seq))[0]
#         assert (is_rectangle(get_net_sequence(act_seq))[1][0]==size[0] and is_rectangle(get_net_sequence(act_seq))[1][1]==size[1]) or (is_rectangle(get_net_sequence(act_seq))[1][1]==size[0] and is_rectangle(get_net_sequence(act_seq))[1][0]==size[1])
#     elif structure=="cube":
#         size=int(size)
#         act_seq = cube(color, size, orientation, location)
#         assert is_cube(get_net_sequence(act_seq))[0]
#         assert is_cube(get_net_sequence(act_seq))[1]==size
#     elif structure=="diagonal":
#         size=int(size)
#         act_seq = diagonal(color, size, orientation, location)
#         assert is_diagonal(get_net_sequence(act_seq))[0]
#         assert is_diagonal(get_net_sequence(act_seq))[1]==size
#     elif structure=="diamond":
#         size=int(size)
#         act_seq = diamond(color, size, orientation, location)
#         assert is_diamond(get_net_sequence(act_seq))[0]
#         assert is_diamond(get_net_sequence(act_seq))[1]==size
#     print(act_seq)
#     print('-------------')
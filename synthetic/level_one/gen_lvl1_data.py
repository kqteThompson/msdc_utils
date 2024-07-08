import json
import numpy as np
S = {"square", "row", "rectangle", "tower", "diagonal", "diamond", "cube"}
L = {"centre", "edge", "corner", ""}
C = {"orange", "red", "green", "blue", "purple", "yellow"}
O = {"horizontal", "vertical",""}
l = []
l_cov = []
for orient in O:
    for col in C:
        for loc in L:
            for shape in S:
                for size in range(3,10):
                    if shape in ["row","diagonal"] and loc=="centre" and f"{shape} {size} {col} {loc}" not in l_cov:
                        l_cov.append(f"{shape} {size} {col} {loc}")
                        l.append(f"Build a {shape} of {size} {col} blocks passing through the {loc}.".replace("  "," "))
                    elif shape in ["row","diagonal"] and f"{shape} {size} {col} {loc}" not in l_cov:
                        l_cov.append(f"{shape} {size} {col} {loc}")
                        if loc=="":
                            l.append(f"Build a {shape} of {size} {col} blocks.".replace("  "," "))
                        else:
                            l.append(f"Build a {shape} of {size} {col} blocks at the {loc}.".replace("  "," "))
                    elif shape=="square" and f"{size} {col} {orient} {shape} {loc}" not in l_cov:
                        if size>5:
                            continue
                        l_cov.append(f"{size} {col} {orient} {shape} {loc}")
                        if loc=="":
                            l.append(f"Build a {size}x{size} {col} {orient} {shape}.".replace("  "," "))
                        else:
                            l.append(f"Build a {size}x{size} {col} {orient} {shape} at the {loc}.".replace("  "," "))
                    elif shape=="cube" and f"{size} {col} {shape} {loc}" not in l_cov:
                        if size>3:
                            continue
                        l_cov.append(f"{size} {col} {shape} {loc}")
                        if loc=="":
                            l.append(f"Build a {size}x{size}x{size} {col} {shape}.".replace("  "," "))
                        else:
                            l.append(f"Build a {size}x{size}x{size} {col} {shape} at the {loc}.".replace("  "," "))
                    elif shape=="rectangle":
                        if size==3:
                            up_lim = 10
                        if size==4:
                            up_lim = 8
                        if size>4:
                            continue
                        r = np.random.randint(size+1,up_lim)
                        if f"{r} {size} {col} {orient} {shape} {loc}" not in l_cov:
                            l_cov.append(f"{r} {size} {col} {orient} {shape} {loc}")
                            if loc=="":
                                l.append(f"Build a {r}x{size} {col} {orient} {shape}.".replace("  "," "))
                            else:
                                l.append(f"Build a {r}x{size} {col} {orient} {shape} at the {loc}.".replace("  "," "))
                    elif shape=="diamond" and f"{col} {orient} {shape} {size}" not in l_cov:
                        if size>6:
                            continue
                        l_cov.append(f"{col} {orient} {shape} {size}")
                        if col=="orange":
                            l.append(f"Build an {col} {orient} {shape} with {size} blocks on a side.".replace("  "," "))
                            l.append(f"Build an {col} {orient} {shape} with axes {2*size-1} spaces long.".replace("  "," "))
                        else:
                            l.append(f"Build a {col} {orient} {shape} with {size} blocks on a side.".replace("  "," "))
                            l.append(f"Build a {col} {orient} {shape} with axes {2*size-1} spaces long.".replace("  "," "))
                    elif shape=="tower" and f"{col} {orient} {shape} {size} {loc}" not in l_cov:
                        l_cov.append(f"{col} {shape} {size} {loc}")
                        if col=="orange":
                            if loc=="":
                                l.append(f"Build an {col} {shape} of size {size}.".replace("  "," "))
                            else:
                                l.append(f"Build an {col} {shape} of size {size} at the {loc}.".replace("  "," "))
                        else:
                            if loc=="":
                                l.append(f"Build a {col} {shape} of size {size}.".replace("  "," "))
                            else:
                                l.append(f"Build a {col} {shape} of size {size} at the {loc}.".replace("  "," "))


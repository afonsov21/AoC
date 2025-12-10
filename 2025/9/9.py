import pandas as pd
import numpy as np
import itertools
file = 'input.txt' 
df = pd.read_csv(file, header=None)

# points = df.dropna().values.tolist()

# print(f"Loaded {len(points)} red tiles.")

# max_area = 0
# best_pair = None
# for p1, p2 in itertools.combinations(points, 2):
#     x1, y1 = p1
#     x2, y2 = p2

#     width = abs(x1 - x2) + 1
#     height = abs(y1 - y2) + 1
    
#     area = width * height

#     if area > max_area:
#         max_area = area
#         best_pair = (p1, p2)

# if best_pair is not None:
#     print(f"Largest Area: {max_area}")
#     print(f"Corners used: {best_pair[0]} and {best_pair[1]}")
# else:
#     print("Could not find any pairs. Check if the input file is empty or formatted correctly.")
#=========EX1 END========

def solve_constrained_rectangle(file_path):

    df = pd.read_csv(file_path, header=None)
    points = df.dropna().values.tolist()
    edges = []
    num_points = len(points)
    for i in range(num_points):
        p1 = points[i]
        p2 = points[(i + 1) % num_points] 
        edges.append((p1, p2))

    max_area = 0
    best_pair = None

    for p1, p2 in itertools.combinations(points, 2):
        x1, y1 = p1
        x2, y2 = p2
       
        width = abs(x1 - x2) + 1
        height = abs(y1 - y2) + 1
        area = width * height

     
        if area <= max_area:
            continue


        rx_min, rx_max = min(x1, x2), max(x1, x2)
        ry_min, ry_max = min(y1, y2), max(y1, y2)

        is_valid = True
        for ep1, ep2 in edges:
            ex1, ey1 = ep1
            ex2, ey2 = ep2
            
            if ex1 == ex2:
                if rx_min < ex1 < rx_max:
                    if max(ry_min, min(ey1, ey2)) < min(ry_max, max(ey1, ey2)):
                        is_valid = False
                        break

            else: 
                if ry_min < ey1 < ry_max:
                    if max(rx_min, min(ex1, ex2)) < min(rx_max, max(ex1, ex2)):
                        is_valid = False
                        break
        
        if not is_valid:
            continue

        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
    
        intersections = 0
        for ep1, ep2 in edges:
            ex1, ey1 = ep1
            ex2, ey2 = ep2
            
            if ex1 == ex2: 
                if min(ey1, ey2) <= cy < max(ey1, ey2):
                    if ex1 > cx:
                        intersections += 1
        if intersections % 2 == 0:
            is_valid = False

        if is_valid:
            max_area = area
            best_pair = (p1, p2)

    return max_area, best_pair


area, corners = solve_constrained_rectangle(file)
print(f"Largest Area: {area}")
if corners:
    print(f"Corners: {corners[0]} and {corners[1]}")
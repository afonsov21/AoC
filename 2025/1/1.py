import numpy as np

file = "input.txt"
pos = 50  
size = 100
total_zeros = 0

with open(file, 'r') as f:
    data = [line.strip() for line in f if line.strip()]

print(f"Starting Position: {pos}")
for curr in data:
    direction = curr[0]
    dist = int(curr[1:])
    
    hits_this_turn = 0
    
    if direction == "R":
        end = pos + dist
        
        hits_this_turn = (end // size) - (pos // size)
        pos = end % size

    else: 
        end = pos - dist
        hits_this_turn = ((pos - 1) // size) - ((end - 1) // size)
        pos = end % size

    total_zeros += hits_this_turn

print(f"Final Password (Total Zero Hits): {total_zeros}")
import pandas as pd
from collections import defaultdict
filename = "input.txt"
with open(filename, 'r') as file:
    lines = file.read()
    lines = lines.split('\n')

# active_beams = set()
# for r, line in enumerate(lines):
#     if 'S' in line:
#         active_beams.add(line.index('S'))
#         start_row = r
#         break

# total_splits = 0

# for r in range(start_row + 1, len(lines)):
#     line = lines[r]
#     next_beams = set()
    
#     for col in active_beams:
#         if 0 <= col < len(line):
#             char = line[col]
            
#             if char == '^':
#                 total_splits += 1
#                 next_beams.add(col - 1) # Left
#                 next_beams.add(col + 1) # Right
#             else:
#                 next_beams.add(col)
                
#     active_beams = next_beams

# print(f"Total times the beam splits: {total_splits}")
#==========END EX1=============
timeline_counts = defaultdict(int)
for r, line in enumerate(lines):
    if 'S' in line:
        timeline_counts[(r, line.index('S'))] = 1
        start_row = r
        break

for r in range(start_row, len(lines)):
    next_timelines = defaultdict(int)
    for (curr_r, curr_c), count in timeline_counts.items():
        if curr_r != r: continue 
        
        if 0 <= curr_c < len(lines[r]):
            char = lines[r][curr_c]
        else:
            char = '.'

        if char == '^':
            next_timelines[(r + 1, curr_c - 1)] += count
            next_timelines[(r + 1, curr_c + 1)] += count
        else:
            next_timelines[(r + 1, curr_c)] += count

    timeline_counts = next_timelines
    
total_timelines = sum(timeline_counts.values())
print(f"Total active timelines: {total_timelines}")
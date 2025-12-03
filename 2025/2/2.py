import math
import pandas as pd
import re
ids = pd.read_csv("text.csv", header = None)
idst = ids.T
invalid = []
debug_list = []
total_sum = 0

def is_repeating(num):
    s = str(num)
    length = len(s)
    for l in range(1, length // 2 + 1):
            if length % l == 0:
                substring = s[:l]
                multiplier = length // l
                if substring * multiplier == s:
                    return True
    return False

for i in range(len(idst)):
    row_string = str(idst.iloc[i, 0]).strip()
    
    parts = row_string.split('-')
    start = int(parts[0])
    end = int(parts[1])
   
    for num in range(start, end + 1):
        if is_repeating(num):
            total_sum += num
            debug_list.append(num)

print(f"Total Sum: {total_sum}")
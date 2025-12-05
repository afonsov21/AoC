import numpy as np
import re
file = "input.txt"
range_pairs = []
raw_ranges = []
single_numbers = []
with open(file, 'r') as f:
    lines = f.readlines()
    for line in lines:
            clean_line = line.strip()
            if not clean_line:
                continue

            if '-' in clean_line:
                parts = clean_line.split('-')
                start = int(parts[0])
                end = int(parts[1])
                range_pairs.append((start, end))
                raw_ranges.append((start, end))
            else:
                number = int(clean_line)
                single_numbers.append(number)
    count = 0
    ranges = []
    raw_ranges.sort()
    merged_ranges = []
    for number in single_numbers:
        found_match = False
        for start, end in range_pairs:
            if start <= number <= end:
                print(f"{number} is inside range {start}-{end}")
                ranges.append((start, end))
                found_match = True
                count += 1
                break 

        if not found_match:
            print(f"{number} is not in any range")
    
    unique_ranges = set(ranges)
    total_count = 0

if raw_ranges:
    current_start, current_end = raw_ranges[0]

    for i in range(1, len(raw_ranges)):
        next_start, next_end = raw_ranges[i]
        if next_start <= current_end + 1:
            current_end = max(current_end, next_end)
        else:
            merged_ranges.append((current_start, current_end))
            current_start, current_end = next_start, next_end

    merged_ranges.append((current_start, current_end))

total_fresh_ids = 0
for start, end in merged_ranges:
    total_fresh_ids += (end - start + 1)

print(f"Total Fresh IDs: {total_fresh_ids}")
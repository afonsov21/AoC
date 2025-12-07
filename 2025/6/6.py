import numpy as np
import pandas as pd
filename = "input.txt"
df = pd.read_csv(filename, sep='\s+', header=None)
symbol_row_index = len(df) - 1
ans1 = 0
ans2 = 0

# for j in df.columns:
#     if df[j][symbol_row_index] == "*":
#         for i in range(0, symbol_row_index - 3):
#             val1 = int(df[j][i])
#             val2 = int(df[j][i+1])
#             val3 = int(df[j][i+2])
#             val4 = int(df[j][i+3])
            
#             ans_mult = val1 * val2 * val3 * val4
#             ans1 += ans_mult



#     if df[j][symbol_row_index] == "+":
#         for i in range(0, symbol_row_index - 3):
#             val5 = int(df[j][i])
#             val6 = int(df[j][i+1])
#             val7 = int(df[j][i+2])
#             val8 = int(df[j][i+3])
            
#             ans_sum = val5 + val6 + val7 + val8
#             ans2 += ans_sum

# print(ans1 + ans2)
#===========EX1 end==============
with open(filename, 'r') as f:
    raw_lines = [line.replace('\n', '') for line in f.readlines()]

max_len = max(len(line) for line in raw_lines)
padded_lines = [line.ljust(max_len) for line in raw_lines]

number_lines = padded_lines[:-1]
operator_line = padded_lines[-1]

grand_total = 0


def is_column_empty(col_idx, lines):
    for line in lines:
        if line[col_idx] != ' ':
            return False
    return True

blocks = []
current_block_indices = []

for col_idx in range(max_len):
    if not is_column_empty(col_idx, number_lines):
        current_block_indices.append(col_idx)
    else:
        if current_block_indices:
            blocks.append(current_block_indices)
            current_block_indices = []

if current_block_indices:
    blocks.append(current_block_indices)


print(f"Found {len(blocks)} problems to solve.\n")

for block in blocks:
    operator = None
    for idx in block:
        char = operator_line[idx]
        if char in ['*', '+']:
            operator = char
            break
            
    if operator is None:
        print(f"Warning: No operator found for block at cols {block}, skipping.")
        continue

    vertical_numbers = []
    
    for col_idx in block:
        num_str = ""
        for line in number_lines:
            char = line[col_idx]
            if char != ' ':
                num_str += char
        
        if num_str:
            vertical_numbers.append(int(num_str))

    block_result = 0
    if operator == '+':
        block_result = np.sum(vertical_numbers)
    elif operator == '*':
        block_result = np.prod(vertical_numbers)

    print(f"Block Result ({operator}): {vertical_numbers} = {block_result}")
    grand_total += block_result
    
print(f"Final Grand Total: {grand_total}")
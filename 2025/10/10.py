import re
import itertools

# def solve_machine(line):
#     lights_match = re.search(r'\[([.#]+)\]', line)
#     if not lights_match:
#         return 0
#     lights_str = lights_match.group(1)
#     target = [1 if c == '#' else 0 for c in lights_str]
#     num_lights = len(target)

#     buttons_matches = re.findall(r'\(([\d,]+)\)', line)
    
#     buttons = []
#     for bm in buttons_matches:
#         indices = [int(x) for x in bm.split(',')]
#         vec = [0] * num_lights
#         for idx in indices:
#             if idx < num_lights:
#                 vec[idx] = 1
#         buttons.append(vec)
    
#     num_buttons = len(buttons)
#     if num_buttons == 0:
#         return 0 if sum(target) == 0 else float('inf')

#     M = []
#     for r in range(num_lights):
#         row = []
#         for c in range(num_buttons):
#             row.append(buttons[c][r])
#         row.append(target[r])
#         M.append(row)
    
#     pivot_cols = []
#     pivot_row_map = {} 
    
#     current_row = 0
#     for col in range(num_buttons):
#         if current_row >= num_lights:
#             break
    
#         pivot = -1
#         for r in range(current_row, num_lights):
#             if M[r][col] == 1:
#                 pivot = r
#                 break
        
#         if pivot != -1:
#             M[current_row], M[pivot] = M[pivot], M[current_row]
#             for r in range(num_lights):
#                 if r != current_row and M[r][col] == 1:
#                     for k in range(col, num_buttons + 1):
#                         M[r][k] ^= M[current_row][k]
            
#             pivot_cols.append(col)
#             pivot_row_map[col] = current_row
#             current_row += 1

#     for r in range(num_lights):
#         all_zeros = True
#         for c in range(num_buttons):
#             if M[r][c] == 1:
#                 all_zeros = False
#                 break
#         if all_zeros and M[r][num_buttons] == 1:
#             return float('inf') 
#     free_vars = [c for c in range(num_buttons) if c not in pivot_cols]
    
#     min_presses = float('inf')
#     for assignment in itertools.product([0, 1], repeat=len(free_vars)):
#         x = [0] * num_buttons
        
#         for i, val in enumerate(assignment):
#             x[free_vars[i]] = val
        
#         for p_col in pivot_cols:
#             row_idx = pivot_row_map[p_col]
#             val = M[row_idx][num_buttons] 
#             for f_col in free_vars:
#                 if M[row_idx][f_col] == 1:
#                     val ^= x[f_col]
#             x[p_col] = val
            
#         weight = sum(x)
#         if weight < min_presses:
#             min_presses = weight
            
#     return min_presses

# def main():
#     total_presses = 0
#     try:
#         with open('input.txt', 'r') as f:
#             for line in f:
#                 if line.strip():
#                     res = solve_machine(line)
#                     if res == float('inf'):
#                         print(f"Warning: A machine configuration is impossible.")
#                     else:
#                         total_presses += res
#         print(f"Total fewest presses: {total_presses}")
#     except FileNotFoundError:
#         print("Error: 'input.txt' not found.")

# if __name__ == '__main__':
#     main()
#===============EX1END=============
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def solve_joltage_machine(line):
    target_match = re.search(r'\{([\d,]+)\}', line)
    if not target_match:
        return 0
    target_vals = [int(x) for x in target_match.group(1).split(',')]
    b = np.array(target_vals)
    num_counters = len(b)
    button_strings = re.findall(r'\(([\d,]+)\)', line)
    
    cols = []
    for bs in button_strings:
        indices = [int(x) for x in bs.split(',')]
        col = np.zeros(num_counters)
        for idx in indices:
            if idx < num_counters:
                col[idx] = 1
        cols.append(col)
        
    if not cols:
        return 0
        
    A = np.column_stack(cols)
    num_buttons = A.shape[1]
    c = np.ones(num_buttons)
    constraints = LinearConstraint(A, lb=b, ub=b)
    integrality = np.ones(num_buttons)
    bounds = Bounds(lb=0, ub=np.inf)
    
    res = milp(c=c, constraints=constraints, integrality=integrality, bounds=bounds)
    
    if res.success:
        return int(np.round(np.sum(res.x)))
    else:
        return 0

def main():
    total_presses = 0
    try:
        with open('input.txt', 'r') as f:
            for line in f:
                if line.strip():
                    total_presses += solve_joltage_machine(line)
        
        print(f"Total fewest presses: {total_presses}")
        
    except FileNotFoundError:
        print("Error: 'input.txt' not found. Please save your puzzle input to this file.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
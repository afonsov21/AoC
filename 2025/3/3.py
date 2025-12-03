file = "input.txt"
total_joltage = 0

def solve_line(line_digits, k=12):
    """
    Finds the largest k-digit number formed by digits in order.
    """
    n = len(line_digits)
    if n < k:
        return 0

    result_digits = []
    current_index = 0
    for i in range(k):
        remaining_needed = (k - 1) - i
        search_end = n - remaining_needed
        search_window = line_digits[current_index : search_end]
        best_digit = max(search_window)
        relative_pos = search_window.index(best_digit)
        current_index += relative_pos + 1
        
        result_digits.append(best_digit)
    return int("".join(str(d) for d in result_digits))

with open(file, 'r') as file:
    for i, line in enumerate(file, 1):
        clean_line = line.strip()
        if not clean_line:
            continue
            
     
        digits = [int(char) for char in clean_line if char.isdigit()]
        
        
        line_val = solve_line(digits, k=12)
        
        if line_val > 0:
            print(f"Line {i} max 12-digit joltage: {line_val}")
            total_joltage += line_val
        else:
            print(f"Line {i}: Not enough batteries (needs 12).")

print(f"Total Output Joltage: {total_joltage}")
        
        
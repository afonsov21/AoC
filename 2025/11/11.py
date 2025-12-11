import sys

# def solve_puzzle(input_file):
#     try:
#         with open(input_file, 'r') as f:
#             lines = f.readlines()
#     except FileNotFoundError:
#         print(f"Error: '{input_file}' not found.")
#         return

#     graph = {}
#     for line in lines:
#         line = line.strip()
#         if not line:
#             continue
    
#         if ':' in line:
#             src, dst_part = line.split(':', 1)
#             src = src.strip()
#             destinations = dst_part.strip().split()
#             graph[src] = destinations

#     memo = {}

#     def count_paths(node):
#         if node == 'out':
#             return 1
        
#         if node in memo:
#             return memo[node]
        
#         if node not in graph:
#             return 0
        
#         total_paths = 0
#         for neighbor in graph[node]:
#             total_paths += count_paths(neighbor)
        
#         memo[node] = total_paths
#         return total_paths

#     result = count_paths('you')
#     print(f"Total paths from 'you' to 'out': {result}")

# if __name__ == "__main__":
#     solve_puzzle("input.txt")
#==============EX1 END============

sys.setrecursionlimit(200000)

def solve_part_two(input_file):
    graph = {}
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: '{input_file}' not found.")
        return

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if ':' in line:
            src, dst_part = line.split(':', 1)
            src = src.strip()
            destinations = dst_part.strip().split()
            graph[src] = destinations
    memo = {}

    def count_paths(current_node, target_node):
        if current_node == target_node:
            return 1
        
        if (current_node, target_node) in memo:
            return memo[(current_node, target_node)]
        
        if current_node not in graph:
            return 0
        
        total = 0
        for neighbor in graph[current_node]:
            total += count_paths(neighbor, target_node)
        
        memo[(current_node, target_node)] = total
        return total
    
    paths_svr_to_dac = count_paths('svr', 'dac')
    paths_dac_to_fft = count_paths('dac', 'fft')
    paths_fft_to_out = count_paths('fft', 'out')
    
    total_sequence_a = paths_svr_to_dac * paths_dac_to_fft * paths_fft_to_out
    paths_svr_to_fft = count_paths('svr', 'fft')
    paths_fft_to_dac = count_paths('fft', 'dac')
    paths_dac_to_out = count_paths('dac', 'out')
    
    total_sequence_b = paths_svr_to_fft * paths_fft_to_dac * paths_dac_to_out

    total_valid_paths = total_sequence_a + total_sequence_b
    print(f"Paths svr -> ... -> dac -> ... -> fft -> ... -> out: {total_sequence_a}")
    print(f"Paths svr -> ... -> fft -> ... -> dac -> ... -> out: {total_sequence_b}")
    print(f"Total paths visiting both dac and fft: {total_valid_paths}")

if __name__ == "__main__":
    solve_part_two("input.txt")
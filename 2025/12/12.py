import sys
import time

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = [line.rstrip() for line in f if line.strip()]

    shapes = {}
    regions = []
    
    current_shape_id = None
    current_shape_lines = []    
    mode = "SHAPES"
    
    for line in lines:
        if ':' in line and 'x' not in line.split(':')[0]:
            if current_shape_id is not None:
                shapes[current_shape_id] = parse_shape_grid(current_shape_lines)
                current_shape_lines = []
            current_shape_id = int(line.split(':')[0])
        elif 'x' in line and ':' in line:
            if current_shape_id is not None:
                shapes[current_shape_id] = parse_shape_grid(current_shape_lines)
                current_shape_id = None
                mode = "REGIONS"
            
            parts = line.split(':')
            dims = parts[0].split('x')
            w, h = int(dims[0]), int(dims[1])
            counts = list(map(int, parts[1].strip().split()))
            regions.append(((w, h), counts))
        else:
            if mode == "SHAPES":
                current_shape_lines.append(line)

    return shapes, regions

def parse_shape_grid(lines):
    coords = []
    for r, row in enumerate(lines):
        for c, char in enumerate(row):
            if char == '#':
                coords.append((r, c))
    return coords

def normalize_shape(coords):
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    sorted_coords = sorted([(r - min_r, c - min_c) for r, c in coords])
    return tuple(sorted_coords)

def generate_variations(base_coords):
    variations = set()
    
    current = base_coords
    for _ in range(2):
        for _ in range(4):
            current = tuple((c, -r) for r, c in current)
            variations.add(normalize_shape(current))
        current = tuple((-r, c) for r, c in current)
        variations.add(normalize_shape(current))
        
    return list(variations)

def get_shape_variations(shapes):
    lookup = {}
    for sid, coords in shapes.items():
        vars_list = generate_variations(coords)
        processed_vars = []
        for v in vars_list:
            h = max(r for r, c in v) + 1
            w = max(c for r, c in v) + 1
            size = len(v)
            processed_vars.append({'coords': v, 'h': h, 'w': w, 'size': size})
        lookup[sid] = processed_vars
    return lookup

def solve_region(width, height, pieces_to_place, shape_lookup):
    total_area = 0
    for pid in pieces_to_place:
        total_area += shape_lookup[pid][0]['size']
    
    if total_area > width * height:
        return False
    detailed_pieces = []
    for pid in pieces_to_place:
        size = shape_lookup[pid][0]['size']
        detailed_pieces.append({'id': pid, 'size': size})

    detailed_pieces.sort(key=lambda x: x['size'], reverse=True)
    
    grid = [False] * (width * height)
    return backtrack(grid, width, height, detailed_pieces, 0, shape_lookup, 0)

def backtrack(grid, w, h, pieces, p_idx, shape_lookup, start_pos_for_identical):
    if p_idx == len(pieces):
        return True
    
    current_piece = pieces[p_idx]
    pid = current_piece['id']

    start_index = 0
    if p_idx > 0 and pieces[p_idx-1]['id'] == pid:
        start_index = start_pos_for_identical
    
    variations = shape_lookup[pid]
    
    for i in range(start_index, len(grid)):
        r0, c0 = divmod(i, w)
        for var in variations:
            if r0 + var['h'] > h or c0 + var['w'] > w:
                continue
            
            fits = True
            indices_to_occupy = []
            
            for dr, dc in var['coords']:
                r, c = r0 + dr, c0 + dc
                idx = r * w + c
                if grid[idx]:
                    fits = False
                    break
                indices_to_occupy.append(idx)
            
            if fits:
                for idx in indices_to_occupy:
                    grid[idx] = True
        
                if backtrack(grid, w, h, pieces, p_idx + 1, shape_lookup, i):
                    return True
                
             
                for idx in indices_to_occupy:
                    grid[idx] = False
                    
    return False

def main():
    print("Parsing input...")
    shapes, regions = parse_input('input.txt')
    
    print("Pre-calculating shape variations...")
    shape_lookup = get_shape_variations(shapes)
    
    print(f"Found {len(regions)} regions to check.")
    
    success_count = 0
    start_time = time.time()
    
    for i, (dims, counts) in enumerate(regions):
        width, height = dims
    
        pieces_to_place = []
        for pid, count in enumerate(counts):
            pieces_to_place.extend([pid] * count)
        if solve_region(width, height, pieces_to_place, shape_lookup):
            success_count += 1
            # print(f"Region {i+1}: Fits!")
        else:
            # print(f"Region {i+1}: Impossible.")
            pass
            
        if (i + 1) % 10 == 0:
            print(f"Processed {i+1}/{len(regions)} regions...")

    end_time = time.time()
    
    print("------------------------------------------------")
    print(f"Total Regions that fit: {success_count}")
    print(f"Time Taken: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()
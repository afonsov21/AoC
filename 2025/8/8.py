import pandas as pd
import numpy as np
from collections import Counter

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.num_clusters = n

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        
        if root_i != root_j:
            self.parent[root_j] = root_i
            self.num_clusters -= 1  
            return True
        return False


data = pd.read_csv('input.txt', header=None)
points = data.values 
N_points = len(points)

diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
dists_matrix = np.sqrt(np.sum(diff**2, axis=-1))


row_idx, col_idx = np.triu_indices(N_points, k=1)
distances = dists_matrix[row_idx, col_idx]

edges = []
for d, r, c in zip(distances, row_idx, col_idx):
    edges.append((d, r, c))

edges.sort(key=lambda x: x[0])
uf = UnionFind(N_points)
# PAIRS_TO_PROCESS = 1000
# target_edges = edges[:PAIRS_TO_PROCESS]

# for dist, p1, p2 in target_edges:
#     uf.union(p1, p2)

# final_roots = [uf.find(i) for i in range(N_points)]
# circuit_sizes = list(Counter(final_roots).values())
# sorted_sizes = sorted(circuit_sizes, reverse=True)

# top_3 = sorted_sizes[:3]

# product = 1
# for s in top_3:
#     product *= s


# print(f"Top 3 circuit sizes: {top_3}")
# print(f"Final Answer (Product): {product}")
#============END EX1======================

for dist, p1, p2 in edges:
    if uf.union(p1, p2):
        if uf.num_clusters == 1:
            print(f"Connecting Point #{p1} and Point #{p2}")
            print(f"Distance: {dist}")
            
            # Get the coordinates
            coord_1 = points[p1]
            coord_2 = points[p2]
            
            print(f"Point 1: {coord_1}")
            print(f"Point 2: {coord_2}")
            answer = coord_1[0] * coord_2[0]
            
            print(f"\nFinal Answer (X1 * X2): {answer}")
            break
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import numpy as np
from itertools import combinations

from util import get_data

data = get_data('day08/day08.txt', 'lines')

def parse_line(line):
    x, y, z = line.split(',')
    return [int(x), int(y), int(z)]

def dist(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)

def get_sorted_distances(points):
    n = len(points)
    distances = []
    for i, j in combinations(range(n), 2):
        p1, p2 = points[i], points[j]
        distance_val = dist(p1, p2)
        distances.append((distance_val, i, j))
    distances.sort(key=lambda x: x[0])
    return n, distances

def find(x, parent):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

def union(a, b, parent, size):
    ra, rb = find(a, parent), find(b, parent)   
    if ra == rb:
        return False
    if size[ra] < size[rb]:
        ra, rb = rb, ra
    parent[rb] = ra
    size[ra] += size[rb]
    return True

def solve(points, part):
    n, distances = get_sorted_distances(points)

    # Houd bij welke punten in welke circuits zitten
    parent = list(range(n))
    size = [1] * n

    if part == 1:
        # Itereer over afstanden en voeg punten toe aan circuits
        for _, i, j in distances[:n]:
            union(i, j, parent, size)

        # Haal de grootte van elke circuit op
        circuit_sizes = {}
        for i in range(n):
            root = find(i, parent)
            circuit_sizes[root] = circuit_sizes.get(root, 0) + 1
        sizes_sorted = sorted(circuit_sizes.values(), reverse=True)

        # Failsafe voor minder dan 3 circuits
        while len(sizes_sorted) < 3:
            sizes_sorted.append(1)

        return sizes_sorted[0] * sizes_sorted[1] * sizes_sorted[2]
    
    elif part == 2:
        merges_remaining = n - 1  # aantal merges om tot één circuit te komen
        last_pair = 0,0

        for _, i, j in distances:
            if union(i, j, parent, size):
                merges_remaining -= 1
                last_pair = (i, j)
                if merges_remaining == 0:
                    break

        # Haal x-coördinaten van het laatste merge-paar op
        p1, p2 = points[last_pair[0]], points[last_pair[1]]
        return p1[0] * p2[0]

points = [parse_line(line) for line in data]
print("Part 1:", solve(points, part = 1))
print("Part 2:", solve(points, part = 2))
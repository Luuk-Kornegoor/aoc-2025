import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from util import *
from functools import lru_cache
from itertools import permutations

data = get_data("day11/day11.txt", "lines")

def parse_input(data):
    server_grid = {}
    for line in data:
        split = line.split(":")
        input = split[0]
        outputs = [out for out in split[1].split()]
        server_grid[input] = outputs
        
    return server_grid

def count_paths(graph, start, end):
    @lru_cache(None)
    # Simpele DFS om paden te tellen
    def dfs(node):
        if node == end:
            return 1
        return sum(dfs(nxt) for nxt in graph.get(node, []))
    return dfs(start)


def solve(graph, start, end, must_visit = None):
    # Part 1: Directe verbinding start -> end
    if must_visit is None or len(must_visit) == 0:
        return count_paths(graph, start, end)
    
    # Part 2: Paden die langs alle must_visit nodes gaan
    # Aantal paden start -> must_visit[0] -> ... -> must_visit[n] -> end
    #       =
    # Som over alle permutaties van must_visit van:
    #       Aantal paden start -> must_visit[0] 
    #           *
    #       Aantal paden must_visit[0] -> must_visit[1] *
    #           ...
    #       Aantal paden must_visit[n] -> end
    
    total = 0
    
    for order in permutations(must_visit):
        seq = [start] + list(order) + [end]
        segment_total = 1
        for i in range(len(seq) - 1):
            segment_paths = count_paths(graph, seq[i], seq[i+1])
            if segment_paths == 0:
                segment_total = 0
                break
            segment_total *= segment_paths
        
        total += segment_total
    
    return total

print("Part 1:", solve(parse_input(data), "you", "out"))
print("Part 2:", solve(parse_input(data), "svr", "out", must_visit=["dac", "fft"]))
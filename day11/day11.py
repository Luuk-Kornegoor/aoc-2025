import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from util import *
from functools import lru_cache

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
    # Simpele DFS om alle paden te tellen
    def dfs(node):
        if node == end:
            return 1
        return sum(dfs(nxt) for nxt in graph.get(node, []))
    return dfs(start)


def solve(graph, start, end, must_visit = None):
    if must_visit is None or len(must_visit) == 0:
        return count_paths(graph, start, end)
    
    # Observatie: 2 mogelijke volgordes om a en b te bezoeken
    # Aantal paden van (start -> end) via must_visit := [a,b] 
    #   = 
    # aantal paden (start -> a) * (a -> b) * (b -> end)
    #   +
    # aantal paden (start -> b) * (b -> a) * (a -> end)
    # TODO: generaliseren voor len(must_visit) > 2
    
    a, b = must_visit

    case1 = (
        count_paths(graph, start, a) *
        count_paths(graph, a, b) *
        count_paths(graph, b, end)
    )

    case2 = (
        count_paths(graph, start, b) *
        count_paths(graph, b, a) *
        count_paths(graph, a, end)
    )

    return case1 + case2

print("Part 1:", solve(parse_input(data), "you", "out"))
print("Part 2:", solve(parse_input(data), "svr", "out", must_visit=["dac", "fft"]))
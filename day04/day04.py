import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from util import *

grid = get_data("day04/day04.txt", "lines")

def check_position(grid: list[str], r: int, c: int) -> int:
    # Controleer max. acht posities rondom grid[r][c]
    count = 0
    rows = len(grid)
    cols = len(grid[0])
    
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            check_r, check_c = r + dr, c + dc
            if 0 <= check_r < rows and 0 <= check_c < cols and grid[check_r][check_c] == '@':
                count += 1
    return count

def solve_part_1(grid: list[str]) -> int:
    # Tel beschikbare '@'
    total = 0
    rows = len(grid)
    cols = len(grid[0])
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '.':
                continue
            if check_position(grid, r, c) < 4:
                total += 1
    return total

def solve_part_2(grid: list[str]) -> int:
    # Verwijder beschikbare '@' iteratief tot exhaustion
    stable = False
    total_removed = 0
    while not stable:
        stable = True
        to_remove = []
        rows = len(grid)
        cols = len(grid[0])
        
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != '@':
                    continue
                if check_position(grid, r, c) < 4:
                    to_remove.append((r, c))
                    stable = False
        for r, c in to_remove:
            grid[r] = grid[r][:c] + '.' + grid[r][c+1:]
            total_removed += 1
    return total_removed
    

print(solve_part_1(grid))
print(solve_part_2(grid))
            
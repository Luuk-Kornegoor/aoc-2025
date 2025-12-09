import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from collections import deque
from util import *

data = get_data('day09/day09.txt', 'lines')

def parse_line(line):
    x, y = line.split(',')
    return [int(x), int(y)]

def solve_part_1(points):
    max_area = 0
    
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            x1, y1 = points[i]
            x2, y2 = points[j]

            area = (abs(x2 - x1)+1) * (abs(y2 - y1)+1)
            max_area = max(max_area, area)

    return max_area 

def solve_part_2(points):
    reds = [tuple(p) for p in points]
    n = len(reds)

    # Stap 1: Bepaal de unieke x- en y-coördinaten
    X = set()
    Y = set()
    for x,y in reds:
        X.add(x)
        X.add(x+1)
        X.add(x-1)
        Y.add(y)
        Y.add(y+1)
        Y.add(y-1)

    X = sorted(X)
    Y = sorted(Y)
    x_map = {x:i for i,x in enumerate(X)}
    y_map = {y:i for i,y in enumerate(Y)}
    W,H = len(X), len(Y)

    # Stap 2: Maak een gecomprimeerde grid
    grid = [[0]*W for _ in range(H)]

    def mark(x,y):
        if x in x_map and y in y_map:
            r,c = y_map[y], x_map[x]
            grid[r][c] = 1

    # Stap 3: Markeer rode randen
    for i in range(n):
        x1,y1 = reds[i]
        x2,y2 = reds[(i+1)%n]
        if x1 == x2:
            step = 1 if y2>y1 else -1
            for y in range(y1,y2+step, step):
                mark(x1,y)
        else:
            step = 1 if x2>x1 else -1
            for x in range(x1,x2+step, step):
                mark(x,y1)

    # Stap 4: BFS van buitenaf om buitengebied te markeren
    outside = [[0]*W for _ in range(H)]
    q = deque()
    for r in [0,H-1]:
        for c in range(W):
            if grid[r][c]==0 and outside[r][c]==0:
                outside[r][c]=1
                q.append((r,c))
    for c in [0,W-1]:
        for r in range(H):
            if grid[r][c]==0 and outside[r][c]==0:
                outside[r][c]=1
                q.append((r,c))
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]
    while q:
        r,c = q.popleft()
        for dr,dc in dirs:
            rr,cc = r+dr, c+dc
            if 0<=rr<H and 0<=cc<W and grid[rr][cc]==0 and outside[rr][cc]==0:
                outside[rr][cc]=1
                q.append((rr,cc))

    # Vul het binnengebied
    for r in range(H):
        for c in range(W):
            if grid[r][c]==1 or outside[r][c]==0:
                grid[r][c]=1

    # Stap 5: Bereken prefix sommen
    psum = [[0]*(W+1) for _ in range(H+1)]
    for r in range(H):
        for c in range(W):
            psum[r+1][c+1] = grid[r][c] + psum[r][c+1] + psum[r+1][c] - psum[r][c]

    # Helper functie om te controleren of rechthoek vrij is
    def rect_allowed(x1,y1,x2,y2):
        r1,c1 = y_map[y1], x_map[x1]
        r2,c2 = y_map[y2], x_map[x2]
        rlo,rhi = min(r1,r2), max(r1,r2)
        clo,chi = min(c1,c2), max(c1,c2)
        total = psum[rhi+1][chi+1]-psum[rhi+1][clo]-psum[rlo][chi+1]+psum[rlo][clo]
        area = (rhi-rlo+1)*(chi-clo+1)
        return total == area

    # Stap 6: Zoek de grootste toegestane rechthoek
    max_area = 0
    for i in range(n):
        x1,y1 = reds[i]
        for j in range(i+1,n):
            x2,y2 = reds[j]
            if rect_allowed(x1,y1,x2,y2):
                area = (abs(x2-x1)+1)*(abs(y2-y1)+1)
                if area > max_area:
                    max_area = area
    return max_area

print("Part 1:", solve_part_1([parse_line(line) for line in data]))
print("Part 2:", solve_part_2([parse_line(line) for line in data]))
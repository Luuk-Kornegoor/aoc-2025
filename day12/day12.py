import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import re
from util import *

data = get_data("day12/day12.txt", "lines")

def parse_data(lines):
    shapes = {}
    i = 0
    n = len(lines)

    shape_header_re = re.compile(r'^(\d+):\s*$')
    region_re = re.compile(r'^(\d+)x(\d+):\s*(.*)$')

    while i < n:
        line = lines[i].strip()

        # Lege regel vóór vorm headers overslaan
        if line == "":
            i += 1
            continue

        # Stop met vormen lezen wanneer we bij de pasvlakken zijn
        if region_re.match(line):
            break

        m = shape_header_re.match(line)
        if not m:
            raise ValueError(f"Invalid shape header: {lines[i]}")
        shape_id = int(m.group(1))
        i += 1

        # Lees vorm uit
        rows = []
        while i < n:
            s = lines[i].strip()
            if s == "":
                break
            if shape_header_re.match(s) or region_re.match(s):
                break
            if all(c in ".#" for c in s):
                rows.append(s)
            else:
                break
            i += 1

        shapes[shape_id] = rows

        # Lege regels na vorm overslaan
        while i < n and lines[i].strip() == "":
            i += 1

    regions = []
    while i < n:
        line = lines[i].strip()
        i += 1

        if line == "":
            continue

        m = region_re.match(line)
        if not m:
            raise ValueError(f"Invalid region line: {line}")

        w = int(m.group(1))
        h = int(m.group(2))
        counts = list(map(int, m.group(3).split()))

        regions.append((w, h, counts))

    # Normaliseer vormen naar lijst
    if shapes:
        max_id = max(shapes.keys())
        shape_list = [shapes.get(i, []) for i in range(max_id + 1)]
    else:
        shape_list = []

    return shape_list, regions

def shape_area(rows):
    return sum(r.count("#") for r in rows)

def can_fit_region(w, h, counts, shape_areas):
    required = sum(counts[i] * shape_areas[i] for i in range(len(counts)))
    return required <= w * h

def solve_part_1(data):
    shapes, regions = parse_data(data)

    shape_areas = [shape_area(s) for s in shapes]

    total = 0
    for w, h, counts in regions:
        counts += [0] * (len(shape_areas) - len(counts))
        if can_fit_region(w, h, counts, shape_areas):
            total += 1
    return total
    
print(f"Part 1: {solve_part_1(data)}")
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from util import *

rots = get_data("day01/day01.txt", "lines")
    
pos = 50
pw1, pw2 = 0, 0
max = 100

for rot in rots:
    direction = rot[0]
    steps = int(rot[1:])
    start = pos  # Bewaar startpositie

    # Bereken de eerste index in steps waar een veelvoud van 100 wordt bereikt
    if direction == "R":
        first = (max - start) % max
        
        if first == 0:
            first = max
            
        if steps >= first:
            # Increment pw2 voor elke keer dat een veelvoud van 100 wordt gepasseerd
            pw2 += ( (steps - first) // max ) + 1
            
        # Normaliseer naar 0-99 range
        pos = (pos + steps) % max

    else:
        # Zelfde idee maar dan andersom
        first = start if start != 0 else max
        if steps >= first:
            pw2 += ( (steps - first) // max ) + 1
            
        # Normaliseer naar 0-99 range
        pos = (pos - steps) % max

    # Part 1
    if pos == 0:
        pw1 += 1

print("Part 1:", pw1)
print("Part 2:", pw2)
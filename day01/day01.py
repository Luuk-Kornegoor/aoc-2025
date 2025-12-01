with open("day01/day01.txt") as f:
    rots = f.read().strip().splitlines()
    f.close()
    
pos = 50
pw1, pw2 = 0, 0

for rot in rots:
    direction = rot[0]
    steps = int(rot[1:])
    start = pos  # Bewaar startpositie

    # Bereken de eerste index in steps waar een veelvoud van 100 wordt bereikt
    if direction == "R":
        first = (100 - start) % 100
        
        if first == 0:
            first = 100
            
        if steps >= first:
            # Increment pw2 voor elke keer dat een veelvoud van 100 wordt gepasseerd
            pw2 += ( (steps - first) // 100 ) + 1
            
        # Normaliseer naar 0-99 range
        pos = (pos + steps) % 100

    else:
        # Zelfde idee maar dan andersom
        first = start if start != 0 else 100
        if steps >= first:
            pw2 += ( (steps - first) // 100 ) + 1
            
        # Normaliseer naar 0-99 range
        pos = (pos - steps) % 100

    # Part 1
    if pos == 0:
        pw1 += 1

print("Part 1:", pw1)
print("Part 2:", pw2)
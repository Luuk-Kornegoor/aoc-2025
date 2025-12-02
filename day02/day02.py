import re

# Haal de komma-gescheiden reeksen uit de input
with open("day02/day02.txt") as f:
    data = f.read().split(",")
    f.close()
    
sum_1, sum_2 = 0, 0

for pair in data:
    # Split elke reeks in lower en upper bound
    lower, upper = pair.split("-")
    
    for i in range(int(lower), int(upper) + 1):
        # Part 1: Is het getal een reeks cijfers die twee keer herhaald wordt?
        if re.match(r"^(\d+)\1$", str(i)):
            sum_1 += i
            
        # Part 2: Is het getal een reeks cijfers die minstens twee keer herhaald wordt?
        if re.match(r"^(\d+)(\1+)$", str(i)):
            sum_2 += i
            
print(f"Part 1: {sum_1}")
print(f"Part 2: {sum_2}")
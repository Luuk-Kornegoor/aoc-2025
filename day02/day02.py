import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from util import *

data = get_data("day02/day02.txt", "comma")

def solve(data: list[str], regex:str) -> int:
    sum = 0
    for pair in data:
        lower, upper = pair.split("-")
        for i in range(int(lower), int(upper) + 1):
            if re.match(regex, str(i)):
                sum += i
                
    return sum
 
# Part 1: Is het getal een reeks cijfers die twee keer herhaald wordt?            
print(f"Part 1: {solve(data, r"^(\d+)\1$")}")

# Part 2: Is het getal een reeks cijfers die minstens twee keer herhaald wordt?
print(f"Part 2: {solve(data, r"^(\d+)(\1+)$")}")
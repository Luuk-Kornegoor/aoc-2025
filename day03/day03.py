import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from util import *

banks = get_data("day03/day03.txt", "lines")

def solve(banks: list[str], nr_digits: int) -> int:
    sum_joltage = 0
    
    for bank in banks:
        joltage = 0
        index = 0
        n = len(bank)
        
        for i in range(nr_digits):
            # Bepaal search space o.b.v. resterend aantal benodigde cijfers
            needed_digits = nr_digits - i - 1
            end_index = n - needed_digits
            segment = bank[index:end_index]
            
            # Selecteer hoogste cijfer binnen toegestane search space
            next_digit = max(segment)
            joltage += 10**(nr_digits - i - 1)*int(next_digit)
            index = bank.index(next_digit, index) + 1
            
        sum_joltage += joltage
        
    return sum_joltage

print("Part 1:", solve(banks, 2))
print("Part 2:", solve(banks, 12))
    
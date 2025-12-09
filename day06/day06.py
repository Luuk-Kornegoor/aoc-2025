import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from itertools import pairwise, zip_longest
from util import *

data = get_data('day06/day06.txt', 'cephalopod')
cols = [' '] + list(zip_longest(*data, fillvalue=' ')) + [' ']
seperators = [i for i, col in enumerate(cols) if set(col) == {' '}]

p1 = p2 = 0
for lo, hi in pairwise(seperators):
    rows = cols[lo+1:hi]
    *operands, op = map(''.join, zip(*rows))
    p1 += eval(op.join(operands))
    p2 += eval(op.join(''.join(row).replace('*',' ').replace('+',' ') for row in rows))

print(f"Part 1: {p1}")
print(f"Part 2: {p2}")
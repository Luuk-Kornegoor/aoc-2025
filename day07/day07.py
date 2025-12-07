import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from util import get_data

data = get_data('day07/day07.txt', 'lines')

start = data[0].index('S')
timeline_counts = { start: 1 }

def solve(data: list[str], timeline_counts: dict[int, int]) -> tuple[int, int]:
    total_splits = 0
    for line in data[1:]:
        new_counts = {}

        for pos, count in timeline_counts.items():
            if line[pos] == '.':
                # Geen splitsing, verder op huidige positie
                new_counts[pos] = new_counts.get(pos, 0) + count
                
            else:
                # Split tijdlijnen in links en rechts
                total_splits += 1
                new_counts[pos - 1] = new_counts.get(pos - 1, 0) + count
                new_counts[pos + 1] = new_counts.get(pos + 1, 0) + count

        timeline_counts = new_counts
        
    return total_splits, sum(timeline_counts.values())

splits, total_timelines = solve(data, timeline_counts)

print(f"Part 1: {splits}")
print(f"Part 2: {total_timelines}")
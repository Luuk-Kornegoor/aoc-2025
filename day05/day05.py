import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from util import *

data = get_data("day05/day05.txt", "lines")
split_index = data.index("")
ranges = data[:split_index]
ids = data[split_index + 1 :]

def solve_part_1(ranges: list[str], ids: list[str]) -> int:
    valid_count = 0
    parsed_ranges = [parse_range(r) for r in ranges]

    for id in ids:
        for start, end in parsed_ranges:
            if start <= int(id) <= end:
                valid_count += 1
                break

    return valid_count

def solve_part_2(ranges: list[str]) -> int:
    merged_ranges = []
    parsed_ranges = sorted([parse_range(r) for r in ranges], key=lambda x: x[0])

    # Voeg alle ranges zoveel mogelijk samen
    for current_start, current_end in parsed_ranges:
        if not merged_ranges or merged_ranges[-1][1] < current_start - 1:
            merged_ranges.append((current_start, current_end))
        else:
            merged_ranges[-1] = (merged_ranges[-1][0], max(merged_ranges[-1][1], current_end))

    total_covered = sum(end - start + 1 for start, end in merged_ranges)
    return total_covered

print(solve_part_1(ranges, ids))
print(solve_part_2(ranges))
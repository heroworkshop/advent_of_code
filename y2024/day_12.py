from collections import defaultdict
from typing import Tuple

from aocd_tools import *

EXAMPLE = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""


def run():
    input_data = load_input_data()
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    entries = grid_from_lines(input_data)
    regions = find_regions(entries)

    print(regions)

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(regions), time_report(start_time))


def find_regions(entries):
    visited = set()
    regions = []
    for p in entries.grid:
        if p not in visited:
            regions.append(get_region(p, visited, entries))
    return regions


def solution1(regions):
    return sum(region[1] for region in regions)


def solution2(regions):
    return sum(region[2] for region in regions)


def get_region(start_p, visited, entries):
    queue = [start_p]
    v = entries.at(start_p)
    size = 0
    walls = 0
    h_sides = defaultdict(list)
    v_sides = defaultdict(list)
    while queue:
        p = queue.pop(0)
        if p not in visited:
            visited.add(p)
            size += 1
            for dp in NEIGHBOURS:
                p_new = Pos(*p) + dp
                if entries.at(p_new) != v:
                    walls += 1
                    if dp[0]:
                        v_sides[(dp[0], p_new[0])].append(p_new[1])
                    else:
                        h_sides[(dp[1], p_new[1])].append(p_new[0])
                if p_new not in visited and p_new in entries.grid and entries.at(p_new) == v:
                    queue.append(p_new)
    v_count = get_sides(v_sides)
    h_count = get_sides(h_sides)
    sides = v_count + h_count
    print(f"{v}: {size} x {walls} hsides={h_count} vsides={v_count} sides={sides}")
    return v, size * walls, size * sides


def get_sides(side_dict: dict[Tuple[int, int], list[int]]):
    return sum(count_distinct_sides(p_list) for p_list in side_dict.values())


def count_distinct_sides(p_list: list[int]) -> int:
    p_list = sorted(p_list)
    s_last = p_list[0]
    count = 1
    for s in p_list[1:]:
        if abs(s - s_last) > 1:
            count += 1
        s_last = s
    return count


def all_neighbours(grid, p):
    x, y = p
    return [
        (x + dx, y + dy)
        for dx, dy in NEIGHBOURS
    ]


if __name__ == "__main__":
    run()

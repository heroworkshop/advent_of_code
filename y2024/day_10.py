import re
from aocd_tools import *


EXAMPLE = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

def run():
    input_data = load_input_data()
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    entries = grid_from_lines(input_data)
    print(entries.render())

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(entries), time_report(start_time))


def solution1(entries):
    total = 0
    for p, v in entries.grid.items():
        if v == "0":
            total += count_paths(entries, p)

    return total

def solution2(entries):
    total = 0
    for p, v in entries.grid.items():
        if v == "0":
            total += count_ratings(entries, p)

    return total


def count_paths(entries, p):
    total = 0
    visited = set()
    queue = [p]
    while queue:
        pos = queue.pop(0)
        if pos in visited:
            continue
        visited.add(pos)
        height = int(entries.at(pos))
        if height == 9:
            total += 1
            continue
        for new_pos in entries.all_neighbours(pos):
            if new_pos not in visited and int(entries.at(new_pos)) == height + 1:
                queue.append(new_pos)
    return total

def count_ratings(entries, p):
    total = 0
    queue = [p]
    while queue:
        pos = queue.pop(0)
        height = int(entries.at(pos))
        if height == 9:
            total += 1
            continue
        for new_pos in entries.all_neighbours(pos):
            if int(entries.at(new_pos)) == height + 1:
                queue.append(new_pos)
    return total

if __name__ == "__main__":
    run()

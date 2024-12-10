import re
from collections import defaultdict

from aocd_tools import *


EXAMPLE = """..........
..........
..........
....a.....
........a.
.....a....
..........
......A...
..........
..........
"""

EXAMPLE_2 = """T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
.........."""
def run():
    input_data = load_input_data()
    # input_data = EXAMPLE_2
    print(f"loaded input data ({len(input_data)} bytes)")
    # entries = int_tuples_from_lines(lines=input_data, sep=" ")
    # a, b = entries.split("\n\n")
    # entries = [process_one_line(line) for line in input_data.splitlines()]
    entries = grid_from_lines(input_data)
    print(entries.render())

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(entries), time_report(start_time))


def process_one_line(line):
    return line

def solution1(entries: Grid):
    antennae = defaultdict(list)
    for p, v in entries.grid.items():
        if v != ".":
            antennae[v].append(p)
    print(antennae)

    antinodes  =set()

    for nodes in antennae.values():
        for a in nodes:
            for b in nodes:
                dx = b[0] - a[0]
                dy = b[1] - a[1]
                anti_node = Pos(a[0]-dx, a[1]-dy)
                if anti_node in nodes:
                    # print(f"{anti_node} overlaps nodes")
                    pass
                elif not entries.in_bounds(anti_node):
                    # print(f"{anti_node} out of bounds")
                    pass
                else:
                    antinodes.add(anti_node)
    return len(antinodes)

def solution2(entries):
    antennae = defaultdict(list)
    for p, v in entries.grid.items():
        if v != ".":
            antennae[v].append(p)
    print(antennae)

    antinodes  =set()

    for ch, nodes in antennae.items():
        print(f"Processing {ch}")
        for a in nodes:
            for b in nodes:
                dx = b[0] - a[0]
                dy = b[1] - a[1]
                anti_node = Pos(a[0], a[1])
                while True and (dx and dy):
                    if not entries.in_bounds(anti_node):
                        # print(f"{anti_node} out of bounds")
                        break
                    else:
                        antinodes.add(anti_node)
                    anti_node = Pos(anti_node[0]-dx, anti_node[1]-dy)
    return len(antinodes)


def extract_lines(entries):
    return entries.split("\n")


if __name__ == "__main__":
    run()

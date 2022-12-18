from collections import deque
from dataclasses import dataclass
from typing import NamedTuple, List, Set

from aocd_tools import load_input_data, Pos3d

EXAMPLE = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

EX0 = """1,1,1
2,1,1"""

EX1 = """1,1,1
3,1,1
2,2,1
2,0,1
2,1,2
2,1,0
0,1,1"""  # 5 + 4 + 5 *5 = 34 (40)


def run():
    input_data = load_input_data(2022, 18)
    # input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    entries = input_data.split("\n")
    entries = set([parse(line) for line in entries])
    print(f"found {len(entries)} cubes")

    print("solution1 = ", solution1(entries))

    print("solution2 = ", solution2(entries))


def parse(line: str):
    return Pos3d(*[int(v) for v in line.split(",")])


VECTS = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
]


def solution1(entries: Set[Pos3d]):
    total = 0
    for p in entries:
        sides = [1 for v in VECTS if (p + Pos3d(*v) not in entries)]
        total += len(sides)
    return total

def determine_extent(nodes: Set[Pos3d]):
    x_vals = [node.x for node in nodes]
    y_vals = [node.y for node in nodes]
    z_vals = [node.z for node in nodes]

    lower = Pos3d(min(x_vals), min(y_vals), min(z_vals))
    upper = Pos3d(max(x_vals), max(y_vals), max(z_vals))
    return lower, upper


def solution2(entries: Set[Pos3d]):  # 1872 < n < 3998
    lower, upper = determine_extent(entries)
    print(f"lower: {lower}")
    print(f"upper: {upper}")
    outside = outer_bubble(lower, upper, entries)
    total = 0

    def is_exposed(p, v):
        node = p + Pos3d(*v)
        return node not in entries and node in outside

    for p in entries:
        sides = [1 for v in VECTS if is_exposed(p, v)]
        total += len(sides)
    return total


def outer_bubble(lower, upper, nodes):
    p = Pos3d(lower.x - 1, lower.y - 1, lower.z - 1)
    stack = [p]
    checked = set()
    empties = set()
    while stack:
        next_p = stack.pop(-1)
        checked.add(next_p)
        for v in VECTS:
            neighbour = next_p + Pos3d(*v)
            if neighbour not in checked and neighbour not in nodes and inside_limits(neighbour, lower, upper):
                stack.append(neighbour)
                empties.add(neighbour)
    return empties


def render_layers(nodes, x_vals, y_vals, z_vals, invert=True):
    air, rock = ".", "#"
    if invert:
        air, rock= rock, air
    for y in y_vals:
        for x in x_vals:
            for z in z_vals:
                ch = rock if Pos3d(x, y, z) in nodes else air
                print(ch, end="")
            print()
        print()


def inside_limits(node: Pos3d, lower: Pos3d, upper: Pos3d):
    return lower.x - 1 <= node.x <= upper.x + 1 and lower.y - 1 <= node.y <= upper.y + 1 and lower.z - 1 <= node.z <= upper.z + 1


if __name__ == "__main__":
    run()

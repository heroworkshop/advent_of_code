from collections import deque

from aocd_tools import load_input_data
from y2017.day_10 import knot_hash


def run():
    input_data = load_input_data(2017, 14)
    print(f"loaded input data ({len(input_data)} bytes)")

    # print("solution1 = ", solution1(input_data))
    print("solution2 = ", solution2(input_data))


def solution1(input_data):
    lines = [f"{input_data}-{i}" for i in range(128)]

    count = 0
    for line in lines:
        hexbytes = knot_hash(line)
        binary = bin(int(hexbytes, 16))[2:].zfill(128)
        count += binary.count("1")

    return count


def solution2(input_data):
    lines = [f"{input_data}-{i}" for i in range(128)]

    grid = make_grid(lines)

    region_count = 0
    while grid:
        p = next(iter(grid))
        print(f"Region {region_count} {p} {len(grid)} cells remaining")
        region = map_region(grid, p)
        for p in region:
            del grid[p]
        region_count += 1

    return region_count


def map_region(grid, start_p):
    queue = deque([start_p])
    found = set()
    while queue:
        p = queue.popleft()
        if p in grid:
            found.add(p)
        for offset in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            x, y = p[0] + offset[0], p[1] + offset[1]
            if (x, y) not in found and (x, y) in grid:
                queue.append((x, y))
    return found


def make_grid(lines):
    grid = {}
    print("Making grid", end="", flush=True)
    for y, line in enumerate(lines):
        hexbytes = knot_hash(line)
        binary = bin(int(hexbytes, 16))[2:].zfill(128)
        for x, ch in enumerate(binary):
            if ch == "1":
                grid[(x, y)] = True
        print(".", end="", flush=True)
    print("Done")
    return grid


if __name__ == "__main__":
    run()

from collections import defaultdict

from aocd_tools import load_input_data


def run():
    input_data = 347991

    print("solution1 = ", solution1(input_data))
    print("solution2 = ", solution2(input_data))


def solution1(target):
    v = 1
    x = 0
    y = 0
    while (v + 2) ** 2 < target:
        v += 2
        x += 1
        y += 1
    location = v ** 2
    print(f"last corner = {location} ({v} ^ 2) x={x} y={y}")

    steps = make_spiral(v)

    for step in steps:
        if location == target:
            break
        location += 1
        x += step[0]
        y += step[1]
        print(f"{location}: ({x}, {y})")

    return abs(x) + abs(y)


def make_spiral(radius):
    steps = [(1, 0)]
    steps.extend([(0, -1) for _ in range(radius)])
    steps.extend([(-1, 0) for _ in range(radius + 1)])
    steps.extend([(0, 1) for _ in range(radius + 1)])
    steps.extend([(1, 0) for _ in range(radius + 1)])
    return steps


def solution2(target):
    grid = defaultdict(int)
    grid[(0, 0)] = 1
    radius = 1
    x, y = 0, 0
    while True:
        path = make_spiral(radius)
        for p in path:
            x += p[0]
            y += p[1]
            value = sum_adjacent(grid, (x, y))
            grid[(x, y)] = value
            if value > target:
                return value
        radius += 2
    return value


def sum_adjacent(grid, p):
    total = 0
    x, y = p
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            total += grid[(x + dx, y + dy)]
    return total


if __name__ == "__main__":
    run()

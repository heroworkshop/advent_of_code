from collections import namedtuple

from aocd_tools import load_input_data

Reindeer = namedtuple("reindeer", "name speed duration rest_time")


def parse(line):
    print(line)
    parts = line.split()
    return Reindeer(parts[0], int(parts[3]), int(parts[6]), int(parts[13]))


def run():
    input_data = load_input_data(2015, 14)
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = input_data.split("\n")
    reindeer = [parse(line) for line in lines]
    print(reindeer)

    print("solution1 = ", solution1(reindeer))
    print("solution2 = ", solution2(reindeer))


def distance(r: Reindeer, limit: int):
    steps = make_profile(limit, r)
    return sum(steps)


def make_profile(limit, r):
    steps = []
    while len(steps) < limit:
        steps.extend([r.speed] * r.duration)
        steps.extend([0] * r.rest_time)
    return steps[:limit]


def solution1(reindeer):
    time_limit = 2503
    distances = [distance(r, time_limit) for r in reindeer]
    return max(distances)


def solution2(reindeer):
    time_limit = 2503
    profiles = [make_profile(time_limit, r) for r in reindeer]
    n = len(profiles)
    distances = [0] * n
    points = [0] * n
    for t in range(time_limit):
        for i in range(n):
            distances[i] += profiles[i][t]
        leader = max(distances)
        for i in range(n):
            points[i] += 1 if distances[i] == leader else 0
    return max(points)


if __name__ == "__main__":
    run()

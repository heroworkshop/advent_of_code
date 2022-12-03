from collections import defaultdict

from aocd_tools import load_input_data


EXAMPLE = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""


def parse(line):
    return line


def run():
    input_data = load_input_data()
    # input_data  = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = [parse(line) for line in input_data.split("\n")]
    # lines = grid_from_lines(input_data, transform=int)
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(lines))


class Cave:
    def __init__(self, name=""):
        self.connections = set()
        self.name = name

    @property
    def is_small(self):
        return self.name.lower() == self.name


def solution1(lines):
    caves = make_caves(lines)
    complete = []
    paths = []

    paths.append(["start"])

    while paths:
        p = paths.pop(-1)
        connections = caves[p[-1]].connections
        for dest in connections:
            add_new_route(paths, p, caves[dest], complete)

    return len(complete)


def add_new_route(paths, p, cave, complete):

    if cave.is_small and cave.name in p:
        return
    new_route = p.copy()
    new_route.append(cave.name)
    if cave.name == "end":
        complete.append(new_route)
    else:
        paths.append(new_route)


def add_new_route2(paths, p, cave, complete):
    if not can_follow_route(p, cave):
        return
    new_route = p.copy()
    new_route.append(cave.name)
    if cave.name == "end":
        complete.append(new_route)
    else:
        paths.append(new_route)


def can_follow_route(p, cave):
    if not cave.is_small:
        return True

    if cave.name not in p:
        return True

    if cave.name == "start":
        return False

    counts = defaultdict(int)
    for name in p:
        if name.lower() == name:
            counts[name] += 1
            if counts[name] > 1:
                return False
    return True


def make_caves(lines):
    caves = defaultdict(Cave)
    for line in lines:
        cave1, _, cave2 = line.partition("-")
        caves[cave1].connections.add(cave2)
        caves[cave2].connections.add(cave1)
        caves[cave1].name = cave1
        caves[cave2].name = cave2
    return caves


def solution2(lines):
    caves = make_caves(lines)
    complete = []
    paths = []

    paths.append(["start"])

    while paths:
        p = paths.pop(-1)
        connections = caves[p[-1]].connections
        for dest in connections:
            add_new_route2(paths, p, caves[dest], complete)
    return len(complete)


if __name__ == "__main__":
    run()

import re
from collections import defaultdict
from dataclasses import dataclass

from aocd_tools import *

EXAMPLE = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""


@dataclass
class Robot:
    pos: Pos
    vel: Pos

    def update(self, limits: Pos):
        self.pos += self.vel
        self.pos = Pos(self.pos.x % limits.x,
                       self.pos.y % limits.y)


def run():
    input_data = load_input_data()
    # input_data = EXAMPLE
    limits = Pos(101, 103)
    # limits = Pos(11, 7)
    print(f"loaded input data ({len(input_data)} bytes)")
    # entries = int_tuples_from_lines(lines=input_data, sep=" ")
    # a, b = entries.split("\n\n")
    robots = [process_one_line(line) for line in input_data.splitlines()]

    print(render(robots, limits))

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(robots, limits), time_report(start_time))


def process_one_line(line):
    m = re.search(r"p=(.+),(.+) v=(.+),(.+)", line)
    return Robot(Pos(int(m[1]),
                     int(m[2])),
                 Pos(int(m[3]),
                     int(m[4])))


def solution1(robots, limits):
    for t in range(1, 101):
        for robot in robots:
            robot.update(limits)
        # print(f"{t=}")
        # print(render(robots, limits))
    a, b, c, d = get_quadrants(robots, limits)
    return a * b * c * d


def solution2(robots, limits):
    for t in range(1, 1000001):
        for robot in robots:
            robot.update(limits)
        if detect_tree(robots, limits):
            print(f"{t=}")
            print(render(robots, limits))
            return t + 100
    return 0


def detect_tree(robots, limits):
    tally = make_tally(robots)
    slopes = set()
    antislopes = set()
    for robot in robots:
        p = robot.pos
        for d in range(1, 5):
            if Pos(p.x + d, p.y + d) not in tally:
                break
        else:
            slopes.add(p.y)
        for d in range(1, 5):
            if Pos(p.x - d, p.y - d) not in tally:
                break
        else:
            antislopes.add(p.y)

    matches = slopes.intersection(antislopes)

    return len(matches) > 0


def render(robots: list[Robot], limits: Pos):
    tally = make_tally(robots)
    lines = []
    for y in range(limits.y):
        line = f"{y:3}|"
        for x in range(limits.x):
            ch = tally.get(Pos(x, y), ".")
            line += str(ch)
        lines.append(line)
    return "\n".join(lines)


def make_tally(robots: list[Robot]) -> dict[Pos, int]:
    tally = defaultdict(int)
    for robot in robots:
        tally[robot.pos] += 1
    return tally


def get_quadrants(robots: list[Robot], limits: Pos):
    quadrants = [0, 0, 0, 0]
    for robot in robots:
        x, y = 0, 0
        if robot.pos.y < limits.y // 2:
            y = 1
        if robot.pos.x < limits.x // 2:
            x = 1
        if robot.pos.y > limits.y // 2:
            y = 2
        if robot.pos.x > limits.x // 2:
            x = 2
        if x and y:
            p = x - 1 + 2 * (y - 1)
            print(robot.pos, p)
            quadrants[p] += 1
        else:
            print(robot.pos, "None")
    return quadrants


if __name__ == "__main__":
    run()

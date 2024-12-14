import re
from contextlib import suppress

from sympy import Symbol

from aocd_tools import *

EXAMPLE = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

"""
Aa + Bb = W
Ca + Db = V

34a + 67b = 5400
94a + 22b = 8400

a = (5400 - 67b) / 34
b = (8400 - 94a) / 22

b = (8400 - 94  (5400 - 67b)  / 22
b = 

b = V - C (W - Bb) / D
b = V - CW/D - BCb/D

b (1 + BC/D) = V - CW/D

b = V - CW/D / (1+BC/D) 
a = (W - B * b) / A 
"""


def run():
    input_data = load_input_data()
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    blocks = input_data.split("\n\n")

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(blocks), time_report(start_time))


def process_one_line(line):
    return line


class NoSolution(ValueError):
    pass


def solve(button_a, button_b, prize):
    solutions = []
    ax, ay = button_a
    bx, by = button_b
    x, y = prize
    for pa in range(0, 100):
        for pb in range(0, 100):
            if pa * ax + pb * bx == x and pa * ay + pb * by == y:
                solutions.append((3 * pa + pb))
    if not solutions:
        raise NoSolution("No solutions found")
    return min(solutions)


def solve2(button_a, button_b, prize):
    from sympy import Eq, solve

    a = Symbol("a", positive=True, integer=True)
    b = Symbol("b", positive=True, integer=True)

    ax, ay = button_a
    bx, by = button_b
    x, y = prize
    sol = solve([Eq(ax * a + bx * b, x),
                 Eq(ay * a + by * b, y),
                 ])
    print(sol)
    d = {s: sol[s].evalf() for s in sol}
    if not sol:
        raise NoSolution("No solution found")
    return int(d[a] * 3 + d[b])


def solution1(blocks):
    total = 0
    for block in blocks:
        with suppress(TypeError, NoSolution):
            button_a, button_b, prize = process_block(block)
            total += solve(button_a, button_b, prize)

    return total


def solution2(blocks):
    total = 0
    for block in blocks:
        with suppress(TypeError, NoSolution):
            button_a, button_b, prize = process_block(block)
            prize = (p + 10000000000000 for p in prize)
            total += solve2(button_a, button_b, prize)

    return total


def process_block(block):
    lines = block.split("\n")
    return tuple(map(process_one_line, lines))


def process_one_line(line):
    m = re.search(r"X.(\d+), Y.(\d+)", line)
    return int(m[1]), int(m[2])


if __name__ == "__main__":
    run()

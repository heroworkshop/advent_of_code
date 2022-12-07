from typing import NamedTuple

from aocd_tools import load_input_data

EXAMPLE = """Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1."""

QUESTION = """Disc #1 has 5 positions; at time=0, it is at position 2.
Disc #2 has 13 positions; at time=0, it is at position 7.
Disc #3 has 17 positions; at time=0, it is at position 10.
Disc #4 has 3 positions; at time=0, it is at position 2.
Disc #5 has 19 positions; at time=0, it is at position 9.
Disc #6 has 7 positions; at time=0, it is at position 0."""


# 1. 0       5       10        15 ...   5n
# 2.   1  3  5  7  9    11              2n + 1


class Disc(NamedTuple):
    positions: int
    start: int


def parse(line):
    parts = line.split()
    return Disc(int(parts[3]), int(parts[-1][:-1]))


def run():
    input_data = QUESTION  # load_input_data(2016, 15)
    # input_data = EXAMPLE
    input_data = [parse(line) for line in input_data.split("\n")]
    print(input_data)
    print("solution1=", solution1(input_data))
    print("solution2=", solution2(input_data))


def solution1v1(input_data):
    solution = 0
    step = 1
    t = 0
    for y, disc in enumerate(input_data, 1):
        t0 = (disc.start + y) % disc.positions
        print(f"{y}:t0={t0:<4}start:{disc.start:<4}positions:{disc.positions:<3}", end="")
        for j in range(10):
            print(f"{t0 + j * disc.positions:5}", end="")
        while True:
            if t % disc.positions == 0:
                solution = t
                step *= disc.positions
                break
            t += step
        print(f"-> {solution} step={step}")
    return solution


def solution1(input_data):
    return find_release_time(input_data)


def find_release_time(input_data):
    release_time = 0
    step = 1
    for y, disc in enumerate(input_data, 1):
        print(f"{y}:start:{disc.start:<4}positions:{disc.positions:<3}", end="")
        while (release_time + y + disc.start) % disc.positions:
            print(f"{release_time:3} ", end="")
            release_time += step
        step *= disc.positions
        print(f"click at {release_time}, step->{step}")
    return release_time


def solution2(input_data):
    input_data.append(Disc(start=0, positions=11))
    return find_release_time(input_data)


if __name__ == "__main__":
    run()

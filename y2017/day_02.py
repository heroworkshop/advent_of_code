from itertools import combinations

from aocd_tools import load_input_data


def run():
    input_data = load_input_data(2017, 2).split("\n")
    print("solution1 = ", solution1(input_data))
    print("solution2 = ", solution2(input_data))


def solution1(lines):
    total = 0
    for line in lines:
        values = [int(v) for v in line.split()]
        total += max(values) - min(values)
    return total

def find_exact_division(values):
    for a, b in [sorted(x) for x in combinations(values, 2)]:
        if b % a == 0:
            return b // a
    raise ValueError


def solution2(lines):
    total = 0
    for line in lines:
        values = [int(v) for v in line.split()]
        total += find_exact_division(values)
    return total

if __name__ == "__main__":
    run()

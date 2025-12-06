import time
from itertools import zip_longest

from aocd_tools import time_report
from y2025.day06_data import DATA

EXAMPLE = """
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   + 
""".strip()

def parse(data):
    lines = [line.strip() for line in data.strip().split("\n")]
    return lines


def part1():
    total = 0
    rows = parse(DATA)
    table = [row.split() for row in rows]
    for col in zip(*table):
        op = col[-1]
        result = int(col[0])
        for num in col[1:-1]:
            if op == "+":
                result += int(num)
            elif op == "*":
                result *= int(num)
        total += result
    return total


def part2():
    total = 0
    rows = [line for line in DATA.strip().split("\n")]
    table = [list(row) for row in rows]
    print(table)
    op = " "
    result = None
    for col in zip_longest(*table, fillvalue=" "):
        print(col)
        if col[-1] in "+*":
            op = col[-1]

        col_str = "".join(col[:-1]).strip()
        if col_str.strip()== "":
            total += result
            print(f"col result: {result}")
            result = None
            continue

        if result is None:
            result = int(col_str)
        else:
            if op == "+":
                result += int(col_str)
            elif op == "*":
                result *= int(col_str)
            print(f"col intermediate result: {result}")
            continue
    total += result
    print(f"col result: {result}")
    return total


if __name__ == "__main__":
    start_time = time.process_time()
    print("part1:", part1())
    print("part2:", part2())
    print(time_report(start_time))

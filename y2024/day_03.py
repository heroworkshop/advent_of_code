import re
from aocd_tools import *


EXAMPLE = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

def run():
    input_data = load_input_data(2024, 3)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    # entries = int_tuples_from_lines(lines=input_data, sep=" ")
    entries = input_data



    print(entries)

    for i, f in enumerate((solution1, solution2), 1):
        print(f"solution{i} = ", f(entries))


def process_one_line(line):
    try:
        return line[0] * line[1]
    except Exception:
        return 1


def solution1(entries):
    lines = extract_lines(entries)
    print(lines)
    return sum(process_one_line(line) for line in lines)


def solution2(entries):
    blocks = [line.split("don't()")[0] for line in entries.split("do()")]
    print(blocks)
    values = [sum(process_one_line(line) for line in extract_lines(lines)) for lines in blocks]
    print(values)
    return sum(values)


def extract_lines(entries):
    lines = []
    pattern = r"mul\((\d|\d{2}|\d{3}),(\d|\d{2}|\d{3})\)"
    for m in re.finditer(pattern, entries):
        lines.append((int(m[1]), int(m[2])))

    return lines


if __name__ == "__main__":
    run()

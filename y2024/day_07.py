import re
from aocd_tools import *


EXAMPLE = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

def run():
    input_data = load_input_data()
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    # entries = int_tuples_from_lines(lines=input_data, sep=" ")
    # a, b = entries.split("\n\n")
    entries = [process_one_line(line) for line in input_data.splitlines()]

    print(entries)

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(entries), time_report(start_time))


def process_one_line(line):
    a, b = line.split(":")
    return int(a), [int(x) for x in b.split(" ") if x]


def solution1(entries):
    total = 0
    for target, components in entries:
        op_count = len(components) - 1
        n = 2 ** op_count
        for i in range(n):
            pattern = bin(i)[2:].zfill(op_count)
            r = evaluate(pattern, components)
            if r == target:
                total += target
                print(f"{target} = {show(pattern, components)}")
                break
        else:
            print(target, ": x")

    return total

def solution2(entries):
    total = 0
    for target, components in entries:
        op_count = len(components) - 1
        n = 3 ** op_count
        for i in range(n):
            pattern = int_to_base3_string(i).zfill(op_count)
            r = evaluate3(pattern, components)
            if r == target:
                total += target
                print(f"{target} = {show3(pattern, components)}")
                break
        else:
            print(target, ": x")

    return total

def int_to_base3_string(n):
  """Converts an integer to its base 3 string representation.

  Args:
    n: The integer to convert.

  Returns:
    The base 3 string representation of n.
  """

  if n == 0:
    return '0'

  result = ''
  while n > 0:
    remainder = n % 3
    result = str(remainder) + result
    n //= 3

  return result

def show(pattern, components):
    s = str(components[0])
    for a,b in zip(pattern, components[1:]):
        op  = "+" if a == "1" else "*"
        s += f" {op} {b}"
    return s


OP3 = {
    "0": "*",
    "1": "+",
    "2": "||"
}
def show3(pattern, components):
    s = str(components[0])
    for a,b in zip(pattern, components[1:]):
        op  = OP3[a]
        s += f" {op} {b}"
    return s

def evaluate(pattern, components):
    total = components[0]
    for p, v in zip(pattern, components[1:]):
        if p == "1":
            total += v
        else:
            total *= v
    return total


def evaluate3(pattern, components):
    total = components[0]
    for p, v in zip(pattern, components[1:]):
        if p == "1":
            total += v
        elif p == "0":
            total *= v
        else:
            total = int(str(total) + str(v))
    return total


def extract_lines(entries):
    return entries.split("\n")


if __name__ == "__main__":
    run()

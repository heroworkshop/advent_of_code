from collections import deque, defaultdict
from functools import reduce

from aocd_tools import load_input_data, grid_from_lines

EXAMPLE = """<{([{{}}[<[[[<>{}]]]>[]]"""

SCORES = {")": 3,
          "]": 57,
          "}": 1197,
          ">": 25137}

COMPLETION_SCORES = {")": 1,
                     "]": 2,
                     "}": 3,
                     ">": 4}


def parse(line):
    return line


def run():
    input_data = load_input_data()
    # input_data  = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = [parse(line) for line in input_data.split("\n")]
    # grid = grid_from_lines(input_data, transform=int)
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(lines))


def find_error(line):
    brackets = {"(": ")", "{": "}", "[": "]", "<": ">"}
    stack = list()
    for ch in line:
        if ch in brackets:
            stack.append(ch)
        else:
            if brackets[stack[-1]] == ch:
                stack.pop(-1)
            else:
                return ch
    return None


def find_missing(line):
    brackets = {"(": ")", "{": "}", "[": "]", "<": ">"}
    stack = list()
    for ch in line:
        if ch in brackets:
            stack.append(ch)
        else:
            if brackets[stack[-1]] == ch:
                stack.pop(-1)
            else:
                raise RuntimeError("Invalid line")

    return [brackets[b] for b in reversed(stack)]


def solution1(lines):
    illegal_chars = [find_error(line) for line in lines]
    scores = [SCORES[illegal_char] for illegal_char in illegal_chars if illegal_char]
    return sum(scores)


def solution2(lines):
    valid_lines = [line for line in lines if not find_error(line)]

    scores = []
    for line in valid_lines:
        missing = find_missing(line)
        score = 0
        for m in missing:
            score *= 5
            score += COMPLETION_SCORES[m]
        scores.append(score)

    scores.sort()
    mid = len(scores) // 2
    return scores[mid]


if __name__ == "__main__":
    run()

import re
from collections import deque
from functools import cache

from aocd_tools import *
from dijkstra import Dijkstra, Step

EXAMPLE = """029A
980A
179A
456A
379A"""

INPUT_DATA = """319A
985A
340A
489A
964A"""


def run():
    input_data = INPUT_DATA
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")

    entries = input_data.splitlines()

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(entries), time_report(start_time))


def get_key_presses(initial_code, level_count=2):
    count = 0
    prev_key = "A"
    for ch in initial_code:
        results = get_level_1_directions(ch, prev_key)
        print(ch, results)
        count += dfs_get_level_2_directions(results[0], level_count)
        print(ch, count)
        prev_key = ch
    return count

@cache
def get_level_1_directions(initial_code, prev_key="A"):
    numeric_queue = deque([(initial_code, "", prev_key)])
    l1_results = []
    while numeric_queue:
        code, presses, start = numeric_queue.pop()
        if not code:
            l1_results.append(presses)
            continue
        next_key = code[0]
        paths = press_numeric(start, next_key)
        for path in paths:
            # print(start, next_key, path)
            numeric_queue.append((code[1:], presses + path + "A", next_key))
    return l1_results

@cache
def dfs_get_level_2_directions(initial_directions, level):
    if level == 0:
        # print(initial_directions)
        return len(initial_directions)
    from_key = "A"
    total = 0
    for ch in initial_directions:
        paths = press_direction(from_key, ch)
        total += dfs_get_level_2_directions(paths[0] + "A", level=level - 1)
        from_key = ch
    return total


def presses_from_path(path):
    result = ""
    p0 = path[0]
    for p in path[1:]:
        diff = p - p0
        result += DIRECTIONS[diff]
        p0 = p
    return result

NUMERIC_PAD = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "0": (1, 3),
    "A": (2, 3),
}


DIRECTION_PAD = {
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
}

DIRECTIONS = {
    (0, -1): "^",
    (-1, 0): "<",
    (0, 1): "v",
    (1, 0): ">",
}

@cache
def press_numeric(current, target):
    p0 = Pos(*NUMERIC_PAD[current])
    p1 = Pos(*NUMERIC_PAD[target])

    d = p1 - p0
    rl_moves = ""
    ud_moves = ""
    if d.x > 0:
        rl_moves += ">" * d.x
    elif d.x < 0:
        rl_moves += "<" * abs(d.x)
    if d.y < 0:
        ud_moves += "^" * abs(d.y)
    elif d.y > 0:
        ud_moves += "v" * d.y
    if ud_moves and rl_moves:
        if p0.y == 3 and p1.x ==0:
            return [ud_moves + rl_moves]
        if p0.x == 0 and p1.y == 3:
            return [rl_moves + ud_moves]
        if d.x < 0:
            return [rl_moves + ud_moves]
        else:
            return [ud_moves + rl_moves]
    if ud_moves:
        return [ud_moves]
    return [rl_moves]

@cache
def press_direction(current, target):
    p0 = Pos(*DIRECTION_PAD[current])
    p1 = Pos(*DIRECTION_PAD[target])

    d = p1 - p0
    rl_moves = ""
    ud_moves = ""
    if d.x > 0:
        rl_moves += ">" * d.x
    elif d.x < 0:
        rl_moves += "<" * abs(d.x)
    if d.y > 0:
        ud_moves += "v" * d.y
    elif d.y < 0:
        ud_moves += "^" * abs(d.y)
    if ud_moves and rl_moves:
        if p0.y == 0 and p1.x == 0:
            return [ud_moves + rl_moves]
        if p0.y == 1 and p0.x == 0:
            return [rl_moves + ud_moves]
        if d.x < 0:
            return [rl_moves + ud_moves]
        else:
            return [ud_moves + rl_moves]
    if ud_moves:
        return [ud_moves]
    return [rl_moves]



def solution1(entries):
    result = 0
    for line in entries:
        a = get_key_presses(line)
        b = int(line[:-1])
        m = a * b
        print(f"{line} {m} = {a}  {b}")
        result += m
    return result


def solution2(entries):
    result = 0
    for line in entries:
        a = get_key_presses(line, level_count=25)
        b = int(line[:-1])
        m = a * b
        print(f"{line} {m} = {a}  {b}")
        result += m
    return result


def extract_lines(entries):
    return entries.split("\n")


if __name__ == "__main__":
    run()

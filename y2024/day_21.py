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
    input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")

    entries = input_data.splitlines()

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(entries), time_report(start_time))


def get_key_presses(s):
    for numeric in s:
        paths = get_numeric_pad_paths(current_numeric, numeric)
    keys1 = directions_from_numeric(s)
    keys2 = indirect_keys_from_directions(keys1)
    keys3 = indirect_keys_from_directions(keys2)
    return keys3


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

def press_numeric(current, target):
    p0 = Pos(*NUMERIC_PAD[current])
    p1 = Pos(*NUMERIC_PAD[target])

    d = p1 - p0
    moves = ""
    if d.x > 0:
        moves += ">" * d.x
    if d.y < 0:
        moves += "^" * abs(d.y)
    if d.x < 0:
        moves += "<" * abs(d.x)
    if d.y > 0:
        moves += "v" * d.y
    return moves


def press_direction(current, target):
    p0 = Pos(*DIRECTION_PAD[current])
    p1 = Pos(*DIRECTION_PAD[target])

    d = p1 - p0
    moves = ""
    if d.x > 0:
        moves += ">" * d.x
    if d.y > 0:
        moves += "v" * d.y
    if d.y < 0:
        moves += "^" * abs(d.y)
    if d.x < 0:
        moves += "<" * abs(d.x)
    return moves








class Solver(Dijkstra):
    def __init__(self, start, end, valid_nodes):
        super().__init__(start)
        self.valid_nodes = valid_nodes
        self.end = end

    def is_win(self, state):
        return state == self.end

    def report(self):
        pass

    @staticmethod
    def serialise(state: Pos):
        return state

    @staticmethod
    def neighbours(state: Pos) -> list[Pos]:
        return [Pos(*p) for p in [(state.x + 1, state.y),
                                  (state.x - 1, state.y),
                                  (state.x, state.y + 1),
                                  (state.x, state.y - 1)]]

    def valid_moves(self, state) -> list[Step]:
        return [Step(1, p) for p in self.neighbours(state) if p in self.valid_nodes]

    def get_all_best_paths(self, start_pos, end_pos):
        paths = []
        queue = [(end_pos, deque())]
        while queue:
            pos, path = queue.pop(0)
            path.appendleft(pos)
            if pos == start_pos:
                paths.append(path)
            else:
                for node in self.nodes[pos].from_state:
                    queue.append((node, path.copy()))
        return paths

@cache
def get_numeric_pad_paths(start: str, finish: str):
    valid_nodes = set(Pos(*p) for p in NUMERIC_PAD.values())
    start_pos = Pos(*NUMERIC_PAD[start])
    end_pos = Pos(*NUMERIC_PAD[finish])
    solver = Solver(start_pos, end_pos, valid_nodes)
    solver.single_solution = False
    solver.search()
    return solver.get_all_best_paths(start_pos, end_pos)

@cache
def get_direction_pad_paths(start: str, finish: str):
    valid_nodes = set(Pos(*p) for p in DIRECTION_PAD.values())
    start_pos = Pos(*DIRECTION_PAD[start])
    end_pos = Pos(*DIRECTION_PAD[finish])
    solver = Solver(start_pos, end_pos, valid_nodes)
    solver.single_solution = False
    solver.search()
    return solver.get_all_best_paths(start_pos, end_pos)

def solution1(entries):
    result = 0
    for line in entries:
        keys = get_key_presses(line)
        a = len(keys)
        b = int(line[:-1])
        m = a * b
        print(f"{line} {keys} {m} = {a}  {b}")
        result += m
    return result


def solution2(entries):
    return 0


def extract_lines(entries):
    return entries.split("\n")


if __name__ == "__main__":
    run()

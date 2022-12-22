from collections import deque
from dataclasses import dataclass
from pprint import pprint
from typing import NamedTuple, List

from aocd_tools import load_input_data, Grid
from dijkstra import Dijkstra, Step

EXAMPLE = """1
2
-3
3
-2
0
4"""


def run():
    input_data = load_input_data(2022, 20)
    #input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    values = input_data.split("\n")
    entries = [int(n) for n in values]

    print("solution1 = ", solution1(entries))

    print("solution2 = ", solution2(entries))


class CircularBuffer:
    def __init__(self, entries):
        self.entries = entries
        self.idx_by_pos = {idx: idx for idx, val in enumerate(entries)}
        self.pos_by_idx = {idx: idx for idx, val in enumerate(entries)}

    def mix(self):
        print(f"initial: {self.ordered()}")
        check_values = set(self.entries)
        for idx in range(len(self.entries)):
            value = self.entries[idx]
            self.move_item(idx, value)
        assert set(self.ordered()) == check_values
            # print(f"{idx:7}: {self.ordered()}")

    def move_item(self, idx, by):
        move_from = self.pos_by_idx[idx] % len(self.entries)
        move_to = (move_from + by) % len(self.entries)
        dp = -1 if by < 0 else 1
        new_positions = {}
        new_positions[move_to % len(self.entries)] = self.idx_by_pos[move_from % len(self.entries)]
        p = move_to
        while p != move_from:
            v = self.idx_by_pos[p]
            p = (p - dp) % len(self.entries)
            new_positions[p] = v

        for p, i in new_positions.items():
            self.idx_by_pos[p] = i
            self.pos_by_idx[i] = p

    def ordered(self):
        return [self.entries[self.idx_by_pos[pos]] for pos in range(len(self.entries))]

    def get_at(self, p):
        v = self.entries[self.idx_by_pos[p % len(self.entries)]]
        print(v)
        return v


def solution1(entries):
    buffer = CircularBuffer(entries)
    buffer.mix()
    zero_index = buffer.entries.index(0)
    zero_p = buffer.pos_by_idx[zero_index]
    return sum(buffer.get_at(p + zero_p) for p in [1000, 2000, 3000])


def solution2(v):
    return


if __name__ == "__main__":
    run()

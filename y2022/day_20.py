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
    # input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    values = input_data.split("\n")
    entries = [int(n) for n in values]
    print(entries)

    print("solution1 = ", solution1(entries))

    print("solution2 = ", solution2(entries))


class SimpleCircularBuffer:
    def __init__(self, entries, m=1):
        self.entries = [(i, int(v) * m) for i, v in enumerate(entries)]

    def get_at(self, i):
        return self.entries[i % len(self.entries)]

    def find_by_index(self, i):
        for idx, pair in enumerate(self.entries):
            if i == pair[0]:
                return idx

    def find_by_value(self, i):
        for idx, pair in enumerate(self.entries):
            if i == pair[1]:
                return idx

    def mix(self):
        size = len(self.entries)
        for i in range(size):
            idx = self.find_by_index(i)
            v = self.entries.pop(idx)
            self.entries.insert((idx + v[1]) % len(self.entries), v)
            # print(self.values())

    def values(self):
        return [v[1] for v in self.entries]

    def grove_coordinates(self):
        zero_index = self.find_by_value(0)
        return [self.get_at(p + zero_index)[1] for p in [1000, 2000, 3000]]


def solution1(entries):
    buffer = SimpleCircularBuffer(entries)
    buffer.mix()
    return sum(buffer.grove_coordinates())


def solution2(entries):
    buffer = SimpleCircularBuffer(entries, 811589153)
    #print(f"initial: {buffer.values()}")
    for count in range(10):
        buffer.mix()
        #print(f"{count:3}: {buffer.values()}")
    return sum(buffer.grove_coordinates())


if __name__ == "__main__":
    run()

from collections import deque
from dataclasses import dataclass
from typing import NamedTuple, List

from aocd_tools import load_input_data, Grid, Pos
from dijkstra import Dijkstra, Step

EXAMPLE = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


def run():
    input_data = load_input_data(2022, 12)
    # input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    values = input_data.split("\n")
    start, end, grid = parse(values)
    # print(grid.render())
    print(start)
    print(end)

    print("solution1 = ", solution1(start, end, grid))

    # print("solution2 = ", solution2(end, grid))


def parse(values: List[str]):
    grid = Grid()
    starting_position = None
    end_position = None
    for y, row in enumerate(values):
        for x, ch in enumerate(row):
            if ch == "E":
                end_position = (x, y)
                ch = "z"
            elif ch == "S":
                starting_position = (x, y)
                ch = "a"
            grid.add((x, y), ord(ch) - ord("a"))
    grid.update_bounds()
    return starting_position, end_position, grid


def extract_last_int(line):
    return int(line.split()[-1])


class Solver(Dijkstra):
    def __init__(self, grid, start, end):
        initial_state = Pos(*start)
        self.end = Pos(*end)
        self.grid = grid
        super().__init__(initial_state)

    @staticmethod
    def serialise(state: Pos):
        return state

    def score(self, state: Pos) -> int:
        """Lower is better. 0 is winner"""
        return abs(self.end.x - state.x) + abs(self.end.y - state.y)
        # return 0 if self.end == state else 1

    def valid_moves(self, state) -> List[Step]:
        moves = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            p = Pos(state.x + dx, state.y + dy)
            if p not in self.grid.grid:
                continue
            if self.grid.at(p) - self.grid.at(state) > 1:
                continue
            moves.append(Step(cost=1, state=p))
        return moves

    def report(self):
        if self.iterations % self.report_rate:
            return
        for y in self.grid.y_vals:
            row = []
            for x in self.grid.x_vals:
                base_chr = 'A' if (x, y) in self.visited else 'a'
                ch = chr(self.grid.at((x, y)) + ord(base_chr))
                row.append(ch)
            print("".join(row))
        print()


def solution1(start, end, grid):
    return find_shortest(end, grid, start)


def find_shortest(end, grid, start):
    solver = Solver(grid, start, end)
    n = solver.search()
    print("Time taken: ms", solver.time_taken * 1000)
    percent = len(solver.visited) / len(grid.grid) * 100
    print("nodes visited:", len(solver.visited), f"({percent:.0f}%)")
    return n


def solution2(end, grid):
    distances = set()
    for start, elevation in grid.grid.items():
        if elevation == 0:
            print(start)
            distances.add(find_shortest(end, grid, start))
    return min(distances)


if __name__ == "__main__":
    run()

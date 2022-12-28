from collections import deque
from contextlib import suppress
from copy import deepcopy
from dataclasses import dataclass
from typing import NamedTuple, List

from aocd_tools import load_input_data, Grid, Pos
from dijkstra import Dijkstra, Step

EXAMPLE = """
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""[1:]

EX0 = """
#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#"""[1:]

DIRECTIONS = {">": Pos(1, 0),
              "<": Pos(-1, 0),
              "v": Pos(0, 1),
              "^": Pos(0, -1),
              "0": Pos(0, 0)
              }
NEIGHBOURS = list(DIRECTIONS.values())


class Blizzard:
    def __init__(self, p: Pos, ch: str):
        self.p = p
        self.ch = ch
        self.d = DIRECTIONS[ch]
        self.reset_p = None

    def move(self, grid: Grid):
        self.p = self.p + self.d
        if grid.at(self.p) == "#":
            self.p = self.reset_position(grid)

    def reset_position(self, grid):
        if self.reset_p is not None:
            return self.reset_p
        self.reset_p = self.p - self.d
        while grid.at(self.reset_p - self.d) != "#":
            self.reset_p = self.reset_p - self.d
        return self.reset_p


@dataclass
class State:
    player: Pos
    time: int

    def __lt__(self, other):
        return False


class Solver(Dijkstra):
    def __init__(self, initial_state, end_pos: Pos, grid, blizzards: List[Blizzard]):
        self.end_pos = end_pos
        self.grid = grid
        self.width = self.grid.width - 2
        self.height = self.grid.height - 2
        self.blizzard_dict = {b.p: b.ch for b in blizzards}
        super().__init__(initial_state)

    @staticmethod
    def serialise(state: State):
        return state.player, state.time

    def score(self, state: State) -> int:
        """Lower is better. 0 is winner"""
        return abs(state.player.x - self.end_pos.x) + abs(state.player.y - self.end_pos.y)

    def valid_moves(self, state) -> List[Step]:
        steps = []
        t = state.time + 1
        for n in NEIGHBOURS:
            # with suppress(KeyError):
            #     if blizzard_dict[state.player] == Pos(-n.x, -n.y):
            #         continue
            p = state.player + n
            if p.y < -1:
                # print(f"{p} < y=-1")
                continue
            if p in self.grid.grid:
                # print(f"{p} in grid")
                continue
            x, y = p
            if self.blizzard_dict.get(Pos((x + t) % self.width, y), ".") == "<":
                # print(f"{p} overlaps row with < blizzard at t={t}")
                continue
            if self.blizzard_dict.get(Pos((x - t) % self.width, y), ".") == ">":
                # print(f"{p} overlaps row with < blizzard at t={t}")
                continue
            if self.blizzard_dict.get(Pos(x, (y + t) % self.height), ".") == "^":
                # print(f"{p} overlaps column with ^ blizzard at t={t}")
                continue
            if self.blizzard_dict.get(Pos(x, (y - t) % self.height), ".") == "v":
                # print(f"{p} overlaps column with v blizzard at t={t}")
                continue

            # print(f"adding {p} at t={t}")
            steps.append(Step(cost=1, state=State(p, t)))
        return steps

    def queue_new_moves(self, move):
        for cost, new_move_state in self.valid_moves(move.state):
            new_step_count = move.step_count + cost
            if self.serialise(new_move_state) in self.visited:
                self.duplicates += 1
                continue
            if new_step_count + self.score(move.state) >= self.best:
                self.pruned += 1
                continue
            self.add_move(new_step_count, new_move_state, move.path)


def run():
    input_data = load_input_data(2022, 24)
    # input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    grid, start_pos, end_pos, blizzards = make_grid(input_data)
    print(render(grid, blizzards, start_pos))
    print(f"start={start_pos}, end={end_pos}")
    print("solution1 = ", solution1(grid, start_pos, end_pos, blizzards))

    grid, start_pos, end_pos, blizzards = make_grid(input_data)
    print("solution2 = ", solution2(grid, start_pos, end_pos, blizzards))


def make_grid(s):
    start_pos = None
    end_pos = None
    blizzards = []
    grid = Grid(default_val=".")
    for y, row in enumerate(s.split("\n"), -1):
        for x, ch in enumerate(row, -1):
            p = Pos(x, y)
            if y == -1 and ch == ".":
                start_pos = Pos(x, y)
            if ch == ".":
                end_pos = Pos(x, y)
            if ch == "#":
                grid.add(p, ch)
            if ch in "<>^v":
                blizzards.append(Blizzard(p, ch))
                # grid.add(p, ch)
    grid.update_bounds()
    return grid, start_pos, end_pos, blizzards


def solution1(grid, start_pos, end_pos, blizzards):  # < 349
    initial_state = State(start_pos, 0)
    solver = Solver(initial_state, end_pos, grid, blizzards)
    solver.store_path = True
    result = solver.search()
    for state in solver.best_path:
        print(state.player)
        print(render_at_t(state.time, grid, blizzards, state.player))
    return result


def solution2(grid, start_pos, end_pos, blizzards):  # 811 > n > 562
    initial_state1 = State(start_pos, 0)
    solver = Solver(initial_state1, end_pos, grid, blizzards)
    stage_1 = solver.search()
    initial_state2 = State(end_pos, stage_1)
    solver = Solver(initial_state2, start_pos, grid, blizzards)
    stage_2 = solver.search()
    initial_state3 = State(start_pos, stage_2+stage_1)
    solver = Solver(initial_state3, end_pos, grid, blizzards)
    stage_3 = solver.search()
    print(f"stages: {stage_1} {stage_2} {stage_3}")
    return stage_1 + stage_2 + stage_3


def render(grid: Grid, blizzards: List[Blizzard], player: Pos):
    rows = []
    blizzard_dict = {b.p: b.ch for b in blizzards}
    for y in range(-1, grid.height-1):
        row = ""
        for x in range(-1, grid.width -1):
            p = Pos(x, y)
            if p == player:
                row += "@"
            elif p in blizzard_dict:
                row += blizzard_dict[p]
            else:
                row += grid.at(p)
        rows.append(row)
    return "\n".join(rows)

def render_at_t(t: int, grid: Grid, blizzards: List[Blizzard], player: Pos):
    rows = []
    width = grid.width - 2
    height = grid.height - 2
    blizzard_dict = {b.p: b.ch for b in blizzards}
    for y in range(-1, grid.height-1):
        row = ""
        for x in range(-1, grid.width - 1):
            p = Pos(x, y)
            if p == player:
                row += "@"
            elif x == -1 or x == grid.x_bounds[1] or y == -1 or y == grid.y_bounds[1]:
                row += grid.at(p)
            elif blizzard_dict.get(Pos((x + t) % width, y), ".") == "<":
                row += "<"
            elif blizzard_dict.get(Pos((x - t) % width, y), ".") == ">":
                row += ">"
            elif blizzard_dict.get(Pos(x, (y + t) % height), ".") == "^":
                row += "^"
            elif blizzard_dict.get(Pos(x, (y - t) % height), ".") == "v":
                row += "v"
            else:
                row += grid.at(p)
        rows.append(row)
    return "\n".join(rows)

if __name__ == "__main__":
    run()

import math
import re
import time
from collections import defaultdict
from pprint import pprint
from typing import NamedTuple

import dijkstra
from aocd_tools import load_input_data, grid_from_lines, time_report, Pos, NEIGHBOURS, Grid
from dijkstra import Dijkstra
from y2024.day_18 import single

EXAMPLE = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""


def run():
    input_data = load_input_data()
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    entries = grid_from_lines(input_data, default_val=" ")
    print(entries.render())
    start, end, nodes = make_maze(entries)

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(start, end, nodes, entries), time_report(start_time))



class State(NamedTuple):
    pos: Pos


class Solver(Dijkstra):
    def __init__(self, start, end, valid_nodes):
        initial_state = State(start)
        super().__init__(initial_state)
        self.end = end
        self.valid_nodes = valid_nodes

    def is_win(self, state) -> bool:
        return state.pos == self.end

    def valid_moves(self, state: State) -> list[dijkstra.Step]:
        moves = []
        for d in NEIGHBOURS:
            new_p = Pos(*state.pos) + Pos(*d)
            if new_p in self.valid_nodes:
                moves.append(dijkstra.Step(1, State(new_p, )))

        return moves


def solution1(start, end, nodes, grid):
    return 0
    max_shortcut = 2
    print(f"{start=}, {end=}, {nodes=}")
    solver = Solver(start, end, nodes)
    base_cost = solver.search()
    print(f"{base_cost=}")
    print(render_path(grid, solver.nodes))
    path = solver.get_best_path(State(end), State(start))
    # print(path)
    count = 0
    # (7, 7) -> (5, 7)
    saving_tally = defaultdict(int)
    for i, p_start in enumerate(path[:-max_shortcut]):
        for p_end in path[i+1:]:
            # if p_start.pos == Pos(7, 7) and p_end.pos == Pos(5, 7):
            #     print(f"{p_start.pos} -> {p_end.pos}")
            shortcut_length = manhattan(p_start.pos, p_end.pos)
            if  shortcut_length <= max_shortcut:
                length = len(path)
                i_end = path.index(p_end)
                i_start = path.index(p_start)
                # print(f"{i_end=} {i_start=} {length=}")
                # print(f"section1 = {i_start} + section2 {length - i_end} = {length - i_end + i_start}")
                new_length = length - i_end + i_start + shortcut_length
                saving = length - new_length
                # print(f"{saving=}")
                saving_tally[saving] += 1
                if saving >= 100:
                    count += 1
    print(saving_tally)
    for i in range(100):
        if i in saving_tally:
            print(f"{saving_tally[i]} cheats save {i} picoseconds")
    return count


def manhattan(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def solution2(start, end, nodes, grid):
    max_shortcut = 20
    print(f"{start=}, {end=}, {nodes=}")
    solver = Solver(start, end, nodes)
    base_cost = solver.search()
    print(f"{base_cost=}")
    print(render_path(grid, solver.nodes))
    path = solver.get_best_path(State(end), State(start))
    # print(path)
    count = 0
    saving_tally = defaultdict(int)
    for i, p_start in enumerate(path[:-max_shortcut]):
        for p_end in path[i+1:]:
            shortcut_length = manhattan(p_start.pos, p_end.pos)
            if  shortcut_length <= max_shortcut:
                length = len(path)
                i_end = path.index(p_end)
                i_start = path.index(p_start)
                # print(f"{i_end=} {i_start=} {length=}")
                # print(f"section1 = {i_start} + section2 {length - i_end} = {length - i_end + i_start}")
                new_length = length - i_end + i_start + shortcut_length
                saving = length - new_length
                # print(f"{saving=}")
                saving_tally[saving] += 1
                if saving >= 100:
                    count += 1
    print(saving_tally)
    for i in range(100):
        if i in saving_tally:
            print(f"{saving_tally[i]} cheats save {i} picoseconds")
    return count


def make_maze(grid: Grid):
    nodes = set()
    for p, v in grid.grid.items():
        if v != "#":
            nodes.add(p)
        if v == "S":
            start = Pos(*p)
        elif v == "E":
            end = Pos(*p)
    return start, end, nodes


def render_path(grid: Grid, path: dict):
    lines = []
    for y in range(grid.height):
        line = ""
        for x in range(grid.width):
            s =State(Pos(x, y))
            if s in path:
                line += single(str(path[s].cost))
            else:
                line += grid.at((x, y))
        lines.append(line)
    return "\n".join(lines)


def render_all_paths(grid: Grid, path: set):
    # pprint(path)
    lines = []
    for y in range(grid.height):
        line = ""
        for x in range(grid.width):
            if (x, y) in path:
                line += "O"
            else:
                line += grid.at((x, y))
        lines.append(line)
    return "\n".join(lines)


if __name__ == "__main__":
    run()

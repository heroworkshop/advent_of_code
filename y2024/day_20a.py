import math
import re
from pprint import pprint

import dijkstra
from aocd_tools import *
from dijkstra import Dijkstra

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
    entries = grid_from_lines(input_data, default_val=".")
    print(entries.render())
    start, end, walls = make_maze(entries)

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(start, end, walls, entries), time_report(start_time))



class State(NamedTuple):
    pos: Pos


class Solver(Dijkstra):
    def __init__(self, start, end, walls):
        initial_state = State(start)
        super().__init__(initial_state)
        self.end = end
        self.walls = walls
        self.store_path = True

    @staticmethod
    def serialise(state):
        return state

    def is_win(self, state) -> bool:
        return state.pos == self.end

    def valid_moves(self, state: State) -> list[dijkstra.Step]:
        moves = []
        for d in NEIGHBOURS:
            new_p = Pos(*state.pos) + Pos(*d)
            if new_p not in self.walls:
                moves.append(dijkstra.Step(1, State(new_p, )))

        return moves


def solution1(start, end, walls, grid):
    print(f"{start=}, {end=}, {walls=}")
    solver = Solver(start, end, walls)
    base_cost = solver.search()
    print(f"{base_cost=}")

    bricks = list(walls)
    count = 0
    rwall = [b for b in bricks if b[0] == grid.width-1]
    print("rwall size=", len(rwall))
    for brick in bricks:
        if brick[0] in (0, grid.width-1):
            continue
        if brick[1] in (0, grid.height-1):
            continue
        new_walls = {w for w in walls if w != brick}
        solver = Solver(start, end, new_walls)
        cost = solver.search()
        if cost != base_cost:
            print(base_cost, cost, base_cost - cost)
        if cost + 100 <= base_cost:
            count += 1


    # print(render_path(grid, solver.best_path))
    return count





def solution2(start, end, walls, grid):
    return 0


def make_maze(grid: Grid):
    walls = set()
    for p, v in grid.grid.items():
        if v == "#":
            walls.add(p)
        elif v == "S":
            start = Pos(*p)
        elif v == "E":
            end = Pos(*p)
    return start, end, walls


R = {
    1: "v",
    3: "^",
    0: ">",
    2: "<",
}


def render_path(grid: Grid, path: list):
    pprint(path)
    steps = {p.pos: p.rotation for p in path}
    lines = []
    for y in range(grid.height):
        line = ""
        for x in range(grid.width):
            if (x, y) in steps:
                line += R[steps[(x, y)]]
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

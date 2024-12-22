import math
import re
from pprint import pprint
from typing import Tuple

import dijkstra
from aocd_tools import *
from dijkstra import Dijkstra

EXAMPLE = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

EXAMPLE2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

EXAMPLE3 = """
##############
#    #       #
#  #   ##### #
#  #   #   # #
#  #   #   # #
#  #   #   # #
#  #####   # #
#  #   #   # #
#  #   #   # #
#  #   #   # #
#S   #   #  E#
##############""".strip()


def run():
    input_data = load_input_data()
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    entries = grid_from_lines(input_data, default_val=".")
    # print(entries.render())
    start, end, walls = make_maze(entries)

    valid_nodes = get_nodes(grid_from_lines(input_data, default_val=" "))


    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(start, end, walls, entries), time_report(start_time))


ROTATIONS = [
    (1, 0),  # EAST
    (0, 1),  # SOUTH
    (-1, 0),  # WEST
    (0, -1),  # NORTH
]


class State(NamedTuple):
    pos: Pos
    rotation: int


class Solver(Dijkstra):
    def __init__(self, initial_state, end, walls):
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
        # move forward
        d = Pos(*ROTATIONS[state.rotation])
        new_p = state.pos + d
        if new_p not in self.walls:
            moves.append(dijkstra.Step(1, State(new_p, state.rotation)))

        # turn right
        moves.append(
            dijkstra.Step(1000, State(state.pos, (state.rotation + 1) % 4))
        )
        # turn left
        moves.append(
            dijkstra.Step(1000, State(state.pos, (state.rotation - 1) % 4))
        )
        return moves


def solution1(start, end, walls, grid):
    return 0
    solver = Solver(State(start, 0), end, walls)
    cost = solver.search()
    print(render_path(grid, solver.get_best_path()))
    return cost


def solution2(start, end, walls, grid):
    solver = Solver(State(start, 0), end, walls)
    solver.single_solution = False
    cost = solver.search()
    # print(render_path(grid, solver.get_best_path()))
    all_paths = solver.get_all_best_path_states(end, start)
    return len(all_paths)


def make_maze(grid: Grid):
    walls = set()
    for p, v in grid.grid.items():
        if v == "#":
            walls.add(p)
        elif v == "S":
            start = Pos(*p)
        elif v == "E":
            end = Pos(*p)
            end = Pos(*p)
    return start, end, walls


def get_nodes(grid: Grid):
    nodes = set()
    for p, v in grid.grid.items():
        if v == ".":
            nodes.add(p)
        elif v == "S":
            start = Pos(*p)
            nodes.add(p)
        elif v == "E":
            nodes.add(p)
            end = Pos(*p)
    return nodes




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

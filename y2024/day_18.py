import math
import re
from pprint import pprint

import dijkstra
from aocd_tools import *
from dijkstra import Dijkstra

EXAMPLE="""5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

def run():
    input_data = load_input_data()
    input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    entries = int_tuples_from_lines(input_data, ",")
    # print(entries.render())
    start, end, walls = (0,0), (6,6), make_maze(entries)

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(start, end, walls, entries), time_report(start_time))


class State(NamedTuple):
    pos: Pos

class Solver(Dijkstra):
    def __init__(self, initial_state, end, walls, size):
        super().__init__(initial_state)
        self.end=end
        self.walls = walls
        self.store_path=False
        self.size = size

    @staticmethod
    def serialise(state):
        return state

    def is_win(self, state) -> bool:
        return state.pos == self.end

    def valid_moves(self, state: State) -> list[dijkstra.Step]:
        moves = []
        for d in NEIGHBOURS:
            new_p = state.pos + d
            if new_p[0]>-1 and new_p[0] < self.size[0] and new_p[1]>-1 and new_p[1]<self.size[1]:
                if new_p not in self.walls:
                    moves.append(dijkstra.Step(1, State(new_p,)))

        return moves


def solution1(start, end, walls, grid):
    solver = Solver(State(start), end, walls, (6,6))
    cost = solver.search()
    # print(render_path(grid, solver.best_path))
    # nodes = set()
    # for c, path in solver.paths:
    #     if c == cost:
    #         for p in path:
    #             nodes.add(p.pos)
    #         print("node_count=", len(nodes))
    # print(render_all_paths(grid, nodes))
    # print("solution2=", len(nodes))
    return cost


def solution2(start, end, walls, grid):
    return 0


def make_maze(lines):
    return {(x,y) for x,y in lines}


def render_path(grid: Grid, path: list):
    pprint(path)
    steps = {p.pos: p.rotation for p in path}
    lines = []
    for y in range(grid.height):
        line =  ""
        for x in range(grid.width):
            if (x,y) in steps:
                line += R[steps[(x,y)]]
            else:
                line += grid.at((x,y))
        lines.append(line)
    return "\n".join(lines)

def render_all_paths(grid: Grid, path: set):
    pprint(path)
    lines = []
    for y in range(grid.height):
        line =  ""
        for x in range(grid.width):
            if (x,y) in path:
                line += "O"
            else:
                line += grid.at((x,y))
        lines.append(line)
    return "\n".join(lines)

if __name__ == "__main__":
    run()

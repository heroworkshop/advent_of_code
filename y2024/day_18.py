import math
import re
from pprint import pprint

import dijkstra
from aocd_tools import *
from dijkstra import Dijkstra

EXAMPLE = """5,4
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
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    entries = int_tuples_from_lines(input_data, ",")
    # print(entries.render())
    start, end, walls = (0, 0), (70, 70), make_maze(entries)

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(start, end, walls, entries), time_report(start_time))


class State(NamedTuple):
    pos: Pos


class Solver(Dijkstra):
    def __init__(self, initial_state, end, walls):
        super().__init__(initial_state)
        self.end = end
        self.walls = walls
        self.store_path = False

    @staticmethod
    def serialise(state):
        return state

    def is_win(self, state) -> bool:
        return state.pos == self.end

    def valid_moves(self, state: State) -> list[dijkstra.Step]:
        moves = []
        for d in NEIGHBOURS:
            new_p = Pos(*state.pos) + Pos(*d)
            if -1 < new_p[0] <= self.end[0] and -1 < new_p[1] <= self.end[1]:
                if new_p not in self.walls:
                    moves.append(dijkstra.Step(1, State(new_p, )))

        return moves

    def render(self):
        return ""
        lines = []
        for y in range(self.end[1] + 1):
            line = ""
            for x in range(self.end[0] + 1):
                state = State(Pos(x,y))
                if (x, y) in self.walls:
                    ch = "#"
                elif state in self.nodes:
                    ch = single(self.nodes[state])
                else:
                    ch = "."
                line += ch
            lines.append(line)
        return "\n".join(lines)

    def report(self):
        if self.iterations % self.report_rate:
            return
        super().report()
        print(self.render())

def single(i):
    return str(i)[-1]


def solution1(start, end, walls, grid):
    walls = set(walls[:1024])
    print(render(walls, end))
    solver = Solver(State(start), end, walls)
    cost = solver.search()
    return cost


def solution2(start, end, blocks, grid):
    walls = set()
    for block in blocks:
        walls.add(block)
        solver = Solver(State(start), end, walls)
        cost = solver.search()
        print(block, cost)
        if cost == math.inf:
            return block


def make_maze(lines):
    return [Pos(x, y) for x, y in lines]


def render(walls: set[tuple[int, int]], end: tuple[int, int]):
    lines = []
    for y in range(end[1]+1):
        line = ""
        for x in range(end[0]+1):
            ch = "#" if (x, y) in walls else"."
            line += ch
        lines.append(line)
    return "\n".join(lines)



if __name__ == "__main__":
    run()

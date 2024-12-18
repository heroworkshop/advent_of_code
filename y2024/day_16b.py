import heapq
import math
import re
from pprint import pprint

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
    input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    entries = grid_from_lines(input_data, default_val=".")
    # print(entries.render())
    start, end, nodes = make_maze(entries)

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(start, end, nodes, entries), time_report(start_time))

ROTATIONS = [
    (1, 0),  # EAST
    (0, 1),  # SOUTH
    (-1, 0),  # WEST
    (0, -1),  # NORTH
]

class State(NamedTuple):
    score: int
    pos: Pos
    rotation: int

class Solver(Dijkstra):
    def __init__(self, initial_state, end, walls):
        super().__init__(initial_state)
        self.end=end
        self.walls = walls
        self.store_path=True

    @staticmethod
    def serialise(state):
        return state

    def is_win(self, state) -> bool:
        return state.pos == self.end

def valid_moves(nodes: dict[Pos, int], state: State) -> list[State]:
    moves = []
    # move forward
    d = Pos(*ROTATIONS[state.rotation])
    new_p = state.pos + d
    if new_p in nodes:
        moves.append(State(state.score + 1, new_p, state.rotation))

    # turn right
    moves.append(State(state.score + 1000, state.pos, (state.rotation+1)%4)
    )
    # turn lett
    moves.append(State(state.score + 1000, state.pos, (state.rotation-1)%4))
    return moves


def solution1(start, end, nodes: dict[Pos, int], grid):
    best_path = set()
    visited = set()
    queue = []
    state = State(0, start, 0)
    heapq.heappush(queue, state)
    while queue:
        state = heapq.heappop(queue)
        if (state.pos, state.rotation) in visited:
            continue
        if state.pos == end:
            return state[0]
        moves = valid_moves(nodes, state)
        for move in moves:
            queue.append(move)
        visited.add((state.pos, state.rotation))
        print(state.pos, state.rotation)

    print(render_path(grid, best_path))
    return state.score



def solution2(start, end, walls, grid):
    return 0

def make_maze(grid: Grid):
    nodes = {}
    for p, v in grid.grid.items():
        if v == ".":
            nodes[p] = math.inf
        elif v =="S":
            start = Pos(*p)
        elif v == "E":
            end = Pos(*p)
            end = Pos(*p)
    return start, end, nodes

R= {
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
        line =  ""
        for x in range(grid.width):
            if (x,y) in steps:
                line += R[steps[(x,y)]]
            else:
                line += grid.at((x,y))
        lines.append(line)
    return "\n".join(lines)

if __name__ == "__main__":
    run()

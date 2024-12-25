import math
from typing import List, Tuple, NamedTuple

from dijkstra import Dijkstra, Step


class Pos(NamedTuple):
    x: int
    y: int


class GridSolver(Dijkstra):
    def __init__(self, initial_state, walls, end):
        super().__init__(initial_state)
        self.walls = walls
        self.end = end
        self.size = Pos(8, 8)

    def is_win(self, state):
        return state == self.end

    def report(self):
        pass

    @staticmethod
    def serialise(state: Pos):
        return state

    @staticmethod
    def neighbours(state: Pos) -> List[Pos]:
        return [Pos(*p) for p in [(state.x + 1, state.y),
                                  (state.x - 1, state.y),
                                  (state.x, state.y + 1),
                                  (state.x, state.y - 1)]]

    def valid_moves(self, state) -> List[Step]:
        return [Step(1, p) for p in self.neighbours(state) if p not in self.walls and self.in_bounds(p)]

    def in_bounds(self, state: Pos) -> bool:
        if state.x <0 or state.x >= self.size.x or state.y < 0 or state.y >= self.size.y:
            return False
        return True
def test_dijkstra__with_empty_grid__takes_direct_path():
    walls = {}
    start_pos = Pos(2, 2)
    solver = GridSolver(start_pos, walls, Pos(0, 0))
    steps = solver.search()
    assert steps == 4


def test_dijkstra__with_wall__goes_round_wall():
    #  ....
    #  .#X.
    #  .#..
    #  0#..
    #  ....
    walls = {(1, 1), (1, 2), (1, 3)}
    start_pos = Pos(0, 3)
    end_pos = (2, 1)
    solver = GridSolver(start_pos, walls, end_pos)
    steps = solver.search()
    assert steps == 6


def test_dijkstra__with_no_path__returns_inf():
    #  .###
    #  .#0#
    #  .###
    #  X...
    #  ....
    walls = {(1, 0), (2, 0), (3, 0),(1, 1), (3, 1), (1, 2), (2, 2), (3, 2)}
    start_pos = Pos(2, 1)
    end_pos = Pos(0, 3)
    solver = GridSolver(start_pos, walls, end_pos)
    steps = solver.search()
    assert steps == math.inf

def test_dijkstra__with_corner__cannot_go_through_corner():
    #  ....
    #  .#X.
    #  ..#..
    #  0#..
    #  ....
    walls = {(1, 1), (2, 2), (1, 3)}
    start_pos = Pos(0, 3)
    end_pos = Pos(2, 1)
    solver = GridSolver(start_pos, walls, end_pos)
    solver.store_path = True
    steps = solver.search()
    assert steps == 6
    path = solver.get_best_path(end_pos, start_pos)
    assert len(path) == 7

def test_dijkstra_with_all_paths():
    walls = {(1, 1)}
    start_pos = Pos(0, 1)
    end_pos = Pos(2, 1)
    solver = GridSolver(start_pos, walls, end_pos)
    solver.store_path = True
    steps = solver.search()
    assert steps == 4
    path = solver.get_best_path(end_pos, start_pos)
    assert len(path) == 5  # includes start and end
    all_paths = solver.get_all_best_path_states(end_pos, start_pos)
    assert(len(all_paths)) == 3 + 3 + 2

from typing import List, Tuple, NamedTuple

from dijkstra import Dijkstra, Step


class Pos(NamedTuple):
    x: int
    y: int


class GridSolver(Dijkstra):
    def __init__(self, initial_state, walls):
        super().__init__(initial_state)
        self.walls = walls

    def report(self):
        pass

    @staticmethod
    def serialise(state: Pos):
        return state

    @staticmethod
    def score(state: Pos) -> int:
        """Lower is better. 0 is winner"""
        return abs(state.x) + abs(state.y)

    @staticmethod
    def neighbours(state: Pos) -> List[Pos]:
        return [Pos(*p) for p in [(state.x + 1, state.y),
                                 (state.x - 1, state.y),
                                 (state.x, state.y + 1),
                                 (state.x, state.y - 1)]]

    def valid_moves(self, state) -> List[Step]:
        return [Step(1, p) for p in self.neighbours(state) if p not in self.walls]


def test_dijkstra__with_empty_grid__takes_direct_path():
    walls = {}
    start_pos = Pos(2, 2)
    solver = GridSolver(start_pos, walls)
    steps = solver.search()
    assert steps == 4

def test_dijkstra__with_wall__goes_round_wall():
    #  ....
    #  .#X.
    #  .#..
    #  0#..
    #  ....
    walls = {(1, 0), (1, 1), (1, 2)}
    start_pos = Pos(2, 2)
    solver = GridSolver(start_pos, walls)
    solver.store_path = True
    steps = solver.search()
    assert len(solver.best_path) == 6
    assert steps == 6
    assert set(solver.best_path).intersection(walls) == set()

from typing import List, Tuple, NamedTuple

from dijkstra import Dijkstra, Move


class Pos(NamedTuple):
    x: int
    y: int


class GridSolver(Dijkstra):
    def __init__(self, initial_state, walls, end):
        super().__init__(initial_state, end)
        self.walls = walls

    def report(self):
        pass

    def is_win(self, state) -> bool:
        return self.end == state

    @staticmethod
    def neighbours(state: Pos) -> List[Pos]:
        return [Pos(*p) for p in [(state.x + 1, state.y),
                                 (state.x - 1, state.y),
                                 (state.x, state.y + 1),
                                 (state.x, state.y - 1)]]

    def valid_moves(self, state) -> List[Move]:
        return [Move(1, p) for p in self.neighbours(state) if p not in self.walls]


def test_dijkstra__with_empty_grid__takes_direct_path():
    walls = {}
    start_pos = Pos(0, 0)
    solver = GridSolver(start_pos, walls, Pos(2, 2))
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
    end_pos = Pos(2, 1)
    solver = GridSolver(start_pos, walls, end_pos)
    steps = solver.search()
    # assert len(solver.best_path) == 6
    assert steps == 6
    # assert set(solver.best_path).intersection(walls) == set()

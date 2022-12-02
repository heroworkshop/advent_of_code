import unittest
from typing import List, Tuple, NamedTuple

from assertpy import assert_that

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


class TestDijkstra(unittest.TestCase):
    def test_dijkstra_withEmptyGrid_takesDirectPath(self):
        walls = {}
        start_pos = Pos(2, 2)
        solver = GridSolver(start_pos, walls)
        steps = solver.search()
        assert_that(steps).is_equal_to(4)

    def test_dijkstra_withWall_goesRoundWall(self):
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
        assert_that(steps).is_equal_to(6)
        assert_that(solver.best_path).is_length(6)
        assert_that(set(solver.best_path).intersection(walls)).is_empty()


if __name__ == '__main__':
    unittest.main()

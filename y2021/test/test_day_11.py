import unittest

from assertpy import assert_that

from y2016.day_11 import ElevatorSolver, State


class TestSolver(unittest.TestCase):
    def test_score_withOneItemPerLevel_returnsSumOfLevels(self):
        state = State(3, [{"a"}, {"b"}, {"c"}, {"d"}])
        solver = ElevatorSolver(state)
        score = solver.score(state)
        assert_that(score).is_equal_to(1 + 2 + 3)

    def test_score_withAllItemsAtLevel0_returnsZero(self):
        state = State(3, [{"a", "b", "c", "d"}, set(), set(), set()])
        solver = ElevatorSolver(state)
        score = solver.score(state)
        assert_that(score).is_equal_to(0)

    def test_is_valid_withProtectedChip_returnsTrue(self):
        floors = [{"CuG", "CuM", "AuG"}]
        solver = ElevatorSolver(State(3, floors))
        result = solver.is_valid(floors)
        assert_that(result).is_true()

    def test_is_valid_withUnProtectedChip_returnsFalse(self):
        floors = [{"AuM", "CuM", "AuG"}]
        solver = ElevatorSolver(State(3, floors))
        result = solver.is_valid(floors)
        assert_that(result).is_false()

    def test_is_valid_withChipOnDifferentFloorFromItsGenerator_returnsFalse(self):
        floors = [{"CuM", "AuG"}, {"CuG"}]
        solver = ElevatorSolver(State(3, floors))
        result = solver.is_valid(floors)
        assert_that(result).is_false()

    def test_is_valid_withNoChips_returnsTrue(self):
        floors = [{"AgG", "CuG", "AuG"}]
        solver = ElevatorSolver(State(3, floors))
        result = solver.is_valid(floors)
        assert_that(result).is_true()

    def test_is_valid_withChipsOnDifferentFloor_returnsTrue(self):
        floors = [{"AgG", "CuG", "AuG"}, {"AuM"}, {"CuM"}]
        solver = ElevatorSolver(State(3, floors))
        result = solver.is_valid(floors)
        assert_that(result).is_true()

    def test_is_valid(self):
        floors = [set(), {'LG'}, {'HG', 'HM'}, {'LM'}]
        solver = ElevatorSolver(State(3, floors))
        result = solver.is_valid(floors)
        assert_that(result).is_true()


if __name__ == '__main__':
    unittest.main()

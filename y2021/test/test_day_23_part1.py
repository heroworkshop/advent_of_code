import unittest

from y2021.day_23_part1 import distance, check_path, Amphipod, solution1, completion_score


class TestDay23(unittest.TestCase):
    def test_distance(self):
        self.assertEqual(4, distance(0, 0))
        self.assertEqual(6, distance(4, 6))
        self.assertEqual(3, distance(6, 4))
        self.assertEqual(10, distance(6, 0))

    # diagram
    """
    #############
    #01.2.3.4.56#
    ###1#3#5#7###
      #0#2#4#6#
      #########
    """
    def test_check_path_withClearPath(self):
        hallway = [None] * 7
        rooms = [1, None, None, None, None, None, None, None]
        result = check_path(0, 0, hallway, rooms)
        self.assertTrue(result)

    def test_check_path_withBlockedPathInRoom(self):
        hallway = [None] * 7
        rooms = [1, 2, None, None, None, None, None, None]
        result = check_path(0, 0, hallway, rooms)
        self.assertFalse(result)

    def test_check_path_withBlockedPathInHallway(self):
        hallway = [None] * 7
        hallway[1] = 3
        rooms = [1, None, None, None, None, None, None, None]
        result = check_path(0, 0, hallway, rooms)
        self.assertFalse(result)


    def test_check_path_withBusyButUnblockedLeftPathInHallway(self):
        hallway = [None, None, 1, 2, 3, 4, 5]
        rooms = [1, None, None, None, None, None, None, None]
        result = check_path(0, 0, hallway, rooms)
        self.assertTrue(result)

    def test_check_path_withBusyButUnblockedRightPathInHallway(self):
        hallway = [1, 2, None, 2, 3, 4, 5]
        rooms = [1, None, None, None, None, None, None, None]
        result = check_path(3, 0, hallway, rooms)
        self.assertTrue(result)

    def test_check_path_withBlockedRightPathInHallway(self):
        hallway = [1, 2, None, None, None, 2, None]
        rooms = [1, None, None, None, None, None, None, None]
        result = check_path(6, 0, hallway, rooms)
        self.assertFalse(result)

    def test_solution_withSingleEntityTakesDirectPath(self):
        amphipods = [
            Amphipod(6, 1, [0, 1], "A"),  # A
        ]
        result = solution1(amphipods)
        self.assertEqual(10, result)

    def test_solution_withTwoEntitiesSameType(self):
        amphipods = [
            Amphipod(6, 1, [0, 1], "A"),  # A
            Amphipod(7, 1, [0, 1], "A"),  # A
        ]
        result = solution1(amphipods)
        self.assertEqual(18, result)

    def test_solution_withTwoEntitiesDifferentType(self):
        amphipods = [
            Amphipod(6, 1, [0, 1], "A"),
            Amphipod(7, 10, [2, 3], "B"),
        ]
        result = solution1(amphipods)
        self.assertEqual(70 + 10, result)

    def test_solution_withFourEntitiesBlocking(self):
        amphipods = [
            Amphipod(1, 1, [0, 1], "A"),
            Amphipod(0, 10, [2, 3], "B"),
            Amphipod(3, 10, [2, 3], "B"),
            Amphipod(2, 1, [0, 1], "A"),
        ]
        result = solution1(amphipods)
        self.assertEqual(112, result)

    def test_score_with3Complete(self):
        amphipods = [
            Amphipod(1, 1, [0, 1], "A"),
            Amphipod(2, 10, [2, 3], "B"),
            Amphipod(0, 1, [0, 1], "A"),
        ]
        rooms = [0, 2, 1, None, None, None, None, None]
        result = completion_score(rooms, amphipods)
        self.assertEqual(3, result)

    def test_score_withBaseRoomWrong(self):
        amphipods = [
            Amphipod(-1, 1, [0, 1], "A"),
            Amphipod(-1, 10, [2, 3], "B"),
        ]
        rooms = [1, 0, 1, None, None, None, None, None]
        result = completion_score(rooms, amphipods)
        self.assertEqual(1, result)

    def test_solution_withThreeEntitiesBlocking(self):
        amphipods = [
            Amphipod(1, 1, [0, 1], "A"),
            Amphipod(0, 10, [2, 3], "B"),
            Amphipod(2, 1, [0, 1], "A"),
        ]
        result = solution1(amphipods)
        self.assertEqual(72, result)


if __name__ == '__main__':
    unittest.main()

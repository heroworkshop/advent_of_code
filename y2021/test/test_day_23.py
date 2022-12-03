import unittest

from y2021.day_23 import distance, check_path, Amphipod, solution1, completion_score, make_room_to_room_move


class TestDay23(unittest.TestCase):
    def test_distance(self):
        self.assertEqual(6, distance(0, 0))
        self.assertEqual(10, distance(4, 6))
        self.assertEqual(5, distance(6, 4))
        self.assertEqual(6, distance(6, 0))

    # diagram
    """
    #############
    #01.2.3.4.56#
    ###3#7#b#f###
      #2#6#a#e#
      #1#5#9#d#
      #0#4#8#c#
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
            Amphipod(12, 1, [0, 1, 2, 3], "A"),  # A
        ]
        result = solution1(amphipods)
        self.assertEqual(14, result)

    def test_solution_withTwoEntitiesSameType(self):
        amphipods = [
            Amphipod(12, 1, [0, 1, 2, 3], "A"),  # A
            Amphipod(13, 1, [0, 1, 2, 3], "A"),  # A
        ]
        result = solution1(amphipods)
        self.assertEqual(13 + 13, result)

    def test_solution_withTwoEntitiesDifferentType(self):
        amphipods = [
            Amphipod(12, 1, [0, 1, 2, 3], "A"),
            Amphipod(13, 10, [4, 5, 6, 7], "B"),
        ]
        result = solution1(amphipods)
        self.assertEqual(110 + 14, result)

    def test_solution_withFourEntitiesBlocking(self):
        amphipods = [
            Amphipod(1, 1, [0, 1, 2, 3], "A"),
            Amphipod(0, 10, [4, 5, 6, 7], "B"),
            Amphipod(2, 10, [4, 5, 6, 7], "B"),
            Amphipod(3, 1, [0, 1, 2, 3], "A"),
        ]
        result = solution1(amphipods)
        self.assertEqual(3 + 80 + 4 + 90 + 5 + 5, result)

    def test_score_with3Complete(self):
        amphipods = [
            Amphipod(1, 1, [0, 1, 2, 3], "A"),
            Amphipod(2, 10, [4, 5, 6, 7], "B"),
        ]
        rooms = [0, 0, 1, None, 1, None, None, None]
        result = completion_score(rooms, amphipods)
        self.assertEqual(3, result)

    def test_score_withBaseRoomWrong(self):
        amphipods = [
            Amphipod(-1, 1, [0, 1, 2, 3], "A"),
            Amphipod(-1, 10, [4, 5, 6, 7], "B"),
        ]
        rooms = [1, 0, 0, 0, 1, None, None, None]
        result = completion_score(rooms, amphipods)
        self.assertEqual(1, result)

    def test_solution_withThreeEntitiesBlocking(self):
        amphipods = [
            Amphipod(4, 1, [0, 1, 2, 3], "A"),
            Amphipod(5, 1, [0, 1, 2, 3], "A"),
            Amphipod(0, 10, [4, 5, 6, 7], "B"),
        ]
        result = solution1(amphipods)
        self.assertEqual(6 + 5 + 100 + 4 + 7, result)

    def test_solution_withFourRooms(self):
        amphipods = [
            Amphipod(4, 1, [0, 1, 2, 3], "A"),
            Amphipod(12, 10, [4, 5, 6, 7], "B"),
            Amphipod(0, 100, [8, 9, 10, 11], "C"),
            Amphipod(8, 1000, [12, 13, 14, 15], "D"),
        ]
        result = solution1(amphipods)
        self.assertEqual(7+120+1200+10000+5, result)

    def test_make_room_to_room_move_withMovingRight(self):
        amphipods = [
            Amphipod(-1, 1, [12, 13, 14, 15], "D"),
        ]
        hallway = [None] * 7
        for start, expected in {0: 14, 4: 12, 8: 10}.items():
            rooms = [None] * 16
            rooms[start] = 1
            move = make_room_to_room_move(amphipods, 0, 0, hallway, start, 12, rooms)
            self.assertEqual(expected, move.energy)

    def test_make_room_to_room_move_withMovingLeft(self):
        amphipods = [
            Amphipod(-1, 1, [0, 1, 2, 3], "A"),
            Amphipod(-1, 10, [4, 5, 6, 7], "B"),
        ]
        hallway = [None] * 7
        for start, expected in {4: 10, 8: 12, 12: 14}.items():
            rooms = [None] * 16
            rooms[start] = 0
            move = make_room_to_room_move(amphipods, 0, 0, hallway, start, 0, rooms)
            self.assertEqual(expected, move.energy)

    def test_make_room_to_room_move_withMovingLeftToSecondSlot(self):
        amphipods = [
            Amphipod(-1, 1, [0, 1, 2, 3], "A"),
            Amphipod(-1, 10, [4, 5, 6, 7], "B"),
        ]
        hallway = [None] * 7
        rooms = [None] * 16
        rooms[0] = 0
        rooms[4] = 0
        move = make_room_to_room_move(amphipods, 0, 0, hallway, 4, 1, rooms)
        self.assertEqual(9, move.energy)

    def test_make_room_to_room_move_withBlockedRoom_returnsNone(self):
        amphipods = [
            Amphipod(-1, 1, [0, 1, 2, 3], "A"),
            Amphipod(-1, 10, [4, 5, 6, 7], "B"),
        ]
        hallway = [None] * 7
        rooms = [None] * 16
        rooms[5] = 1
        rooms[4] = 0
        move = make_room_to_room_move(amphipods, 0, 0, hallway, 4, 0, rooms)
        self.assertEqual(None, move)

    def test_make_room_to_room_move_withBlockedHallway_returnsNone(self):
        amphipods = [
            Amphipod(-1, 1, [0, 1, 2, 3], "A"),
            Amphipod(-1, 10, [4, 5, 6, 7], "B"),
        ]
        hallway = [None] * 7
        rooms = [None] * 16
        hallway[2] = 1
        rooms[4] = 0
        move = make_room_to_room_move(amphipods, 0, 0, hallway, 4, 0, rooms)
        self.assertEqual(None, move)


if __name__ == '__main__':
    unittest.main()

import unittest

from y2021.day_23_retry import GameBoard, Room, Amphipod, run


class TestGameBoard(unittest.TestCase):
    def test_str_withEmptyBoard(self):
        board = GameBoard()
        expected = ("#############\n"
                    "#...........#\n"
                    "###.#.#.#.###\n"
                    "###.#.#.#.###\n"
                    "###.#.#.#.###\n"
                    "###.#.#.#.###")
        self.assertEqual(expected, str(board))

    def test_str_withFilledBoard(self):
        board = GameBoard()
        for ch in "DCBA":
            board.rooms[0].push(ch)
        for ch in "HGFE":
            board.rooms[1].push(ch)
        for ch in "LKJI":
            board.rooms[2].push(ch)
        for ch in "PONM":
            board.rooms[3].push(ch)

        expected = ("#############\n"
                    "#...........#\n"
                    "###A#E#I#M###\n"
                    "###B#F#J#N###\n"
                    "###C#G#K#O###\n"
                    "###D#H#L#P###")
        self.assertEqual(expected, str(board))

    def test_str_withHalfFilledBoard(self):
        board = GameBoard()
        for ch in "DC":
            board.rooms[0].push(ch)
        for ch in "HG":
            board.rooms[1].push(ch)
        for ch in "LK":
            board.rooms[2].push(ch)
        for ch in "PO":
            board.rooms[3].push(ch)

        expected = ("#############\n"
                    "#...........#\n"
                    "###.#.#.#.###\n"
                    "###.#.#.#.###\n"
                    "###C#G#K#O###\n"
                    "###D#H#L#P###")
        self.assertEqual(expected, str(board))

    def test_str_withFilledHallway(self):
        board = GameBoard(hallway="AB.C.D.E.FG")

        expected = ("#############\n"
                    "#AB.C.D.E.FG#\n"
                    "###.#.#.#.###\n"
                    "###.#.#.#.###\n"
                    "###.#.#.#.###\n"
                    "###.#.#.#.###")
        self.assertEqual(expected, str(board))

    def test_hash_withDifferentBoards(self):
        b1 = GameBoard(rooms=("A",))
        b2 = GameBoard()
        self.assertEqual(2, len({b1, b2}))

    def test_hash_withIdenticalBoards(self):
        b1 = GameBoard(rooms=("A",))
        b2 = GameBoard(rooms=("A",))
        self.assertEqual(1, len({b1, b2}))

    def test_moves_withMultipleSingles(self):
        b = GameBoard(rooms=("D", "C", "B", "A"))
        moves = b.moves(0)
        self.assertEqual(7 * 4, len(moves))

    def test_moves_withOneOccupant(self):
        b = GameBoard(rooms=("B",))
        moves = b.moves(0)
        self.assertEqual(7, len(moves))
        energies = {m.energy for m in moves}
        self.assertEqual({60, 50, 50, 70, 90, 110, 120}, energies)

    def test_moves_withOneFullRoom(self):
        b = GameBoard(rooms=("DDDA",))
        moves = b.moves(0)
        self.assertEqual(7, len(moves))
        energies = {m.energy for m in moves}
        self.assertEqual({3, 2, 2, 4, 6, 8, 9}, energies)

    def test_moves_withOccupantInHome_returnsNoMoves(self):
        b = GameBoard(rooms=("A",))
        moves = b.moves(0)
        self.assertEqual(0, len(moves))

    def test_moves_withHallwayOccupant_returnsOneMove(self):
        b = GameBoard(hallway="A")
        moves = b.moves(0)
        energies = {m.energy for m in moves}
        self.assertEqual({6}, energies)

    def test_moves_with2UnblockedHallwayOccupants_returns2Moves(self):
        b = GameBoard(hallway="A..B")
        moves = b.moves(0)
        energies = {m.energy for m in moves}
        self.assertEqual({6, 50}, energies)

    def test_moves_with1UnblockedBHallwayOccupant_returns1Move(self):
        b = GameBoard(hallway="AB")
        moves = b.moves(0)
        energies = {m.energy for m in moves}
        self.assertEqual({70}, energies)

    def test_moves_with2BlockedCHallwayOccupant_returnsNoMoves(self):
        b = GameBoard(hallway="...C.A")
        moves = b.moves(0)
        self.assertEqual(0, len(moves))

    def test_moves_with2BlockedDAHallwayOccupant_returnsNoMoves(self):
        b = GameBoard(hallway="...D.A")
        moves = b.moves(0)
        self.assertEqual(0, len(moves))

    def test_moves_withRoomDHallwayBlockedByAs_returnsNoMoves(self):
        b = GameBoard(hallway="AA.A..", rooms=("D",))
        moves = b.moves(0)
        self.assertEqual(0, len(moves))

    def test_moves_withBlockedHallway_returnsNoMoves(self):
        b = GameBoard(hallway="AA.A.A.A.AA", rooms=("B", "B", "B", "B"))
        moves = b.moves(0)
        self.assertEqual(0, len(moves))

    def test_is_winner_withSingleA(self):
        b = GameBoard(rooms=("A",))
        self.assertTrue(b.is_winner())

    def test_is_winner_with4As(self):
        b = GameBoard(rooms=("AAAA",))
        self.assertTrue(b.is_winner())

    def test_is_winner_withOneWrongPiece(self):
        b = GameBoard(rooms=("AAAA", "C"))
        self.assertFalse(b.is_winner())

    def test_path_clear(self):
        b = GameBoard(rooms=("B",), hallway=".A")
        self.assertFalse(b.path_clear(0, 0))
        self.assertTrue(b.path_clear(1, 0))
        self.assertTrue(b.path_clear(2, 0))


class TestRoom(unittest.TestCase):
    def test_empty_withEmptyRoom_returnsTrue(self):
        self.assertTrue(Room().empty())

    def test_depth_with_fullRoom_returnsZero(self):
        r = Room("ABCD")
        self.assertEqual(0, r.depth)


class TestAmphipod(unittest.TestCase):
    def test_is_home_withEmptyMatchingRoom(self):
        room = Room()
        a = Amphipod("A")
        self.assertTrue(a.is_home(room, 0))

    def test_is_home_withFilledSameMatchingRoom(self):
        room = Room("AAA")
        a = Amphipod("A")
        self.assertTrue(a.is_home(room, 0))

    def test_is_home_withFilledDifferentMatchingRoom(self):
        room = Room("BBA")
        a = Amphipod("A")
        self.assertFalse(a.is_home(room, 0))


class TestSolver(unittest.TestCase):
    def test_withOneAmphipod(self):
        state = "", "A"
        result = run(state)
        self.assertEqual(10, result)

    def test_withOneAmphipod(self):
        state = "D", ""
        result = run(state)
        self.assertEqual(14000, result)

    def test_withTwoAmphipodsAB(self):
        state = "B", "A"
        result = run(state)
        self.assertEqual(7 + 100 + 5, result)

    def test_withTwoAmphipodsABBlocking(self):
        state = "BA",
        result = run(state)
        self.assertEqual(4 + 100 + 5, result)

    def test_withTwoAmphipodsCD(self):
        state = "C", "D"
        result = run(state)
        self.assertEqual(1200 + 12000, result)

    def test_withFourAmphipodsAAAA(self):
        state = "", "AAAA"
        result = run(state)
        self.assertEqual(7 * 4, result)

    def test_withFourAmphipodsAAAA(self):
        state = "", "", "DDDD"
        result = run(state)
        self.assertEqual(7000 * 4, result)

    def test_withFourRoomCDBA(self):
        state = "D", "C", "B", "A"
        result = run(state)
        self.assertEqual(11 + 14000 + 70 + 1000 + 50 + 5, result)


if __name__ == '__main__':
    unittest.main()

import unittest
from y2020.day_24 import process_input, solution1


class TestDay24(unittest.TestCase):
    def test_solution1_with_stepOutStepIn(self):
        instructions = [
            "wewe",
            "ewew",
            "neswnesw",
            "swneswne",
            "nwsenwse",
            "senwsenw"
        ]
        for moves in instructions:
            result = solution1(process_input(moves))
            self.assertEqual(1, result)

    def test_solution1_with_stepOutStepInStepOut(self):
        instructions = [
            "wew",
            "ewe",
            "neswne",
            "swnesw",
            "nwsenw",
            "senwse"
        ]
        for moves in instructions:
            result = solution1(process_input(moves))
            self.assertEqual(1, result)

    def test_solution1_with_twoFlips(self):
        instructions = [
            "wew",
            "ewe",
            "neswne",
            "swnesw",
            "nwsenw",
            "senwse"
        ]
        for moves in instructions:
            result = solution1(process_input(f"{moves}\n{moves}"))
            self.assertEqual(2, result)

    def test_solution1_withCircle(self):
        instructions = [
            "wnese",
            "enwsw",
            "nwswseenenw",
        ]
        for moves in instructions:
            result = solution1(process_input(moves))
            self.assertEqual(1, result)

    def test_solution1_withTwoCircles(self):
        instructions = [
            "nwswseenenw\nswswenenw",
        ]
        for moves in instructions:
            result = solution1(process_input(moves))
            self.assertEqual(0, result)


if __name__ == '__main__':
    unittest.main()

import unittest

from day01 import parse, GridWalker


class TestGridWalker(unittest.TestCase):
    def test_follow_instructions_withCircularPath_returnsToStart(self):
        input_data = "R1, R1, R1, R1"
        instructions = [parse(line) for line in input_data.split(",")]
        distance = GridWalker().follow_instructions(instructions)
        self.assertEqual(0, distance)

class TestUniquePointGridWalker(unittest.TestCase):
    def test_follow_instructions_withCircularPath_returnsToStart(self):
        input_data = "R1, R1, R1, R1"
        instructions = [parse(line) for line in input_data.split(",")]
        distance = GridWalker().follow_instructions(instructions)
        self.assertEqual(0, distance)

if __name__ == '__main__':
    unittest.main()

import unittest

from y2020.day_14 import parse, Computer, ComputerMk2

M1 = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0""".strip()

M2 = """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""".strip()

class TestDay14(unittest.TestCase):
    def test_parse(self):
        lines = parse(M1)
        self.assertEqual(4, len(lines))

    def test_run(self):
        computer = Computer()
        computer.run(parse(M1))
        self.assertEqual(165, sum(computer.memory.values()))

    def test_run_mk2(self):
        computer = ComputerMk2()
        computer.run(parse(M2))
        self.assertEqual(208, sum(computer.memory.values()))

if __name__ == '__main__':
    unittest.main()

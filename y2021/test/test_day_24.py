import unittest

from y2021.day_24 import Alu, parse_raw_program


class TestAlu(unittest.TestCase):
    def test_run_withBitsProgram(self):
        program = """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2"""
        program = parse_raw_program(program)
        alu = Alu([10])
        alu.run(program)
        self.assertEqual(0, alu.registers["z"])
        self.assertEqual(1, alu.registers["y"])
        self.assertEqual(0, alu.registers["x"])
        self.assertEqual(1, alu.registers["w"])

        alu = Alu([256 + 8 + 4])
        alu.run(program)
        self.assertEqual(0, alu.registers["z"])
        self.assertEqual(0, alu.registers["y"])
        self.assertEqual(1, alu.registers["x"])
        self.assertEqual(1, alu.registers["w"])

    def test_run_withNumberCompareProgram(self):
        program = """inp z
inp x
mul z 3
eql z x"""
        program = parse_raw_program(program)
        alu = Alu([1,3])
        alu.run(program)
        self.assertEqual(1, alu.registers["z"])

        alu = Alu([1,4])
        alu.run(program)
        self.assertEqual(0, alu.registers["z"])

        alu = Alu([111, 333])
        alu.run(program)
        self.assertEqual(1, alu.registers["z"])

if __name__ == '__main__':
    unittest.main()

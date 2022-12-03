from collections import defaultdict, namedtuple
from contextlib import suppress

from aocd_tools import load_input_data


EXAMPLE = """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""


class BunnyMachine:
    def __init__(self, program):
        self.registers = defaultdict(int)
        self.program = program
        self.pc = 0

    def get_value(self, x):
        with suppress(ValueError):
            return int(x)
        return self.registers[x]

    def cpy(self, x, y):
        self.registers[y] = self.get_value(x)

    def inc(self, x):
        self.registers[x] += 1

    def dec(self, x):
        self.registers[x] -= 1

    def jnz(self, x, y):
        if self.get_value(x) == 0:
            return
        self.pc += self.get_value(y) - 1

    def execute(self, line):
        op_code = line[0]
        params = line[1:]

        f = getattr(self, op_code)
        f(*params)

    def run(self):
        while self.pc < len(self.program):
            self.execute(self.program[self.pc])
            self.pc += 1

        return self.registers["a"]


def parse(line):
    return line.split()


def run():
    input_data = load_input_data()
    # input_data  = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = [parse(line) for line in input_data.split("\n")]
    # lines = grid_from_lines(input_data, transform=int)
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(lines))


def solution1(lines):
    return BunnyMachine(lines).run()


def solution2(lines):
    m = BunnyMachine(lines)
    m.registers["c"] = 1
    return m.run()


if __name__ == "__main__":
    run()

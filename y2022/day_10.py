from typing import NamedTuple, List

from aocd_tools import load_input_data

EX0 = """noop
addx 3
addx -5"""

EXAMPLE = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


class Instruction(NamedTuple):
    opcode: int
    parameters: List[int]


class ClockCircuit:
    def __init__(self):
        self.x = 1
        self.cycle = 0
        self.signal_strength = [self.x]
        self.rows = []
        self.row = ""
        self.crt_pos = 0

    def current_pixel(self):
        return "#" if self.crt_pos in [self.x-1, self.x, self.x+1] else "."

    def render_pixel(self):
        self.row += self.current_pixel()
        self.crt_pos += 1
        if len(self.row) == 40:
            self.rows.append(self.row)
            self.row = ""
            self.crt_pos = 0


    def run(self, program: List[Instruction]):
        operations = {
            "noop": self.noop,
            "addx": self.addx
        }
        for instruction in program:
            operations[instruction.opcode](*instruction.parameters)


    def noop(self):
        self.clock_tick()

    def addx(self, v):
        self.clock_tick()
        self.clock_tick()
        self.x += v

    def clock_tick(self):
        self.render_pixel()
        self.cycle += 1
        self.signal_strength.append(self.x * self.cycle)

        print(f"{self.cycle:3}{self.crt_pos:3}{self.x:4}{self.signal_strength[self.cycle]:6} {self.row}")


def run():
    input_data = load_input_data(2022, 10)
    #input_data = EXAMPLE
    # input_data = EX0

    print(f"loaded input data ({len(input_data)} bytes)")

    values = input_data.split("\n")
    values = [parse(line) for line in values]
    print(values[:50])

    print("solution1 = ", solution1(values))

    print("solution2 = ", solution2(values))


def parse(line: str) -> Instruction:
    parts = line.split()
    op = parts.pop(0)
    parameters = [int(s) for s in parts]
    return Instruction(op, parameters)



def solution1(values: List[Instruction]):
    circuit = ClockCircuit()
    circuit.run(values)
    signals = [circuit.signal_strength[t] for t in range(20, 260, 40)]
    print(signals)
    for line in circuit.rows:
        print(line)
    return sum(signals)


def solution2(values):
    return


if __name__ == "__main__":
    run()

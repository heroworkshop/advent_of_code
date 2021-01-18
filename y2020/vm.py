from collections import namedtuple


class GameBoy:
    def __init__(self, program):
        self.program = program
        self.pc = 0
        self.accumulator = 0
        self.lines_run = set()
        self.debug = False

    def run(self):
        instruction_table = {
            "jmp": self.jmp,
            "acc": self.acc,
            "nop": self.nop
        }
        while True:
            if self.pc in self.lines_run:
                self.on_repeated_instruction()
            try:
                line = self.program[self.pc]
            except IndexError:
                break

            if self.debug:
                print(line)
            self.lines_run.add(self.pc)

            try:
                instruction_table[line.op](line.params)
            except KeyError:
                raise RuntimeError(f"Invalid instruction {line.op}")

            self.pc += 1

    def jmp(self, params):
        self.pc += int(params[0]) - 1

    def acc(self, params):
        self.accumulator += int(params[0])

    def nop(self, params):
        pass

    def on_repeated_instruction(self):
        raise RepeatedInstruction(self.accumulator)


def parse_lines(lines):
    return [parse_line(line) for line in lines]


def parse_line(line):
    parts = line.split()
    return Instruction(parts[0], parts[1:])


Instruction = namedtuple("instruction", "op params")


class RepeatedInstruction(RuntimeError):
    pass
from aocd_tools import load_input_data


class VChip:
    OPCODES = {
        "addr", "addi",
        "mulr", "muli",
        "banr", "bani",
        "borr", "bori",
        "gtir", "gtri", "gtrr",
        "eqir", "eqri", "eqrr"
    }

    def exec(self, opcode, a, b, c):
        getattr(self, opcode)(a, b, c)

    def __init__(self, registers=None, n_registers=4):
        self.registers = registers.copy() if registers else [0] * n_registers

    def addr(self, a, b, c):
        self.registers[c] = self.registers[a] + self.registers[b]

    def addi(self, a, b, c):
        self.registers[c] = self.registers[a] + b

    def mulr(self, a, b, c):
        self.registers[c] = self.registers[a] * self.registers[b]

    def muli(self, a, b, c):
        self.registers[c] = self.registers[a] * b

    def banr(self, a, b, c):
        self.registers[c] = self.registers[a] & self.registers[b]

    def bani(self, a, b, c):
        self.registers[c] = self.registers[a] & b

    def borr(self, a, b, c):
        self.registers[c] = self.registers[a] | self.registers[b]

    def bori(self, a, b, c):
        self.registers[c] = self.registers[a] | b

    def gtir(self, a, b, c):
        self.registers[c] = 1 if a > self.registers[b] else 0

    def gtri(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] > b else 0

    def gtrr(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0

    def eqir(self, a, b, c):
        self.registers[c] = 1 if a == self.registers[b] else 0

    def eqri(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] == b else 0

    def eqrr(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0


def parse(line):
    def registers(s):
        _, _, vstr = before.strip("]").partition("[")
        return [int(v) for v in vstr.split(",")]

    before, bytecode, after = line.split("\n")
    return registers(before), [int(i) for i in bytecode.split(" ")], registers(after)


def run():
    input_data = load_input_data(2018, 16)
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = [parse(line) for line in input_data.split("\n\n") if line.strip()]
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(lines))


def solution1(lines):
    valid_opcodes = []
    for before, bytecode, after in lines:
        valid = []
        for opcode in VChip.OPCODES:
            chip = VChip(before)
            chip.exec(opcode, bytecode[1], bytecode[2], bytecode[3])
            if chip.registers == after:
                valid.append(opcode)
        valid_opcodes.append(valid)
    return [len(valids) for valids in valid_opcodes]


def solution2(lines):
    return


if __name__ == "__main__":
    run()

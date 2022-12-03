from collections import defaultdict, namedtuple, deque
from contextlib import suppress

from aocd_tools import load_input_data

EXAMPLE = """"""


class Alu:

    def __init__(self, input_buffer):
        self.registers = defaultdict(int)
        self.input_buffer = deque(input_buffer)

    def exec(self, opcode, params):
        getattr(self, opcode)(*params)

    def add(self, a, b):
        b = self.interpret_params(b)
        self.registers[a] += b

    def mod(self, a, b):
        b = self.interpret_params(b)
        self.registers[a] = self.registers[a] % b

    def mul(self, a, b):
        b = self.interpret_params(b)
        self.registers[a] *= b

    def div(self, a, b):
        b = self.interpret_params(b)
        self.registers[a] = self.registers[a] // b

    def eql(self, a, b):
        b = self.interpret_params(b)
        self.registers[a] = int(self.registers[a] == b)

    def inp(self, w):
        self.registers[w] = self.input_buffer.popleft()

    def interpret_params(self, b):
        try:
            b = int(b)
        except ValueError:
            b = self.registers[b]
        return b

    def run(self, program):
        for op_code, params in program:
            self.exec(op_code, params)
        return self.registers["z"] == 0


def parse(line):
    parts = line.split()
    return parts[0], parts[1:]


def parse_raw_program(raw):
    return [parse(line) for line in raw.split("\n") if line]


def run():
    input_data = load_input_data()
    # input_data  = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    # lines = parse_raw_program(input_data)
    # lines = grid_from_lines(input_data, transform=int)
    print("solution1 = ", solution1(input_data))
    print("solution2 = ", solution2(input_data))


class Solver:
    def __init__(self, program):
        self.program = program
        self.cache = {}

    def solve(self, input_value, z_register):
        # with suppress(KeyError):
        #     return self.cache[(input_value, z_register)]
        alu = Alu([input_value])
        alu.registers["z"] = z_register
        alu.run(self.program)
        # self.cache[(input_value, z_register)] = alu.registers["z"]
        return alu.registers["z"]


class NativeSolver:
    def __init__(self, level):
        consts = [
            (26, 1, 10, 25, 2),
            (26, 1, 10, 25, 4),
            (26, 1, 14, 25, 8),
            (26, 1, 11, 25, 7),
            (26, 1, 14, 25, 12),
            (26, 26, -14, 25, 7),
            (26, 26, 0, 25, 10),
            (26, 1, 10, 25, 14),
            (26, 26, -10, 25, 2),
            (26, 1, 13, 25, 6),
            (26, 26, -12, 25, 8),
            (26, 26, -3, 25, 11),
            (26, 26, -11, 25, 5),
            (26, 26, -2, 25, 11),
        ]
        self.c = consts[level]

    def solve(self, w, z):
        c = self.c
        # mul x 0
        # add x z
        # mod x 26
        x = z % c[0]
        # div z 1
        z = z // c[1]
        # add x 10
        x += c[2]
        # eql x w
        # eql x 0
        x = int(x != w)
        # mul y 0
        # add y 25
        # mul y x
        # add y 1
        y = c[3] * x + 1
        # mul z y
        z *= y
        # mul y 0
        # add y w
        # add y 2
        # mul y x
        # add z y
        z += (w + c[4]) * x
        return z


def make_sub_solvers(input_data):
    parts = [parse_raw_program("inp" + part) for part in input_data.split("inp") if part]
    return [NativeSolver(level) for level, part in enumerate(parts)]


def rev_solve(solvers):
    max_z = 10000000
    zvals = defaultdict(dict)
    zvals[14][0] = ""
    for level in reversed(range(14)):
        print(f"level {level}")
        found = False
        for z in range(max_z):
            if z % (max_z / 100) == 0:
                print("#" if found else ".", end="")
                found = False
            for inp_val in reversed(range(1, 10)):
                result = solvers[level].solve(inp_val, z)
                if result in zvals[level + 1]:
                    found = True
                    zvals[level][z] = str(inp_val) + zvals[level + 1][result]
        print(f"\nzvals: {len(zvals[level])}")
        if len(zvals[level]) < 20:
            print(zvals[level])
        del zvals[level + 1]

    combinations = [int(v) for v in zvals[0].values()]
    return min(combinations)


def solution1(lines):
    solvers = make_sub_solvers(lines)
    return rev_solve(solvers)


def solution1b(lines):
    model_number = 19998707849208

    solvers = make_sub_solvers(lines)

    while True:
        input_buffer = [int(ch) for ch in f"{model_number}"]
        if "0" in input_buffer:
            continue
        z_val = 0
        for input_val, solver in zip(input_buffer, solvers):
            z_val = solver.solve(input_val, z_val)

        if z_val == 0:
            break
        if model_number % 9999 == 0:
            print(model_number, z_val)
        model_number -= 1

    return model_number


def solution2(lines):
    return None


if __name__ == "__main__":
    run()

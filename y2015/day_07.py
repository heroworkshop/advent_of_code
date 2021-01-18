from contextlib import suppress

from aocd_tools import load_input_data

EXAMPLE = """
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i""".strip()


class Wire:
    def __init__(self, v1, op=None, v2=None):
        self.guess = 1
        self.v1 = v1
        self.op = op
        self.v2 = v2
        self.solved = False
        if v1[0] in "0123456789" and op is None:
            self.guess = int(v1)
            self.solved = True


def run():
    input_data = load_input_data(2015, 7)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    print("solution1 = ", solution1(input_data.split("\n")))
    print("solution2 = ", solution2(input_data.split("\n")))


def parse(line, circuit):
    inputs, _, wire = line.partition("->")
    inputs = inputs.strip().split(" ")
    wire = wire.strip()
    if len(inputs) == 1:
        circuit[wire] = Wire(v1=inputs[0])
    elif len(inputs) == 2:
        circuit[wire] = Wire(op=inputs[0], v1=inputs[1])
    else:
        circuit[wire] = Wire(v1=inputs[0], op=inputs[1], v2=inputs[2])


def guess_from_input(inp, circuit):
    if inp is None:
        return None
    if inp[0] in "123456789":
        return int(inp)

    return circuit[inp].guess

def solve(wire_name, circuit):
    target_wire = wire_name
    print("solve ", wire_name)
    queue = [wire_name]
    previous_v = circuit[wire_name].guess
    while queue:
        wire_name = queue.pop(0)
        wire = circuit[wire_name]

        a = guess_from_input(wire.v1, circuit)
        b = guess_from_input(wire.v2, circuit)

        wire.guess = run_op(wire.op, a, b)
        if wire_name == target_wire:
            print(f"{wire_name} = {wire.guess}")

        if not circuit[wire.v1].solved:
            queue.append(wire.v1)
        with suppress(KeyError):
            if wire.v2:
                w = circuit[wire.v2]
                if not w.solved:
                    queue.append(wire.v2)
        previous_v = wire.guess

    return circuit[target_wire].guess



def run_op(op, v1, v2=None):
    if op is None:
        return v1
    op = "op_" + op.lower()
    return globals()[op](v1, v2)


def op_not(v1, v2):
    return v1 ^ 0xffff


def op_and(v1, v2):
    return v1 & v2


def op_or(v1, v2):
    return v1 | v2


def op_lshift(v1, v2):
    return v1 << v2


def op_rshift(v1, v2):
    return v1 >> v2


def solution1(lines, solve_for="a"):
    circuit = dict()
    for line in lines:
        parse(line, circuit)

    return solve(solve_for, circuit)


def solution2(lines):
    return


if __name__ == "__main__":
    run()

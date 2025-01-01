import re
from aocd_tools import *


EXAMPLE = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""


EXAMPLE2 = """x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00"""

class Gate(NamedTuple):
    in1: str
    in2: str
    gate: str
    out: str


def parse_initial_values(lines):
    values = {}
    for line in lines.splitlines():
        left, right = line.split(": ")
        values[left] = int(right)
    return values


def parse_gates(lines):
    gates = []
    for line in lines.splitlines():
        ins, outs = line.split(" -> ")
        in1, gate, in2 = ins.split()
        gates.append(Gate(in1, in2, gate, outs))
    return gates

def run():
    input_data = load_input_data()
    input_data = EXAMPLE2
    print(f"loaded input data ({len(input_data)} bytes)")
    a, b = input_data.split("\n\n")
    initial_values = parse_initial_values(a)
    gates = parse_gates(b)

    for i, f in enumerate((solution1, solution2), 1):
        start_time = time.process_time()
        print(f"solution{i} = ", f(initial_values, gates), time_report(start_time))


def eval_gate(f, a, b):
    if a is None or b is None:
        return None
    return f(a, b)

LOGIC_GATES = {
    "AND": lambda a, b: a and b,
    "OR": lambda a, b: a or b,
    "XOR": lambda a, b: a ^ b,
}


def solution1(initial_values, gates):
    z_wires = solve(initial_values, gates)

    bin_value = "".join(str(v[1]) for v in sorted(z_wires, reverse=True))
    return int(bin_value, 2)


def solve(initial_values, gates, gate_map=None):
    gate_map = gate_map or {}
    wires = initial_values.copy()
    while True:
        for gate in gates:
            out = gate_map.get(gate.out, gate.out)
            wires[out] = eval_gate(LOGIC_GATES[gate.gate], wires.get(gate.in1), wires.get(gate.in2))

        z_wires = [(name, value) for name, value in wires.items() if name.startswith("z")]
        if all(z[1] is not None for z in z_wires):
            return z_wires

def solution2_example(initial_values, gates):
    x_wires = [(name, value) for name, value in initial_values.items() if name.startswith("x")]
    xbin_value = "".join(str(v[1]) for v in sorted(x_wires, reverse=True))
    y_wires = [(name, value) for name, value in initial_values.items() if name.startswith("y")]
    ybin_value = "".join(str(v[1]) for v in sorted(y_wires, reverse=True))
    print(xbin_value, " = ", int(xbin_value, 2))
    print(ybin_value, " = ", int(ybin_value, 2))
    target = int(xbin_value, 2) + int(ybin_value, 2)
    print(f"{target=} {target:b}")

    swaps = {"z05":"z00", "z00":"z05",
             "z01":"z02", "z02":"z01",}
    z_wires = solve(initial_values, gates, swaps)
    bin_value = "".join(str(v[1]) for v in sorted(z_wires, reverse=True))
    result = int(bin_value, 2)
    print(f"actual: {bin_value} = {result}")
    return result


def solution2(initial_values, gates):
    out_wires = [gate.out for gate in gates]
    x_wires = [(name, value) for name, value in initial_values.items() if name.startswith("x")]
    xbin_value = "".join(str(v[1]) for v in sorted(x_wires, reverse=True))
    y_wires = [(name, value) for name, value in initial_values.items() if name.startswith("y")]
    ybin_value = "".join(str(v[1]) for v in sorted(y_wires, reverse=True))
    print(xbin_value, " = ", int(xbin_value, 2))
    print(ybin_value, " = ", int(ybin_value, 2))
    target = int(xbin_value, 2) + int(ybin_value, 2)
    print(f"{target=} {target:b}")

    swaps = {"z05":"z00", "z00":"z05",
             "z01":"z02", "z02":"z01",}
    z_wires = solve(initial_values, gates, swaps)
    bin_value = "".join(str(v[1]) for v in sorted(z_wires, reverse=True))
    result = int(bin_value, 2)
    print(f"actual: {bin_value} = {result}")
    return result


def extract_lines(entries):
    return entries.split("\n")


if __name__ == "__main__":
    run()

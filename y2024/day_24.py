import math
import re
from itertools import combinations
from random import sample, choice, shuffle, randint

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


def parse_gates(lines: str) -> list[Gate]:
    gates = []
    for line in lines.splitlines():
        ins, outs = line.split(" -> ")
        in1, gate, in2 = ins.split()
        gates.append(Gate(in1, in2, gate, outs))
    return gates

def run():
    input_data = load_input_data()
    # input_data = EXAMPLE2
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
    i = 0
    while i<100:
        for gate in gates:
            out = gate_map.get(gate.out, gate.out)
            wires[out] = eval_gate(LOGIC_GATES[gate.gate], wires.get(gate.in1), wires.get(gate.in2))

        z_wires = [(name, value) for name, value in wires.items() if name.startswith("z")]
        if all(z[1] is not None for z in z_wires):
            return z_wires
        i += 1
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

def solution2(initial_values, gates: list[Gate]):
    wires_check(gates, initial_values)
    for adder_id in range(43):
        analyse_adder(adder_id, gates)
        print("-"*40)

def wires_check(gates: list[Gate], initial_values):
    for adder_id in range(43):
        results = {}
        for xv, yv in [(1, 0), (0, 1)]:
            clear_all_inputs(initial_values)
            x = f"x{adder_id:02}"
            y = f"y{adder_id:02}"
            initial_values[x] = xv
            initial_values[y] = yv
            target = get_target(initial_values)
            z_wires = solve(initial_values, gates, {})
            bin_value = "".join(str(v[1]) for v in sorted(z_wires, reverse=True))
            result = int(bin_value, 2)
            results[(xv, yv)] = result == target
        print(f"{adder_id} {results}")


def clear_all_inputs(initial_values):
    for adder_id in range(43):
        x = f"x{adder_id:02}"
        y = f"y{adder_id:02}"
        initial_values[x] = 0
        initial_values[y] = 0

def analyse_adder(adder_id: int, gates: list[Gate]):
    x = f"x{adder_id:02}"
    y = f"y{adder_id:02}"
    z = f"z{adder_id:02}"

    in1_tab = {}
    in2_tab = {}
    out_tab = {}
    for g in gates:
        row = in1_tab.get(g.in1, [])
        row.append(g)
        in1_tab[g.in1] = row
        row = in2_tab.get(g.in2, [])
        row.append(g)
        in2_tab[g.in2] = row
        row = out_tab.get(g.out, [])
        row.append(g)
        out_tab[g.out] = row
    l1a = in1_tab.get(x)
    l1b = in2_tab.get(x)
    print(f"{l1a=}")
    print(f"{l1b=}")
    for g in l1a or l1b:
        l2a = in1_tab.get(g.out)
        l2b = in2_tab.get(g.out)
        print(f"{l2a=}")
        print(f"{l2b=}")
    result_gate = out_tab.get(z)
    print(f"{z}: {result_gate}")



def solution2_(initial_values, gates):

    out_wires = [gate.out for gate in gates]

    # print(xbin_value, " = ", int(xbin_value, 2))
    # print(ybin_value, " = ", int(ybin_value, 2))


    potential_swaps = list(combinations(list(gate.out for gate in gates), 2))
    scores = {v: math.inf for v in potential_swaps}
    print(f"Potential swaps: {len(potential_swaps)}")
    i = 0
    best_diff = math.inf
    print("Seeding...")
    swap_opts = [('frp', 'jgm'), ('bmp', 'njk'), ('pvm', 'ctv'), ('z06', 'z05')]
    while True:
        for k in initial_values:
            initial_values[k] = randint(0, 1)
        target = get_target(initial_values)
        # print(f"{target=} {target:b}")
        swaps = {k:v for k,v in swap_opts}
        rev_swaps = {v:k for k,v in swap_opts}
        swaps.update(rev_swaps)
        z_wires = solve(initial_values, gates, swaps)
        bin_value = "".join(str(v[1]) for v in sorted(z_wires, reverse=True))
        try:
            result = int(bin_value, 2)
        except ValueError:
            result = 0
        diff = abs(target - result)
        best_diff = min(diff, best_diff)
        for s in swap_opts:
            scores[s] = min(scores[s], diff)
        if target == result and check_swaps(swaps, gates, initial_values):
            print("Final answer:", swaps)
            return ",".join(sorted(swaps))
        i += 1
        if i % 100 == 0:
            ranked = list(scores)
            ranked.sort(key=scores.get)
            print(ranked[:4])
            print(i, best_diff)
        if i > 16000:
            break
        swap_opts = sample(potential_swaps, 4)

    print("Evolution...")
    old_swaps = ranked[:4]
    i = 0
    while True:
        for k in initial_values:
            initial_values[k] = randint(0, 1)
        target = get_target(initial_values)
        # print(f"{target=} {target:b}")
        shuffle(old_swaps)
        swap_opts = old_swaps[1:]
        while True:
            new_pair = choice(potential_swaps)
            uniques = {x for sublist in swap_opts for x in sublist}
            if new_pair[0] not in uniques and new_pair[1] not in uniques:
                break
        swap_opts.append(new_pair)
        swaps = {k:v for k,v in swap_opts}
        rev_swaps = {v:k for k,v in swap_opts}
        swaps.update(rev_swaps)
        z_wires = solve(initial_values, gates, swaps)
        bin_value = "".join(str(v[1]) for v in sorted(z_wires, reverse=True))
        try:
            result = int(bin_value, 2)
        except ValueError:
            result = 0
        diff = abs(target - result)
        if diff < best_diff:
            old_swaps = swap_opts[::]
            best_diff = diff
        for s in swap_opts:
            scores[s] = min(scores[s], diff)
        if target == result and check_swaps(swaps, gates, initial_values):
            break
        i += 1
        if i % 100 == 0:
            ranked = list(scores)
            ranked.sort(key=scores.get)
            print(ranked[:4])
            uniques = {x for sublist in old_swaps for x in sublist}
            print(",".join(sorted(uniques)))
            print(i, best_diff)

    print("Final answer:", swaps)
    return ",".join(sorted(swaps))


def get_target(initial_values):
    x_wires = [(name, value) for name, value in initial_values.items() if name.startswith("x")]
    xbin_value = "".join(str(v[1]) for v in sorted(x_wires, reverse=True))
    y_wires = [(name, value) for name, value in initial_values.items() if name.startswith("y")]
    ybin_value = "".join(str(v[1]) for v in sorted(y_wires, reverse=True))
    target = int(xbin_value, 2) + int(ybin_value, 2)
    return target


def extract_lines(entries):
    return entries.split("\n")


def check_swaps(swaps, gates, initial_values)->bool:
    initial_values = initial_values.copy()
    for _ in range(100):
        for k in initial_values:
            initial_values[k] = randint(0, 1)
        x_wires = [(name, value) for name, value in initial_values.items() if name.startswith("x")]
        xbin_value = "".join(str(v[1]) for v in sorted(x_wires, reverse=True))
        y_wires = [(name, value) for name, value in initial_values.items() if name.startswith("y")]
        ybin_value = "".join(str(v[1]) for v in sorted(y_wires, reverse=True))
        target = int(xbin_value, 2) + int(ybin_value, 2)
        z_wires = solve(initial_values, gates, swaps)
        bin_value = "".join(str(v[1]) for v in sorted(z_wires, reverse=True))
        try:
            result = int(bin_value, 2)
        except ValueError:
            result = 0
        if result != target:
            return False
    return True

if __name__ == "__main__":
    run()

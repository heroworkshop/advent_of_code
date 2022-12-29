import operator
from contextlib import suppress
from pprint import pprint

from aocd_tools import load_input_data

EXAMPLE = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""


def run():
    input_data = load_input_data(2022, 21)
    # input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    entries = input_data.split("\n")
    pairs = [e.split(": ") for e in entries]
    entries = {p[0]: p[1] for p in pairs}
    print(entries)

    print("solution1 = ", solution1(entries))
    print("solution2 = ", solution2(entries))



def solution1(entries):
    return evaluate(entries, "root")


def evaluate(entries, name):
    v = entries[name]
    with suppress(ValueError):
        return int(v)

    if "+" in v:
        a, b = v.split(" + ")
        return evaluate(entries, a) + evaluate(entries, b)
    if "-" in v:
        a, b = v.split(" - ")
        return evaluate(entries, a) - evaluate(entries, b)
    if "*" in v:
        a, b = v.split(" * ")
        return evaluate(entries, a) * evaluate(entries, b)
    if "/" in v:
        a, b = v.split(" / ")
        return evaluate(entries, a) / evaluate(entries, b)

    raise RuntimeError(f"Could not evaluate '{v}'")


def isnumber(x):
    return isinstance(x, int) or isinstance(x, float)

def fast_evaluate(entries, name):
    v = entries[name]
    if isnumber(v):
        return v
    a, b, op = v
    if isnumber(a) and isnumber(b):
        entries[name] = op(a, b)

    return op(fast_evaluate(entries, a), fast_evaluate(entries, b))


def solution2(entries):
    old_root = entries["root"]
    parts = old_root.split()
    a = parts[0]
    b = parts[-1]
    print(f"wait for {a} == {b}")
    entries = parse(entries)
    while True:
        r = simplify(entries)
        print(f"simplified {r}")
        pprint(entries)
        if not r:
            break

    # answer < 3272260914327
    #for i in range(11111152034000, 100_000_000_000_000):
    # for i in range(10000):
    i = 3272260914328
    di = 1
    direction = 1
    while True:
        entries["humn"] = i
        diff = fast_evaluate(entries, a) - fast_evaluate(entries, b)
        print(i, diff, di)
        if diff == 0:
            return i
        if diff/abs(diff) != direction:
            di = max(1, di) // 2
            direction = - direction
        i += di *direction


def parse(entries):
    parsed = {}
    for k, v in entries.items():
        with suppress(ValueError):
            parsed[k] = int(v)
            continue
        if "+" in v:
            a, b = v.split(" + ")
            parsed[k] = (a, b, operator.add)
        if "-" in v:
            a, b = v.split(" - ")
            parsed[k] = (a, b, operator.sub)
        if "*" in v:
            a, b = v.split(" * ")
            parsed[k] = (a, b, operator.mul)
        if "/" in v:
            a, b = v.split(" / ")
            parsed[k] = (a, b, lambda a, b: a/b)
    return parsed


def simplify(entries):
    updated = 0
    for k, v in entries.items():
        if isinstance(v, tuple):
            a, b, op = v
            if "humn" in (a, b):
                continue
            if isinstance(entries[a], int) and isinstance(entries[b], int):
                entries[k] = op(entries[a], entries[b])
                updated += 1
    return updated


if __name__ == "__main__":
    run()

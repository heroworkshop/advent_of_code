from aocd_tools import load_input_data, ints_from_lines


def run():
    input_data = load_input_data(2021, 2)
    print(f"loaded input data ({len(input_data)} bytes)")

    entries = parse_cmds(input_data)
    # print(entries)

    print("solution1 = ", solution1(entries))
    print("solution2 = ", solution2(entries))


def parse_cmds(input_data):
    def parse_line(x):
        op, mag = x.split()
        return op, int(mag)
    return [parse_line(line) for line in input_data.split("\n")]


def solution1(cmds):
    depth = 0
    x = 0
    for op, mag in cmds:
        if op == "up":
            depth -= mag
        elif op == "down":
            depth += mag
        elif op == "forward":
            x += mag
    return x * depth



def solution2(cmds):
    depth = 0
    x = 0
    aim = 0
    for op, mag in cmds:
        if op == "up":
            aim -= mag
        elif op == "down":
            aim += mag
        elif op == "forward":
            x += mag
            depth += aim * mag
    return x * depth


if __name__ == "__main__":
    run()

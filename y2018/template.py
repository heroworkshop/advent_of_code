from aocd_tools import load_input_data

EXAMPLE = """"""

def parse(line):
    return int(line)


def run():
    input_data = load_input_data(2020, 00)
    # input_data  = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = [parse(line) for line in input_data.split("\n")]
    # lines = grid_from_lines(input_data, transform=int)
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(lines))


def solution1(lines):
    return


def solution2(lines):
    return


if __name__ == "__main__":
    run()

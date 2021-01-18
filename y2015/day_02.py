from aocd_tools import load_input_data, ints_from_lines, grid_from_lines

def run():
    input_data = load_input_data(2015, 2)
    print(f"loaded input data ({len(input_data)} bytes)")
    print("solution1 = ", solution1(input_data.split("\n")))
    print("solution2 = ", solution2(input_data.split("\n")))

def solution1(lines):
    areas = [wrapping(line) for line in lines]
    return sum(areas)

def solution2(lines):
    areas = [ribbon(line) for line in lines]
    return sum(areas)

def wrapping(line):
    a, b, c = parse_dimensions(line)
    sides = [a*b, a*c, b*c]
    slack = min(sides)
    return 2*sum(sides) + slack


def ribbon(line):
    a, b, c = parse_dimensions(line)
    perimeters = [a+b, b+c, a+c]
    return 2*min(perimeters) + a*b*c

def parse_dimensions(line):
    return (int(v) for v in line.split("x"))


if __name__ == "__main__":
    run()

from collections import defaultdict, namedtuple

from input_data.day8 import INPUT_DATA

Instruction = namedtuple("instructions", "a b operation")

WIDTH = 50
HEIGHT = 6


def rect(grid, width, height):
    for y in range(height):
        for x in range(width):
            grid[(x, y)] = True


def rotate_row(grid, y, by):
    row = [grid[(x, y)] for x in range(WIDTH)]
    for x in range(WIDTH):
        tx = (x + by) % WIDTH
        grid[(tx, y)] = row[x]


def rotate_column(grid, x, by):
    col = [grid[(x, y)] for y in range(HEIGHT)]
    for y in range(HEIGHT):
        ty = (y + by) % HEIGHT
        grid[(x, ty)] = col[y]


OPERATIONS = {"rect": ("x", rect),
              "rotate row y=": (" by ", rotate_row),
              "rotate column x=": (" by ", rotate_column)
              }


def parse(line):
    for op, params in OPERATIONS.items():
        if op in line:
            _, _, line = line.partition(op)
            a, _, b = line.partition(params[0])

            return Instruction(int(a), int(b), params[1])
    raise RuntimeError(f"Invalid line {line}")


def run():
    input_data = [parse(line) for line in INPUT_DATA.split("\n")]
    print("solution1=", solution1(input_data))
    print("solution2=", solution2(input_data))


def solution1(input_data):
    grid = defaultdict(bool)
    for instruction in input_data:
        instruction.operation(grid, instruction.a, instruction.b)
    print(render(grid))
    return len([p for p in grid.values() if p])


def solution2(input_data):
    return


def render(grid):
    result = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            result.append("#" if grid[(x, y)] else " ")
        result.append("\n")
    return "".join(result)

if __name__ == "__main__":
    run()

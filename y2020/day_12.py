from collections import namedtuple

from aocd_tools import load_input_data


EXAMPLE = """
F10
N3
F7
R90
F11""".strip()

Instruction = namedtuple("instruction", "direction distance")

TRANSLATIONS = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0)
}

def run():
    input_data = load_input_data(2020, 12)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = input_data.split("\n")
    instructions = [parse(line) for line in lines]
    print("solution1 = ", solution1(instructions))
    print("solution2 = ", solution2(instructions))


def parse(line):
    return Instruction(line[0], int(line[1:]))


def solution1(instructions):
    pos = (0, 0)
    facing = (1, 0)
    for instruction in instructions:
        if instruction.direction in TRANSLATIONS:
            pos = translate(pos, TRANSLATIONS[instruction.direction], instruction.distance)
        elif instruction.direction in "RL":
            facing = rotate(facing, instruction)
        elif instruction.direction in "F":
            pos = translate(pos, facing, instruction.distance)
        else:
            raise ValueError(f"Unknown instruction '{instruction}'")
        print(f"{instruction} {pos}")

    return abs(pos[0]) + abs(pos[1])



def rotate(facing, instruction:Instruction):
    # 0, 1 -> -1, 0
    # 0, -1 -> 1, 0
    # 1, 0 -> 0, 1
    # -1, 0 -> 0, -1
    r = instruction.direction
    dx, dy = facing
    for _ in range(instruction.distance // 90):
        if r == "R":
            dx, dy = dy * -1, dx
        elif r == "L":
            dx, dy = dy, dx * -1
        else:
            raise ValueError(f"Unknown rotation {r}")
    return dx, dy


def translate(pos, vector, distance):
    x, y = pos
    x += vector[0] * distance
    y += vector[1] * distance
    return x, y


def solution2(instructions):
    pos = (0, 0)
    waypoint = (10, -1)
    for instruction in instructions:
        if instruction.direction in TRANSLATIONS:
            waypoint = translate(waypoint, TRANSLATIONS[instruction.direction], instruction.distance)
        elif instruction.direction in "RL":
            waypoint = rotate(waypoint, instruction)
        elif instruction.direction in "F":
            pos = translate(pos, waypoint, instruction.distance)
        else:
            raise ValueError(f"Unknown instruction '{instruction}'")
        print(f"{instruction} {pos}")

    return abs(pos[0]) + abs(pos[1])


if __name__ == "__main__":
    run()

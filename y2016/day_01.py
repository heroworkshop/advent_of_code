from collections import namedtuple

from input_data.day1 import INPUT_DATA

Instruction = namedtuple("instruction", "direction distance")

DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))


def parse(line):
    line = line.strip()
    return Instruction(line[0], int(line[1:]))


def run():
    input_data = [parse(line) for line in INPUT_DATA.split(",")]
    print("solution1=", solution1(input_data))
    print("solution2=", solution2(input_data))


def manhattan_distance(p):
    return abs(p[0]) + abs(p[1])


class GridWalker:
    def __init__(self):
        self.p = (0, 0)
        self.d = 3

    def move(self, instruction):
        points = []
        v = instruction.distance
        direction = instruction.direction
        if direction == "R":
            self.d = (self.d + 1) % 4
        else:
            self.d = (self.d - 1) % 4
        while v:
            self.p = (self.p[0] + DIRECTIONS[self.d][0], self.p[1] + DIRECTIONS[self.d][1])
            points.append(self.p)
            v -= 1
        return points

    def follow_instructions(self, instructions):
        for instruction in instructions:
            self.move(instruction)
        return manhattan_distance(self.p)


class UniquePointGridWalker(GridWalker):
    def follow_instructions(self, instructions):
        visited = {(0, 0)}
        for instruction in instructions:
            points = self.move(instruction)
            for p in points:
                if p in visited:
                    return manhattan_distance(p)
                visited.add(p)
        raise RuntimeError("No duplicates found")


def solution1(input_data):
    sleigh = GridWalker()
    return sleigh.follow_instructions(input_data)


def solution2(input_data):
    sleigh = UniquePointGridWalker()
    return sleigh.follow_instructions(input_data)


if __name__ == "__main__":
    run()

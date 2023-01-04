from typing import NamedTuple

from aocd_tools import load_input_data, Pos

EXAMPLE = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

EX2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""


class Move(NamedTuple):
    dx: int
    dy: int
    count: int


DIRECTIONS = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}


def parse_move(line: str):
    direction, dist = line.split()
    v = DIRECTIONS[direction]
    return Move(*v, int(dist))


def run():
    input_data = load_input_data(2022, 9)
    input_data = EX2

    print(f"loaded input data ({len(input_data)} bytes)")

    values = input_data.split("\n")
    values = [parse_move(line) for line in values]
    print(values[:50])

    print("solution1 = ", solution1(values))

    print("solution2 = ", solution2(values))


def do_moves(moves, length):
    snake = [Pos(0, 0) for _ in range(length)]

    def tail():
        return snake[length - 1]

    def head():
        return snake[0]

    history = {tail()}
    for move in moves:
        for _ in range(move.count):
            snake[0] = execute_move(head(), move.dx, move.dy)
            for n in range(length - 1):
                snake[n + 1] = follow(snake[n], snake[n + 1])
            history.add(tail())
            show(snake)
            print()
    return history


def show(snake):
    snake_positions = {p: n for n, p in enumerate(snake)}
    for y in range(-16, 6):
        for x in range(-13, 14):
            v = snake_positions.get((x, y), ".")
            print(v, end="")
        print()


def execute_move(item: Pos, dx: int, dy: int):
    return Pos(item.x + dx, item.y + dy)


def follow(head: Pos, tail: Pos) -> Pos:
    dx = head.x - tail.x
    dy = head.y - tail.y
    if abs(dx) < 2 and abs(dy) < 2:
        return tail
    if dx:
        dx = dx // abs(dx)
    if dy:
        dy = dy // abs(dy)
    tail = Pos(tail.x + dx, tail.y + dy)
    return tail


def solution1(values):
    return len(do_moves(values, 2))


def solution2(values):
    return len(do_moves(values, 10))


if __name__ == "__main__":
    run()

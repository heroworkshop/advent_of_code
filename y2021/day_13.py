from collections import defaultdict, namedtuple

from aocd_tools import load_input_data, Grid

EXAMPLE = """"""

Dot = namedtuple("dot", "x y")


def parse_fold(line):
    parts = line.split()
    axis, v = parts[-1].split("=")
    return axis, int(v)


def parse_dot(dot):
    parts = [int(v) for v in dot.split(",")]
    return Dot(*parts)


def run():
    input_data = load_input_data()
    # input_data  = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    dots, folds = input_data.split("\n\n")
    dots = set(parse_dot(p) for p in dots.split("\n"))
    folds = [parse_fold(f) for f in folds.split("\n")]

    print("solution1 = ", solution1(dots, folds))
    print("solution2 = ", solution2(dots, folds))


def fold_x(d: Dot, pos):
    return 2 * pos - d.x, d.y


def fold_y(d: Dot, pos):
    return d.x, 2 * pos - d.y


def do_fold(fold, dots):
    pos = fold[1]
    axis = fold[0]

    transform = {
        "x": (lambda dot: dot.x, fold_x),
        "y": (lambda dot: dot.y, fold_y)
    }

    dot_pos, move_dot = transform[axis]

    movers = [d for d in dots if dot_pos(d) > pos]

    for d in movers:
        new_d = Dot(*move_dot(d, pos))
        dots.add(new_d)
        dots.remove(d)


def solution1(dots, folds):
    fold = folds[0]
    do_fold(fold, dots)
    return len(dots)


def solution2(dots, folds):
    for fold in folds[1:]:
        do_fold(fold, dots)
    grid = Grid()
    for p in dots:
        grid.add(p, u'\u2588')

    return "\n" + grid.render()


if __name__ == "__main__":
    run()

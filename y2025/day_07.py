from aocd_tools import grid_from_lines
from y2025.day07_data import DATA

EXAMPLE = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
""".strip()

def parse(data):
    lines = [line.strip() for line in data.strip().split("\n")]
    return lines


def part1():
    result = 0
    data=DATA
    rows = parse(data)

    p = rows[0].index("S")
    beams = {p}
    for y, row in enumerate(rows):
        print(y, row)
    grid = grid_from_lines(lines=data, default_val=".")
    print(grid)
    for y in range(grid.height):
        new_beams = set()
        for beam in beams:
            if grid.at((beam, y)) == "^":
                new_beams.add(beam + 1)
                new_beams.add(beam - 1)
                result += 1
            else:
                new_beams.add(beam)
        beams = new_beams
    return result


def part2():
    data=DATA
    rows = parse(data)
    p = rows[0].index("S")
    grid = grid_from_lines(lines=data, default_val=".")

    beams = {p : 1}
    y = 0
    while y < grid.height:
        print(y, beams)
        new_beams = {}
        for x, count in beams.items():
            if grid.at((x, y)) == "^":
                new_beams[x-1] = new_beams.get(x - 1, 0) + count
                new_beams[x+1] = new_beams.get(x + 1, 0) + count
            else:
                new_beams[x] = new_beams.get(x, 0) + count
        beams = new_beams
        y += 1

    return sum(beams.values())


if __name__ == "__main__":
    print("part1:", part1())
    print("part2:", part2())

from aocd_tools import *

EXAMPLE = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""


def run():
    input_data = load_input_data()
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    # entries = int_tuples_from_lines(lines=input_data, sep=" ")
    entries = grid_from_lines(input_data)
    print(entries.render())

    for i, f in enumerate((solution1, solution2), 1):
        print(f"solution{i} = ", f(entries))


def process_one_line(line):
    return line


def solution1(entries: Grid):
    directions = ALL_DIRECTIONS
    n = NEIGHBOURS
    count = 0
    for x in entries.x_vals:
        for y in entries.y_vals:
            for d in directions:
                p = Pos(x, y)
                for ch in "XMAS":
                    if entries.at(p) != ch:
                        break
                    p = p + d
                else:
                    count += 1
    return count


def solution2(entries):
    count = 0
    for x in entries.x_vals:
        for y in entries.y_vals:
            if entries.at((x, y)) != "A":
                continue
            if {entries.at((x - 1, y - 1)), entries.at((x + 1, y + 1))} != {"M", "S"}:
                continue
            if {entries.at((x - 1, y + 1)), entries.at((x + 1, y - 1))} != {"M", "S"}:
                continue
            count += 1
    return count


if __name__ == "__main__":
    run()

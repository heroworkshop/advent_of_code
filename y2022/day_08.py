from aocd_tools import load_input_data, grid_from_lines, Grid

EXAMPLE = """30373
25512
65332
33549
35390
"""


def run():
    input_data = load_input_data(2022, 8)
    #input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    lines = input_data.split("\n")
    grid = grid_from_lines(input_data, default_val=0, transform=int)
    print(grid.render())


    print("solution1 = ", solution1(grid))

    print(grid.at((2, 1)))
    print(scenic_score(2, 1, grid))
    print(grid.at((2, 3)))
    print(scenic_score(2, 3, grid))
    print("solution2 = ", solution2(grid))


def solution1(grid: Grid):
    total = 0
    for y in range(grid.y_bounds.max + 1):
        for x in range(grid.width):
            if is_visible(x, y, grid):
                print("x", end="")
                total += 1
            else:
                print(".", end="")
        print()
    return total


def is_visible(x, y, grid):
    if x == 0 or y == 0 or x == grid.x_bounds.max or y == grid.y_bounds.max:
        return True
    height = grid.at((x, y))
    left = [grid.at((x1, y)) for x1 in range(x)]
    if all_lower(left, height):
        return True
    right = [grid.at((x1, y)) for x1 in range(x + 1, grid.width + 1)]
    if all_lower(right, height):
        return True
    up = [grid.at((x, y1)) for y1 in range(y)]
    if all_lower(up, height):
        return True
    down = [grid.at((x, y1)) for y1 in range(y + 1, grid.y_bounds.max + 1)]
    if all_lower(down, height):
        return True


def scenic_score(x, y, grid):
    if x == 0 or y == 0 or x == grid.x_bounds.max or y == grid.y_bounds.max:
        return 0
    height = grid.at((x, y))
    left = 0
    for x1 in range(x-1, -1, -1):
        h = grid.at((x1, y))
        left += 1
        if h >= height:
            break

    right = 0
    for x1 in range(x+1, grid.x_bounds.max+1):
        h = grid.at((x1, y))
        right += 1
        if h >= height:
            break

    down = 0
    for y1 in range(y+1, grid.y_bounds.max+1):
        h = grid.at((x, y1))
        down += 1
        if h >= height:
            break

    up = 0
    for y1 in range(y-1, -1, -1):
        h = grid.at((x, y1))
        up += 1
        if h >= height:
            break

    return left * right * up * down


def all_lower(line, height):
    for h in line:
        if h >= height:
            return False
    return True


def solution2(grid: Grid):
    scores = []
    for y in range(grid.y_bounds.max + 1):
        for x in range(grid.width):
            scores.append(scenic_score(x, y, grid))
    return max(scores)


if __name__ == "__main__":
    run()

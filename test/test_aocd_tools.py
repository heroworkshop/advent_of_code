from aocd_tools import Grid, grid_from_lines, int_tuples_from_lines, ints_from_lines


def test_int_tuples_from_lines():
    lines = """
    1, 2, 3
    4, 5, 6
    """
    result = int_tuples_from_lines(lines, ",")
    assert result == [(1, 2, 3), (4, 5, 6)]


def test_ints_from_lines():
    lines = """
    1
    4
    3
    """
    result = ints_from_lines(lines)
    assert result == [1, 4, 3]


def test_bounds():
    grid = Grid()
    grid.add((-1, -2), "#")
    grid.add((5, 10), "#")
    grid.update_bounds()
    assert grid.x_bounds.min == -1
    assert grid.y_bounds.min == -2
    assert grid.x_bounds.max == 5
    assert grid.y_bounds.max == 10


def test_linear_index():
    grid = Grid()
    grid.add((0, 0), ".")
    grid.add((1, 1), ".")
    grid.update_bounds()
    assert grid.linear_index((0, 0)) == 0
    assert grid.linear_index((1, 0)) == 1
    assert grid.linear_index((0, 1)) == 2
    assert grid.linear_index((1, 1)) == 3


def test_grid_from_lines():
    lines = ("aaa\n"
             "bbb\n"
             "ccc\n")

    grid = grid_from_lines(lines)
    assert grid.x_bounds.min == 0
    assert grid.x_bounds.max == 2
    assert grid.y_bounds.min == 0
    assert grid.x_bounds.max == 2
    assert grid.at((0, 0)) == "a"

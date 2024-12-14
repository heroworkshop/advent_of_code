import pytest

from aocd_tools import *
from y2024 import day_04


@pytest.mark.parametrize('test_input,expected', [
    ("XMAS", 1)
])
def test_solution1(test_input, expected):
    grid = grid_from_lines(test_input)
    result = day_04.solution1(grid)
    assert result == expected



EXAMPLE1 = """MFS
FAF
MFS"""
def test_solution2():
    grid = grid_from_lines(EXAMPLE1)
    result = day_04.solution2(grid)
    assert result == 1
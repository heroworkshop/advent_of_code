import pytest

from y2024 import day_13


def test_solve():
    # Arrange
    # Act
    button_a = 94, 34
    button_b = 22, 67
    prize = 8400, 5400
    result = day_13.solve(button_a, button_b, prize)
    assert result == 280

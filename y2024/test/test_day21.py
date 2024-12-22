import pytest

from y2024 import day_21


def test_get_key_presses():
    # Arrange

    # Act
    result = day_21.get_key_presses("379A")
    # Assert
    assert result == "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"


def test_press_numeric_A_to_7():
    result = day_21.press_numeric("A", "7")
    assert result == "^^^<<"

def test_press_numeric_7_to_A():
    result = day_21.press_numeric("7", "A")
    assert result == ">>vvv"


def test_directions_from_numeric():
    result = day_21.directions_from_numeric("029A")
    assert result == "<A^A>^^AvvvA"
import pytest

from y2024 import day_21


def test_get_key_presses():
    result = day_21.get_key_presses("379A")
    assert result == len("<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A")


def test_solution1():
    entries = ["319A", "985A", "340A", "489A", "964A"]
    result = day_21.solution1(entries)
    assert result == 215374

def test_press_numeric_A_to_7__avoids_empty_square():
    result = day_21.press_numeric("A", "7")
    assert result == ["^^^<<"]

def test_press_numeric_7_to_A_avoids_empty_square():
    result = day_21.press_numeric("7", "A")
    assert result == [">>vvv"]

def test_press_numeric_8_to_A():
    result = day_21.press_numeric("8", "A")
    assert result == ["vvv>"]

def test_get_key_presses__level0():
    result = day_21.get_key_presses("0", level_count=0) # <A
    assert result == 2

def test_get_key_presses__level1():
    result = day_21.get_key_presses("0", level_count=1) # v<<A>>^A
    assert result == 8

def test_get_key_presses__level2():
    result = day_21.get_key_presses("0", level_count=2)  # <vA<AA>>^AvAA<^A>A
    assert result == 10 + 8

# def test_dfs_get_level_2_directions():
#     dfs_get_level_2_directions("A", )

# def test_directions_from_numeric():
#     result = day_21.directions_from_numeric("029A")
#     assert result == "<A^A>^^AvvvA"


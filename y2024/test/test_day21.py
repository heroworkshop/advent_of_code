import pytest

from y2024 import day_21
from y2024.day_21 import get_numeric_pad_paths


def test_get_key_presses():
    result = day_21.get_key_presses("379A")
    assert len(result) == len("<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A")


def test_solution1():
    entries = ["319A", "985A", "340A", "489A", "964A"]
    result = day_21.solution1(entries)
    assert result == 215374

def test_press_numeric_A_to_7():
    result = day_21.press_numeric("A", "7")
    assert result == "^^^<<"

def test_press_numeric_7_to_A():
    result = day_21.press_numeric("7", "A")
    assert result == ">>vvv"


def test_directions_from_numeric():
    result = day_21.directions_from_numeric("029A")
    assert result == "<A^A>^^AvvvA"

def test_get_numeric_pad_paths():
    paths = get_numeric_pad_paths("A", "2")
    assert len(paths) == 2

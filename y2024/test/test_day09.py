import random

from y2024.day_09 import solution1b, solution2
from y2024.day_09 import solution1, extract


def test_example():
    v = "2333133121414131402"
    entries = extract(v)
    result = solution1b(entries)
    assert result == 1928


def test_short():
    v = "129"  # 0..111111111
    entries = extract(v)
    result = solution1b(entries)
    assert result == sum(range(1, 10))


def test_short2():
    v = "199"  # 0.........111111111
    entries = extract(v)
    result = solution1b(entries)
    assert result == sum(range(1, 10))


def test_short3():
    v = "12345"  # 0..111....22222
    entries = extract(v)
    result = solution1b(entries)
    assert result == 1 * 2 + 2 * 2 + 3 + 4 + 5 + 6 * 2 + 7 * 2 + 8 * 2


def test_no_gaps():
    v = "10101010101"  # 012345
    entries = extract(v)
    result = solution1b(entries)
    assert result == 1 * 1 + 2 * 2 + 3 * 3 + 4 * 4 + 5 * 5


def test_no_gaps_long():
    v = "1" + "01" * 5000  # 012345
    entries = extract(v)
    result = solution1b(entries)
    assert result == sum([n * v for n, v in enumerate(range(5000 + 1))])


def test_one_gap():
    v = "11101010101"  # 051234
    entries = extract(v)
    result = solution1b(entries)
    assert result == 1 * 5 + 2 * 1 + 3 * 2 + 4 * 3 + 5 * 4

def test_compare():
    for length in range(5, 21, 2):
        for n in range(10):
            v = "".join([str(random.randint(0, 9)) for _ in range(length)])
            print(v)
            entries = extract(v)
            result_1 = solution1(entries)
            result_1b = solution1b(entries)
            assert result_1 == result_1b

def test_one_gap__corner_case():
    v = "82673"  # 051234
    entries = extract(v)
    result = solution1b(entries)
    assert result == 2*(8+9) + sum(range(10, 16)) + 2 *16


def test_solution2():
    v = "2333133121414131402"  # 051234
    entries = extract(v)
    result = solution2(entries)
    assert result == 2858
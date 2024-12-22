import pytest

from y2024.day_22 import mix, prune, next_secret, make_price_table, process_one_line, solution2, get_digits


def test_mix():
    result = mix(42, 15)
    assert result == 37


def test_prune():
    result = prune(100000000)
    assert result == 16113920


@pytest.mark.parametrize('test_input,expected', [
    (123, 15887950),
    (15887950, 16495136),
    (16495136, 527345),
    (527345, 704524),
    (704524, 1553684),
    (1553684, 12683156),
    (12683156, 11100544),
    (11100544, 12249484),
    (12249484, 7753432),
    (7753432, 5908254),
])
def test_next_secret(test_input, expected):
    result = next_secret(test_input)
    assert result == expected


def test_next_secret_10_times():
    result = []
    secret = 123
    for _ in range(10):
        secret = next_secret(secret)
        result.append(secret)
    assert result == [
        15887950,
        16495136,
        527345,
        704524,
        1553684,
        12683156,
        11100544,
        12249484,
        7753432,
        5908254,
    ]


def test_make_price_table():
    result = make_price_table(123, 10)
    #     123: 3
    # 15887950: 0 (-3)
    # 16495136: 6 (6)
    #   527345: 5 (-1)
    #   704524: 4 (-1)
    #  1553684: 4 (0)
    # 12683156: 6 (2)
    # 11100544: 4 (-2)
    # 12249484: 4 (0)
    #  7753432: 2 (-2)
    assert result[(-3, 6, -1, -1)] == 4
    assert result[(6, -1, -1, 0)] == 4
    assert result[(-1, -1, 0, 2)] == 6


def test_get_digits():
    result = get_digits(10, 123)
    assert result == [
        (0, -3),
        (6, 6),
        (5, -1),
        (4, -1),
        (4, 0),
        (6, 2),
        (4, -2),
        (4, 0),
        (2, -2),
        (4, 2)
    ]


EXAMPLE2 = """1
2
3
2024"""


def test_solution2():
    entries = [process_one_line(line) for line in EXAMPLE2.splitlines()]

    result = solution2(entries)

    assert result == 23

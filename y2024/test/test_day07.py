from y2024 import day_07


def test_all_multiply():
    t = 2*5*6*12*100*3
    entries = [
        (t, (2, 5, 6, 12, 100, 3))
    ]
    result = day_07.solution1(entries)
    assert result == t

def test_solution_2():
    entries = [
        (192, (17, 8, 14))
    ]
    result = day_07.solution2(entries)
    assert result == 192


def test_evaluate3():
    result = day_07.evaluate3("21", [17,8,14])
    assert result == 192
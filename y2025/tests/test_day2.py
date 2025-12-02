from y2025.day_02 import is_invalid

def test_is_valid():
    assert is_invalid("262262262") is True
    assert is_invalid("12") is False

    assert is_invalid("11") is True

import unittest

from assertpy import assert_that

from y2022.day_25 import from_snafu, to_snafu

EXAMPLES = """1    1
     2        2
    1=        3
    1-        4
    10        5
1=-0-2     1747
 12111      906
  2=0=      198
    21       11
  2=01      201
   111       31
 20012     1257
   112       32
 1=-1=      353
  1-12      107
    12        7
    1=        3
   122       37"""

def parse(line):
    snafu, decimal = line.split()
    return snafu, int(decimal)


class TestSnafuConversion(unittest.TestCase):
    def setUp(self):
        parsed = [parse(line) for line in EXAMPLES.split("\n")]
        self.examples = {v[0]: v[1] for v in parsed}

    def test_from_snafu(self):
        for snafu, decint in self.examples.items():
            with self.subTest(snafu=snafu, decint=decint):
                result = from_snafu(snafu)
                assert_that(result).is_equal_to(decint)

    def test_to_snafu(self):
        for snafu, decint in self.examples.items():
            with self.subTest(snafu=snafu, decint=decint):
                result = to_snafu(decint)
                assert_that(result).is_equal_to(snafu)


if __name__ == '__main__':
    unittest.main()

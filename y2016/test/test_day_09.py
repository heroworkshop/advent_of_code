import unittest

from day_09 import decompress, parse


class TestDay09(unittest.TestCase):
    def test_decompress(self):
        sub_tests = [("(2x2)abcdef", "abab"),
                     ("(2x3)abcdef", "ababab"),
                     ("(3x2)abcdef", "abcabc"),
                     ("(5x2)(5x5)abcdef", "(5x5)(5x5)"),
                     ]
        for seq, expected in sub_tests:
            result, p = decompress(seq, 0)
            self.assertEqual(expected, result)

    def test_parse(self):
        sub_tests = [("(2x2)abcdef", "ababcdef"),
                     ("(2x3)abcdef", "abababcdef"),
                     ("(3x2)abcdef", "abcabcdef"),
                     ("(5x2)(5x5)abcdef", "(5x5)(5x5)abcdef"),
                     ]
        for seq, expected in sub_tests:
            result = parse(seq)
            self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()

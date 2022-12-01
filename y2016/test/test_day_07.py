import unittest

from day_07 import contains_abba, supports_tls, parse


class TestDay07(unittest.TestCase):

    def test_parse(self):
        result = parse("a[b]c[d]e")
        self.assertEqual(["a", "c", "e"], result.main)
        self.assertEqual(["b", "d"], result.hypernet)

    def test_contains_abba_in4LetterAbba_returnsTrue(self):
        s = "ABBA"
        self.assertTrue(contains_abba(s))

    def test_contains_abba_inLongEndsWithAbba_returnsTrue(self):
        s = "CCCDAAD"
        self.assertTrue(contains_abba(s))

    def test_contains_abba_withAbbaMissing_returnsFalse(self):
        s = "CCCDAD"
        self.assertFalse(contains_abba(s))

    def test_supports_tls_withAbbaOutside_returnsTrue(self):
        parts = parse("abba[mnop]qrst")
        self.assertTrue(supports_tls(parts))

    def test_supports_tls_withAbbaOutsideInLargerString_returnsTrue(self):
        parts = parse("ioxxoj[asdfgh]zxcvbn")
        self.assertTrue(supports_tls(parts))

    def test_supports_tls_withAbbaInside_returnsFalse(self):
        parts = parse("abcd[bddb]xyyx")
        self.assertFalse(supports_tls(parts))

    def test_supports_tls_withNoAbba_returnsFalse(self):
        parts = parse("aaaa[qwer]tyui")
        self.assertFalse(supports_tls(parts))

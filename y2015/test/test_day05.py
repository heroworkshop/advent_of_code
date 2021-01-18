import unittest
from y2015.day_05 import contains_repeating_pair, contains_split_pair, is_new_nice


class TestNewNice(unittest.TestCase):
    def test_repeating_pair(self):
        self.assertTrue(contains_repeating_pair("yzsmlbnftftgwadz"))
        self.assertTrue(contains_repeating_pair("xyxy"))
        self.assertTrue(contains_repeating_pair("aabcdefgaa"))
        self.assertFalse(contains_repeating_pair("aaa"))

    def test_split_pair(self):
        self.assertTrue(contains_split_pair("abcdefeghi"))

    def test_new_nice(self):
        self.assertTrue(is_new_nice("qjhvhtzxzqqjkmpb"))
        self.assertTrue(is_new_nice("xxyxx"))
        self.assertFalse(is_new_nice("uurcxstgmygtbstg"))
        self.assertFalse(is_new_nice("ieodomkazucvgmuy"))


if __name__ == '__main__':
    unittest.main()

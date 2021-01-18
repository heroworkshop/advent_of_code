import unittest

from y2017.day_09 import unescape, remove_garbage, make_tree


class TestDay08(unittest.TestCase):
    def test_unescape_withEscapedChars_removesThem(self):
        result = unescape("{!!!{}", "!")
        self.assertEqual("{}", result)

    def test_remove_garbage_withSingleGarbage_removesIt(self):
        result = remove_garbage("{<abc>}")
        self.assertEqual("{}", result)

    def test_remove_garbage_withMultipleGarbage_removesAll(self):
        result = remove_garbage("{<abc>123<def>}")
        self.assertEqual("{123}", result)

    def test_remove_garbage_withGarbageStartCharInsideGarbage_removesIt(self):
        result = remove_garbage("{<<<<abc>}")
        self.assertEqual("{}", result)

    def test_count_withSingleNode_returns1(self):
        result = make_tree("{}").count()
        self.assertEqual(1, result)

    def test_count_withTwoChildren_returns5(self):
        result = make_tree("{{}{}}").count()
        self.assertEqual(5, result)

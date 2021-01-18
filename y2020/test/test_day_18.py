import unittest

from y2020.day_18 import parse, evaluate, tokenise, TokenType, evaluate_advanced


class TestDay18(unittest.TestCase):
    def test_evaluate_withNoBrackets(self):
        expr = "1 + 2 * 3 + 4 * 5 + 6"
        result = evaluate(parse(expr))
        self.assertEqual(71, result)

    def test_evaluate_withBrackets(self):
        expr = "1 + (2 * 3) + (4 * (5 + 6))"
        result = evaluate(parse(expr))
        self.assertEqual(51, result)

    def test_tokenise_withBrackets(self):
        expr = "(1 + 2)"
        result = tokenise(parse(expr))
        self.assertEqual(TokenType.CLOSE_BRACKET, result[4].type)

    def test_evaluate_adv_withNoBrackets(self):
        expr = "1 + 2 * 3 + 4 * 5 + 6"
        result = evaluate_advanced(parse(expr))
        self.assertEqual(231, result)
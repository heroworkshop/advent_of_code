import unittest

from y2021.day_18 import SnailfishNumber, make_snailfish_number, explode, make_snailfish_list, sf_list_to_str, split


class SnailFishList(unittest.TestCase):
    def test_explode_withNoLeft(self):
        n = make_snailfish_list("[[[[[9,7],1],2],3],4]")
        explode(n)
        self.assertEqual("[[[[0,8],2],3],4]", sf_list_to_str(n))

    def test_split(self):
        n = make_snailfish_list("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]")
        explode(n)
        split(n)
        self.assertEqual("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]", sf_list_to_str(n))


class TestSnailfishNumbers(unittest.TestCase):
    def test_make_snailfish_number_withSingleLevel(self):
        n = make_snailfish_number("[1,2]")
        self.assertEqual(1, n.left)
        self.assertEqual(2, n.right)

    def test_make_snailfish_number_withTwoLevels(self):
        n = make_snailfish_number("[1,[2,3]]")
        self.assertEqual(1, n.left)
        self.assertEqual(2, n.right.left)
        self.assertEqual(3, n.right.right)

    def test_explode_withNoLeft(self):
        n = make_snailfish_number("[[[[[9,7],1],2],3],4]")
        n.left.left.left.explode_left()
        s = n.render()
        self.assertEqual("[[[[0,8],2],3],4]", s)
        self.assertEqual(0, n.left.left.left.left)
        self.assertEqual(8, n.left.left.left.right)

    def test_reduce_withLeftAndRight(self):
        n = make_snailfish_number("[[6,[5,[4,[3,2]]]],1]")
        n.reduce()
        s = n.render()
        self.assertEqual("[[6,[5,[7,0]]],3]", s)

    def test_explode_withLeftAndRight(self):
        n = make_snailfish_number("[[6,[5,[4,[3,2]]]],1]")
        n.left.right.right.explode_right()
        s = n.render()
        self.assertEqual("[[6,[5,[7,0]]],3]", s)

    def test_explode_withLeftAndDescendingRight(self):
        n = make_snailfish_number("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
        n.left.right.right.explode_right()
        s = n.render()
        self.assertEqual("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", s)

    def test_explode_withNoRight(self):
        n = make_snailfish_number("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
        n.right.right.right.explode_right()
        s = n.render()
        self.assertEqual("[[3,[2,[8,0]]],[9,[5,[7,0]]]]", s)

    def test_magnitude(self):
        n = make_snailfish_number("[[9,1],[1,9]]")
        self.assertEqual(129, n.magnitude())

if __name__ == '__main__':
    unittest.main()

import unittest
from assertpy import assert_that

from y2022.day_13 import parse
from y2022.day_13 import packet_compare, Packet


class TestPacketCompare(unittest.TestCase):
    def test_empty_lists_leftShorter(self):
        entry = ("[]\n"
                 "[[]]")
        packet = parse(entry)
        assert_that(packet_compare(packet)).is_true()

    def test_empty_lists_rightShorter(self):
        entry = ("[[]]\n"
                 "[]")
        packet = parse(entry)
        assert_that(packet_compare(packet)).is_false()

    def test_ints(self):
        entry = ("[1,1,3,1,1]\n"
                 "[1,1,5,1,1]")
        packet = parse(entry)
        assert_that(packet_compare(packet)).is_true()

    def test_pair2(self):
        entry = ("[[1],[2,3,4]]\n"
                 "[[1],4]")
        packet = parse(entry)
        assert_that(packet_compare(packet)).is_true()

    def test_pair3(self):
        entry = ("[9]\n"
                 "[[8,7,6]]")
        packet = parse(entry)
        assert_that(packet_compare(packet)).is_false()

    def test_pair4(self):
        entry = ("[[4,4],4,4]\n"
                 "[[4,4],4,4,4]")
        packet = parse(entry)
        assert_that(packet_compare(packet)).is_true()

    def test_pair5(self):
        entry = ("[7,7,7,7]\n"
                 "[7,7,7]")
        packet = parse(entry)
        assert_that(packet_compare(packet)).is_false()

    def test_pair6(self):
        entry = ("[]\n"
                 "[3]")
        packet = parse(entry)
        assert_that(packet_compare(packet)).is_true()

    def test_pair7(self):
        entry = ("[[[]]]\n"
                 "[[]]")
        packet = parse(entry)
        assert_that(packet_compare(packet)).is_false()

    def test_pair8(self):
        entry = ("[1,[2,[3,[4,[5,6,7]]]],8,9]\n"
                 "[1,[2,[3,[4,[5,6,0]]]],8,9]")
        packet = parse(entry)
        assert_that(packet_compare(packet)).is_false()

    def test_pair8_inverted(self):
        entry = ("[1,[2,[3,[4,[5,6,0]]]],8,9]\n"
                 "[1,[2,[3,[4,[5,6,7]]]],8,9]")
        packet = parse(entry)
        assert_that(packet_compare(packet)).is_true()

    def test_short_left(self):
        entry = ("[2, 10, 6, 3]\n"
                 "[2, 10, 6, 3, 2]")
        packet = parse(entry)
        assert_that(packet_compare(packet)).is_true()

    def test_corner_case(self):
        entry = ("[[], [[], []], []]\n"
                 "[[], [[]], [[], 4], [3, [], [[4, 8, 8, 6, 6], [3, 2], 8]]]")
        packet = parse(entry)
        assert_that(packet_compare(packet)).is_false()



if __name__ == '__main__':
    unittest.main()

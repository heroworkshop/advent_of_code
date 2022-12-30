import unittest

from assertpy import assert_that

from aocd_tools import Pos
from y2022.day_17_part2 import GroundedBlocks, valid_bits


class TestGrounded(unittest.TestCase):
    def test_add_withEmptyGrounded(self):
        grounded = GroundedBlocks()
        grounded.add([1, 2, 3], Pos(0, 0))
        assert_that(grounded.top_y).is_equal_to(2)
        assert_that(grounded.rows[0]).is_equal_to(3)
        assert_that(grounded.rows[1]).is_equal_to(2)
        assert_that(grounded.rows[2]).is_equal_to(1)

    def test_add_withxPosEquals2(self):
        grounded = GroundedBlocks()
        grounded.add([1, 2, 3], Pos(2, 0))
        assert_that(grounded.top_y).is_equal_to(2)
        assert_that(grounded.rows[0]).is_equal_to(12)
        assert_that(grounded.rows[1]).is_equal_to(8)
        assert_that(grounded.rows[2]).is_equal_to(4)

    def test_add_withMultipleBlocks_dropsOldBlocks(self):
        grounded = GroundedBlocks()
        for i in range(4):
            grounded.add([1, 2, 3], Pos(0, i * 3))
        assert_that(grounded.top_y).is_equal_to(11)
        assert_that(grounded.rows[9]).is_equal_to(3)
        assert_that(grounded.rows[10]).is_equal_to(2)
        assert_that(grounded.rows[11]).is_equal_to(1)
        assert_that(1).is_not_in(grounded.rows)
        assert_that(0).is_not_in(grounded.rows)

    def test_overlaps_withBlockAboveGround(self):
        grounded = GroundedBlocks()
        grounded.add([1, 2, 3], Pos(2, 0))
        p = Pos(0, 3)
        row = 127
        assert_that(grounded.overlaps(p, row)).is_false()

    def test_overlaps_withBlockOverlappingGround(self):
        grounded = GroundedBlocks()
        grounded.add([1, 2, 3], Pos(2, 0))
        p = Pos(2, 2)
        row = 1
        assert_that(grounded.overlaps(p, row)).is_true()

    def test_render(self):
        grounded = GroundedBlocks()
        grounded.add([1, 2, 3], Pos(2, 0))
        grounded.add([127], Pos(0, 3))
        s = grounded.render()
        expected = ("|#######|\n"
                    "|..#....|\n"
                    "|...#...|\n"
                    "|..##...|\n"
                    "---------"
                    )
        assert_that(s).is_equal_to(expected)



class TestValidBits(unittest.TestCase):
    def test_withShiftedIntoLeftWall_returnsFalse(self):
        grounded = GroundedBlocks()
        shape = [1, 2, 3]
        pos = Pos(-1, 0)
        assert_that(valid_bits(pos, shape, grounded)).is_false()

    def test_withShiftedUpToRightWall_returnsTrue(self):
        # |.......|     |.......|
        # |#......|  => |.....#.|
        # |.#.....|     |......#|
        # |##.....|     |.....##|
        grounded = GroundedBlocks()
        shape = [1, 2, 3]
        pos = Pos(5, 0)
        assert_that(valid_bits(pos, shape, grounded)).is_true()

    def test_withShiftedIntoRightWall_returnsFalse(self):
        # |.......|     |.......|
        # |#......|  => |......#|
        # |.#.....|     |.......#
        # |##.....|     |......##
        grounded = GroundedBlocks()
        shape = [1, 2, 3]
        pos = Pos(6, 0)
        assert_that(valid_bits(pos, shape, grounded)).is_false()

    def test_withShiftedJustAboveGround_returnsTrue(self):
        grounded = GroundedBlocks()
        grounded.add([127], Pos(0, 0))
        shape = [1, 2, 3]
        pos = Pos(0, 1)
        assert_that(valid_bits(pos, shape, grounded)).is_true()

    def test_withShiftedIntoGround_returnsFalse(self):
        grounded = GroundedBlocks()
        grounded.add([127], Pos(0, 0))
        shape = [1, 2, 3]
        pos = Pos(0, 0)
        assert_that(valid_bits(pos, shape, grounded)).is_false()

    def test_withShiftedIntoGroundNonOverlapping_returnsTrue(self):
        grounded = GroundedBlocks()
        grounded.add([9], Pos(0, 0))
        shape = [1, 2, 3]
        pos = Pos(1, 0)
        assert_that(valid_bits(pos, shape, grounded)).is_true()

    def test_withShiftedIntoGroundOverlapping_returnsFalse(self):
        grounded = GroundedBlocks()
        grounded.add([9], Pos(0, 0))
        shape = [1, 2, 3]
        pos = Pos(0, 0)
        assert_that(valid_bits(pos, shape, grounded)).is_false()


if __name__ == '__main__':
    unittest.main()

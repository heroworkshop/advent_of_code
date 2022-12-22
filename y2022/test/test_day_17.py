import unittest

from assertpy import assert_that

from aocd_tools import Pos
from y2022.day_17 import make_rock_prefab_bits, GroundedBlocks, valid_bits


class TestPrefabs(unittest.TestCase):
    def test_make_rock_prefab_bits_withHorizontalBar_returnsSingleRow(self):
        s = "####"
        result = make_rock_prefab_bits(s)
        assert_that(result).is_equal_to([15])

    def test_make_rock_prefab_bits_withVerticalBar_returns4Times1Bit(self):
        s = (
            "#\n"
            "#\n"
            "#\n"
            "#"
        )
        result = make_rock_prefab_bits(s)
        assert_that(result).is_equal_to([1, 1, 1, 1])

    def test_make_rock_prefab_bits_withBox_returns2Times2Bit(self):
        s = (
            "##\n"
            "##"
        )
        result = make_rock_prefab_bits(s)
        assert_that(result).is_equal_to([3, 3])

    def test_make_rock_prefab_bits_withLShape_returnsCorrectPattern(self):
        s = (
            "..#\n"
            "..#\n"
            "###"
        )
        result = make_rock_prefab_bits(s)
        assert_that(result).is_equal_to([4, 4, 7])


class TestGroundedBlocks(unittest.TestCase):
    def test_add_row(self):
        blocks = GroundedBlocks()
        shape = [1, 2, 3]
        blocks.add(shape)
        assert_that(blocks.top).is_equal_to(2)
        assert_that(blocks.rows[blocks.top]).is_equal_to(1)
        assert_that(blocks.rows[blocks.top-1]).is_equal_to(2)
        assert_that(blocks.rows[blocks.top-2]).is_equal_to(3)

    def test_add_row_withShiftRight(self):
        blocks = GroundedBlocks()
        shape = [1, 2, 3]
        blocks.add(shape, x=2)
        assert_that(blocks.top).is_equal_to(2)
        assert_that(blocks.rows[blocks.top]).is_equal_to(4)
        assert_that(blocks.rows[blocks.top-1]).is_equal_to(8)
        assert_that(blocks.rows[blocks.top-2]).is_equal_to(12)

    def test_overlaps_withShapeAtTopRow_returnsTrue(self):
        blocks = GroundedBlocks()
        shape = [1, 2, 3]
        blocks.add(shape)
        assert_that(blocks.overlaps(Pos(0, 2), 7)).is_true()

    def test_overlaps_withShapeAboveTopRow_returnsFalse(self):
        blocks = GroundedBlocks()
        shape = [1, 2, 3]
        blocks.add(shape)
        assert_that(blocks.overlaps(Pos(0, 4), 7)).is_false()

    def test_overlaps_withShapeAtTopRowWithNonOverlappingShape_returnsFalse(self):
        blocks = GroundedBlocks()
        shape = [1, 2, 3]
        blocks.add(shape)
        assert_that(blocks.overlaps(Pos(0, 2), 6)).is_false()

    def test_overlaps_withShapeAtTopRowShiftedRightWithNonOverlappingShape_returnsFalse(self):
        blocks = GroundedBlocks()
        shape = [1, 2, 3]
        blocks.add(shape)
        assert_that(blocks.overlaps(Pos(1, 2), 7)).is_false()

    def test_overlaps_withShapeAtTopRowShiftedRightWithNonOverlappingShape_returnsFalse(self):
        blocks = GroundedBlocks()
        shape = [8, 2, 3]
        blocks.add(shape)
        assert_that(blocks.overlaps(Pos(3, 2), 1)).is_true()

    def test_overlaps_withShapeBelowTopRowWithNonOverlappingShape_returnsFalse(self):
        blocks = GroundedBlocks()
        shape = [1, 2, 3]
        blocks.add(shape)
        assert_that(blocks.overlaps(Pos(0, 0), 12)).is_false()

    def test_overlaps_withShapeBelowTopRowWithOverlappingShape_returnsTrue(self):
        blocks = GroundedBlocks()
        shape = [1, 2, 3]
        blocks.add(shape)
        assert_that(blocks.overlaps(Pos(0, 0), 2)).is_true()

    def test_overlaps_withShapeBelowBuffer_raisesRuntimeError(self):
        blocks = GroundedBlocks(buffer_size=11)
        shape = [1, 2, 3]
        for _ in range(4):
            blocks.add(shape)
        assert_that(blocks.overlaps).raises(RuntimeError).when_called_with(Pos(0, 0), 2)


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
        grounded.add([127])
        shape = [1, 2, 3]
        pos = Pos(0, 1)
        assert_that(valid_bits(pos, shape, grounded)).is_true()

    def test_withShiftedIntoGround_returnsFalse(self):
        grounded = GroundedBlocks()
        grounded.add([127])
        shape = [1, 2, 3]
        pos = Pos(0, 0)
        assert_that(valid_bits(pos, shape, grounded)).is_false()

    def test_withShiftedIntoGroundNonOverlapping_returnsTrue(self):
        grounded = GroundedBlocks()
        grounded.add([9])
        shape = [1, 2, 3]
        pos = Pos(1, 0)
        assert_that(valid_bits(pos, shape, grounded)).is_true()

    def test_withShiftedIntoGroundOverlapping_returnsFalse(self):
        grounded = GroundedBlocks()
        grounded.add([9])
        shape = [1, 2, 3]
        pos = Pos(0, 0)
        assert_that(valid_bits(pos, shape, grounded)).is_false()

if __name__ == '__main__':
    unittest.main()

import unittest

from assertpy import assert_that

from y2022.day_19 import Blueprint, Resources


class TestSolver(unittest.TestCase):
    # def test_solve_withExampleBlueprint1(self):
    #     blueprint = Blueprint(1, Resources(ore=4),
    #                           Resources(ore=2),
    #                           Resources(ore=3, clay=14),
    #                           Resources(ore=2, obsidian=7))
    #     after_18 = blueprint.geodes_mined(18)
    #     assert_that(after_18).is_equal_to(0)
    #     after_19 = blueprint.geodes_mined(19)
    #     assert_that(after_19).is_equal_to(1)
    def test_withFreeGeodeRobots(self):
        blueprint = Blueprint(1, ore=Resources(ore=1),
                              clay=Resources(ore=1),
                              obsidian=Resources(ore=0, clay=1),
                              geode=Resources())
        result = blueprint.geodes_mined(2)
        assert_that(result).is_equal_to(1)

    def test_solve_withJustEnoughForOneGeode_returns1(self):
        """for 1 geode robot, need 1 obsidian
        for obsidian robot need 1 clay
        for clay robot need 1 ore.

        t=1 make 1 ore
        t=2 make 1 clay robot
        t=3 make 1 clay
        t=4 make 1 obsidian robot
        t=5 make 1 obsidian
        t=6 make geode robot
        t=7 make 1 geode
        """
        blueprint = Blueprint(1, ore=Resources(ore=1),
                              clay=Resources(ore=1),
                              obsidian=Resources(ore=0, clay=1),
                              geode=Resources(ore=0, obsidian=1))
        after_7 = blueprint.geodes_mined(7)
        assert_that(after_7).is_equal_to(1)

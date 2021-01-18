import unittest

from aocd_tools import grid_from_lines
from y2018.day_13 import extract_cars, Car

example_map = r"""
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """.strip()


class TestCars(unittest.TestCase):
    def test_index_orderedByPosition(self):
        car1 = Car((5, 5), "<")
        car2 = Car((10, 5), ">")
        car3 = Car((5, 6), ">")
        self.assertLess(car1.index(), car2.index())
        self.assertLess(car1.index(), car3.index())

    def test_move_withEastboundCar_movesEast(self):
        input_data = "-->--"
        grid = grid_from_lines(input_data)
        cars = extract_cars(grid)
        cars[0].move(grid)
        self.assertEqual((3, 0), cars[0].pos)

    def test_move_withWestboundCar_movesWest(self):
        input_data = "--<--"
        grid = grid_from_lines(input_data)
        cars = extract_cars(grid)
        cars[0].move(grid)
        self.assertEqual((1, 0), cars[0].pos)

    def test_move_withNorthboundCar_movesNorth(self):
        input_data = ("|\n"
                      "^\n"
                      "|")
        grid = grid_from_lines(input_data)
        cars = extract_cars(grid)
        cars[0].move(grid)
        self.assertEqual((0, 0), cars[0].pos)

    def test_move_withSouthboundCar_movesSouth(self):
        input_data = ("|\n"
                      "v\n"
                      "|")
        grid = grid_from_lines(input_data)
        cars = extract_cars(grid)
        cars[0].move(grid)
        self.assertEqual((0, 2), cars[0].pos)

    def test_turn_withOneCrossroad_turnsLeft(self):
        car = Car((0, 0), ">")
        car.on_tile("+")
        self.assertEqual((0, -1), car.vel)

    def test_turn_withTwoCrossroad_turnsLeftThenStraight(self):
        car = Car((0, 0), ">")
        car.on_tile("+")
        car.on_tile("+")
        self.assertEqual((0, -1), car.vel)

    def test_turn_withThreeCrossroads_turnsLeftThenStraightThenRight(self):
        car = Car((0, 0), ">")
        car.on_tile("+")
        car.on_tile("+")
        car.on_tile("+")
        self.assertEqual((1, 0), car.vel)

    def test_turn_withFourCrossroads_turnsLeftThenStraightThenRightThenLeft(self):
        car = Car((0, 0), ">")
        car.on_tile("+")
        car.on_tile("+")
        car.on_tile("+")
        car.on_tile("+")
        self.assertEqual((0, -1), car.vel)

class TestExtractCars(unittest.TestCase):
    def setUp(self):
        self.grid = grid_from_lines(example_map)

    def test_extract_cars_returnsCorrectCoords(self):
        cars = extract_cars(self.grid)
        coords = {c.pos for c in cars}
        self.assertIn((2, 0), coords)
        self.assertIn((9, 3), coords)

    def test_extract_cars_withEasterlyCar_isMovingEast(self):
        input_data = "-->--"
        cars = extract_cars(grid_from_lines(input_data))
        self.assertEqual((1, 0), cars[0].vel)

    def test_extract_cars_withWesterlyCar_isMovingWest(self):
        input_data = "--<--"
        cars = extract_cars(grid_from_lines(input_data))
        self.assertEqual((-1, 0), cars[0].vel)

    def test_extract_cars_withNortherlyCar_isMovingNorth(self):
        input_data = "|\n|\n|\n^\n|\n|"
        cars = extract_cars(grid_from_lines(input_data))
        self.assertEqual((0, -1), cars[0].vel)

    def test_extract_cars_withSoutherlyCar_isMovingSouth(self):
        input_data = "|\n|\n|\nv\n|\n|"
        cars = extract_cars(grid_from_lines(input_data))
        self.assertEqual((0, 1), cars[0].vel)

    def test_extract_cars_withCars_replacesWithTrack(self):
        input_data = "-->--<--v--^--"
        grid = grid_from_lines(input_data)
        extract_cars(grid)
        self.assertEqual("--------|--|--", grid.render().strip())


if __name__ == '__main__':
    unittest.main()

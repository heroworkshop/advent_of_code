import copy
import itertools
from contextlib import suppress

from aocd_tools import load_input_data, grid_from_lines

example1 = r"""
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """.strip()

example2 = r"""
/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/""".strip()


class Car:
    def __init__(self, pos, ch, grid_width=100000):
        self.pos = pos
        self.vel = self.vel_from_ch(ch)
        self.width = grid_width
        self.turn_schedule = itertools.cycle([self.turn_left, self.straight, self.turn_right])

    @staticmethod
    def vel_from_ch(ch):
        vel = {"<": (-1, 0),
               ">": (1, 0),
               "^": (0, -1),
               "v": (0, 1)}
        return vel[ch]

    def index(self):
        return self.pos[0] + self.pos[1] * self.width

    def move(self):
        self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])

    def on_tile(self, tile):
        if tile == "+":
            turn = next(self.turn_schedule)
            turn()
        elif tile == "\\":
            if self.vel[0]:
                self.turn_right()
            else:
                self.turn_left()
        elif tile == r"/":
            if self.vel[0]:
                self.turn_left()
            else:
                self.turn_right()

    def turn_left(self):
        # 1, 0 -> 0, -1
        # -1, 0 -> 0, 1
        # 0, 1 -> 1, 0
        # 0, -1 -> -1, 0
        self.vel = (self.vel[1], -self.vel[0])

    def turn_right(self):
        # 1, 0 -> 0, 1
        # -1, 0 -> 0, -1
        # 0, 1 -> -1, 0
        # 0, -1 -> 1, 0
        self.vel = (-self.vel[1], self.vel[0])

    def straight(self):
        pass


def extract_cars(grid):
    track_replacements = {
        ">": "-",
        "<": "-",
        "^": "|",
        "v": "|",
    }
    cars = []
    for p, ch in grid.grid.items():
        if ch in "<>^v":
            cars.append(Car(p, ch))
            grid.grid[p] = track_replacements[ch]
    return cars


def car_index(car):
    return car.index()


def render_grid(grid, cars):
    car_repr = {(0, 1): "v",
                (0, -1): "^",
                (1, 0): ">",
                (-1, 0): "<"
                }
    prerendered_grid = copy.deepcopy(grid)

    for c in cars:
        prerendered_grid.grid[c.pos] = car_repr[c.vel]

    return prerendered_grid.render()

def run():
    # input_data = example2
    input_data = load_input_data(2018, 13)
    print(f"loaded input data ({len(input_data)} bytes)")

    grid = grid_from_lines(input_data)
    print(grid.render())

    cars = extract_cars(grid)
    positions = {c.pos for c in cars}
    while len(cars) > 1:
        cars.sort(key=car_index)
        for car in cars:
            with suppress(KeyError):
                positions.remove(car.pos)
            car.move()
            positions.add(car.pos)
            if len(positions) != len(cars):
                crash_pos = car.pos
                print("collision at ", crash_pos)
                cars = find_cars_not_at(cars, crash_pos)
                positions = {c.pos for c in cars}
                continue
            car.on_tile(grid.at(car.pos))
        # print(render_grid(grid, cars))
    print("last car at ", cars[0].pos)


def remove_cars_at(cars, pos):
    for c in cars:
        if c.pos == pos:
            cars.remove(c)


def find_cars_not_at(cars, pos):
    return [c for c in cars if c.pos != pos]


if __name__ == "__main__":
    run()

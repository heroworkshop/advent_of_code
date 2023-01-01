import threading
from functools import partial
from time import sleep

import pygame

from grid.controller import PygameGridController
from grid.model import Grid
from grid.view import PygameGridView
from aocd_tools import Grid as AocGrid, Pos

from day_22 import run as solver_run

WIDTH, HEIGHT = 1200, 800
CELL_SIZE = 4

COLOUR_VALS = {
    "#": 1,
    " ": 0,
}


def draw_background(surf):
    surf.fill((0, 0, 0))


class Controller(PygameGridController):
    def __init__(self, screen):
        super().__init__(None)
        self.screen = screen
        self.grid = None
        self.last_pos = None

    def redraw(self):
        if self.view:
            self.view.draw()

    def initialise_view(self, aoc_grid):
        grid = Grid(aoc_grid.width, aoc_grid.height)
        width = grid.width * CELL_SIZE
        height = grid.height * CELL_SIZE
        self.view = PygameGridView(grid, width, height, CELL_SIZE, self.screen)
        self.view.show_grid = False

    def update(self, player, aoc_grid: AocGrid):
        if not self.view:
            self.initialise_view(aoc_grid)
            self.update_from_aoc_grid(aoc_grid)
        if self.last_pos is not None:
            self.interpolate(player.pos, self.last_pos)
        self.last_pos = player.pos
        self.view.grid.fill_cell(*player.pos, 3)
        sleep(0.01)

    def interpolate(self, to_pos, from_pos):
        dx, dy = to_pos - from_pos
        dx = dx // abs(dx) if dx else 0
        dy = dy // abs(dy) if dy else 0
        dp = Pos(dx, dy)
        p = from_pos
        while p != to_pos:
            p = p + dp
            self.view.grid.fill_cell(*p, 2)

    def on_event(self, event):
        super().on_event(event)
        if event.type != pygame.KEYDOWN:
            return

    def start_solver(self):
        solver = partial(solver_run, self)
        self.search = threading.Thread(target=solver)
        self.search.start()

    def update_from_aoc_grid(self, aoc_grid: AocGrid):
        self.view.grid.clear()
        for k, v in aoc_grid.grid.items():
            self.view.grid.fill_cell(*k, COLOUR_VALS.get(v, 0))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    controller = Controller(screen)

    controller.start_solver()
    while running:
        clock.tick(50)
        draw_background(screen)

        controller.redraw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            controller.on_event(event)

        pygame.display.flip()


if __name__ == "__main__":
    main()

import threading
from functools import partial
from time import sleep

import pygame

from aocd_tools import Grid as AocGrid, Pos
from grid.controller import PygameGridController
from grid.model import Grid
from grid.view import PygameGridView


class AocController(PygameGridController):
    def __init__(self, screen, solver_run, colour_vals, cell_size=8):
        super().__init__(None)
        self.screen = screen
        self.grid = None
        self.last_pos = None
        self.search = None
        self.solver_run = solver_run
        self.cell_size = cell_size
        self.colour_vals = colour_vals
        self.sleep_between_frames = 0.01

    def redraw(self):
        if self.view:
            with self.view.grid.lock:
                self.view.draw()

    def initialise_view(self, aoc_grid):
        grid = Grid(aoc_grid.width, aoc_grid.height)
        width = grid.width * self.cell_size
        height = grid.height * self.cell_size
        self.view = PygameGridView(grid, width, height, self.cell_size, self.screen)
        self.view.show_grid = False

    def update(self, aoc_grid: AocGrid):
        if not self.view:
            self.initialise_view(aoc_grid)
        self.update_from_aoc_grid(aoc_grid)
        sleep(self.sleep_between_frames)

    def on_event(self, event):
        super().on_event(event)
        if event.type == pygame.MOUSEWHEEL:
            self.zoom(1 if event.y > 0 else -1)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS:
                self.zoom(1)
            elif event.key == pygame.K_MINUS:
                self.zoom(-1)
            elif event.key == pygame.K_LEFT:
                self.view.offset += Pos(self.cell_size, 0)
            elif event.key == pygame.K_RIGHT:
                self.view.offset += Pos(-self.cell_size, 0)
            elif event.key == pygame.K_UP:
                self.view.offset += Pos(0, self.cell_size)
            elif event.key == pygame.K_DOWN:
                self.view.offset += Pos(0, -self.cell_size)

    def start_solver(self):
        solver = partial(self.solver_run, self)
        self.search = threading.Thread(target=solver)
        self.search.start()

    def update_from_aoc_grid(self, aoc_grid: AocGrid):
        self.view.grid.clear()
        for k, v in aoc_grid.grid.items():
            self.view.grid.fill_cell(*k, self.colour_vals.get(v, 0))

    def zoom(self, amount):
        self.view.pixel_size = max(1, self.view.pixel_size + amount)

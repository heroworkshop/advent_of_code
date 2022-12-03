import threading

import pygame

import y2021
from grid.model import Grid
from grid.controller import PygameGridController
from grid.view import PygameGridView
from y2021.day25_visualisation.solver import setup_grid, run

CELL_SIZE = 4


class SeaCucumberGridView(PygameGridView):
    COLOUR_TABLE = {
        ">": (0xff, 0x00, 0x00),
        ".": (0x10, 0x10, 0x10),
        "v": (0x00, 0x00, 0xff),
        }


def main():
    grid = setup_grid()
    width = grid.width * CELL_SIZE
    height = grid.height * CELL_SIZE

    pygame.init()
    screen = pygame.display.set_mode([width, height])
    clock = pygame.time.Clock()

    # grid = Grid(grid.width, grid.height)
    grid_view = SeaCucumberGridView(grid, width, height, CELL_SIZE, screen)
    grid_controller = PygameGridController(grid_view)

    finished = False
    while not finished:
        clock.tick(25)
        screen.fill((0, 0, 0))
        grid_view.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                y2021.day25_visualisation.solver.stop_threads = True
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    finished = True
                if event.key == pygame.K_r:
                    grid.clear()
                if event.key == pygame.K_c:
                    grid.clear()
                if event.key == pygame.K_SPACE:
                    search = threading.Thread(target=run,
                                              args=(grid,))
                    search.start()
            grid_controller.on_event(event)

        grid_controller.handle_mouse()


if __name__ == "__main__":
    main()

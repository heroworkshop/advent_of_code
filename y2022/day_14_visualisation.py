import pygame

from grid_controller import AocController
from day_14 import run as solver_run

WIDTH, HEIGHT = 1200, 800
CELL_SIZE = 1

COLOUR_VALS = {
    "#": 1,
    ".": 0,
    "o": 2
}


def draw_background(surf):
    surf.fill((0, 0, 0))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    controller = AocController(screen=screen, solver_run=solver_run, colour_vals=COLOUR_VALS, cell_size=CELL_SIZE)

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

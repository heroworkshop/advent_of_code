from contextlib import suppress

import pygame


class PygameGridController:
    def __init__(self, view):
        self.view = view
        self.pen_colour = 3

    def on_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_c:
            self.view.grid.clear()
        elif event.key == pygame.K_g:
            self.view.show_grid = not self.view.show_grid

    def grid_pos_from_screen_pos(self, pos):
        x, y = pos
        col = x // self.view.pixel_size
        row = y // self.view.pixel_size
        return col, row

    def handle_mouse(self):
        if pygame.mouse.get_pressed()[0]:
            gx, gy = self.grid_pos_from_screen_pos(pygame.mouse.get_pos())
            self.view.grid.fill_cell(gx, gy, self.pen_colour)


class PygameNumberGridController(PygameGridController):
    keys = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
            pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            with suppress(ValueError):
                n = self.keys.index(event.key)
                self.view.grid.fill_cell(*self.view.selected, n)

    def handle_mouse(self):
        if pygame.mouse.get_pressed()[0]:
            gx, gy = self.grid_pos_from_screen_pos(pygame.mouse.get_pos())
            self.view.selected = (gx, gy)

import pygame


class PygameGridView:
    COLOUR_TABLE = {
        0: (0x88, 0x88, 0x88),
        1: (0xaa, 0xaa, 0xaa),
        2: (0x00, 0xff, 0x00),
        3: (0xff, 0x00, 0x00),
        4: (0x00, 0x00, 0xff),
        5: (0xff, 0xff, 0xff),
        6: (0x00, 0xff, 0xff),
        7: (0xff, 0xff, 0x00),
        8: (0xff, 0x00, 0xff),
        9: (0xff, 0x66, 0x33),
    }

    def __init__(self, grid, width, height, pixel_size, screen):
        self.grid = grid
        self.width = width
        self.height = height
        self.pixel_size = pixel_size
        self.selected = (0, 0)
        self.grid_line_width = 1
        self.show_grid = True
        self.screen = screen

    def draw(self):
        for row, y in enumerate(range(0, self.height, self.pixel_size)):
            for col, x in enumerate(range(0, self.width, self.pixel_size)):
                self.draw_pixel((col, row), (x, y))

    def draw_pixel(self, grid_position, position):
        pixel_value = self.grid.value(*grid_position)
        if not pixel_value and not self.show_grid:
            return
        border_width = 0 if pixel_value else self.grid_line_width
        colour = self.COLOUR_TABLE[pixel_value]
        x, y = position
        pixel_rect = pygame.Rect(x, y, self.pixel_size, self.pixel_size)
        pygame.draw.rect(self.screen, colour, pixel_rect, border_width)


class PygameNumberGridView(PygameGridView):
    def draw_pixel(self, grid_position, position):
        pixel_value = self.grid.value(*grid_position)
        width = 1
        colour = self.COLOUR_TABLE[4] if self.selected == grid_position else self.COLOUR_TABLE[1]
        x, y = position
        pixel_rect = pygame.Rect(x, y, self.pixel_size, self.pixel_size)
        pygame.draw.rect(self.screen, colour, pixel_rect, width)
        font = pygame.font.SysFont("comicsansms", 30)

        if pixel_value:
            if not self.grid.is_valid(*grid_position):
                colour = self.COLOUR_TABLE[3]
            text = font.render(str(pixel_value), True, colour)
            dx = (pixel_rect.width - text.get_width()) // 2
            dy = (pixel_rect.height - text.get_height()) // 2
            self.screen.blit(text, (pixel_rect.x + dx, pixel_rect.y + dy))


class PygameSudokuGridView(PygameNumberGridView):
    def draw(self):
        colour = self.COLOUR_TABLE[5]
        for row, y in enumerate(range(0, self.height, self.pixel_size * 3)):
            for col, x in enumerate(range(0, self.width, self.pixel_size * 3)):
                rect = pygame.Rect(x, y, self.pixel_size * 3, self.pixel_size * 3)
                pygame.draw.rect(self.screen, colour, rect, 3)
        with self.grid.lock:
            super().draw()

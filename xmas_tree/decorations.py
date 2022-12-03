from random import randint

import pygame


def dim(color):
    r, g, b = color
    return r // 5, g // 5, b // 5


class Decoration(pygame.sprite.Sprite):
    def __init__(self, color, position, radius=20):
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.colors = [color, dim(color)]
        self.color = color
        self.frame = 0
        self.timer = randint(0, 2) * 25
        self.position = position
        self.image = self.setup_image()
        self.refresh_image()

    def update(self):
        self.timer += 1
        if self.timer == 51:
            self.timer = 0
            self.frame += 1
            self.color = self.colors[self.frame % len(self.colors)]
            self.refresh_image()

    def setup_image(self):
        pass

    def refresh_image(self):
        pass


class XmasLight(Decoration):
    def __init__(self, color, position, radius=20):
        super().__init__(color, position, radius)

    def setup_image(self):
        return pygame.Surface([self.radius * 2, self.radius * 2])

    def refresh_image(self):
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
        self.image.set_colorkey((0, 0, 0))

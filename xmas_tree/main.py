from random import randint, choice

import pygame

from xmas_tree.decorations import XmasLight

WIDTH, HEIGHT = 800, 600
TREE_GREEN = (0, 200, 50)
LIGHT_COLORS = [
    (255, 255, 50),
    (255, 50, 20),
    (100, 100, 255)
]

def draw_background(surf):
    surf.fill((0, 0, 0))

    cx, cy = WIDTH // 2, HEIGHT // 2
    size = size0 = 600
    y = HEIGHT - size // 3
    for n in range(5):
        t = [(cx - size // 2, y), (cx + size // 2, y), (cx, y - size // 3)]
        size = int(size * 0.75)
        y -= size // 4
        pygame.draw.polygon(surf, points=t, color=TREE_GREEN, width=0)

    r = pygame.Rect((cx - size0 // 14, cy + 100, size0 // 7, size0 // 6))
    pygame.draw.rect(surf, (200, 100, 50), r, 0)





def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    running = True

    draw_background(screen)

    all_sprites = pygame.sprite.Group()
    while len(all_sprites) < 50:
        x, y = randint(0, WIDTH-1), randint(0, HEIGHT-1)
        if screen.get_at((x, y)) == TREE_GREEN:
            color = choice(LIGHT_COLORS)
            all_sprites.add(XmasLight(color, (x, y), 5))

    while running:
        clock.tick(60)

        draw_background(screen)
        for sprite in all_sprites:
            screen.blit(sprite.image, sprite.rect)
        all_sprites.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()


if __name__ == "__main__":
    main()

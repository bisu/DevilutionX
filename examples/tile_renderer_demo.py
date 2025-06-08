"""Simple demo of isometric tile rendering using Pygame."""

import pygame
import random

TILE_WIDTH = 64
TILE_HEIGHT = 32
MAP_WIDTH = 10
MAP_HEIGHT = 10

# Simple player sprite size
PLAYER_RADIUS = 12

# Colors for a few tile types
TILE_COLORS = [
    (110, 170, 70),  # grass
    (194, 194, 194), # stone
    (120, 70, 20),   # dirt
    (0, 120, 160),   # water
]


def create_tile_surfaces():
    """Return a surface for each tile color shaped as an isometric diamond."""
    tiles = []
    for color in TILE_COLORS:
        surf = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)
        # Draw diamond shape
        points = [
            (TILE_WIDTH // 2, 0),
            (TILE_WIDTH - 1, TILE_HEIGHT // 2),
            (TILE_WIDTH // 2, TILE_HEIGHT - 1),
            (0, TILE_HEIGHT // 2),
        ]
        pygame.draw.polygon(surf, color, points)
        tiles.append(surf)
    return tiles


def random_map():
    return [[random.randrange(len(TILE_COLORS)) for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]


class TileRenderer:
    def __init__(self, screen, tiles, origin):
        self.screen = screen
        self.tiles = tiles
        self.origin_x, self.origin_y = origin

    def draw_map(self, grid):
        for y, row in enumerate(grid):
            for x, tile in enumerate(row):
                sx = (x - y) * (TILE_WIDTH // 2) + self.origin_x
                sy = (x + y) * (TILE_HEIGHT // 2) + self.origin_y
                self.screen.blit(self.tiles[tile], (sx, sy))


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        size = PLAYER_RADIUS * 2
        self.surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, (255, 50, 50), (PLAYER_RADIUS, PLAYER_RADIUS), PLAYER_RADIUS)

    def move(self, dx, dy):
        self.x = max(0, min(MAP_WIDTH - 1, self.x + dx))
        self.y = max(0, min(MAP_HEIGHT - 1, self.y + dy))

    def draw(self, screen, origin):
        sx = (self.x - self.y) * (TILE_WIDTH // 2) + origin[0]
        sy = (self.x + self.y) * (TILE_HEIGHT // 2) + origin[1] - PLAYER_RADIUS
        screen.blit(self.surface, (sx, sy))


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    tiles = create_tile_surfaces()
    grid = random_map()
    origin = (400, 100)
    renderer = TileRenderer(screen, tiles, origin=origin)
    player = Player(MAP_WIDTH // 2, MAP_HEIGHT // 2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1)
                elif event.key == pygame.K_LEFT:
                    player.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0)

        screen.fill((0, 0, 0))
        renderer.draw_map(grid)
        player.draw(screen, origin)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

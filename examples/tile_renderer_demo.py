"""Simple demo of isometric tile rendering using Pygame."""

import pygame
import random

TILE_WIDTH = 64
TILE_HEIGHT = 32
MAP_WIDTH = 10
MAP_HEIGHT = 10

# Player sprite size
PLAYER_WIDTH = 28
PLAYER_HEIGHT = 40

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


def create_player_frames():
    """Create a very simple male character with two walking frames."""
    skin_color = (210, 160, 120)
    shirt_color = random.choice([(40, 80, 180), (180, 60, 60), (60, 140, 60)])
    pants_color = random.choice([(30, 30, 100), (50, 50, 50), (20, 60, 120)])

    frames = []
    for step in range(2):
        surf = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        head_center = (PLAYER_WIDTH // 2, 6)
        pygame.draw.circle(surf, skin_color, head_center, 5)
        pygame.draw.rect(surf, shirt_color, (PLAYER_WIDTH // 2 - 4, 12, 8, 10))
        arm_y = 14
        pygame.draw.rect(surf, shirt_color, (PLAYER_WIDTH // 2 - 8, arm_y, 4, 8))
        pygame.draw.rect(surf, shirt_color, (PLAYER_WIDTH // 2 + 4, arm_y, 4, 8))
        leg_y = 22
        if step == 0:
            pygame.draw.rect(surf, pants_color, (PLAYER_WIDTH // 2 - 5, leg_y, 4, 12))
            pygame.draw.rect(surf, pants_color, (PLAYER_WIDTH // 2 + 1, leg_y, 4, 12))
        else:
            pygame.draw.rect(surf, pants_color, (PLAYER_WIDTH // 2 - 6, leg_y, 4, 12))
            pygame.draw.rect(surf, pants_color, (PLAYER_WIDTH // 2 + 2, leg_y, 4, 12))
        frames.append(surf)
    return frames


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
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.frames = create_player_frames()
        self.frame = 0
        self.anim_time = 0.0

    def update(self, dx, dy, dt):
        """Move the player smoothly and advance animation when walking."""
        speed = 2.0  # tiles per second (slower movement)

        target_vx = dx * speed
        target_vy = dy * speed
        smooth = min(1.0, 10.0 * dt)
        self.vx += (target_vx - self.vx) * smooth
        self.vy += (target_vy - self.vy) * smooth

        self.x += self.vx * dt
        self.y += self.vy * dt
        self.x = max(0, min(MAP_WIDTH - 1, self.x))
        self.y = max(0, min(MAP_HEIGHT - 1, self.y))

        if abs(self.vx) > 0.01 or abs(self.vy) > 0.01:
            self.anim_time += dt
            if self.anim_time >= 0.2:
                self.anim_time = 0.0
                self.frame = (self.frame + 1) % len(self.frames)

    def draw(self, screen, origin):
        sx = (self.x - self.y) * (TILE_WIDTH // 2) + origin[0] - PLAYER_WIDTH // 2
        sy = (self.x + self.y) * (TILE_HEIGHT // 2) + origin[1] - PLAYER_HEIGHT
        screen.blit(self.frames[self.frame], (sx, sy))


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
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        player.update(dx, dy, dt)

        screen.fill((0, 0, 0))
        renderer.draw_map(grid)
        player.draw(screen, origin)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

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


def create_obstacle_surfaces():
    """Return surfaces for tree and rock obstacles."""
    surfaces = {}
    # Tree: trunk with green canopy
    tree = pygame.Surface((32, 48), pygame.SRCALPHA)
    pygame.draw.rect(tree, (100, 60, 20), (14, 28, 4, 12))
    pygame.draw.circle(tree, (30, 140, 30), (16, 20), 12)
    surfaces["tree"] = tree

    # Rock: small gray boulder
    rock = pygame.Surface((32, 24), pygame.SRCALPHA)
    pygame.draw.polygon(rock, (120, 120, 120), [(4, 20), (16, 4), (28, 20)])
    pygame.draw.polygon(rock, (160, 160, 160), [(6, 18), (16, 8), (26, 18)])
    surfaces["rock"] = rock
    return surfaces


def random_obstacles(surfaces, count=12):
    """Create a list of obstacles and a set of blocked tiles."""
    obstacles = []
    blocked = set()
    while len(obstacles) < count:
        x = random.randint(0, MAP_WIDTH - 1)
        y = random.randint(0, MAP_HEIGHT - 1)
        if (x, y) in blocked or (x == MAP_WIDTH // 2 and y == MAP_HEIGHT // 2):
            continue
        kind = random.choice(list(surfaces.keys()))
        obstacles.append({"x": x, "y": y, "kind": kind})
        blocked.add((x, y))
    return obstacles, blocked


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

    def draw_objects(self, player, obstacles, surfaces):
        """Draw the player together with obstacles with correct occlusion."""
        objects = [{"x": player.x, "y": player.y, "kind": "player"}]
        for ob in obstacles:
            objects.append({"x": ob["x"], "y": ob["y"], "kind": ob["kind"]})

        objects.sort(key=lambda o: o["x"] + o["y"])

        for obj in objects:
            sx = (obj["x"] - obj["y"]) * (TILE_WIDTH // 2) + self.origin_x
            sy = (obj["x"] + obj["y"]) * (TILE_HEIGHT // 2) + self.origin_y

            if obj["kind"] == "player":
                sx -= PLAYER_WIDTH // 2
                sy -= PLAYER_HEIGHT
                self.screen.blit(player.frames[player.frame], (sx, sy))
            else:
                surf = surfaces[obj["kind"]]
                sx -= surf.get_width() // 2
                sy -= surf.get_height()
                self.screen.blit(surf, (sx, sy))


class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.frames = create_player_frames()
        self.frame = 0
        self.anim_time = 0.0

    def update(self, dx, dy, dt, blocked):
        """Move the player smoothly with basic collision handling."""
        speed = 2.0  # tiles per second (slower movement)

        target_vx = dx * speed
        target_vy = dy * speed
        smooth = min(1.0, 10.0 * dt)
        self.vx += (target_vx - self.vx) * smooth
        self.vy += (target_vy - self.vy) * smooth

        new_x = self.x + self.vx * dt
        new_y = self.y + self.vy * dt

        if (round(new_x), round(self.y)) not in blocked:
            self.x = new_x
        else:
            self.vx = 0.0

        if (round(self.x), round(new_y)) not in blocked:
            self.y = new_y
        else:
            self.vy = 0.0

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
    obstacle_surfaces = create_obstacle_surfaces()
    grid = random_map()
    obstacles, blocked = random_obstacles(obstacle_surfaces)
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
        player.update(dx, dy, dt, blocked)

        screen.fill((0, 0, 0))
        renderer.draw_map(grid)
        renderer.draw_objects(player, obstacles, obstacle_surfaces)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

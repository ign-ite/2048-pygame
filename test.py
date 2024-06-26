import pygame
import random
import math
import numpy as np
import copy

pygame.init()

FPS = 60

WIDTH, HEIGHT = 800, 800
ROWS = 4
COLS = 4

RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLS

OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)

FONT = pygame.font.SysFont("comicsans", 60, bold=True)
MOVE_VEL = 20

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")


class Tile:
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT

    def get_color(self):
        color_index = int(math.log2(self.value)) - 1
        color = self.COLORS[color_index]
        return color

    def draw(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        text = FONT.render(str(self.value), 1, FONT_COLOR)
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]


def draw_grid(window):
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)


def draw(window, tiles):
    window.fill(BACKGROUND_COLOR)

    for tile in tiles.values():
        tile.draw(window)

    draw_grid(window)

    pygame.display.update()


def get_random_pos(tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)

        if f"{row}{col}" not in tiles:
            break

    return row, col


def move_tiles(tiles, direction):
    moved = False
    blocks = set()

    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-1, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (1, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -1)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, 1)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")

    sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

    for tile in sorted_tiles:
        if boundary_check(tile):
            continue

        next_tile = get_next_tile(tile)
        while next_tile and next_tile.value == 0:
            tile.row += delta[1]
            tile.col += delta[0]
            next_tile = get_next_tile(tile)
            moved = True

        if next_tile and next_tile.value == tile.value and next_tile not in blocks:
            next_tile.value *= 2
            tile.value = 0
            blocks.add(next_tile)
            moved = True
        else:
            tile.row -= delta[1]
            tile.col -= delta[0]

    return moved


def add_random_tile(tiles):
    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)


def end_move(tiles):
    if len(tiles) == 16:
        return "lost"

    add_random_tile(tiles)
    return "continue"


def update_tiles(tiles):
    updated_tiles = {}
    for tile in tiles.values():
        if tile.value != 0:
            updated_tiles[f"{tile.row}{tile.col}"] = tile
    return updated_tiles


def generate_tiles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles


def simulate_move(tiles, direction):
    new_tiles = copy.deepcopy(tiles)
    moved = move_tiles(new_tiles, direction)
    if not moved:
        return tiles, 0

    new_tiles = update_tiles(new_tiles)
    add_random_tile(new_tiles)
    score = sum(tile.value for tile in new_tiles.values())
    return new_tiles, score


def mcts(tiles, simulations=100):
    directions = ["left", "right", "up", "down"]
    scores = {direction: 0 for direction in directions}

    for direction in directions:
        for _ in range(simulations):
            new_tiles, score = simulate_move(tiles, direction)
            scores[direction] += score

    best_direction = max(scores, key=scores.get)
    return best_direction


def main(window):
    clock = pygame.time.Clock()
    run = True

    tiles = generate_tiles()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Use MCTS to determine the best move
        best_move = mcts(tiles)
        moved = move_tiles(tiles, best_move)

        if moved:
            tiles = update_tiles(tiles)
            add_random_tile(tiles)

        draw(window, tiles)

    pygame.quit()


if __name__ == "__main__":
    main(WINDOW)

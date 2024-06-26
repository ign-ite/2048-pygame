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
    score = 0
    blocks = set()

    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        )
        ceil = True
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        )
        ceil = False
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        )
        ceil = True
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
        )
        ceil = False

    sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

    for i, tile in enumerate(sorted_tiles):
        if boundary_check(tile):
            continue

        next_tile = get_next_tile(tile)
        if not next_tile:
            tile.move((delta[0] * RECT_WIDTH, delta[1] * RECT_HEIGHT))
            moved = True
        elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
            if merge_check(tile, next_tile):
                tile.move((delta[0] * RECT_WIDTH, delta[1] * RECT_HEIGHT))
            else:
                next_tile.value *= 2
                score += next_tile.value
                sorted_tiles.pop(i)
                blocks.add(next_tile)
                moved = True
        elif move_check(tile, next_tile):
            tile.move((delta[0] * RECT_WIDTH, delta[1] * RECT_HEIGHT))
            moved = True
        else:
            continue

        tile.set_pos(ceil)

    update_tiles(tiles, sorted_tiles)
    return moved, score


def end_move(tiles):
    if len(tiles) == 16:
        return "lost"

    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"


def update_tiles(tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile


def generate_tiles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles


def add_random_tile(tiles):
    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)


def simulate_move(tiles, direction):
    new_tiles = copy.deepcopy(tiles)
    moved, score = move_tiles(new_tiles, direction)
    if not moved:
        return tiles, False, 0

    add_random_tile(new_tiles)
    return new_tiles, True, score


def ai_move(tiles, searches_per_move, search_length):
    moves = ["left", "right", "up", "down"]
    scores = {move: 0 for move in moves}

    for first_move in moves:
        simulated_tiles, valid, score = simulate_move(tiles, first_move)

        if not valid:
            continue

        scores[first_move] += score

        for _ in range(searches_per_move):
            move_number = 1
            search_tiles = copy.deepcopy(simulated_tiles)
            is_valid = True

            while is_valid and move_number <= search_length:
                next_move = random.choice(moves)
                search_tiles, is_valid, score = simulate_move(search_tiles, next_move)
                if is_valid:
                    scores[first_move] += score
                    move_number += 1

    best_move = max(scores, key=scores.get)
    return best_move


def main(window):
    clock = pygame.time.Clock()
    run = True
    tiles = generate_tiles()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

                if event.key == pygame.K_LEFT:
                    moved, score = move_tiles(tiles, "left")
                    if moved:
                        add_random_tile(tiles)

                if event.key == pygame.K_RIGHT:
                    moved, score = move_tiles(tiles, "right")
                    if moved:
                        add_random_tile(tiles)

                if event.key == pygame.K_UP:
                    moved, score = move_tiles(tiles, "up")
                    if moved:
                        add_random_tile(tiles)

                if event.key == pygame.K_DOWN:
                    moved, score = move_tiles(tiles, "down")
                    if moved:
                        add_random_tile(tiles)

                if event.key == pygame.K_SPACE:
                    best_move = ai_move(tiles, searches_per_move=100, search_length=10)
                    if best_move == "left":
                        moved, score = move_tiles(tiles, "left")
                    elif best_move == "right":
                        moved, score = move_tiles(tiles, "right")
                    elif best_move == "up":
                        moved, score = move_tiles(tiles, "up")
                    elif best_move == "down":
                        moved, score = move_tiles(tiles, "down")

                    if moved:
                        add_random_tile(tiles)

        draw(window, tiles)

    pygame.quit()


if __name__ == "__main__":
    main(WINDOW)
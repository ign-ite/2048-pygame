import pygame
import random
import math


pygame.init()

FPS = 60

WIDTH, HEIGHT = 800, 800
ROWS = 4
COL = 4

RECT_HEIGHT = WIDTH // ROWS
RECT_WIDTH = WIDTH // COL

OUTLINE_COLOR = (255, 255, 0)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 205, 205)
FONT_COLOR = (0, 0, 0)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048: The Game')

FONT = pygame.font.SysFont('Arial', 60, bold=True)
MOVE_VEL = 20

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
        pass

    def draw(self, window):
        pass

    def set_pos(self):
        pass

    def move(self, delta):
        pass

def draw_grid(window):
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, ROWS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)
    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)
def draw(window):
    window.fill(BACKGROUND_COLOR)
    draw_grid(window)
    pygame.display.update()
def main(window):
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw(window)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(WINDOW)
import pygame
import random
import math

pygame.init()

FPS = 130

WIDTH, HEIGHT = 800, 800
ROWS = 4
COLUMNS = 4
RECTANGULAR_HEIGHT = HEIGHT // ROWS
RECTANGULAR_WIDTH = WIDTH // COLUMNS

OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 193, 180)
FONT_COLOR = (119, 110, 101)

icon = pygame.image.load("2048 Icon.png")
pygame.display.set_icon(icon)
FONT = pygame.font.SysFont("Clear Sans", 80, bold=True)
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

    def __init__(self ,value, row, column):
        self.value = value
        self.row = row
        self.column = column
        self.x = column * RECTANGULAR_WIDTH
        self.y = row * RECTANGULAR_HEIGHT

    def get_color(self):
        color_index = int(math.log2(self.value)) - 1
        color = self.COLORS[color_index]
        return color

    def draw(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECTANGULAR_WIDTH, RECTANGULAR_HEIGHT))

        text = FONT.render(str(self.value), 1, FONT_COLOR)
        window.blit(
            text,
            (self.x + (RECTANGULAR_WIDTH / 2 - text.get_width() / 2)
             , self.y + (RECTANGULAR_HEIGHT / 2 - text.get_height() / 2)
             ),
            )

    def set_pos(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / RECTANGULAR_HEIGHT)
            self.column = math.ceil(self.x / RECTANGULAR_WIDTH)
        else:
            self.row = math.floor(self.y / RECTANGULAR_HEIGHT)
            self.column = math.floor(self.x / RECTANGULAR_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]


def draw_grid(window):
    for row in range(1, ROWS):
        y = row * RECTANGULAR_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0,y), (WIDTH, y), OUTLINE_THICKNESS)

    for column in range(1, COLUMNS):
        x = column * RECTANGULAR_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x,0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0,0, WIDTH, HEIGHT), OUTLINE_THICKNESS)


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
        col = random.randrange(0, COLUMNS)

        if f"{row}{col}" not in tiles:
            break

    return row,col

def func(x):
    return x.col

def move_tiles(window, tiles, clock, direction):
    updated = True
    blocks = set()

    if direction == "left":
        sort_function = lambda x:x.column
        reverse = False
        delta = (-MOVE_VEL, 0)
        boundary_check = lambda tile: tile.column == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.column - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x > next_tile.x +RECTANGULAR_WIDTH + MOVE_VEL
        )
        ceil = True
    elif direction == "right":
        sort_function = lambda x: x.column
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.column == COLUMNS -1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.column + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x  + RECTANGULAR_WIDTH + MOVE_VEL < next_tile.x)
        ceil = False
    elif direction == "up":
        sort_function = lambda x:x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.column}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y > next_tile.y +RECTANGULAR_HEIGHT + MOVE_VEL
        )
        ceil = True
    elif direction == "down":
        sort_function = lambda x:x.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.column}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y + RECTANGULAR_HEIGHT + MOVE_VEL < next_tile.y
        )
        ceil = False

    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_function, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                if merge_check(tile,next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *=2
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)

            elif move_check(tile,next_tile):
                tile.move(delta)
            else:
                continue

            tile.set_pos(ceil)
            updated = True

        update_tiles(window,tiles,sorted_tiles)

    return end_move(tiles)

def end_move(tiles):
    if len(tiles) == 16:
        return "lost"


    row, column = get_random_pos(tiles)
    tiles[f"{row}{column}"] = Tile(random.choice([2,4]), row, column)
    return "continue"
def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.column}"] = tile

    draw(window,tiles)

def generate_tiles():
    tiles = {}
    for i in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles


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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    result = move_tiles(window, tiles, clock, "left")
                if event.key == pygame.K_RIGHT:
                    result = move_tiles(window, tiles, clock, "right")
                if event.key == pygame.K_UP:
                    result = move_tiles(window, tiles, clock, "up")
                if event.key == pygame.K_DOWN:
                    result = move_tiles(window, tiles, clock, "down")

                if result == "lost":
                    game_over_text = FONT.render("Game Over!", True, (119,110, 101))
                    text_width, text_height = game_over_text.get_size()
                    text_x = (WIDTH - text_width) // 2
                    text_y = (HEIGHT - text_height) // 2
                    window.blit(game_over_text, (text_x, text_y))
                    pygame.display.update()
                    pygame.time.delay(2500)
                    run = False

        draw(window, tiles)

    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)



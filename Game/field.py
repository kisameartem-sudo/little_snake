import pygame
from PIL.ImageChops import offset

from snake.little_snake.settings import HEIGHT, NUM_CELLS
from snake.little_snake.colors import color_manager

class Field:
    def __init__(self):
        self.surface = pygame.Surface((HEIGHT, HEIGHT))
        self.num_cells = NUM_CELLS
        self.cell_size = HEIGHT // self.num_cells
        self.snake_body_size = int(self.cell_size * 0.7)
        self.body_offset = (self.cell_size - self.snake_body_size) // 2
        self.cells = []
        self._create_field()

    def _create_field(self):
        for col in range(self.num_cells):
            self.cells.append([])
            for row in range(self.num_cells):
                self.cells[col].append(pygame.Rect(self.cell_size*col, self.cell_size*row, self.cell_size, self.cell_size))

    def draw_cells(self):
        for col in range(self.num_cells):
            for cell in self.cells[col]:
                pygame.draw.rect(
                    self.surface,
                    color_manager.get_color('field_background'),
                    cell,)

                pygame.draw.rect(
                    self.surface,
                    color_manager.get_color('grid_border'),
                    cell,
                    width=2,
                )

    def draw_snake(self, snake):
        cur_snake = snake
        """Рисуем голову"""
        self.draw_square('snake_head', cur_snake[0][0], cur_snake[0][1], 10)

        if len(cur_snake) > 1:
            self.draw_snake_tail(cur_snake[1:])

    def draw_snake_tail(self, tail):
        if len(tail) > 1:
            self.draw_snake_body(tail[:-1])
        tail = tail.pop()
        self.draw_square('snake_body', tail[0], tail[1], 5)

    def draw_snake_body(self, body):
        for seg in body:
            self.draw_rect('snake_body', seg[0], seg[1], 5)

    def draw_rect(self, color, x, y, bord):
        rect_to_draw = (
            x * self.cell_size + self.body_offset,
            y * self.cell_size,
            self.snake_body_size,
            self.cell_size)
        pygame.draw.rect(
            self.surface,
            color_manager.get_color(color),
            rect_to_draw,
            border_radius=bord
        )
        if x > self.num_cells - 1:
            self.draw_part(color, x - self.num_cells, y, bord)
        if x < 0:
            self.draw_part(color, self.num_cells + x, y, bord)
        if y > self.num_cells - 1:
            self.draw_part(color, x, y - self.num_cells, bord)
        if y < 0:
            self.draw_part(color, x, self.num_cells + y, bord)

    def draw_fruits(self, fruits):
        for fruit in fruits:
            self.draw_square('fruit_1', fruit[0], fruit[1], 40)

    def draw_coins(self, coins):
        for coin in coins:
            self.draw_square('coin', coin[0], coin[1], 40)

    def draw_square(self, color, x, y, bord):
        pygame.draw.rect(
            self.surface,
            color_manager.get_color(color),
            (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
            border_radius=bord
        )
        if x > self.num_cells-1:
            self.draw_part(color, x - self.num_cells, y, bord, False)
        if x < 0:
            self.draw_part(color, self.num_cells + x, y, bord, False)
        if y > self.num_cells-1:
            self.draw_part(color, x, y - self.num_cells, bord, False)
        if y < 0:
            self.draw_part(color, x, self.num_cells + y, bord, False)

    def draw_part(self, color, x, y, bord, is_body=True):
        if is_body:
            rect_to_draw = (x * self.cell_size + self.body_offset,
                            y * self.cell_size,
                            self.snake_body_size,
                            self.cell_size)
        else:
            rect_to_draw = (x * self.cell_size,
                            y * self.cell_size,
                            self.cell_size,
                            self.cell_size)

        pygame.draw.rect(
            self.surface,
            color_manager.get_color(color),
            rect_to_draw,
            border_radius=bord
        )

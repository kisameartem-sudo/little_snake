import pygame
from color_shema import color_manager

class Field:
    def __init__(self, field_size):
        self.surface = pygame.Surface((field_size, field_size))
        self.num_cells = 20
        self.cell_size = field_size // self.num_cells
        self.cells = []
        self._create_field()

    def _create_field(self):
        for col in range(self.num_cells):
            self.cells.append([])
            for row in range(self.num_cells):
                self.cells[col].append(pygame.Rect(self.cell_size*col, self.cell_size*row, self.cell_size, self.cell_size))

    def draw_cells(self):
        self.surface.fill((248, 248, 248))
        for col in range(self.num_cells):
            for cell in self.cells[col]:
                pygame.draw.rect(
                    self.surface,
                    color_manager.colors['background'].color_RGB,
                    cell,)

                pygame.draw.rect(
                    self.surface,
                    color_manager.colors['cells_bord'].color_RGB,
                    cell,
                    width=2,
                )

    def draw_snake(self, snake):
        cur_snake = snake
        self.draw_rect('snake_head', cur_snake[0][0], cur_snake[0][1], 10)

        if len(cur_snake) > 1:
            for seg in cur_snake[1:]:
                self.draw_rect('snake_segment', seg[0], seg[1], 5)

    def draw_fruits(self, fruits):
        for fruit in fruits:
            self.draw_rect('fruit', fruit[0], fruit[1], 40)


    def draw_rect(self, color, x, y, bord):
        pygame.draw.rect(
            self.surface,
            color_manager.colors[color].color_RGB,
            (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
            border_radius=bord
        )

        self.draw_rect(color, x - self.num_cells, y, bord) if x > self.num_cells-1 else None
        self.draw_rect(color, self.num_cells + x, y, bord) if x < 0 else None
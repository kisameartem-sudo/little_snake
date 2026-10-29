import pygame

from snake.little_snake.settings import HEIGHT, NUM_CELLS
from snake.little_snake.colors import color_manager
from snake.little_snake.Game.snake_renderer import SnakeRenderer

class Field:
    def __init__(self):
        """ПОЛЕ"""
        self.surface = pygame.Surface((HEIGHT, HEIGHT))
        self.num_cells = NUM_CELLS
        self.cell_size = HEIGHT // self.num_cells
        """ЗМЕЯ"""
        self.snake_renderer = SnakeRenderer(self.surface, self.cell_size, self.num_cells)

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
                    width=1,
                )

    def draw_snake(self, visual_snake, logical_snake, direction, prev_snake, alpha):
        self.snake_renderer.prepare_snake_to_draw(visual_snake, logical_snake, direction, prev_snake, alpha)

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
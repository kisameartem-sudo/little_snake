import pygame
from dataclasses import dataclass
from color_shema import color_manager

# @dataclass()
# class Cell:
#     # assignment: str
#     color: tuple[int, int, int]

class Field:
    def __init__(self, field_size):
        self.surface = pygame.Surface((field_size, field_size))
        self.num_cells = 20
        self.cell_size = field_size // 20
        self.cells = []
        self._create_field()

    def _create_field(self):
        for i in range(self.num_cells):
            self.cells.append([])
            for j in range(self.num_cells):
                self.cells[i].append(pygame.Rect(self.cell_size*i, self.cell_size*j, self.cell_size, self.cell_size))

    def draw_cells(self):
        self.surface.fill((248, 248, 248))
        for row in range(self.num_cells):
            for cell in self.cells[row]:
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

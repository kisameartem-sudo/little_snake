import pygame
from dataclasses import dataclass
from color_shema import color_manager

@dataclass()
class Cell:
    assignment: str
    color: tuple[int, int, int]
    cell_rect:object
    cell_bord: object


class Field:
    def __init__(self, w):
        self.surface = pygame.Surface((w, w))
        w = w // 20
        self.cell_shape = (w, w)
        self.cells = {}


    def __create_field(self):
        ...
        # for i in range(self.num_width):
        #     for _ in range(self.num_height):
        #         self.cells.setdefault(i+1, []).append(Cell('field', color_manager.colors['background'].color_rgb))

    def draw_cells(self):
        return self.surface.fill(color_manager.colors['cells_bord'].color_RGB)
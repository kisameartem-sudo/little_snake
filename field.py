import pygame
from dataclasses import dataclass
from color_shema import color_manager

@dataclass()
class Cell:
    assignment: str
    color: tuple[int, int, int]
    cell_shape = (20, 20)


class FieldCells:
    def __init__(self):
        self.num_width = self.num_height = 600 // 20
        self.cells = {}

    def __create_field(self):
        for i in range(self.num_width):
            for _ in range(self.num_height):
                self.cells.setdefault(i+1, []).append(Cell('field', color_manager.colors['background'].color_rgb))

    def draw_cells(self):
        pass
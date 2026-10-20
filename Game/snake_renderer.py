import pygame

from snake.little_snake.colors import color_manager

class SnakeRenderer:
    def __init__(self, surface, cell_size, num_cells):
        self.head_color = color_manager.get_color('snake_head')
        self.body_color = color_manager.get_color('snake_body')
        self.tail_color = color_manager.get_color('snake_body')
        self.surface = surface
        self.cell_size = cell_size
        self.num_cells = num_cells
        self.snake_body_size = int(self.cell_size * 0.7)
        self.body_offset = (self.cell_size - self.snake_body_size) // 2

    def get_state(self,seg_prev, seg_cur, seg_next):
        """Определяем состояние сегментов тела"""
        prev_state = 'vert' if seg_prev[0] == seg_cur[0] else 'hor'
        next_state = 'vert' if seg_next[0] == seg_cur[0] else 'hor'
        if prev_state == next_state:
            cur_state = prev_state
        else:
            prev_state = self.get_side(seg_cur, seg_prev)
            next_state = self.get_side(seg_cur, seg_next)
            cur_state = 'corner'
        return prev_state, cur_state, next_state

    def get_side(self, cur, neighbour):
        """Определяем направление сегментов для угла"""
        if cur[0] == neighbour[0]:
            return 'UP' if (cur[1] - neighbour[1]) % self.num_cells == 1 else 'DOWN'
        else:
            return 'LEFT' if (cur[0] - neighbour[0]) % self.num_cells == 1 else 'RIGHT'

    def draw_tail(self, tail, logical_snake):
        cell_left = tail[0] * self.cell_size
        cell_top = tail[1] * self.cell_size

        cell_right = cell_left + self.cell_size
        cell_bottom = cell_top + self.cell_size

        center_x = cell_left + self.cell_size // 2
        center_y = cell_top + self.cell_size // 2

        body_left = cell_left + self.body_offset
        body_right = body_left + self.snake_body_size

        body_top = cell_top + self.body_offset
        body_bottom = body_top + self.snake_body_size

        match self.get_side(logical_snake[-1], logical_snake[-2]):
            case 'UP':
                triang = ((body_left, cell_top), (body_right, cell_top), (center_x, body_bottom))
            case 'DOWN':
                triang = ((center_x, body_top), (body_right, cell_bottom), (body_left, cell_bottom))
            case 'LEFT':
                triang = ((cell_left, body_top), (body_right, center_y), (cell_left, body_bottom))
            case 'RIGHT':
                triang = ((body_left, center_y), (cell_right, body_top), (cell_right, body_bottom))

        self.draw_polygon(triang, self.body_color)

    def draw_polygon(self, polygon, color):
        pygame.draw.polygon(
            self.surface,
            color,
            polygon)
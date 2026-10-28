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
        self.field_width = self.cell_size * self.num_cells
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

    def prepare_part_of_corner(self, orientation, x, y):
        """Готовим углы тела к отрисовке"""
        if orientation == 'UP':
            x = x * self.cell_size + self.body_offset
            y = y * self.cell_size
            width = self.snake_body_size
            height = self.cell_size // 2
        elif orientation == 'DOWN':
            x = x * self.cell_size + self.body_offset
            y = y * self.cell_size + self.cell_size // 2
            width = self.snake_body_size
            height = self.cell_size // 2
        elif orientation == 'LEFT':
            x = x * self.cell_size
            y = y * self.cell_size + self.body_offset
            width = self.cell_size // 2
            height = self.snake_body_size
        elif orientation == 'RIGHT':
            x = x * self.cell_size + self.cell_size // 2
            y = y * self.cell_size + self.body_offset
            width = self.cell_size // 2
            height = self.snake_body_size

        return x, y, width, height

    def draw_snake_body(self, visual_snake, logical_snake):
        """Готовим тело к отрисовке"""
        for i, seg in enumerate(visual_snake[1:-1]):
            cur_state = self.get_state(logical_snake[i], logical_snake[i+1], logical_snake[i+2])
            self.draw_snake_part(self.identify_body_part(cur_state, seg[0], seg[1]))

    def identify_body_part(self, state, x, y):
        """Готовим части тела к отрисовке"""
        rect_to_draw = []
        match state[1]:
            case 'vert':
                rect_to_draw.append((
                    x * self.cell_size + self.body_offset,
                    y * self.cell_size,
                    self.snake_body_size,
                    self.cell_size))
            case 'hor':
                rect_to_draw.append((
                    x * self.cell_size,
                    y * self.cell_size + self.body_offset,
                    self.cell_size,
                    self.snake_body_size))
            case 'corner':
                rect_to_draw.append(self.prepare_part_of_corner(state[0], x, y))
                rect_to_draw.append((
                    x * self.cell_size + self.body_offset,
                    y * self.cell_size + self.body_offset,
                    self.snake_body_size,
                    self.snake_body_size))
                rect_to_draw.append((self.prepare_part_of_corner(state[2], x, y)))
        return rect_to_draw

    def draw_head(self, x, y):
        pygame.draw.rect(
            self.surface,
            self.head_color,
            (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
            border_radius=10
        )

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

        self.draw_polygon(triang, self.tail_color)

    def draw_snake_part(self, rect_to_draw):
        """Отрисовываем части тела"""
        for part in rect_to_draw:
            part = pygame.Rect(part)
            alt_parts = []
            if part.right > self.field_width:
                alt_parts.append(part.move(-self.field_width, 0))
            if part.left < 0:
                alt_parts.append(part.move(self.field_width, 0))
            if part.bottom > self.field_width:
                alt_parts.append(part.move(0, -self.field_width))
            if part.top < 0:
                alt_parts.append(part.move(0, self.field_width))

            pygame.draw.rect(self.surface, self.body_color, part, border_radius=5)
            if alt_parts:
                for alt in alt_parts:
                    pygame.draw.rect(self.surface, self.body_color, alt, border_radius=5)

    def draw_polygon(self, polygon, color):
        pygame.draw.polygon(
            self.surface,
            color,
            polygon)
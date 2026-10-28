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
        self.snake_body_size = int(self.cell_size * 0.5)
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

    # def prepare_part_of_corner(self, orientation, x, y):
    #     """Готовим углы тела к отрисовке"""
    #     if orientation == 'UP':
    #         x = x * self.cell_size + self.body_offset
    #         y = y * self.cell_size
    #         width = self.snake_body_size
    #         height = self.cell_size // 2
    #     elif orientation == 'DOWN':
    #         x = x * self.cell_size + self.body_offset
    #         y = y * self.cell_size + self.cell_size // 2
    #         width = self.snake_body_size
    #         height = self.cell_size // 2
    #     elif orientation == 'LEFT':
    #         x = x * self.cell_size
    #         y = y * self.cell_size + self.body_offset
    #         width = self.cell_size // 2
    #         height = self.snake_body_size
    #     elif orientation == 'RIGHT':
    #         x = x * self.cell_size + self.cell_size // 2
    #         y = y * self.cell_size + self.body_offset
    #         width = self.cell_size // 2
    #         height = self.snake_body_size
    #
    #     return x, y, width, height

    def draw_snake_body(self, visual_snake, logical_snake):
        """Готовим тело к отрисовке"""
        for i, seg in enumerate(visual_snake[1:-1]):
            cur_state = self.get_state(logical_snake[i], logical_snake[i+1], logical_snake[i+2])
            # self.draw_snake_part(self.identify_body_part(cur_state, seg[0], seg[1]))
            local_seg, direction = SnakeRenderer.identify_body_part(cur_state)
            seg_global = self.rotate_and_transform_part(local_seg, seg[0], seg[1], direction)
            self.draw_polygon(seg_global, self.body_color)


    @staticmethod
    def identify_body_part(state):
        """Готовим части тела к отрисовке"""
        match state[1]:
            case 'vert':
                return ((0.2, 0), (0.8, 0), (0.8, 1), (0.2, 1)), 'RIGHT'
            case 'hor':
                return ((0, 0.2), (1, 0.2), (1, 0.8), (0, 0.8)), 'RIGHT'
            case 'corner':
                sides = frozenset((state[0], state[2]))

                if sides == frozenset(('UP', 'RIGHT')):
                    direction = 'RIGHT'
                elif sides == frozenset(('RIGHT', 'DOWN')):
                    direction = 'DOWN'
                elif sides == frozenset(('DOWN', 'LEFT')):
                    direction = 'LEFT'
                elif sides == frozenset(('LEFT', 'UP')):
                    direction = 'UP'
                return ((0.2, 0), (0.8, 0), (0.8, 0.2), (1, 0.2), (1, 0.8), (0.2, 0.8)), direction

    def draw_head(self, x, y, direction):
        head_local = (
            (1, 0.4),  #Право-верх
            (1, 0.6),  #Право-низ
            (0.8, 0.8), #Центр-право-низ
            (0.4, 0.8), #Центр-лево-низ
            (0, 0.7),  #Лево-низ
            (0, 0.3),  #Лево-верх
            (0.4, 0.2),  #Центр-лево-верх
            (0.8, 0.2)  #Центр-право-верх
        )

        head_global = self.rotate_and_transform_part(head_local, x, y, direction)
        self.draw_polygon(head_global, self.head_color)

    def rotate_and_transform_part(self, part_local, x, y, direction):
        match direction:
            case 'RIGHT':
                pass
            case 'UP':
                part_local = tuple((yy, 1 - xx) for xx, yy in part_local)
            case 'LEFT':
                part_local = tuple((1 - xx, 1 - yy) for xx, yy in part_local)
            case 'DOWN':
                part_local = tuple((1 - yy, xx) for xx, yy in part_local)

        part_global = []

        for local_x, local_y in part_local:
            part_global.append(((x + local_x) * self.cell_size,
                                (y + local_y) * self.cell_size))
        return part_global

    def draw_tail(self, tail, logical_snake):
        tail_local = (
            (1, 0.3),
            (1, 0.7),
            (0, 0.5)
        )
        direction = self.get_side(logical_snake[-1], logical_snake[-2])

        tail_global = self.rotate_and_transform_part(tail_local, tail[0], tail[1], direction)
        self.draw_polygon(tail_global, self.tail_color)

    # def draw_snake_part(self, rect_to_draw):
    #     """Отрисовываем части тела"""
    #     for part in rect_to_draw:
    #         part = pygame.Rect(part)
    #         alt_parts = []
    #         if part.right > self.field_width:
    #             alt_parts.append(part.move(-self.field_width, 0))
    #         if part.left < 0:
    #             alt_parts.append(part.move(self.field_width, 0))
    #         if part.bottom > self.field_width:
    #             alt_parts.append(part.move(0, -self.field_width))
    #         if part.top < 0:
    #             alt_parts.append(part.move(0, self.field_width))
    #
    #         pygame.draw.rect(self.surface, self.body_color, part, border_radius=5)
    #         if alt_parts:
    #             for alt in alt_parts:
    #                 pygame.draw.rect(self.surface, self.body_color, alt, border_radius=5)

    def draw_polygon(self, polygon, color):
        pygame.draw.polygon(
            self.surface,
            color,
            polygon)
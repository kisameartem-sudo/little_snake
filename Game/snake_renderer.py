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
        self.snake_body_width = 0.6
        self.figure_edges = ((1 - self.snake_body_width) / 2, (1 + self.snake_body_width) / 2)

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

    def draw_snake_body(self, visual_snake, logical_snake):
        """Готовим тело к отрисовке"""
        for i, seg in enumerate(visual_snake[1:-1]):
            cur_state = self.get_state(logical_snake[i], logical_snake[i+1], logical_snake[i+2])
            # self.draw_snake_part(self.identify_body_part(cur_state, seg[0], seg[1]))
            local_seg, direction = self.identify_body_part(cur_state)
            seg_global = self.rotate_and_transform_part(local_seg, seg[0], seg[1], direction)
            self.draw_polygon(seg_global, self.body_color)

    def identify_body_part(self, state):
        """Готовим части тела к отрисовке"""
        match state[1]:
            case 'vert':
                return ((
                    (self.figure_edges[0], 0),
                    (self.figure_edges[1], 0),
                    (self.figure_edges[1], 1),
                    (self.figure_edges[0], 1)),
                        'RIGHT')
            case 'hor':
                return ((
                    (0, self.figure_edges[0]),
                    (1, self.figure_edges[0]),
                    (1, self.figure_edges[1]),
                    (0, self.figure_edges[1])),
                        'RIGHT')
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
                return ((
                    (self.figure_edges[0], 0),
                    (self.figure_edges[1], 0),
                    (self.figure_edges[1], self.figure_edges[0]),
                    (1, self.figure_edges[0]),
                    (1, self.figure_edges[1]),
                    (0.2, self.figure_edges[1])),
                        direction)

    def draw_head(self, x, y, direction):
        head_local = (
            (1, 0.4),  #Право-верх
            (1, 0.6),  #Право-низ
            (0.8, 0.9), #Центр-право-низ
            (0.4, 0.8), #Центр-лево-низ
            (0, self.figure_edges[1]),  #Лево-низ
            (0, self.figure_edges[0]),  #Лево-верх
            (0.4, 0.2),  #Центр-лево-верх
            (0.8, 0.1)  #Центр-право-верх
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


    def draw_polygon(self, polygon, color):
        left = min(point[0] for point in polygon)
        right = max(point[0] for point in polygon)
        up = min(point[1] for point in polygon)
        down = max(point[0] for point in polygon)
        shifted_polygon = []
        if right > self.field_width:
            shifted_polygon.append([
                (px - self.field_width, py)
                for px, py in polygon
            ])
        if left < 0:
            shifted_polygon.append([
                (px + self.field_width, py)
                for px, py in polygon
            ])
        if down > self.field_width:
            shifted_polygon.append([
                (px, py - self.field_width)
                for px, py in polygon
            ])
        if up < 0:
            shifted_polygon.append([
                (px, py + self.field_width)
                for px, py in polygon
            ])

        pygame.draw.polygon(
            self.surface,
            color,
            polygon)

        if shifted_polygon:
            for sh_poly in shifted_polygon:
                pygame.draw.polygon(
                    self.surface,
                    color,
                    sh_poly)
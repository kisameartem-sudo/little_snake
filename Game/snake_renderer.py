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

    def prepare_snake_to_draw(self, visual_snake, logical_snake, direction, prev_snake, alpha):
        cur_snake = visual_snake
        old_snake = prev_snake
        """Рисуем голову"""
        self.draw_head(cur_snake[0][0], cur_snake[0][1], direction)

        if len(cur_snake) == 2:
            """Рисуем хвост"""
            self.draw_tail(cur_snake[-1], logical_snake)
        elif len(cur_snake) > 2:
            """Рисуем хвост"""
            self.draw_tail(cur_snake[-1], logical_snake)
            """Готовим и рисуем тело"""
            self.draw_snake_body(visual_snake, logical_snake, old_snake, alpha)

    def draw_snake_body(self, visual_snake, logical_snake, old_snake, alpha):
        """Готовим тело к отрисовке"""
        for i, seg in enumerate(visual_snake[1:-1]):
            """Разбиваем тело не сегменты и работаем с каждым сегментом отдельно"""
            #Получаем состояние сегмента в конечной точке перемещения
            cur_state = self.get_state(logical_snake[i], logical_snake[i+1], logical_snake[i+2])
            # Получаем состояние сегмента в начальной точке перемещения
            old_state = self.get_state(old_snake[i], old_snake[i+1], old_snake[i+2]) if i + 2 < len(old_snake) else None
            #Определяем вид сегмента для конечной точки перемещения
            local_seg, direction = self.identify_body_part(cur_state)
            # Определяем вид сегмента для начальной точки перемещения
            if old_state is not None:
                old_local, old_direction = self.identify_body_part(old_state)

            rotated_seg = self.rotate_part(local_seg, direction)

            if (old_state is not None and
                    old_state[1] == 'hor' and
                    cur_state[1] == 'corner' and
                    direction == 'RIGHT'):
                rotated_seg = self.interpolate_local_shape(old_local, rotated_seg, alpha)

            if (old_state is not None
                    and old_state[1] == 'vert'
                    and cur_state[1] == 'corner'
                    and direction == 'RIGHT'
            ):
                rotated_seg = self.interpolate_local_shape(old_local, rotated_seg, alpha)

            seg_global = self.transform_part(rotated_seg, seg[0], seg[1])
            self.draw_polygon(seg_global, self.body_color)

    def identify_body_part(self, state):
        """Готовим части тела к отрисовке"""
        a, b = self.figure_edges[0], self.figure_edges[1]
        match state[1]:
            case 'vert':
                return ((
                            (a, 0), (b, 0),  # Верхнее ребро
                            (b, 0.5),  # Центр-право
                            (b, 1), (a, 1),  # Нижнее ребро
                            (a, 0.5)  # Центр-лево
                        ), 'RIGHT')
            case 'hor':
                return ((
                            (0, a), (b, a), (1, a),  # Верхнее ребро
                            (1, b), (a, b), (0, b)  # Нижнее ребро
                        ), 'RIGHT')
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
                            (a, 0), (b, 0),  # Верхнее ребро
                            (b, a),  # Внутренний поворотный угол
                            (1, a), (1, b),  # Правое ребро
                            (a, b)  # Внешний поворотный угол
                        ), direction)

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

        rotated_head = self.rotate_part(head_local, direction)
        head_global = self.transform_part(rotated_head, x, y)
        self.draw_polygon(head_global, self.head_color)

    def interpolate_local_shape(self, old_local, new_local, alpha):

        cur_local = []
        for (old_x, old_y), (target_x, target_y) in zip(old_local, new_local):
            cur_local.append(
                (old_x + (target_x - old_x) * alpha, old_y + (target_y - old_y) * alpha)
            )
        return cur_local

    def rotate_part(self, part_local, direction):
        match direction:
            case 'RIGHT':
                pass
            case 'UP':
                part_local = tuple((yy, 1 - xx) for xx, yy in part_local)
            case 'LEFT':
                part_local = tuple((1 - xx, 1 - yy) for xx, yy in part_local)
            case 'DOWN':
                part_local = tuple((1 - yy, xx) for xx, yy in part_local)
        return part_local

    def transform_part(self, part_local, x, y):
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

        rotated_tail = self.rotate_part(tail_local, direction)
        tail_global = self.transform_part(rotated_tail, tail[0], tail[1])
        self.draw_polygon(tail_global, self.tail_color)


    def draw_polygon(self, polygon, color):
        left = min(point[0] for point in polygon)
        right = max(point[0] for point in polygon)
        up = min(point[1] for point in polygon)
        down = max(point[1] for point in polygon)
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
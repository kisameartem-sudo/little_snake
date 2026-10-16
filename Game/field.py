import pygame

from snake.little_snake.settings import HEIGHT, NUM_CELLS
from snake.little_snake.colors import color_manager

class Field:
    def __init__(self):
        """ПОЛЕ"""
        self.surface = pygame.Surface((HEIGHT, HEIGHT))
        self.num_cells = NUM_CELLS
        self.cell_size = HEIGHT // self.num_cells
        """ЗМЕЯ"""
        self.snake_body_size = int(self.cell_size * 0.7)
        self.body_offset = (self.cell_size - self.snake_body_size) // 2
        self.snake_direction = None

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

    def draw_snake(self, visual_snake, logical_snake, direction):
        self.snake_direction = direction
        cur_snake = visual_snake
        """Рисуем голову"""
        self.draw_square('snake_head', cur_snake[0][0], cur_snake[0][1], 10)

        if len(cur_snake) == 2:
            """Рисуем хвост"""
            self.draw_tail(cur_snake[-1], logical_snake, 'snake_body')
        elif len(cur_snake) > 2:
            """Рисуем хвост"""
            self.draw_tail(cur_snake[-1], logical_snake, 'snake_body')
            """Готовим тело к отрисовке"""
            self.prepare_snake_body(visual_snake, logical_snake)

    @staticmethod
    def get_state(seg_prev, seg_cur, seg_next):
        """Определяем состояние сегментов тела"""
        prev_state = 'vert' if seg_prev[0] == seg_cur[0] else 'hor'
        next_state = 'vert' if seg_next[0] == seg_cur[0] else 'hor'
        if prev_state == next_state:
            cur_state = prev_state
        else:
            prev_state = Field.get_side(seg_cur, seg_prev)
            next_state = Field.get_side(seg_cur, seg_next)
            cur_state = 'corner'
        return prev_state, cur_state, next_state

    @staticmethod
    def get_side(cur, neighbour):
        """Определяем направление сегментов для угла"""
        if cur[0] == neighbour[0]:
            return 'UP' if (cur[1] - neighbour[1]) % NUM_CELLS == 1 else 'DOWN'
        else:
            return 'LEFT' if (cur[0] - neighbour[0]) % NUM_CELLS == 1 else 'RIGHT'

    def prepare_snake_body(self, visual_snake, logical_snake):
        """Готовим тело к отрисовке"""
        for i, seg in enumerate(visual_snake[1:-1]):
            state = self.get_state(logical_snake[i], logical_snake[i+1], logical_snake[i+2])
            self.prepare_snake_part_to_draw(state, 'snake_body', seg[0], seg[1])

    def prepare_snake_part_to_draw(self, state, color, x, y):
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
        for rect in rect_to_draw:
            self.draw_snake_part(rect, color, x, y)

    def draw_tail(self, tail, logical_snake, color):
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

        match Field.get_side(logical_snake[-1], logical_snake[-2]):
            case 'UP':
                p1 = (body_left, cell_top)
                p2 = (body_right, cell_top)
                p3 = (center_x, body_bottom)
            case 'DOWN':
                p1 = (center_x, body_top)
                p2 = (body_right, cell_bottom)
                p3 = (body_left, cell_bottom)
            case 'LEFT':
                p1 = (cell_left, body_top)
                p2 = (body_right, center_y)
                p3 = (cell_left, body_bottom)
            case 'RIGHT':
                p1 = (body_left, center_y)
                p2 = (cell_right, body_top)
                p3 = (cell_right, body_bottom)

        pygame.draw.polygon(
            self.surface,
            color_manager.get_color(color),
            (p1, p2, p3))

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

    def draw_snake_part(self, rect_to_draw, color, x, y, bord=5):
        """Отрисовываем части тела"""
        pygame.draw.rect(
            self.surface,
            color_manager.get_color(color),
            rect_to_draw,
            border_radius=bord
        )
        if x > self.num_cells - 1:
            self.draw_part(color, x - self.num_cells, y, bord)
        if x < 0:
            self.draw_part(color, self.num_cells + x, y, bord)
        if y > self.num_cells - 1:
            self.draw_part(color, x, y - self.num_cells, bord)
        if y < 0:
            self.draw_part(color, x, self.num_cells + y, bord)

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
        if x > self.num_cells-1:
            self.draw_part(color, x - self.num_cells, y, bord, False)
        if x < 0:
            self.draw_part(color, self.num_cells + x, y, bord, False)
        if y > self.num_cells-1:
            self.draw_part(color, x, y - self.num_cells, bord, False)
        if y < 0:
            self.draw_part(color, x, self.num_cells + y, bord, False)

    def draw_part(self, color, x, y, bord, is_body=True):
        if is_body:
            rect_to_draw = (x * self.cell_size + self.body_offset,
                            y * self.cell_size,
                            self.snake_body_size,
                            self.cell_size)
        else:
            rect_to_draw = (x * self.cell_size,
                            y * self.cell_size,
                            self.cell_size,
                            self.cell_size)

        pygame.draw.rect(
            self.surface,
            color_manager.get_color(color),
            rect_to_draw,
            border_radius=bord
        )
from collections import deque

class Snake:
    def __init__(self, x, y, num_cells):
        self.direction = None
        self.wrong_directions = {
            'UP': 'DOWN',
            'DOWN': 'UP',
            'LEFT': 'RIGHT',
            'RIGHT': 'LEFT'
        }
        self.snake = deque()
        self.snake.appendleft((x, y))
        self.max_cell = num_cells


    def update_direction(self, new_direction):
        if self.wrong_directions[new_direction] == self.direction:
            return
        self.direction = new_direction

    def next_head_pos(self):
        match self.direction:
            case 'UP':
                return self.snake[0][0], (self.snake[0][1] - 1) % self.max_cell
            case 'DOWN':
                return self.snake[0][0], (self.snake[0][1] + 1) % self.max_cell
            case 'LEFT':
                return (self.snake[0][0] - 1) % self.max_cell, self.snake[0][1]
            case 'RIGHT':
                return (self.snake[0][0] + 1) % self.max_cell, self.snake[0][1]
            case None:
                return self.snake[0][0], self.snake[0][1]
        return None

    def move(self, with_grow=False):
        self.snake.appendleft(self.next_head_pos())
        if not with_grow:
            self.snake.pop()

    def get_snake(self):
        return list(self.snake)
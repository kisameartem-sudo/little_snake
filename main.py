import pygame
from color_shema import color_manager
from field import Field
from snake import Snake
from fruit import Fruits


class Game:
    def __init__(self):
        pygame.init()

        self.width = 800
        self.height = 600
        self.FPS = 60
        self.running = True
        self.field = Field(600)

        self.snake = Snake(15,
                           15,
                           self.field.num_cells)
        self.fruits = Fruits(self.field.num_cells,
                             set(self.snake.get_snake()))

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('My_Snake')
        self.clock = pygame.time.Clock()

        self.moving = {
            'move_timer': 0,
            'move_interval': 0.3
        }

        self.previous_snake = self.snake.get_snake()

    # -------------------------------------------------
    # Обработка событий нажатия кнопок
    # -------------------------------------------------

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Проверка нажатия на крестик
                self.running = False

            elif event.type == pygame.KEYDOWN:
                '''Полверка нажатий кнопок'''
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_w:
                    self.snake.update_direction('UP')
                if event.key == pygame.K_d:
                    self.snake.update_direction('RIGHT')
                if event.key == pygame.K_a:
                    self.snake.update_direction('LEFT')
                if event.key == pygame.K_s:
                    self.snake.update_direction('DOWN')

    # -------------------------------------------------
    # Непрерывный ввод
    # -------------------------------------------------
    def handle_input(self):
        ...

    # -------------------------------------------------
    # 3. Изменение состояния
    # -------------------------------------------------
    def update(self, dt):
        self.moving['move_timer'] += dt

        if self.moving['move_timer'] >= self.moving['move_interval']:
            self.moving['move_timer'] -= self.moving['move_interval']

            snake = self.snake.get_snake()
            snake_head = self.snake.next_head_pos()
            self.previous_snake = snake

            if snake_head in self.fruits.get_fruits():
                self.fruits.remove_fruit(snake_head, set(snake))
                self.snake.move(True)
            else:
                self.snake.move()

            if self.fruits.update_delay():
                self.fruits.add_fruit(set(snake))


    # -------------------------------------------------
    # 4. Отрисовка
    # -------------------------------------------------
    def render(self):
        self.field.draw_cells()  # Рисуем поле
        self.field.draw_fruits(self.fruits.get_fruits())

        alpha = self.moving['move_timer'] / self.moving['move_interval']

        snake_head = self.snake.get_snake()[0]
        visual_x = self.previous_snake[0][0] + (snake_head[0] - self.previous_snake[0][0]) * alpha
        visual_y = self.previous_snake[0][1] + (snake_head[1] - self.previous_snake[0][1]) * alpha
        self.field.draw_snake([[visual_x, visual_y]])
        # self.field.draw_snake(self.snake.get_snake())  # Рисуем змею

        self.screen.fill(color_manager.colors['background'].color_RGB)  # Рисуем задник
        self.screen.blit(self.field.surface, (200, 0))  # Отображаем поле

        pygame.display.flip()

    def play(self):
        try:
            while self.running:
                dt = self.clock.tick(self.FPS) / 1000.0
                self.handle_events()
                self.handle_input()
                self.update(dt)
                self.render()

        finally:
            pygame.quit()



def main():
    snake_game = Game()
    snake_game.play()

if __name__ == '__main__':
    main()
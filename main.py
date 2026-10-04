import pygame
from colors import color_manager
from snake.little_snake.Game.field import Field
from snake.little_snake.Game.main_menu import MainMenu
from snake.little_snake.Game.ui import UI
from snake.little_snake.Game.game_over_menu import GameOverMenu
from snake.little_snake.Game.pause_menu import PauseMenu
from Entities.snake import Snake
from snake.little_snake.Entities.fruit import Fruits
from settings import WIDTH, HEIGHT, FPS, NUM_CELLS, SNAKE_START_POS
from enum import Enum

class GameState(Enum):
    MAIN_MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4

class Game:
    def __init__(self):
        pygame.init()
        self.game_state = GameState.MAIN_MENU
        # Окно приложения---------------------------
        self.width = WIDTH
        self.height = HEIGHT
        self.FPS = FPS
        self.running = True
        self.field = Field()
        self.main_menu = MainMenu()
        self.game_over_menu = GameOverMenu()
        self.g_o_alpha = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.g_o_alpha.fill((255, 0, 0, 100))
        self.pause_menu = PauseMenu()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('My_Snake')
        self.clock = pygame.time.Clock()

    def new_game_start(self):
        self.ui = UI()
        self.snake = Snake(SNAKE_START_POS[0],
                           SNAKE_START_POS[1],
                           NUM_CELLS)

        self.moving = {
            'move_timer': 0,
            'move_interval': 0.3
        }
        # self.is_snake_live = True
        self.previous_snake = self.snake.get_snake()
        self.fruits = Fruits(set(self.snake.get_snake()))
        self.eating_fruit = None

    # -------------------------------------------------
    # Обработка событий нажатия кнопок
    # -------------------------------------------------

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Проверка нажатия на крестик
                self.running = False

            elif self.game_state == GameState.PLAYING:
                '''События во время игры'''
                if event.type == pygame.KEYDOWN:
                    '''Проверка нажатий кнопок'''
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = GameState.MAIN_MENU

                    if event.key == pygame.K_SPACE:
                        self.game_state = GameState.PAUSED

                    if event.key == pygame.K_w:
                        self.snake.update_direction('UP')
                    if event.key == pygame.K_d:
                        self.snake.update_direction('RIGHT')
                    if event.key == pygame.K_a:
                        self.snake.update_direction('LEFT')
                    if event.key == pygame.K_s:
                        self.snake.update_direction('DOWN')

            elif self.game_state == GameState.PAUSED:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.new_game_start()
                        self.game_state = GameState.PLAYING
                    if event.key == pygame.K_SPACE:
                        self.game_state = GameState.PLAYING

            elif self.game_state == GameState.GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.new_game_start()
                        self.game_state = GameState.PLAYING
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = GameState.MAIN_MENU

            elif self.game_state == GameState.MAIN_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        button_clicked = self.main_menu.get_button_clicked(event.pos)
                        match button_clicked:
                            case 'START':
                                self.new_game_start()
                                self.game_state = GameState.PLAYING
                            case 'EXIT':
                                self.running = False

    # -------------------------------------------------
    # Непрерывный ввод
    # -------------------------------------------------
    def handle_input(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.main_menu.buttons:
            hovered = self.main_menu.get_button(button).is_hovered(mouse_pos)
            self.main_menu.get_button(button).change_button_state(hovered)


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

            if self.eating_fruit is not None:
                self.fruits.remove_fruit(self.eating_fruit, set(self.snake.get_snake()))
                self.eating_fruit = None

            if snake_head in self.fruits.get_fruits():
                if snake_head in snake[1:]:
                    self.game_state = GameState.GAME_OVER
                else:
                    self.snake.move(True)
                    self.eating_fruit = snake_head
            else:
                if snake_head in snake[1:-1]:
                    self.game_state = GameState.GAME_OVER
                else:
                    self.snake.move()

            if self.fruits.update_delay():
                self.fruits.add_fruit(set(self.snake.get_snake()))


    # -------------------------------------------------
    # 4. Отрисовка
    # -------------------------------------------------
    def draw_scene(self):
        self.field.draw_cells()  # Рисуем поле
        self.field.draw_fruits(self.fruits.get_fruits())

        alpha = self.moving['move_timer'] / self.moving['move_interval']
        snake_to_draw = self.moving_snake(self.previous_snake, self.snake.get_snake(), alpha, NUM_CELLS)

        self.field.draw_snake(snake_to_draw)
        self.screen.blit(self.ui.surface, (0, 0))
        self.screen.blit(self.field.surface, (WIDTH - HEIGHT, 0))  # Отображаем поле

    def render(self):
        if self.game_state == GameState.PLAYING:
            self.draw_scene()

        elif self.game_state == GameState.MAIN_MENU:
            self.main_menu.draw_main_menu()
            self.screen.blit(self.main_menu.surface, (0, 0))

        elif self.game_state == GameState.PAUSED:
            self.draw_scene()
            self.screen.blit(self.pause_menu.surface,
                             (
                                 (WIDTH - self.pause_menu.surface.get_width()) // 2,
                                 (HEIGHT - self.pause_menu.surface.get_height()) // 2)
                             )

        elif self.game_state == GameState.GAME_OVER:
            self.draw_scene()
            self.screen.blit(self.g_o_alpha, (0, 0))
            self.screen.blit(self.game_over_menu.surface,
                             (
                                 (WIDTH - self.game_over_menu.surface.get_width()) // 2,
                                 (HEIGHT - self.game_over_menu.surface.get_height()) // 2)
                             )

        pygame.display.flip()

    def play(self):
        try:
            while self.running:
                dt = self.clock.tick(self.FPS) / 1000.0
                self.handle_events()

                if self.game_state == GameState.MAIN_MENU:
                    self.handle_input()

                if self.game_state == GameState.PLAYING:
                    self.update(dt)
                self.render()

        finally:
            pygame.quit()

    @staticmethod
    def wrapped_delta(old, new, field_size):
        half_size = field_size // 2
        delta = new - old
        return delta - field_size if delta > half_size else (
                delta + field_size) if delta < -half_size else delta


    @staticmethod
    def moving_snake(old_snake, snake, alpha, field_size):
        snake_to_draw = []

        for i, seg in enumerate(snake):
            if i < len(old_snake):
                visual_x = old_snake[i][0] + Game.wrapped_delta(old_snake[i][0], seg[0], field_size) * alpha
                visual_y = old_snake[i][1] + Game.wrapped_delta(old_snake[i][1], seg[1], field_size) * alpha
                snake_to_draw.append((visual_x, visual_y))
            else:
                snake_to_draw.append(snake[-1])

        return snake_to_draw


def main():
    snake_game = Game()
    snake_game.play()

if __name__ == '__main__':
    main()
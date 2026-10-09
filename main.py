import pygame
from snake.little_snake.save_manager import SaveManager
from snake.little_snake.Game.field import Field
from snake.little_snake.Game.main_menu import MainMenu
from snake.little_snake.Game.ui import UI
from snake.little_snake.Game.game_over_menu import GameOverMenu
from snake.little_snake.Game.pause_menu import PauseMenu
from Entities.snake import Snake
from snake.little_snake.Entities.fruit import Fruits
from snake.little_snake.Entities.coin import Coins
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
        self.user_manager = SaveManager()
        self.g_o_alpha = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.g_o_alpha.fill((255, 0, 0, 100))
        self.pause_menu = PauseMenu()
        self.pause_menu.set_surface_shift(
            ((WIDTH - self.pause_menu.surface.get_width()) // 2,
             (HEIGHT - self.pause_menu.surface.get_height()) // 2))
        self.game_over_menu.set_surface_shift((
                                 (WIDTH - self.game_over_menu.surface.get_width()) // 2,
                                 (HEIGHT - self.game_over_menu.surface.get_height()) // 2))
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
        self.previous_snake = self.snake.get_snake()
        self.fruits = Fruits(set(self.snake.get_snake()))
        self.coins = Coins(set(self.snake.get_snake() + list(self.fruits.get_fruits())))

        self.eating_fruit = None
        self.eating_coin = None

        self.score = 0
        self.live_timer = 0
        self.collected_coins = 0

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
                    if event.key == pygame.K_o:
                        self.game_state = GameState.GAME_OVER

            elif self.game_state == GameState.PAUSED:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        button_clicked = self.pause_menu.get_button_clicked(event.pos)
                        match button_clicked:
                            case 'Continue':
                                self.game_state = GameState.PLAYING
                            case 'Restart':
                                self.new_game_start()
                                self.game_state = GameState.PLAYING

            elif self.game_state == GameState.GAME_OVER:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        button_clicked = self.game_over_menu.get_button_clicked(event.pos)
                        match button_clicked:
                            case 'Main menu':
                                self.game_state = GameState.MAIN_MENU
                            case 'Restart':
                                self.new_game_start()
                                self.game_state = GameState.PLAYING
                            case 'Exit':
                                self.running = False

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
        if self.game_state == GameState.MAIN_MENU:
            self.main_menu.update_hover(pygame.mouse.get_pos())
        elif self.game_state == GameState.PAUSED:
            self.pause_menu.update_hover(pygame.mouse.get_pos())
        elif self.game_state == GameState.GAME_OVER:
            self.game_over_menu.update_hover(pygame.mouse.get_pos())

    # -------------------------------------------------
    # 3. Изменение состояния
    # -------------------------------------------------
    def update(self, dt):
        self.moving['move_timer'] += dt
        self.live_timer += dt

        if self.moving['move_timer'] >= self.moving['move_interval']:
            self.moving['move_timer'] -= self.moving['move_interval']

            snake = self.snake.get_snake()
            snake_head = self.snake.next_head_pos()
            self.previous_snake = snake

            """Обработка фруктов"""
            if self.eating_fruit is not None:
                self.fruits.remove_fruit(self.eating_fruit, self.get_excludes())
                self.eating_fruit = None

            """Обработка монет"""
            if self.eating_coin is not None:
                self.coins.remove_coin(self.eating_coin)
                self.eating_coin = None

            if snake_head in self.fruits.get_fruits():
                if snake_head in snake[1:]:
                    self.user_manager.update_user_data(self.collected_coins, self.score)
                    self.game_state = GameState.GAME_OVER
                else:
                    self.snake.move(True)
                    self.eating_fruit = snake_head
                    self.score += 20

            elif snake_head in self.coins.get_coins():
                self.snake.move()
                self.eating_coin = snake_head
                self.collected_coins += 1
                self.score += 100

            else:
                if snake_head in snake[1:-1]:
                    self.user_manager.update_user_data(self.collected_coins, self.score)
                    self.game_state = GameState.GAME_OVER
                else:
                    self.snake.move()

            if self.fruits.update_delay():
                self.fruits.add_fruit(self.get_excludes())

            if self.coins.update_delay():
                self.coins.add_coin(self.get_excludes())

    # -------------------------------------------------
    # 4. Отрисовка
    # -------------------------------------------------
    def draw_scene(self):
        self.field.draw_cells()  # Рисуем поле
        self.field.draw_fruits(self.fruits.get_fruits())
        self.field.draw_coins(self.coins.get_coins())

        alpha = self.moving['move_timer'] / self.moving['move_interval']
        snake_to_draw = self.moving_snake(self.previous_snake, self.snake.get_snake(), alpha, NUM_CELLS)

        self.field.draw_snake(snake_to_draw)
        self.screen.blit(self.ui.surface, (0, 0))
        self.screen.blit(self.field.surface, (WIDTH - HEIGHT, 0))  # Отображаем поле

    def get_excludes(self):
        return set(
                self.snake.get_snake() +
                list(self.fruits.get_fruits()) +
                list(self.coins.get_coins())
            )

    def render(self):
        if self.game_state == GameState.PLAYING:
            self.draw_scene()

        elif self.game_state == GameState.MAIN_MENU:
            self.main_menu.draw_main_menu()
            self.screen.blit(self.main_menu.surface, (0, 0))

        elif self.game_state == GameState.PAUSED:
            self.draw_scene()
            self.pause_menu.draw_pause_menu()
            self.screen.blit(self.pause_menu.surface, self.pause_menu.coordinate_shift)

        elif self.game_state == GameState.GAME_OVER:
            self.draw_scene()
            self.screen.blit(self.g_o_alpha, (0, 0))
            self.game_over_menu.draw_game_over_menu(self.score, self.collected_coins, self.formatted_timer(self.live_timer))
            self.screen.blit(self.game_over_menu.surface, self.game_over_menu.coordinate_shift)

        pygame.display.flip()

    def play(self):
        try:
            while self.running:
                dt = self.clock.tick(self.FPS) / 1000.0
                self.handle_events()

                if self.game_state in (GameState.MAIN_MENU, GameState.PAUSED, GameState.GAME_OVER):
                    self.handle_input()

                if self.game_state == GameState.PLAYING:
                    self.update(dt)

                self.render()

        finally:
            self.user_manager.save_user_data()
            pygame.quit()

    @staticmethod
    def formatted_timer(cur_time):
        seconds = int(cur_time)
        minutes = seconds // 60
        seconds = seconds % 60
        return f'{minutes:02d}:{seconds:02d}'

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
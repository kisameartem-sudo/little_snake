import pygame
from Computer_graph.snake.settings import GAME_OVER_WIDTH, GAME_OVER_HEIGHT
from Computer_graph.snake.colors import color_manager

class GameOverMenu:
    def __init__(self):
        self.surface = pygame.Surface((GAME_OVER_WIDTH, GAME_OVER_HEIGHT))
        self.texts = [] # пока заглушка
        self.title_font = pygame.font.Font(None, 50)
        self.font = pygame.font.Font(None, 30)
        self.center_x = GAME_OVER_WIDTH // 2
        self.available_height = GAME_OVER_HEIGHT - 200
        self.gap_title = 30

        self.draw_game_over_menu()



    def draw_game_over_menu(self):
        self.surface.fill(color_manager.colors['menu'].color_RGB)

        title = self.title_font.render("GAME OVER", True, "black")
        info = self.font.render(
            "ESC: Главное меню\nR: начать заново", True,"black")

        total_height = (title.get_height() + self.gap_title + info.get_height())
        y = (self.available_height - total_height) // 2

        title_rect = title.get_rect(midtop=(self.center_x, y))

        y += title.get_height() + self.gap_title

        info_rect = info.get_rect(midtop=(self.center_x, y))

        self.surface.blit(title, title_rect)
        self.surface.blit(info, info_rect)
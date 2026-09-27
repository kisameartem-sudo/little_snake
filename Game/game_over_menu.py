import pygame
from Computer_graph.snake.settings import WIDTH, HEIGHT
from Computer_graph.snake.colors import color_manager

class GameOverMenu:
    def __init__(self):
        self.surface = pygame.Surface((WIDTH - HEIGHT, WIDTH - HEIGHT))
        self.texts = [] # пока заглушка
        self.draw_game_over_menu()
        self.title_font = pygame.font.Font(None, 30)



    def draw_game_over_menu(self):
        self.surface.fill(color_manager.colors['menu'].color_RGB)

        info = self.font.render(
            (
                "ESC — Главное меню"
                "R — начать заново"
            ),
            True,
            (50, 50, 50),
        )

        self.surface.blit(info, (20, 20))
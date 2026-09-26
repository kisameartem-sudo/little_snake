import pygame
from Computer_graph.snake.settings import WIDTH, HEIGHT
from Computer_graph.snake.colors import color_manager

class MainMenu:
    def __init__(self):
        self.surface = pygame.Surface((WIDTH // 2, HEIGHT // 2))
        self.buttons = {} # пока заглушка

    def draw_buttons(self):
        pass

    def draw_menu(self):
        self.surface.fill(color_manager.colors['main_menu'].color_RGB)
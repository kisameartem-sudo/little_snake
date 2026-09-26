import pygame
from Computer_graph.snake.settings import WIDTH, HEIGHT
from Computer_graph.snake.colors import color_manager

class MainMenu:
    def __init__(self):
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.buttons = {} # пока заглушка
        self.draw_menu()

    def draw_buttons(self):
        pass

    def draw_menu(self):
        self.surface.fill(color_manager.colors['main_menu'].color_RGB)
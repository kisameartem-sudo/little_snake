import pygame
from Computer_graph.snake.settings import WIDTH, HEIGHT
from Computer_graph.snake.colors import color_manager

class UI:
    def __init__(self):
        self.surface = pygame.Surface((WIDTH - HEIGHT, HEIGHT))
        self.texts = [] # пока заглушка
        self.draw_ui()



    def draw_ui(self):
        self.surface.fill(color_manager.colors['background'].color_RGB)
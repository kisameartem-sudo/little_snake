import pygame
from snake.little_snake.settings import WIDTH, HEIGHT
from snake.little_snake.colors import color_manager

class MainMenu:
    def __init__(self):
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.texts = [] # пока заглушка
        self.draw_main_menu()



    def draw_main_menu(self):
        self.surface.fill(color_manager.colors['menu'].color_RGB)
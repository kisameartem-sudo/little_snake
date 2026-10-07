import pygame
from snake.little_snake.Game.base_menu import BaseMenu
from snake.little_snake.settings import WIDTH, HEIGHT
from snake.little_snake.colors import color_manager
from snake.little_snake.Game.button import Button

class MainMenu(BaseMenu):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.button_width = 400
        self.button_height = 100
        self.button_font = 50
        self.gap = 10
        self.buttons = {}
        self.new_button('START')
        self.new_button('MARKET')
        self.new_button('INFO')
        self.new_button('EXIT')
        self.set_buttons_pos()
        self.draw_main_menu()

    def set_buttons_pos(self):
        for i, button in enumerate(self.buttons):
            button_height = (self.gap + self.button_height // 2) + i * (self.gap + self.button_height)
            self.get_button(button).set_center((WIDTH // 2, button_height))

    def draw_main_menu(self):
        self.surface.fill(color_manager.colors['menu'].color_RGB)

        for button in self.buttons:
            self.buttons[button].draw_button(self.surface)
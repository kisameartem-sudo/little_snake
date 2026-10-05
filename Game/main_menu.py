import pygame
from snake.little_snake.settings import WIDTH, HEIGHT
from snake.little_snake.colors import color_manager
from snake.little_snake.Game.button import Button

class MainMenu:
    def __init__(self):
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.button_width = 400
        self.button_height = 100
        self.gap = 10
        self.buttons = {}
        self.new_button('START')
        self.new_button('MARKET')
        self.new_button('INFO')
        self.new_button('EXIT')
        self.set_buttons_pos()
        self.draw_main_menu()

    def new_button(self, text):
        self.buttons[text] = Button(self.button_width, self.button_height, text, 50)

    def set_buttons_pos(self):
        for i, button in enumerate(self.buttons):
            button_height = (self.gap + self.button_height // 2) + i * (self.gap + self.button_height)
            self.get_button(button).set_center((WIDTH // 2, button_height))

    def get_button(self, text):
        return self.buttons[text]

    def get_button_clicked(self, mouse_pos):
        for button in self.buttons:
            if self.buttons[button].is_hovered(mouse_pos):
                return button

    def update_hover(self, mouse_pos):
        for button in self.buttons:
            self.buttons[button].change_button_state(
                self.buttons[button].is_hovered(mouse_pos)
            )

    def draw_main_menu(self):
        self.surface.fill(color_manager.colors['menu'].color_RGB)

        for button in self.buttons:
            self.buttons[button].draw_button(self.surface)
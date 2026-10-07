import pygame
from snake.little_snake.Game.button import Button

class BaseMenu:
    def __init__(self):
        self.surface: object
        self.coordinate_shift = (0, 0)
        self.title_font = pygame.font.Font(None, 50)

        self.button_width: int
        self.button_height: int
        self.button_font: int
        self.button_gap: int
        self.buttons = {}

    def new_button(self, text):
        self.buttons[text] = Button(
            self.button_width,
            self.button_height,
            text,
            self.button_font)

    def set_surface_shift(self, position):
        self.coordinate_shift = position

    def screen_to_local(self, mouse_pos):
        return (mouse_pos[0] - self.coordinate_shift[0], mouse_pos[1] - self.coordinate_shift[1])

    def get_button(self, text):
        return self.buttons[text]

    def get_button_clicked(self, mouse_pos):
        shift_mouse_pos = self.screen_to_local(mouse_pos)
        for button in self.buttons:
            if self.buttons[button].is_hovered(shift_mouse_pos):
                return button

    def update_hover(self, mouse_pos):
        shift_mouse_pos = self.screen_to_local(mouse_pos)
        for button in self.buttons:
            self.buttons[button].change_button_state(
                self.buttons[button].is_hovered(shift_mouse_pos)
            )

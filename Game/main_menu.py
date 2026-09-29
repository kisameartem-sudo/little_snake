import pygame
from snake.little_snake.settings import WIDTH, HEIGHT
from snake.little_snake.colors import color_manager

class MainMenu:
    def __init__(self):
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.button_width = 400
        self.button_height = 100
        self.gap = 10
        self.font = pygame.font.Font(None, 50)
        self.buttons = {}
        self.new_button('START')
        self.new_button('MARKET')
        self.new_button('INFO')
        self.new_button('EXIT')
        self.draw_main_menu()

    def new_button(self, text):
        self.buttons[text] = [pygame.Rect(0,0,self.button_width,self.button_height),
                              False]

    def get_button(self, text):
        return self.buttons[text][0]

    def check_button(self, text):
        return self.buttons[text][1]

    def change_button_state(self, text, state):
        self.buttons[text][1] = state

    def draw_main_menu(self):
        self.surface.fill(color_manager.colors['menu'].color_RGB)

        for i, button in enumerate(self.buttons):
            button_height = (self.gap + self.button_height // 2) + i * (self.gap + self.button_height)
            self.get_button(button).center = (WIDTH // 2, button_height)

            pygame.draw.rect(
                self.surface,
                color_manager.colors['fruit'].color_RGB
                if self.check_button(button)
                else color_manager.colors['snake_head'].color_RGB,
                self.get_button(button)
            )
            title = self.font.render(button, True, "black")
            title_rect = title.get_rect(center = self.get_button(button).center)
            self.surface.blit(title, title_rect)
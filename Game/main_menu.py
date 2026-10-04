import pygame
from snake.little_snake.settings import WIDTH, HEIGHT
from snake.little_snake.colors import color_manager

class Button:
    def __init__(self, width, height, text):
        self.width, self.height = width, height
        self.text = text
        self.hovered = False
        self.button_rect = pygame.Rect(0, 0, self.width, self.height)
        self.base_color = color_manager.colors['snake_head'].color_RGB
        self.hovered_color = color_manager.colors['fruit'].color_RGB

        self.font = pygame.font.Font(None, 50)

    def get_state(self):
        return self.hovered

    def change_button_state(self, state: bool):
        self.hovered = state

    def set_center(self, position):
        self.button_rect.center = position

    def is_hovered(self, mouse_pos):
        return self.button_rect.collidepoint(mouse_pos)

    def draw_button(self, menu_surface):
        pygame.draw.rect(
            menu_surface,
            self.hovered_color if self.get_state() else self.base_color,
            self.button_rect,
            border_radius=10
        )

        title = self.font.render(self.text, True, "black")
        title_rect = title.get_rect(center=self.button_rect.center)
        menu_surface.blit(title, title_rect)

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
        self.buttons[text] = Button(self.button_width, self.button_height, text)

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

    def draw_main_menu(self):
        self.surface.fill(color_manager.colors['menu'].color_RGB)

        for button in self.buttons:
            self.buttons[button].draw_button(self.surface)
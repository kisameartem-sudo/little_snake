import pygame
from snake.little_snake.settings import PAUSE_MENU_WIDTH, PAUSE_MENU_HEIGHT
from snake.little_snake.colors import color_manager
from snake.little_snake.Game.button import Button

class PauseMenu:
    def __init__(self):
        self.surface = pygame.Surface(
            (PAUSE_MENU_WIDTH, PAUSE_MENU_HEIGHT),
            pygame.SRCALPHA)
        self.title_font = pygame.font.Font(None, 50)
        self.font = pygame.font.Font(None, 30)
        self.center_x = PAUSE_MENU_WIDTH // 2
        self.gap_title = 10
        self.gap_info = 5

        self.button_width = 150
        self.button_height = 70
        self.button_gap = 5
        self.buttons = {}
        self.new_button('Continue')
        self.new_button('Restart')
        self.set_buttons_pos()
        self.draw_pause_menu()

    def new_button(self, text):
        self.buttons[text] = Button(self.button_width, self.button_height, text, 40)

    def set_buttons_pos(self):
        for i, button in enumerate(self.buttons):
            button_width = (self.button_gap + self.button_width // 2) + i * (self.button_gap + self.button_width)
            print(button_width)
            self.get_button(button).set_center((button_width, 120))

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

    def draw_pause_menu(self):
        self.surface.fill(color_manager.colors['menu'].color_RGB + (100,))
        pygame.draw.rect(
            self.surface,
            color_manager.colors['fruit'].color_RGB,
            pygame.Rect(0, 0, PAUSE_MENU_WIDTH, PAUSE_MENU_HEIGHT),
            width=4
        )

        title = self.title_font.render("PAUSE", True, "black")
        total_height = (title.get_height() + 100)
        y = (PAUSE_MENU_HEIGHT - total_height) // 2
        title_rect = title.get_rect(midtop=(self.center_x, y))
        self.surface.blit(title, title_rect)

        for button in self.buttons:
            self.buttons[button].draw_button(self.surface)

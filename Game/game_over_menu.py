import pygame
from snake.little_snake.Game.base_menu import BaseMenu
from snake.little_snake.settings import GAME_OVER_WIDTH, GAME_OVER_HEIGHT
from snake.little_snake.colors import color_manager

class GameOverMenu(BaseMenu):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((GAME_OVER_WIDTH, GAME_OVER_HEIGHT))
        self.title_font = pygame.font.Font(None, 50)
        self.sub_title_font = pygame.font.Font(None, 30)
        self.center_x = GAME_OVER_WIDTH // 2
        self.height_to_title = 10
        self.gap_title = 30
        self.gap_info = 5
        self.gap = 5

        self.buttons = {}
        self.button_width = 120
        self.button_height = 40
        self.button_gap = 10
        self.button_font = 30

        self.new_button('Restart')
        self.new_button('Main menu')
        self.new_button('Exit')
        self.set_buttons_pos()
        self.draw_game_over_menu()

    def set_buttons_pos(self):
        for i, button in enumerate(self.buttons):
            button_x = self.button_gap + self.button_width // 2 + i * (self.button_gap + self.button_width)
            button_y = GAME_OVER_HEIGHT - self.button_height // 2 - self.button_gap
            self.get_button(button).set_center((button_x, button_y))

    def draw_game_over_menu(self):
        self.surface.fill(color_manager.colors['menu'].color_RGB)
        pygame.draw.rect(
            self.surface,
            color_manager.colors['fruit'].color_RGB,
            pygame.Rect(0, 0, GAME_OVER_WIDTH, GAME_OVER_HEIGHT),
            width=4
        )

        title = self.title_font.render("GAME OVER", True, "black")
        sub_title = self.sub_title_font.render('...Stats...', True, "black")

        total_height = (title.get_height() + self.gap_title)
        y = (self.height_to_title + total_height) // 2
        title_rect = title.get_rect(midtop=(self.center_x, y))

        y += title_rect.height + self.gap_title
        self.surface.blit(sub_title, (10, y))

        self.surface.blit(title, title_rect)

        for button in self.buttons:
            self.buttons[button].draw_button(self.surface)
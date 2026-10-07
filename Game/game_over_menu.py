import pygame
from snake.little_snake.Game.base_menu import BaseMenu
from snake.little_snake.settings import GAME_OVER_WIDTH, GAME_OVER_HEIGHT
from snake.little_snake.colors import color_manager

class GameOverMenu(BaseMenu):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((GAME_OVER_WIDTH, GAME_OVER_HEIGHT))
        self.title_font = pygame.font.Font(None, 50)
        self.font = pygame.font.Font(None, 30)
        self.center_x = GAME_OVER_WIDTH // 2
        self.available_height = GAME_OVER_HEIGHT - 200
        self.gap_title = 30
        self.gap_info = 5
        self.gap = 5

        self.buttons = {}
        self.button_width = 150
        self.button_height = 70
        self.button_gap = 5
        self.button_font = 40

        self.new_button('RESTART')
        self.new_button('Main menu')
        self.set_buttons_pos()
        self.draw_game_over_menu()

    def set_buttons_pos(self):
        for i, button in enumerate(self.buttons):
            button_width = (self.button_gap + self.button_width // 2) + i * (self.button_gap + self.button_width)
            self.get_button(button).set_center((button_width, 120))

    def draw_game_over_menu(self):
        self.surface.fill(color_manager.colors['menu'].color_RGB)
        pygame.draw.rect(
            self.surface,
            color_manager.colors['fruit'].color_RGB,
            pygame.Rect(0, 0, GAME_OVER_WIDTH, GAME_OVER_HEIGHT),
            width=4
        )

        title = self.title_font.render("GAME OVER", True, "black")
        info1 = self.font.render("ESC: Главное меню", True,"black")
        info2 = self.font.render("R: начать заново", True, "black")

        total_height = (title.get_height() + self.gap_title +
                        info1.get_height() + self.gap_info + info2.get_height())
        y = (self.available_height - total_height) // 2

        title_rect = title.get_rect(midtop=(self.center_x, y))

        y += title.get_height() + self.gap_title

        info1_rect = info1.get_rect(midtop=(self.center_x, y))

        y += info1.get_height() + self.gap_info

        info2_rect = info2.get_rect(midtop=(self.center_x, y))

        self.surface.blit(title, title_rect)
        self.surface.blit(info1, info1_rect)
        self.surface.blit(info2, info2_rect)

        for button in self.buttons:
            self.buttons[button].draw_button(self.surface)
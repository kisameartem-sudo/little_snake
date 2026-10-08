import pygame
from snake.little_snake.Game.base_menu import BaseMenu
from snake.little_snake.settings import GAME_OVER_WIDTH, GAME_OVER_HEIGHT
from snake.little_snake.colors import color_manager

class GameOverMenu(BaseMenu):
    def __init__(self):
        super().__init__()
        """Фундамент"""
        self.surface = pygame.Surface((GAME_OVER_WIDTH, GAME_OVER_HEIGHT))
        self.title_font = pygame.font.Font(None, 50)
        self.stats_font = pygame.font.Font(None, 30)

        """Области"""
        self.title_area = pygame.Rect(0, 0, GAME_OVER_WIDTH, 0)
        self.stats_area = pygame.Rect(0, 0, GAME_OVER_WIDTH, 0)
        self.buttons_area = pygame.Rect(0, 0, GAME_OVER_WIDTH, 0)
        self.calc_areas()

        """Вспомогательные параметры"""
        self.center_x = GAME_OVER_WIDTH // 2
        self.height_to_title = 10
        self.gap_info = 10
        self.stats_gap = 20

        """Кнопки"""
        self.button_width = 120
        self.button_height = 40
        self.button_gap = 10
        self.button_font = 30

        self.new_button('Restart')
        self.new_button('Main menu')
        self.new_button('Exit')
        self.set_buttons_pos()


    def set_buttons_pos(self):
        for i, button in enumerate(self.buttons):
            button_x = self.button_gap + self.button_width // 2 + i * (self.button_gap + self.button_width)
            button_y = self.buttons_area.centery
            self.get_button(button).set_center((button_x, button_y))

    def calc_areas(self):
        self.title_area.height = 80
        self.buttons_area.height = 60
        self.stats_area.height = GAME_OVER_HEIGHT - 80 - 60

        self.stats_area.top = self.title_area.bottom
        self.buttons_area.top = self.stats_area.bottom

    def draw_areas(self):
        self.surface.fill(color_manager.colors['menu'].color_RGB)

        pygame.draw.rect(
            self.surface,
            color_manager.colors['fruit'].color_RGB,
            pygame.Rect(0, 0, GAME_OVER_WIDTH, GAME_OVER_HEIGHT),
            width=4
        )

        pygame.draw.rect(
            self.surface,
            color_manager.colors['fruit'].color_RGB,
            self.title_area,
            width=2
        )

        pygame.draw.rect(
            self.surface,
            color_manager.colors['fruit'].color_RGB,
            self.stats_area,
            width=2
        )

        pygame.draw.rect(
            self.surface,
            color_manager.colors['fruit'].color_RGB,
            self.buttons_area,
            width=2
        )

    def draw_stats(self, score, coins, live_time):
        sub_title = self.stats_font.render('Stats...:', True, "black")
        sub_title_rect = sub_title.get_rect(topleft=(self.stats_area.left + self.gap_info, self.stats_area.top + self.gap_info))
        self.surface.blit(sub_title, sub_title_rect)

        scores_title = self.stats_font.render(f'Набрано очков: {score}', True, "black")
        coins_title = self.stats_font.render(f'Собрано монет: {coins}', True, "black")
        live_time_title = self.stats_font.render(f'Время жизни: {live_time}', True, "black")

        scores_title_rect = scores_title.get_rect(topleft=(self.stats_area.left + self.gap_info, sub_title_rect.bottom + self.stats_gap))
        coins_title_rect = coins_title.get_rect(topleft=(self.stats_area.left + self.gap_info, scores_title_rect.bottom + self.stats_gap))
        live_time_title_rect = live_time_title.get_rect(topleft=(self.stats_area.left + self.gap_info, coins_title_rect.bottom + self.stats_gap))

        self.surface.blit(scores_title, scores_title_rect)
        self.surface.blit(coins_title, coins_title_rect)
        self.surface.blit(live_time_title, live_time_title_rect)

    def draw_game_over_menu(self, score, coins=0, live_time=0):
        self.draw_areas()

        title = self.title_font.render("GAME OVER", True, "black")

        title_rect = title.get_rect(center=self.title_area.center)
        self.surface.blit(title, title_rect)

        self.draw_stats(score, coins, live_time)

        for button in self.buttons:
            self.buttons[button].draw_button(self.surface)
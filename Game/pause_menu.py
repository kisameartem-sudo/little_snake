import pygame
from snake.little_snake.settings import PAUSE_MENU_WIDTH, PAUSE_MENU_HEIGHT
from snake.little_snake.colors import color_manager

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

        self.draw_pause_menu()



    def draw_pause_menu(self):
        self.surface.fill(color_manager.colors['menu'].color_RGB + (100,))
        pygame.draw.rect(
            self.surface,
            color_manager.colors['fruit'].color_RGB,
            pygame.Rect(0, 0, PAUSE_MENU_WIDTH, PAUSE_MENU_HEIGHT),
            width=4
        )

        title = self.title_font.render("PAUSE", True, "black")
        info1 = self.font.render("SPACE: Продолжить", True,"black")
        info2 = self.font.render("R: начать заново", True, "black")

        total_height = (title.get_height() + self.gap_title +
                        info1.get_height() + self.gap_info + info2.get_height())
        y = (PAUSE_MENU_HEIGHT - total_height) // 2

        title_rect = title.get_rect(midtop=(self.center_x, y))

        y += title.get_height() + self.gap_title

        info1_rect = info1.get_rect(midtop=(self.center_x, y))

        y += info1.get_height() + self.gap_info

        info2_rect = info2.get_rect(midtop=(self.center_x, y))

        self.surface.blit(title, title_rect)
        self.surface.blit(info1, info1_rect)
        self.surface.blit(info2, info2_rect)
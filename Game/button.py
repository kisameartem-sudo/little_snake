from snake.little_snake.colors import color_manager
import pygame

class Button:
    def __init__(self, width, height, text, font_size):
        self.width, self.height = width, height
        self.text = text
        self.hovered = False
        self.button_rect = pygame.Rect(0, 0, self.width, self.height)
        self.base_color = color_manager.colors['snake_head'].color_RGB
        self.hovered_color = color_manager.colors['fruit'].color_RGB

        self.font = pygame.font.Font(None, font_size)

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
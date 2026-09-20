import pygame
from color_shema import color_manager
from field import Field


class Game:
    def __init__(self):
        pygame.init()

        self.width = 800
        self.height = 600
        self.FPS = 60
        self.running = True
        self.field = Field(600)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('My_Snake')
        self.clock = pygame.time.Clock()

    # -------------------------------------------------
    # Обработка событий нажатия кнопок
    # -------------------------------------------------

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Проверка нажатия на крестик
                self.running = False

            elif event.type == pygame.KEYDOWN:
                '''Полверка нажатий кнопок'''
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    # -------------------------------------------------
    # Непрерывный ввод
    # -------------------------------------------------
    def handle_input(self):
        ...

    # -------------------------------------------------
    # 3. Изменение состояния
    # -------------------------------------------------
    def update(self):
        ...

    # -------------------------------------------------
    # 4. Отрисовка
    # -------------------------------------------------
    def render(self):
        self.field.draw_cells()
        self.screen.fill(color_manager.colors['background'].color_RGB)
        self.screen.blit(self.field.surface, (200, 0))

        pygame.display.flip()

    def play(self):
        try:
            while self.running:
                dt = self.clock.tick(self.FPS) / 1000.0
                self.handle_events()
                self.handle_input()
                self.update()
                self.render()

        finally:
            pygame.quit()



def main():
    snake_game = Game()
    snake_game.play()

if __name__ == '__main__':
    main()
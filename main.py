import pygame
from color_shema import color_manager


pygame.init()

width, height, FPS = 800, 600, 60

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('My_Snake')
clock = pygame.time.Clock()

states = {
    'running': True
}

# -------------------------------------------------
# Обработка событий нажатия кнопок
# -------------------------------------------------

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Проверка нажатия на крестик
            states['running'] = False

        elif event.type == pygame.KEYDOWN:
            '''Полверка нажатий кнопок'''
            if event.key == pygame.K_ESCAPE:
                states['running'] = False

# -------------------------------------------------
# Непрерывный ввод
# -------------------------------------------------
def handle_input():
    ...

# -------------------------------------------------
# 3. Изменение состояния
# -------------------------------------------------
def update():
    ...

# -------------------------------------------------
# 4. Отрисовка
# -------------------------------------------------
def render():
    screen.fill(color_manager.colors['background'].color_RGB)

    pygame.display.flip()

try:
    while states['running']:
        dt = clock.tick(FPS) / 1000.0
        handle_events()
        handle_input()
        update()
        render()

finally:
    pygame.quit()



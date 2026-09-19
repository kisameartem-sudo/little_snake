import pygame


pygame.init()

width, height = 800, 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('My_Snake')
clock = pygame.time.Clock()

states = {
    'running': True
}

#---------------------------------
# Обработка событий нажатия кнопок
#---------------------------------

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Проверка нажатия на крестик
            states['running'] = False

        elif event.type == pygame.KEYDOWN:
            '''Полверка нажатий кнопок'''
            if event.key == pygame.K_ESCAPE:
                states['running'] = False

try:
    while states['running']:
        clock.tick(60)

finally:
    pygame.quit()



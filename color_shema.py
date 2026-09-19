from dataclasses import dataclass

@dataclass
class Color_schema:
    name: str
    color_RGB: tuple[int, int, int]

class Color_manager:
    def __init__(self):
        self.colors = {}

    def add_color(self, assignment: str, name: str, rgb: tuple[int, int, int]):
        self.colors[assignment] = Color_schema(name, rgb)

color_manager = Color_manager()


color_manager.add_color('snake_segment', 'Бирюзово-синий', (39, 113, 122))
color_manager.add_color('snake_head', 'Припылённая бирюза', (48, 143, 149))
color_manager.add_color('cells', 'Тёплый бежевый', (199, 173, 143))
color_manager.add_color('background', 'Мягкий айвори', (232, 230, 221))
color_manager.add_color('fruit', 'Винно-красный', (102, 11, 18))



# ('', 'Глубокий бирюзовый', (27, 80, 86))
# ('', 'Тёмный бордовый', (68, 23, 26))
# ('', 'Глубокий бирюзовый', (37, 74, 80))
# ('', 'Приглушённая бирюза', (62, 136, 149))
# ('', 'Песочно-бежевый', (193, 163, 127))



from dataclasses import dataclass

@dataclass
class ColorInfo:
    name: str
    color_RGB: tuple[int, int, int]

class ColorManager:
    def __init__(self):
        self.colors = {}

    def add_color(self, assignment: str, name: str, rgb: tuple[int, int, int]):
        self.colors[assignment] = ColorInfo(name, rgb)

    def get_color(self, assignment: str):
        return self.colors[assignment].color_RGB

color_manager = ColorManager()

"""Игровой мир:"""
color_manager.add_color('field_background', 'Мягкий айвори', (232, 230, 221))
color_manager.add_color('grid_border', 'Глубокий оливково-зелёный', (91, 110, 84))

"""Интерфейс:"""
color_manager.add_color('menu_background', 'Молочно-льняной', (223, 215, 201))
color_manager.add_color('menu_border', 'Серо-тауповый', (154, 140, 127))
color_manager.add_color('button_default', 'Пыльный оливковый', (134, 138, 96))
color_manager.add_color('button_hover', 'Песочно-золотой', (210, 184, 120))
color_manager.add_color('text_primary', 'Тёмный шоколадно-сливовый', (70, 48, 47))

"""Сущности:"""
color_manager.add_color('snake_head', 'Бирюзово-синий', (39, 113, 122))
color_manager.add_color('snake_body', 'Тёмный хвойно-зелёный', (38, 62, 53))
color_manager.add_color('fruit_1', 'Винно-красный', (102, 11, 18))
color_manager.add_color('fruit_2', 'Тёмный бордовый', (68, 23, 26))
color_manager.add_color('fruit_3', 'Тёмный бордовый', (61, 1, 13))
color_manager.add_color('coin', 'Золотистый', (181, 177, 67))


"""Неиспользуемое"""
# color_manager.add_color('dusty_turquoise', 'Припылённая бирюза', (48, 143, 149))
# color_manager.add_color('warm_beige', 'Тёплый бежевый', (199, 173, 143))
#
# color_manager.add_color('sand_beige', 'Песочно-бежевый', (193, 163, 127))
# color_manager.add_color('golden', 'Золотистый', (240, 227, 0))
# color_manager.add_color('deep_turquoise_1', 'Глубокий бирюзовый', (27, 80, 86))
#
# color_manager.add_color('deep_turquoise_2', 'Глубокий бирюзовый', (37, 74, 80))
# color_manager.add_color('muted_turquoise', 'Приглушённая бирюза', (62, 136, 149))
#
# color_manager.add_color('sage_green', 'Шалфейно-зелёный', (112, 140, 120))
#
# color_manager.add_color('beige_gold', 'Бежево-золотой', (201, 176, 129))
#
# color_manager.add_color('copper_gold', 'Медно-золотой', (176, 126, 88))
# color_manager.add_color('muted_antique_gold', 'Приглушённый античный золотой', (184, 161, 94))
#
# color_manager.add_color('warm_clay', 'Тёплый глиняный', (168, 119, 96))
# color_manager.add_color('powder_pink_beige', 'Пудрово-розово-бежевый', (196, 166, 157))
# color_manager.add_color('cool_gray_turquoise', 'Холодный серо-бирюзовый', (103, 138, 140))
#
# color_manager.add_color('deep_petroleum_blue', 'Глубокий нефтяной синий', (32, 59, 66))

"""Старье"""
# color_manager.add_color('snake_segment', 'Бирюзово-синий', (39, 113, 122))
# color_manager.add_color('snake_head', 'Припылённая бирюза', (48, 143, 149))
# color_manager.add_color('cells_bord', 'Тёплый бежевый', (199, 173, 143))
# color_manager.add_color('background', 'Мягкий айвори', (232, 230, 221))
# color_manager.add_color('fruit', 'Винно-красный', (102, 11, 18))
# color_manager.add_color('menu', 'Песочно-бежевый', (193, 163, 127))
# color_manager.add_color('coin', 'Золотистый', (240, 227, 0))




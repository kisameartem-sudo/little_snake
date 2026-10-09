from enum import Enum

WIDTH = 800
HEIGHT = 600
FPS = 60

GAME_OVER_WIDTH = 400
GAME_OVER_HEIGHT = 400

PAUSE_MENU_WIDTH = 315
PAUSE_MENU_HEIGHT = 200

NUM_CELLS = 10

# FRUITS---------------------------
MAX_NUM_FRUITS = 4
DELAY_TO_NEW_FRUIT = 20

# COINS---------------------------
MAX_NUM_COINS = 2
DELAY_TO_NEW_COIN = 100

# SNAKE----------------------------
SNAKE_START_POS = (1, 1)

# SAVE_MANAGER----------------------------
USER_DATA = 'player_data.json'

class KEYBOARD_KEYS(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


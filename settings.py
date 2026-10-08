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
DELAY_TO_NEW_FRUIT = 4

# COINS---------------------------
MAX_NUM_COINS = 2
DELAY_TO_NEW_COIN = 30

# SNAKE----------------------------
SNAKE_START_POS = (1, 1)


class KEYBOARD_KEYS(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


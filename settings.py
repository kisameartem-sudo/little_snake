from enum import Enum

WIDTH = 800
HEIGHT = 600
FPS = 60

GAME_OVER_WIDTH = 400
GAME_OVER_HEIGHT = 400

NUM_CELLS = 10

# FRUITS---------------------------
MAX_NUM_FRUITS = 4
DELAY_TO_NEW_FRUIT = 4

# SNAKE----------------------------
SNAKE_START_POS = (1, 1)


class KEYBOARD_KEYS(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


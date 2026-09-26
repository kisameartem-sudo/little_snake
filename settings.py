from enum import Enum
import pygame

WIDTH = 800
HEIGHT = 600
FPS = 60

NUM_CELLS = 10

# FRUITS---------------------------
MAX_NUM_FRUITS = 4
DELAY_TO_NEW_FRUIT = 4

# SNAKE----------------------------
SNAKE_START_POS = (1, 1)


class KEYBOARD_KEYS(Enum):
    UP = 'UP'
    DOWN = 'DOWB'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


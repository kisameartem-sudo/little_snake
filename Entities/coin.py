from random import randint
from snake.little_snake.settings import NUM_CELLS, MAX_NUM_COINS, DELAY_TO_NEW_COIN

class Coins:
    def __init__(self, excluded):
        self.max_cell = NUM_CELLS - 1
        self.coins = set()
        self.add_coin(excluded)
        self.delay_to_add_coin = DELAY_TO_NEW_COIN

    def update_delay(self):
        self.delay_to_add_coin -= 1
        if self.delay_to_add_coin == 0:
            self.delay_to_add_coin = DELAY_TO_NEW_COIN
            return True

    def add_coin(self, excluded: set):
        if len(self.coins) == MAX_NUM_COINS:
            return

        while True:
            coin_cell = (randint(0, self.max_cell), randint(0, self.max_cell))

            if coin_cell not in excluded:
                self.coins.add(coin_cell)
                break

    def remove_coin(self, cell: tuple[int, int]):
        self.coins.remove(cell)

    def get_coins(self):
        return tuple(self.coins)

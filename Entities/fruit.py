from random import randint
from snake.little_snake.settings import NUM_CELLS, MAX_NUM_FRUITS, DELAY_TO_NEW_FRUIT

class Fruits:
    def __init__(self, excluded):
        self.max_cell = NUM_CELLS - 1
        self.fruits = set()
        self.add_fruit(excluded)
        self.delay_to_add_fruit = MAX_NUM_FRUITS

    def update_delay(self):
        self.delay_to_add_fruit -= 1
        if self.delay_to_add_fruit == 0:
            self.delay_to_add_fruit = 4
            return True

    def add_fruit(self, excluded: set):
        if len(self.fruits) == MAX_NUM_FRUITS:
            return

        excluded.update(self.fruits)

        while True:
            fruit_cell = (randint(0, self.max_cell), randint(0, self.max_cell))

            if fruit_cell not in excluded:
                self.fruits.add(fruit_cell)
                break

    def remove_fruit(self, cell: tuple[int, int], excluded: set):
        self.fruits.remove(cell)
        self.add_fruit(excluded)

    def get_fruits(self):
        return tuple(self.fruits)

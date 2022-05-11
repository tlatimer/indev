import logging.handlers
import random
from collections import Counter

from Rooms import RoomsTable
from Items import ItemsTable


# we use the logger to write to the console
# Debug    - verbose variable manipulation
# Info     - long descriptions
# Warning  - statuses
# Error    - short descriptions
# Critical - input prompts
def init_logger(console_level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create file handler
    fh = logging.handlers.RotatingFileHandler(
        filename='log.txt',
        maxBytes=8192,
        backupCount=8,
    )
    fh.setLevel(logging.DEBUG)
    fh.doRollover()

    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(console_level)

    # create formatters and add it to the handlers
    fh.setFormatter(
        logging.Formatter('%(asctime)s | %(message)s', datefmt='%Y/%m/%d %a %H:%M:%S')
    )
    ch.setFormatter(
        logging.Formatter("%(message)s")  # "\\x1b[37m" +
    )

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logging.debug('Logging Started')


class GameState:
    def __init__(self, name):
        self.name = name
        random.seed(name)

        self.hp = 20
        self.water = 20
        self.food = 20
        self.inventory = ['canteen']
        # self.status_effects = []  # TODO

    def is_alive(self):
        return self.hp > 0

    def do_stat_ticks(self):
        capacity = self.inventory.count('Canteen') * 10
        leaky = self.inventory.count('Leaky Canteen')
        if leaky > 0 and self.water > capacity:
            self.water = max(self.water - leaky, capacity)
            logging.warning("Your canteen is leaking...")

        self.water -= 1
        if self.water < 0:
            self.water = 0
            self.hp -= 1
            logging.warning("You're so thirsty...")

        self.food -= 1
        if self.food < 0:
            self.food = 0
            self.hp -= 1
            logging.warning("You're so hungry...")

        if self.hp < 5:
            logging.warning("A feeling of unease comes over you")

        logging.debug(f'hp: {self.hp}\twater: {self.water}\tfood: {self.food}\n')


class RoomManager:
    def __init__(self, game_state):
        self.gs = game_state
        self.rt = RoomsTable(game_state)
        self.it = ItemsTable()

    def move(self):
        logging.critical("[wasd] to move; [b] for backpack")
        choice = input()
        logging.debug(choice)
        if choice == 'b':
            self.view_backpack()
        # discard the input and move randomly instead
        return self.rt.get_rand_room()

    def view_backpack(self):
        self.it.view_backpack(self.gs.inventory)

        logging.error(f'hp: {self.gs.hp}\twater: {self.gs.water}\tfood: {self.gs.food}\n')
        return self.move()  # recursion just made the flow easier, no actual recursion algorithm used


def main():
    init_logger(logging.DEBUG)
    while True:  # outer loop to restart the game after death
        logging.error("And your name is?")
        name = input()
        logging.debug(name)
        gs = GameState(name)
        rm = RoomManager(gs)

        while gs.is_alive():  # main game loop
            cur_room = rm.move()  # move to the next room
            cur_room.enter()

            gs.do_stat_ticks()

        logging.error(f'{name} has met their end.')


if __name__ == '__main__':
    main()

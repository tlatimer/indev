import logging.handlers
import random
from collections import Counter

import Rooms2


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

        self.hp = 10
        self.water = 10
        self.food = 10
        self.inventory = ['canteen']
        # self.status_effects = []  # TODO

    def is_alive(self):
        return self.hp > 0

    def do_stat_ticks(self):
        leaky = self.inventory.count('leaky canteen')
        if leaky > 0:
            logging.warning("Your canteen is leaking...")
            self.water -= leaky

        self.water -= 1
        if self.water < 0:
            self.water = 0
            logging.warning("You're so thirsty...")
            self.hp -= 1

        self.food -= 1
        if self.food < 0:
            self.food = 0
            logging.warning("You're so hungry...")
            self.hp -= 1

        if self.hp < 5:
            logging.warning("A feeling of unease flows through you")


class RoomManager:
    def __init__(self, game_state):
        self.gs = game_state
        self.rt = Rooms2.RoomsTable(game_state)

    def move(self):
        logging.critical("[wasd] to move; [b] for backpack")
        c = input()
        if c == 'b':
            self.view_backpack()
        # discard the input and move randomly instead
        return self.rt.get_rand_room()

    def view_backpack(self):
        pretty_inv = Counter(self.gs.inventory)
        for item, count in pretty_inv.most_common():
            logging.error(f'{count}\t{item}')

        logging.error(f'hp: {self.gs.hp}\twater: {self.gs.water}\tfood: {self.gs.food}\n')
        return self.move()  # recursion just made the flow easier, no actual recursion algorithm used


def main():
    init_logger(logging.DEBUG)
    while True:  # outer loop to restart the game after death
        logging.error("And your name is?")
        name = input()
        gs = GameState(name)
        rm = RoomManager(gs)

        while gs.is_alive():  # main game loop
            cur_room = rm.move()  # move to the next room
            cur_room.enter()

            gs.do_stat_ticks()

        logging.error(f'{name} has met their end.')


if __name__ == '__main__':
    main()
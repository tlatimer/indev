import random
from collections import Counter

import Rooms2


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

    def do_stats_tick(self):
        leaky = self.inventory.count('leaky canteen')
        if leaky > 0:
            print("Your canteen is leaking...")
            self.water -= leaky

        self.water -= 1
        if self.water < 0:
            self.water = 0
            print("You're so thirsty...")
            self.hp -= 1

        self.water -= 1
        if self.water < 0:
            self.water = 0
            print("You're so hungry...")
            self.hp -= 1

        if self.hp < 5:
            print("A feeling of unease flows through you")


class RoomManager:
    def __init__(self, game_state):
        self.gs = game_state
        self.rt = Rooms2.RoomsTable(game_state)

    def move(self):
        c = input("[wasd] to move; [b] for backpack?")
        if c == 'b':
            self.view_backpack()
        # discard the input and move randomly instead
        return self.rt.get_rand_room()

    def view_backpack(self):
        pretty_inv = Counter(self.gs.inventory)
        for item, count in pretty_inv.most_common():
            print(f'{count}\t{item}')

        print(f'hp: {self.gs.hp}\twater: {self.gs.water}\tfood: {self.gs.food}\n')
        return self.move()  # recursion just made the flow easier, no actual recursion algorithm used


def main():
    while True:  # outer loop to restart the game after death
        name = input("And your name is?")
        gs = GameState(name)
        rm = RoomManager(gs)

        while gs.is_alive():  # main game loop
            cur_room = rm.move()  # move to the next room
            cur_room.enter()

            gs.do_stats_tick()

        print(f'{name} has met their end.')


if __name__ == '__main__':
    main()

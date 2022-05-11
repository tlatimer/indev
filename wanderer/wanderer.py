import random

from Rooms import RoomsTable
from Items import ItemsTable


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
        capacity = self.inventory.count('Canteen') * 10
        leaky = self.inventory.count('Leaky Canteen')
        if leaky > 0 and self.water > capacity:
            self.water = max(self.water - leaky, capacity)
            print("Your canteen is leaking...")

        self.water -= 1
        if self.water < 0:
            self.water = 0
            self.hp -= 1
            print("You're so thirsty...")

        self.food -= 1
        if self.food < 0:
            self.food = 0
            self.hp -= 1
            print("You're so hungry...")

        if self.hp < 5:
            print("A feeling of unease comes over you")

        print(f'hp: {self.hp}\twater: {self.water}\tfood: {self.food}\n')


class RoomManager:
    def __init__(self, game_state):
        self.gs = game_state
        self.rt = RoomsTable(game_state)
        self.it = ItemsTable()

    def move(self):
        print("[wasd] to move; [b] for backpack")
        choice = input()
        print(choice)
        if choice == 'b':
            self.view_backpack()
        # discard the input and move randomly instead
        return self.rt.get_rand_room()

    def view_backpack(self):
        self.it.view_backpack(self.gs.inventory)

        print(f'hp: {self.gs.hp}\twater: {self.gs.water}\tfood: {self.gs.food}\n')
        return self.move()  # recursion just made the flow easier, no actual recursion algorithm used


def main():
    while True:  # outer loop to restart the game after death
        print("And your name is?")
        name = input()
        print(name)
        gs = GameState(name)
        rm = RoomManager(gs)

        while gs.is_alive():  # main game loop
            cur_room = rm.move()  # move to the next room
            cur_room.enter()

            gs.do_stat_ticks()

        print(f'{name} has met their end.')


if __name__ == '__main__':
    main()

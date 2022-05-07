import random
from collections import Counter

import Rooms


class GameState:
    def __init__(self, name):
        self.name = name
        random.seed(name)

        self.hp = 10
        self.water = 10
        self.food = 10
        self.inventory = ['canteen']
        self.status_effects = []

    def is_alive(self):
        if self.hp < 1:
            return False
        else:
            return True

    def do_stats_tick(self):
        self.water -= 1

        leaky = self.inventory.count('leaky canteen')
        if leaky > 0:
            print("Your canteen is leaking...")
            self.water -= leaky

        if self.water < 0:
            self.water = 0
            print("You're so thirsty...")
            self.hp -= 1

        if self.food > 0:
            self.food -= 1
        else:
            print("You're so hungry...")
            self.hp -= 1


class RoomManager:
    def __init__(self, gs):
        self.rooms = {
            Rooms.Room(gs): 1,
            Rooms.Fountain(gs): 1,
            Rooms.Trap(gs): 2,
            Rooms.Treasure(gs): 2,
            Rooms.Feast(gs): 2
            Rooms.Sleep(gs): 2
            Rooms.KeyChest(gs): 2
        }

        self.gs = gs

    def get_rand_room(self):
        return Rooms.choice_from_dict(self.rooms)

    def move(self):
        c = input("[wasd] to move; [b] for backpack?")
        if c == 'b':
            self.view_backpack()
        # discard the input and move randomly instead
        return self.get_rand_room()

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
            print('\n' + cur_room.room_text)
            cur_room.update()  # apply effects, asks user for input then makes choice
            gs.do_stats_tick()

        print(f'{name} has met their end.')


if __name__ == '__main__':
    main()

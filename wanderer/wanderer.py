import random

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
            Rooms.Room(gs): 5,
            Rooms.Fountain(gs): 1,
            Rooms.Trap(gs): 2,
            Rooms.Treasure(gs): 3,
        }

    def get_rand_room(self):
        kwargs = {
            'population': list(self.rooms.keys()),  # has to be a list to be sub-scriptable
            'weights': list(self.rooms.values()),
        }
        return random.choices(**kwargs)[0]  # random.choices returns a list, only return first element

    def move(self):
        input("[wasd] Where would you like to go next?")
        # discard the input and move randomly instead
        return self.get_rand_room()


def main():
    while True:  # outer loop to restart the game after death
        name = input("And your name is?")
        gs = GameState(name)
        rm = RoomManager(gs)

        while gs.is_alive():  # main game loop
            cur_room = rm.move()  # move to the next room
            print('\n' + cur_room.room_text)
            cur_room.action()  # asks user for input then makes choice
            gs.do_stats_tick()

        print(f'{name} has met their end.')


if __name__ == '__main__':
    main()

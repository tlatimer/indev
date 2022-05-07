import random

import Rooms


class GameState:
    hp = 10
    water = 10
    food = 10
    gold = 0
    inventory = ['canteen']
    status_effects = []

    def __init__(self, name):
        self.name = name
        random.seed(name)

    def is_alive(self):
        if self.hp < 1 or self.water < 1 or self.food < 1:
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
    rooms = {
        Rooms.Room(): 5,
        Rooms.Fountain(): 1
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
        rm = RoomManager()

        while gs.is_alive():  # main game loop
            cur_room = rm.move()  # move to the next room
            print('\n' + cur_room.room_text)
            cur_room.action(gs)  # asks user for input then makes choice

        print(f'{name} has met their end.')


if __name__ == '__main__':
    main()

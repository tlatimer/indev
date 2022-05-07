from collections import Counter
import random

import wanderer_strings as ws

room_types = {
    'empty',
    'chest',  # loot
    'feast',  # refill food and water
    'bed',  # refill hp, save point
    'trapped',  # lose hp
    'puzzle',
}


class Room:
    room_text = "There doesn't seem to be anything here.\n"
    global_actions = {
        'p': "Pass By",
        'b': "Check Backpack"
    }

    def __init__(self, game_state):
        self.gs = game_state

    def action(self):
        pass  # override me

    def get_choice(self):
        for key, text in self.actions.items():
            print(f'[{key}]  {text}')

        choice = input('?')
        if choice in self.global_actions:
            if choice == 'p':
                return ''
            elif choice == 'b':  # TODO: move this 'check backpack' somewhere else
                pretty_inv = Counter(self.gs.inventory)
                for item, count in pretty_inv.most_common():
                    print(f'{count}\t{item}')
                print(f'hp: {self.gs.hp}\twater: {self.gs.water}\tfood: {self.gs.food}\n')
                return self.get_choice()
        else:
            return choice


class BlankRoom(Room):
    room_text = "STUFF."

    def __init__(self, game_state):
        super().__init__(game_state)

        self.actions = {
            'a': 'Action',
        }
        self.actions.update(self.global_actions)

    def action(self):
        c = self.get_choice()
        # do stuff


class Treasure(Room):
    room_text = "Loot! Sweet, shiny loot!"

    def __init__(self, game_state):
        super().__init__(game_state)

        self.actions = {
        }
        self.actions.update(self.global_actions)

    def action(self):
        for _ in range(3):
            kwargs = {
                'population': list(ws.items.keys()),  # has to be a list to be sub-scriptable
                'weights': list(ws.items.values()),
            }
            item = random.choices(**kwargs)[0]  # random.choices returns a list, only return first element
            print(f'You found a [{item}]!')
            self.gs.inventory.append(item)
        self.get_choice()


class Fountain(Room):
    room_text = "There is a serene fountain gently bubbling nearby."

    def __init__(self, game_state):
        super().__init__(game_state)

        self.actions = {
            'd': "Drink",
            'f': "Fill Canteens"
        }
        self.actions.update(self.global_actions)

    def action(self):
        c = self.get_choice()
        if c == 'f':
            num_canteens = self.gs.inventory.count('canteen') + self.gs.inventory.count('leaky canteen')
            max_water = num_canteens * 10
            self.gs.water = max_water
        elif c == 'd':
            self.gs.water = max(10, self.gs.water)


class Trap(Room):
    room_text = "As you enter the room, your ankle gets hooked on a tripwire and three arrows shoot at you."

    def __init__(self, game_state):
        super().__init__(game_state)

        self.actions = {
        }
        self.actions.update(self.global_actions)

    def action(self):
        for _ in range(3):
            canteen_count = self.gs.inventory.count('canteen')
            arrow_hit = random.choices(
                ['canteen', 'body', 'miss'],
                weights=[canteen_count, 3, 5]
            )[0]  # random.choices returns a list

            if arrow_hit == 'body':
                self.gs.hp -= 1
                print(f"This arrow hits your body! You have {self.gs.hp} hp left.")
            elif arrow_hit == 'canteen':
                print('This arrow struck your backpack and put a hole in a canteen!')
                self.gs.inventory.remove('canteen')
                self.gs.inventory.append('leaky canteen')
            else:
                print("This arrow missed.")

        self.get_choice()


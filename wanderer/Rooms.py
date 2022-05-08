import random

import wanderer_strings as ws


def choice_from_dict(choice_dict):
    kwargs = {
        'population': list(choice_dict.keys()),  # has to be a list to be sub-scriptable
        'weights': list(choice_dict.values()),
    }
    return random.choices(**kwargs)[0]  # random.choices returns a list, we want a value


class Room:
    room_text = "There doesn't seem to be anything here.\n"
    global_actions = {
        # 'i': "Inspect Closer"  # TODO
        'p': "Pass By",
    }

    def __init__(self, game_state):
        self.gs = game_state

    def update(self):
        pass  # override me

    def get_choice(self):
        for key, text in self.actions.items():
            print(f'[{key}]  {text}')

        return input('?')


class BlankRoom(Room):
    room_text = "STUFF."

    def __init__(self, game_state):
        super().__init__(game_state)

        self.actions = {
            'a': 'Action',
        }
        self.actions.update(self.global_actions)

    def update(self):
        c = self.get_choice()  # don't call if there's no interactive prompt


class Treasure(Room):
    room_text = "Loot! Sweet, shiny loot!"

    def __init__(self, game_state):
        super().__init__(game_state)

        self.actions = self.global_actions

    def update(self):
        for _ in range(3):
            self.get_item()

    def get_item(self):
        item = choice_from_dict(ws.items)
        print(f'You found a [{item}]!')
        self.gs.inventory.append(item)


class Drink(Room):
    room_text = "There is a serene fountain gently bubbling nearby."

    def __init__(self, game_state):
        super().__init__(game_state)

        self.actions = {
            'd': "Drink",
            'f': "Fill Canteens"
        }
        self.actions.update(self.global_actions)

    def update(self):
        c = self.get_choice()
        if c == 'f':
            num_canteens = self.gs.inventory.count('canteen') + 0.5 * self.gs.inventory.count('leaky canteen')
            self.gs.water = int(num_canteens) * 10
        elif c == 'd':
            self.gs.water = max(10, self.gs.water)


class Trap(Room):
    room_text = "As you enter the room, your ankle gets hooked on a tripwire and three arrows shoot at you."

    def __init__(self, game_state):
        super().__init__(game_state)

        self.actions = {
        }
        self.actions.update(self.global_actions)

    def update(self):
        for _ in range(3):
            canteen_count = self.gs.inventory.count('canteen')
            arrow_hit = choice_from_dict({
                'canteen': canteen_count,
                'body': 3,
                'miss': 5,
            })

            if arrow_hit == 'body':
                self.gs.hp -= 1
                print(f"An arrow hits your body! You have {self.gs.hp} hp left.")
            elif arrow_hit == 'canteen':
                print('An arrow struck your backpack and put a hole in a canteen!')
                if self.gs.inventory.count('canteen') > 0:
                    self.gs.inventory.remove('canteen')
                    self.gs.inventory.append('leaky canteen')
            else:
                print("An arrow missed.")

        self.get_choice()


class Feast(Room):
    room_text = "You find a lavish feast worthy of a king laid out, with no one else in sight."

    def __init__(self, game_state):
        super().__init__(game_state)

        self.actions = {
            'e': 'Eat',
            'g': 'Gorge',
        }
        self.actions.update(self.global_actions)

    def update(self):
        c = self.get_choice()
        if c == 'e':
            print("You eat a healthy share.")
            self.gs.food = 10
        elif c == 'g':
            print("You gorge, like a guilty man at his last meal. Enjoy the cholesterol.")
            self.gs.food = 12
            self.gs.hp -= 2


class Sleep(Room):
    room_text = "You find a guest bedroom, with a lock on the inside of the door and a comfy mattress."

    def __init__(self, game_state):
        super().__init__(game_state)

        self.actions = {
            's': 'Sleep',
        }
        self.actions.update(self.global_actions)

    def update(self):
        c = self.get_choice()
        if c == 's':
            self.gs.hp = 10
            self.gs.food -= 1


class KeyChest(Treasure):
    def __init__(self, game_state):
        super().__init__(game_state)
        self.color = random.choices(ws.key_colors)[0]
        self.room_text = f"You find an elaborate chest, with {self.color} jewels gleaming on every edge. It is locked."

        self.actions = {
            'u': 'Unlock',
        }
        self.actions.update(self.global_actions)  # adds pass_by

    def update(self):
        c = self.get_choice()
        key_name = f'{ws.key_colors} Key'
        if c == 'u':
            if key_name in self.gs.inventory:
                self.gs.inventory.remove[key_name]
                for _ in range(10):
                    self.get_item()
            else:
                print("You unfortunately don't have the right key.")

import random

import pandas as pd

from Items import ItemsTable
from common_funcs import find_file, get_weighted_rand


class RoomsTable:
    def __init__(self, game_state):
        self.gs = game_state

        rooms_file = find_file('wanderer - rooms')
        # items_file = find_table_file('wanderer - items')

        self.df = pd.read_csv(rooms_file).fillna('')
        self.rooms = list(self.df['name'])
        self.weights = list(self.df['probability'])

    def get_rand_room(self):
        name = get_weighted_rand(self.rooms, self.weights)
        data = self.get_room_data(name)
        return ROOM_TYPES[data['type']](self, name)

    def get_room_data(self, room_name):
        data = self.df[self.df['name'].str.match(room_name)].to_dict(orient='list')
        for k, v in data.items():
            data[k] = v[0]
        return data


class RoomTemplate:
    def __init__(self, rooms_table, room_name):
        self.data = rooms_table.get_room_data(room_name)
        self.gs = rooms_table.gs  # game_state
        self.it = ItemsTable()
        self.loot = []

    def enter(self, has_choice=True):
        print(f"\n-={self.data['name']}=-")
        print(f"\n{self.data['entry_text']}")

        if self.loot:
            self.show_loot()

        if has_choice:
            self.handle_choice()

    def show_loot(self):
        for item in self.loot:
            print(f'You see an [{item}]!')

    def get_choice(self):
        options = ['5', '4', '3', '2', '1']
        for i in options[::-1]:
            if i == '4' and not self.loot:
                continue

            col = f'action{i}'
            if self.data[col]:
                print(f"[{i}] {self.data[col]}")
            else:
                options.remove(i)

        choice = input('[#]?')

        if choice not in options:
            print('Invalid Choice. Try again.')
            return self.get_choice()

        choice_str = self.data[f'action{str(choice)}']
        return choice_str

    def handle_choice(self):
        choice = self.get_choice()
        if choice[-1] == '+':
            self.gs.do_stat_ticks()

        if choice == 'Take Loot':
            self.gs.inventory += self.loot
        elif choice == 'Inspect+':
            print('You spend some extra time looking around.')
            self.inspect()
        elif choice in ['Leave', 'Turn Around']:
            pass
        else:
            return choice
        return None

    def inspect(self):
        pass  # TODO: overwrite me

    def generate_loot(self, max_items):
        for _ in range(random.randint(2, max_items)):
            item = self.it.get_rand_item()
            self.loot.append(item)


class room(RoomTemplate):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)

    def enter(self):
        super().enter(False)


class loot(RoomTemplate):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)

        self.generate_loot(self.data['max_loot'])


class key_loot(loot):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)
        self.color = random.choice(['Red', 'Green', 'Blue'])

    def handle_choice(self):
        choice = super().handle_choice()  # returns None if it was handled generically
        if not choice:
            return
        elif choice == 'Unlock':
            key_name = f'{self.color} Key'
            if key_name in self.gs.inventory:
                self.gs.inventory.remove(key_name)
                self.generate_loot(self.data['max_loot'])
                self.show_loot()
                super().handle_choice()
            else:
                print(f"You don't have a [{self.color} Key]")
                super().handle_choice()


class trap(RoomTemplate):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)
        self.num_traps = random.randint(2, 10)

    def enter(self):
        print(f"\n-={self.data['name']}=-")
        print(f"\n{self.data['entry_text']}")

        if self.loot:
            for item in self.loot:
                print(f'You see an [{item}]!')

        for _ in range(self.num_traps):
            self.fire_trap()

    def fire_trap(self):
        canteen_count = self.gs.inventory.count('canteen')
        arrow_hit = random.choice(['canteen'] * canteen_count + ['body'] * 3 + ['miss'] * 5)

        if arrow_hit == 'body':
            self.gs.hp -= 1
            print(f"An arrow hits your body! You have {self.gs.hp} hp left.")
        elif arrow_hit == 'canteen':
            print('An arrow struck your backpack and put a hole in a canteen!')
            self.gs.inventory.remove('canteen')
            self.gs.inventory.append('leaky canteen')
        else:
            print("An arrow missed.")


class eat(RoomTemplate):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)

    def handle_choice(self):
        choice = super().handle_choice()  # returns None if it was handled generically
        if not choice:
            return
        elif choice == 'Eat':
            print("You eat a healthy share.")
            self.gs.food = 10
        elif choice == 'Gorge':
            print("You gorge, like a guilty man at his last meal. Enjoy the cholesterol.")
            self.gs.food = 12
            self.gs.hp -= 2


class drink(RoomTemplate):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)

    def handle_choice(self):
        choice = super().handle_choice()  # returns None if it was handled generically
        if not choice:
            return
        elif choice == 'Drink':
            self.gs.water = max(10, self.gs.water)
            self.handle_choice()
        elif choice == 'Fill Canteens':
            num_canteens = self.gs.inventory.count('canteen') + 0.5 * self.gs.inventory.count('leaky canteen')
            self.gs.water = int(num_canteens) * 10
            self.gs.hp -= 1


class sleep(RoomTemplate):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)


class riddle(RoomTemplate):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)


ROOM_TYPES = {  # has to be at the bottom or else the classes aren't declared yet
    'room': room,
    'loot': loot,
    'key_loot': key_loot,
    'trap': trap,
    'eat': eat,
    'drink': drink,
    'sleep': sleep,
    'riddle': riddle,
}

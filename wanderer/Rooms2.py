import logging
import os
import random
from glob import glob
import pandas as pd

ITEMS = ['canteen', 'Red Key', 'Green Key', 'Blue Key', 'gold coin', 'silver coin', 'copper coin', 'stray rock']


def find_table_file(filename_prefix):
    files = glob(fr'C:\Users\*\Downloads\{filename_prefix}*')
    files += glob(fr'.\{filename_prefix}*')
    if not files:
        input(f'No file found for file "{filename_prefix}"'
              '[Press Enter to Exit]')
        exit(1)

    files.sort(key=os.path.getmtime, reverse=True)

    return files[0]


def get_weighted_rand(choices, weights):
    return random.choices(
        population=choices,
        weights=weights
    )[0]  # random.choices returns a list, we want the value


class RoomsTable:
    def __init__(self, game_state):
        self.gs = game_state

        rooms_file = find_table_file('wanderer - rooms')
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

        self.gs = rooms_table.gs

    def enter(self):
        logging.error(f"\n-={self.data['name']}=-")
        logging.info(f"\n{self.data['entry_text']}")

        self.handle_choice()

    def get_choice(self):
        options = [1, 2, 3]
        for i in options:
            col = f'action{i}'
            if self.data[col]:
                logging.error(f"[{i}] {self.data[col]}")

        choice = input()
        if choice not in [str(x) for x in options]:
            logging.critical('Invalid Choice. Try again.')
            self.get_choice()

        return self.data[f'action{str(choice)}']

    def handle_choice(self):
        choice = self.get_choice()
        # TODO: overwrite me
        # TODO: 5 - inspect
        pass


class room(RoomTemplate):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)

    def enter(self):
        logging.error(f"\n-={self.data['name']}=-")
        logging.info(f"\n{self.data['entry_text']}")


class loot(RoomTemplate):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)

        self.loot = []
        self.generate_loot(5)

    def handle_choice(self):
        choice = self.get_choice()
        if choice == 'Take Loot':
            self.gs.inventory += self.loot

    def generate_loot(self, max_items):
        for _ in range(random.randint(2, max_items)):
            item = random.choice(ITEMS)
            self.loot.append(item)
            logging.info(f'You see an [{item}]!')


class keyloot(loot):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)
        self.color = random.choice(['Red', 'Green', 'Blue'])

    def enter(self):
        logging.error(f"\n-={self.data['name']}=-")
        logging.info(f"\n{self.data['entry_text'].format(color=self.color)}")

        self.handle_choice()


class trap(RoomTemplate):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)
        self.num_trap = random.randint(2, 10)

    def enter(self):
        logging.error(f"\n-={self.data['name']}=-")
        logging.info(f"\n{self.data['entry_text'].format(num=self.num_trap)}")

        for _ in range(self.num_trap):
            self.fire_trap()

    def fire_trap(self):
        canteen_count = self.gs.inventory.count('canteen')
        arrow_hit = random.choice(['canteen'] * canteen_count + ['body'] * 3 + ['miss'] * 5)

        if arrow_hit == 'body':
            self.gs.hp -= 1
            logging.info(f"An arrow hits your body! You have {self.gs.hp} hp left.")
        elif arrow_hit == 'canteen':
            logging.info('An arrow struck your backpack and put a hole in a canteen!')
            self.gs.inventory.remove('canteen')
            self.gs.inventory.append('leaky canteen')
        else:
            logging.info("An arrow missed.")


class eat(RoomTemplate):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)

    def handle_choice(self):
        choice = self.get_choice()
        if choice == 'Eat':
            logging.info("You eat a healthy share.")
            self.gs.food = 10
        elif choice == 'Gorge':
            logging.info("You gorge, like a guilty man at his last meal. Enjoy the cholesterol.")
            self.gs.food = 12
            self.gs.hp -= 2


class drink(RoomTemplate):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)

    def handle_choice(self):
        choice = self.get_choice()
        if choice == 'Drink':
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


ROOM_TYPES = {
    'room': room,
    'loot': loot,
    'keyloot': keyloot,
    'trap': trap,
    'eat': eat,
    'drink': drink,
    'sleep': sleep,
    'riddle': riddle,
}

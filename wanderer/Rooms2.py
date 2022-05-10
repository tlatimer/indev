import logging
import os
import random
from glob import glob

import pandas as pd


def find_file(filename_prefix):
    """Checks each dir, then if it finds file(s) in that dir returns the most recent one"""
    patterns = [
        fr'C:\Users\*\Downloads\{filename_prefix}*',
        fr'.\{filename_prefix}*',
    ]

    for p in patterns:
        files = glob(p)
        if files:
            break

    assert files  # fails if no files were found

    files.sort(key=getmtime, reverse=True)

    modified_time = datetime.fromtimestamp(getmtime(files[0])).strftime('%Y/%m/%d %a %H:%M:%S')
    logging.debug(f'Using {files[0]}: modified {modified_time}')
    # print(f'Using {files[0]}: modified {modified_time}')
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

    def on_entry(self):
        logging.error(f"\n-={self.data['name']}=-")
        logging.info(f"\n{self.data['entry_text']}")

        choice = self.get_choice()
        self.handle_choice(choice)

    def get_choice(self):
        for i, col in [  # TODO: there's gotta be a better way to do this
            (1, 'action1'),
            (2, 'action2'),
            (3, 'action3'),
        ]:
            if self.data[col]:
                logging.error(f"[{i}] {self.data[col]}")

        return input('[#]?')

    def handle_choice(self, choice):
        # TODO: overwrite me
        # TODO: 5 - inspect
        pass


class room(RoomTemplate):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)


class loot(RoomTemplate):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)


class keyloot(RoomTemplate):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)

    def on_entry(self):
        logging.error(f"\n-={self.data['name']}=-")
        logging.info(f"\n{self.data['entry_text']}")

        choice = self.get_choice()
        self.handle_choice(choice)


class trap(RoomTemplate):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)

    def on_entry(self):
        logging.error(f"\n-={self.data['name']}=-")
        logging.info(f"\n{self.data['entry_text']}")

        choice = self.get_choice()
        self.handle_choice(choice)


class eat(RoomTemplate):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)


class drink(RoomTemplate):
    def __init__(self, rooms_table, room_name):
        super().__init__(rooms_table, room_name)


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

if __name__ == '__main__':
    rooms = RoomsTable()
    rooms.print_text('Feast')
    raise hell  # break into debug mode

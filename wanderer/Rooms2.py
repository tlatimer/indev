import pandas as pd
import os
from glob import glob

import Rooms


def find_table_file(filename_prefix):
    files = glob(fr'C:\Users\*\Downloads\{filename_prefix}*')
    files += glob(fr'.\{filename_prefix}*')
    if not files:
        input(f'No file found for file "{filename_prefix}"'
              '[Press Enter to Exit]')
        exit(1)

    files.sort(key=os.path.getmtime, reverse=True)

    print(f'Using {files[0]}: modified {os.path.getmtime(files[0])}')
    return files[0]


class RoomsTable:
    def __init__(self):
        rooms_file = find_table_file('wanderer - rooms')
        # items_file = find_table_file('wanderer - items')

        self.df = pd.read_csv(rooms_file)

    def print_entry_text(self, rm_entry_txt):
        row = pd.df[self.df['name'].str.match(rm_entry_txt)]
        return row['name']


if __name__ == '__main__':
    rooms = RoomsTable()
    raise hell

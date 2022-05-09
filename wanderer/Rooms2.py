import pandas as pd
import os
from glob import glob
import logging


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

        self.df = pd.read_csv(rooms_file).fillna('')

    def print_text(self, name):
        row = self.df[self.df['name'].str.match(name)]

        logging.error(f"-={row['name'].iloc[0]}=-")
        logging.info(row['entry_text'].iloc[0])

    def print_choices(self, name):
        row = self.df[self.df['name'].str.match(name)]

        for i, col in [
            (1, 'action1'),
            (2, 'action2'),
            (3, 'action3'),
        ]:
            if row[col].iloc[0]:
                logging.error(f"[{i}] {row[col].iloc[0]}")


if __name__ == '__main__':
    rooms = RoomsTable()
    rooms.print_text('Feast')
    raise hell

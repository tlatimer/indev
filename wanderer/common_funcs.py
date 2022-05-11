import random
from datetime import datetime
from glob import glob
from os.path import getmtime
import logging


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
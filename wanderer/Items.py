from common_funcs import find_file, get_weighted_rand
import csv

from collections import Counter
from pprint import pprint


class ItemsTable:
    def __init__(self):
        items_file = find_file('wanderer - items')
        self.item_list = []
        self.item_weights = []
        self.item_dict = dict()

        with open(items_file) as f:
            reader = csv.reader(f)
            _ = next(reader)  # we don't care about the names of the headers
            tier_probabilities = next(reader)
            for row in reader:
                self.item_dict[row[0]] = []
                for i in range(2, len(tier_probabilities)):
                    if row[i]:  # ignore blanks
                        self.item_list.append(row[i])

                        item_weight = int(row[1]) * int(tier_probabilities[i])
                        self.item_weights.append(item_weight)

                        self.item_dict[row[0]].append(row[i])

    def get_rand_item(self):
        return get_weighted_rand(self.item_list, self.item_weights)


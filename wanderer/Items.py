from common_funcs import find_file, get_weighted_rand
import csv
from tabulate import tabulate

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

    def view_backpack(self, inv_list):
        inv_count = Counter(inv_list)
        table_rows = []
        for category, items in self.item_dict.items():
            cat_count = 0
            cat_list = []
            for i in items:
                item_count = inv_count.get(i, 0)
                cat_count += item_count

                if item_count > 0:
                    cat_list.append(item_count)
                    cat_list.append(i)
                else:
                    cat_list += ['', '']

            if cat_count > 0:
                table_rows.append(cat_list)

        print(tabulate(table_rows, tablefmt="github"))
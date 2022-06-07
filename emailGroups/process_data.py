import load_data_json


def main():
    groups_dict = load_data_json.main()

<<<<<<< HEAD
    # convert to Groups
=======
    # convert to Group objects
>>>>>>> extrapolateTheCheckbook
    groups = {}
    for name, emails in groups_dict.items():
        groups[name] = Group(name, emails)

    for g in groups.values():
<<<<<<< HEAD
        g.find_parent(groups)
=======
        g.calc_family(groups)

    group_sizes = {}
    for name, g in groups.items():
        group_sizes[name] = g.cum_len()
>>>>>>> extrapolateTheCheckbook

    raise hell


class Group:
    def __init__(self, name, group_members):
        self.name = name
        self.members = set(group_members)
        self.parent = None
        self.parent_score = 0
        self.children = []

<<<<<<< HEAD
    def find_parent(self, other_groups):
=======
    def calc_family(self, other_groups):
>>>>>>> extrapolateTheCheckbook
        for name, g in other_groups.items():
            if name == self.name:
                continue  # don't want to compare to yourself

<<<<<<< HEAD
            score = len(g.members & self.members) / len(g.members | self.members)
            if score > self.parent_score:
                self.parent = name
                self.parent_score = score
        if self.parent:
            other_groups[self.parent].children.append(self.name)
=======
            score = len(g.members & self.members) / len(g.members | self.members)  # maybe do log() of denominator?
            if score > self.parent_score:
                self.parent = name
                self.parent_score = score

        if self.parent:
            other_groups[self.parent].children.append(other_groups[self.name])

    def cum_len(self):
        return len(self.members) + sum([i.cum_len() for i in self.children])
>>>>>>> extrapolateTheCheckbook


if __name__ == '__main__':
    main()

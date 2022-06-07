import load_data_json


def main():
    groups_dict = load_data_json.main()

    # convert to Groups
    groups = {}
    for name, emails in groups_dict.items():
        groups[name] = Group(name, emails)

    for g in groups.values():
        g.find_parent(groups)

    raise hell


class Group:
    def __init__(self, name, group_members):
        self.name = name
        self.members = set(group_members)
        self.parent = None
        self.parent_score = 0
        self.children = []

    def find_parent(self, other_groups):
        for name, g in other_groups.items():
            if name == self.name:
                continue  # don't want to compare to yourself

            score = len(g.members & self.members) / len(g.members | self.members)
            if score > self.parent_score:
                self.parent = name
                self.parent_score = score
        if self.parent:
            other_groups[self.parent].children.append(self.name)


if __name__ == '__main__':
    main()

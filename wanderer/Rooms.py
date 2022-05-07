from collections import Counter

room_types = {
    'empty',
    'chest',  # loot
    'feast',  # refill food and water
    'bed',  # refill hp, save point
    'trapped',  # lose hp
    'puzzle',
}


class Room:
    room_text = "There doesn't seem to be anything here."
    global_actions = {
        'p': "Pass By",
        'i': "Check Inventory"
    }

    def action(self, game_state):
        pass  # override me

    def get_choice(self, gs):
        for key, text in self.actions.items():
            print(f'[{key}]  {text}')

        choice = input('?')
        if choice in self.global_actions:
            if choice == 'p':
                return ''
            elif choice == 'i':  # TODO: move this 'check inventory' somewhere else
                pretty_inv = Counter(gs.inventory)
                for item, count in pretty_inv.most_common():
                    print(f'{count}\t{item}')
                print(f'hp: {gs.hp}\twater: {gs.water}\tfood: {gs.food}\n')
                return self.get_choice(gs)
        else:
            return choice


class Fountain(Room):
    room_text = "There is a serene fountain gently bubbling nearby."

    def __init__(self):
        self.actions = {
            'd': "Drink",
            'f': "Fill Canteens"
        }
        self.actions.update(self.global_actions)

    def action(self, game_state):
        c = self.get_choice(game_state)
        if c == 'f':
            max_water = game_state.inventory.count('canteen') * 10
            game_state.water = max_water
        elif c == 'd':
            game_state.water = max(10, game_state.water)
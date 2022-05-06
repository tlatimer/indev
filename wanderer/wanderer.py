import wanderer_strings as ws


def main():
    pass


# class Room:
#     def __init__(self, pos, prev_room):
#         self.pos = pos
#
#         if prev_room:
#             self.came_from = self.calc_came_from(prev_room)
#
#     def calc_came_from(self, prev_room):
#         dx = self.pos[0] - prev_room.pos[0]
#         dy = self.pos[1] - prev_room.pos[1]
#
#         if (dx, dy) == (0, 1):  # TODO: Verify these directions match the deltas
#             return 'north'
#         if (dx, dy) == (0, -1):
#             return 'south'
#         if (dx, dy) == (1, 0):
#             return 'east'
#         if (dx, dy) == (-1, 0):
#             return 'west'


if __name__ == '__main__':
    main()

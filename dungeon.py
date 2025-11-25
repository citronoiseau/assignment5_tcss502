import random
from room import RoomFactory
from item import ItemFactory


# things to implement: position of Adventurer
# think how adventurer will move around the maze
class Dungeon:
    def __init__(self, size):
        self._size = size
        self._maze = [[1 for x in range(self._size)] for y in range(self._size)]
        self._rooms = {}  # dictionary to store rooms and coordinates as keys and values

    def generate(self):
        self.generate_path_with_dfs()  # after that our self._maze has 0 values -> where our rooms will go
        self.assign_pillars()
        self.assign_items()

    def __str__(self):
        output_lines = []

        for y in range(self._size):  # each row of rooms
            row_top = []
            row_mid = []
            row_bot = []

            for x in range(self._size):  # each room in the row
                room = self._rooms[(x, y)]
                top, mid, bot = str(room).split(
                    "\n"
                )  # have to split because assigning for the entire maze

                row_top.append(top)
                row_mid.append(mid)
                row_bot.append(bot)

            # join all rows horizontally
            output_lines.append(" ".join(row_top))
            output_lines.append(" ".join(row_mid))
            output_lines.append(" ".join(row_bot))

            # gap between rooms
            output_lines.append("")

        return "\n".join(output_lines)

    def generate_path_with_dfs(self, x=0, y=0, visited=None, parent_room=None):
        if visited is None:
            visited = set()
        visited.add((x, y))

        # create room
        room = self.create_room(x, y)
        # assign doors
        if parent_room:
            self.assign_doors(room, x, y, parent_room)

        # DFS
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        random.shuffle(directions)
        for direction_x, direction_y in directions:
            next_x, next_y = x + direction_x, y + direction_y
            if 0 <= next_x < self._size and 0 <= next_y < self._size:
                if (next_x, next_y) not in visited:
                    self.generate_path_with_dfs(next_x, next_y, visited, room)

    def create_room(self, x, y):
        if (x, y) not in self._rooms:
            # randomize later
            if (x, y) == (0, 0):
                room = RoomFactory.create_entrance(x, y)
            elif (x, y) == (self._size - 1, self._size - 1):
                room = RoomFactory.create_exit(x, y)
            else:
                room = RoomFactory.create_room(x, y)
            self._rooms[(x, y)] = room
        else:
            room = self._rooms[(x, y)]

        return room

    def assign_doors(self, room, x, y, parent_room):
        direction_x = x - parent_room._x
        direction_y = y - parent_room._y

        if direction_x == 1:
            room.set_neighbor("W", parent_room)
            parent_room.set_neighbor("E", room)
        elif direction_x == -1:
            room.set_neighbor("E", parent_room)
            parent_room.set_neighbor("W", room)
        elif direction_y == 1:
            room.set_neighbor("N", parent_room)
            parent_room.set_neighbor("S", room)
        elif direction_y == -1:
            room.set_neighbor("S", parent_room)
            parent_room.set_neighbor("N", room)

    def assign_pillars(self):
        pillars = ["abstraction", "encapsulation", "inheritance", "polymorphism"]
        # get rooms that are not exit or entrance
        available_rooms = available_rooms = [
            room for room in self._rooms.values() if room.get_type() == "Room"
        ]
        # sample 4 random rooms
        selected_rooms = random.sample(available_rooms, 4)

        # assign pillar
        for room, pillar_name in zip(selected_rooms, pillars):
            room.assign_pillar(pillar_name)

    def assign_items(self):
        chance = 0.1  # probability for each item

        for room in self._rooms.values():
            if room.get_type() == "Room" and room.get_pillar() is None:
                # Healing Potion
                if random.random() < chance:
                    room.add_item(ItemFactory.create_healing_potion())
                # Vision Potion
                if random.random() < chance:
                    room.add_item(ItemFactory.create_vision_potion())
                # Pit
                if random.random() < chance:
                    room.add_item(ItemFactory.create_pit())

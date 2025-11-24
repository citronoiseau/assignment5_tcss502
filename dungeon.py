import random
from room import RoomFactory


class Dungeon:
    def __init__(self, size):
        self._size = size
        self._maze = [[1 for x in range(self._size)] for y in range(self._size)]
        self._rooms = {}  # dictionary to store rooms and coordinates as keys and values

    def generate(self):
        self.generate_path_with_dfs()  # after that our self._maze has 0 values -> where our rooms will go
        self.assign_pillars()
        self.assign_items()

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
        dx = x - parent_room._x
        dy = y - parent_room._y

        if dx == 1:
            room.set_neighbor("W", parent_room)
            parent_room.set_neighbor("E", room)
        elif dx == -1:
            room.set_neighbor("E", parent_room)
            parent_room.set_neighbor("W", room)
        elif dy == 1:
            room.set_neighbor("N", parent_room)
            parent_room.set_neighbor("S", room)
        elif dy == -1:
            room.set_neighbor("S", parent_room)

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
        items = ["healing_potion", "vision_potion", "pit"]
        chance = 0.1  # can modify this constant

        for room in self._rooms.values():
            if room.get_type() == "Room" and room.get_pillar() is None:
                for item in items:
                    if random.random() < chance:
                        room.add_item(item)

import random
from room import RoomFactory


class Dungeon:
    def __init__(self, size):
        self._size = size
        self._maze = [[1 for x in range(self._size)] for y in range(self._size)]
        self._rooms = {}  # dictionary to store rooms and coordinates as keys and values

    def generate(self):

        # for future randomize entrance and exit
        start_x, start_y = 0, 0  # prob can randomize later
        self._rooms[(start_x, start_y)] = RoomFactory.create_entrance(start_x, start_y)

        end_x, end_y = self._size - 1, self._size - 1  # prob can randomize later
        self._rooms[(end_x, end_y)] = RoomFactory.create_exit(end_x, end_y)

        self.generate_path_with_dfs(
            start_x, start_y
        )  # after that our self._maze has 0 values -> where our rooms will go
        self.place_rooms()
        self.assign_pillars()
        self.assign_items()

    def generate_path_with_dfs(self, x, y, visited=None):
        if visited == None:
            visited = set()  # using set so no same values
        visited.add((x, y))
        self._maze[y][x] = 0  # mark as 0 for room generation in future

        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left
        random.shuffle(directions)
        for direction_x, direction_y in directions:
            next_x, next_y = x + direction_x, y + direction_y
            if 0 <= next_x < self._size and 0 <= next_y < self._size:
                if (next_x, next_y) not in visited:
                    self.generate_path_with_dfs(next_x, next_y, visited)

    def place_rooms(self):
        for y in range(self._size):
            for x in range(self._size):
                if self._maze[y][x] == 0:
                    if (
                        x,
                        y,
                    ) not in self._rooms:  # already created Entrance and Exit, so need to skip it
                        room = RoomFactory.create_room(x, y)
                        self._rooms[(x, y)] = room
                    self.assign_doors(self._rooms[(x, y)], x, y)

    def assign_doors(self, room, x, y):
        if y > 0 and self._maze[y - 1][x] == 0:
            room.doors["N"] = True

        if y < self._size - 1 and self._maze[y + 1][x] == 0:
            room.doors["S"] = True

        if x > 0 and self._maze[y][x - 1] == 0:
            room.doors["W"] = True

        if x < self._size - 1 and self._maze[y][x + 1] == 0:
            room.doors["E"] = True

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

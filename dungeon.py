import random
from room import RoomFactory
from item import ItemFactory


class Dungeon:
    """
    Represents the dungeon that contains rooms, items, pillars,
    the adventurer, and all dungeon-generation and movement logic.
    """

    def __init__(self, size):
        """
        Initializes the dungeon with a given size

        Args:
            size (int): Size of the dungeon grid (size x size)
        """
        self._size = size
        self._maze = [[1 for x in range(self._size)] for y in range(self._size)]
        self._rooms = {}  # dictionary to store rooms and coordinates as keys and values
        self._entrance_coords = None
        self._exit_coords = None
        self._adventurer = None
        self._current_room = None

    def generate(self):
        """
        Generates the dungeon layout, including entrance, exit,
        rooms, pillars, and items
        """
        self._entrance_coords = self.random_edge_coords_generator()
        self._exit_coords = self.random_edge_coords_generator()
        # loop to ensure that entrance coords != exit coords
        while self._exit_coords == self._entrance_coords:
            self._exit_coords = self.random_edge_coords_generator()
        self.generate_path_with_dfs() 
        self.assign_pillars()
        self.assign_items()

    def random_edge_coords_generator(self):
        """
        Generates random coordinates along the edge of the dungeon for future entrance/exit creation

        Returns:
            tuple: (x, y) coordinates on a random dungeon edge
        """
        side = random.choice(["north", "south", "west", "east"])

        if side == "north":
            return (random.randint(0, self._size - 1), 0)

        elif side == "south":
            return (random.randint(0, self._size - 1), self._size - 1)

        elif side == "west":
            return (0, random.randint(0, self._size - 1))

        else:  # east
            return (self._size - 1, random.randint(0, self._size - 1))

    def generate_path_with_dfs(self, x=0, y=0, visited=None, parent_room=None):
        """
        Recursively generates the dungeon using Depth-First Search

        Args:
            x (int): Current x-coordinate
            y (int): Current y-coordinate
            visited (set): Set of visited coordinates
            parent_room (RoomConstructor): Parent room for door linking
        """
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
        """
        Creates a room at the given coordinates
        Creates an entrance/exit at the randomized coordinates

        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.

        Returns:
            RoomConstructor: Created room
        """
        if (x, y) not in self._rooms:
            if (x, y) == self._entrance_coords:
                room = RoomFactory.create_entrance(x, y)
            elif (x, y) == self._exit_coords:
                room = RoomFactory.create_exit(x, y)
            else:
                room = RoomFactory.create_room(x, y)
            self._rooms[(x, y)] = room
        else:
            room = self._rooms[(x, y)]

        return room

    def assign_doors(self, room, x, y, parent_room):
        """
        Assigns doors between two adjacent rooms

        Args:
            room (RoomConstructor): Current room
            x (int): X-coordinate of the current room
            y (int): Y-coordinate of the current room
            parent_room (RoomConstructor): Previously visited room
        """
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
        """
        Randomly assigns four pillars to random non-entrance, non-exit rooms
        """
        pillars = ["abstraction", "encapsulation", "inheritance", "polymorphism"]
        # get rooms that are not exit or entrance
        available_rooms = [
            room for room in self._rooms.values() if room.get_type() == "Room"
        ]
        # sample 4 random rooms
        selected_rooms = random.sample(available_rooms, 4)

        # assign pillar
        for room, pillar_name in zip(selected_rooms, pillars):
            room.assign_pillar(pillar_name)

    def assign_items(self):
        """
        Randomly assigns items and pits to rooms that do not contain pillars
        """
        chance = 0.3  # probability for each item

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
                    room.add_pit(ItemFactory.create_pit())

    # game processing
    def set_adventurer(self, adventurer):
        """
        Places the adventurer in the entrance room

        Args:
            adventurer (Adventurer): The player character
        """
        self._adventurer = adventurer
        self._current_room = self._rooms[self._entrance_coords]

    def get_current_room(self):
        """
        Returns the room the adventurer is currently in

        Returns:
            RoomConstructor: The current room
        """
        return self._current_room

    def move_adventurer(self, direction):
        """
        Moves the adventurer in the given direction if a door exists

        Args:
            direction (str): 'N' or 'S' or 'E' or 'W'.
        """
        next_room = self._current_room.get_neighbors()[direction]
        if next_room:
            self._current_room = next_room
            return self._current_room
        return []

    def process_room(self):
        messages = []
        room = self._current_room

        if room.get_type() == "Room":
            items = room.pick_items()
            for item in items:
                if item.get_type() == "healing_potion":
                    self._adventurer.add_healing_potion()
                    messages.append("You found a Healing Potion!")

            pit = room.get_pit()
            if pit:
                damage = pit.get_damage()
                self._adventurer.take_damage(damage)
                messages.append(f"You fell into a pit and took {damage} damage!")

        if room.get_type() == "Room" and room.get_pillar():
            pillar = room.pick_pillar()
            if pillar:
                self._adventurer.add_pillar(pillar)
                messages.append(f"You obtained the pillar of {pillar}!")

        return messages

  # show the entire dungeon
    def __str__(self):
        """
        Returns a string representation of the entire dungeon map

        Returns:
            str:Vvisualization of the dungeon.
        """
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

    def get_dungeon_grid(self):
        return self._rooms

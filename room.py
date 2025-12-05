from abc import ABC, abstractmethod

items = ["healing_potion", "vision_potion", "pit", "empty"]


class RoomConstructor(ABC):
    """
    Abstract class representing a room in the dungeon
    """

    def __init__(self, type, x, y):
        """
        Initializes a room with a type and grid coordinates

        Args:
            type (str): The room type (Entrance, Exit, or Room)
            x (int): X-coordinate in the dungeon grid
            y (int): Y-coordinate in the dungeon grid
        """
        self._type = type
        self._x = x
        self._y = y
        self._neighbors = {"N": None, "S": None, "E": None, "W": None}

    def __str__(self):
        """
        Returns a string representation of the room

        Returns:
            str: Visual 3x3 representation of the room
        """
        top = "*" + ("-" if self.has_door("N") else "*") + "*"

        left = "|" if self.has_door("W") else "*"
        right = "|" if self.has_door("E") else "*"
        middle = f"{left}{self.get_display_char()}{right}"

        bottom = "*" + ("-" if self.has_door("S") else "*") + "*"

        return f"{top}\n{middle}\n{bottom}"

    def get_type(self):
        """
        Returns the type of the room

        Returns:
            str: Room type (Entrance, Exit, or Room)
        """
        return self._type

    def get_display_char(self):
        """
        Returns the character used to visually represent the room's contents

        Returns:
            str: Display character for the room
        """
        if self.get_type() == "Entrance":
            return "i"
        elif self.get_type() == "Exit":
            return "O"
        elif self.get_type() == "Room" and self.get_pillar():
            pillar_namings = {
                "abstraction": "A",
                "encapsulation": "E",
                "inheritance": "I",
                "polymorphism": "P",
            }
            return pillar_namings.get(self._pillar)
        elif len(self.get_items()) > 1:
            return "M"
        elif len(self.get_items()) == 1:
            return self._items[0].display_char()
        elif self.get_pit():
            return self._pit.display_char()
        else:
            return " "

    def has_door(self, direction):
        """
        Checks whether the room has a neighbor in a given direction

        Args:
            direction (str): 'N' or 'S' or 'E' or 'W'

        Returns:
            bool: True if a door exists in that direction
        """
        return self._neighbors[direction] is not None

    def get_neighbors(self):
        """
        Returns the dictionary of neighboring rooms

        Returns:
            dict: Direction-to-room mapping
        """
        return self._neighbors

    def set_neighbor(self, direction, room):
        """
        Connects a neighboring room in the given direction

        Args:
            direction (str):'N' or 'S' or 'E' or 'W'.
            room (RoomConstructor): The neighboring room object
        """
        if direction in self._neighbors:
            self._neighbors[direction] = room


class Entrance(RoomConstructor):
    """
    Represents the entrance of the dungeon
    """

    def __init__(self, x, y):
        """
        Creates an entrance room

        Args:
            x (int): X-coordinate of the entrance
            y (int): Y-coordinate of the entrance
        """
        super().__init__("Entrance", x, y)


class Exit(RoomConstructor):
    """
    Represents the exit of the dungeon
    """

    def __init__(self, x, y):
        """
        Creates an exit room

        Args:
            x (int): X-coordinate of the exit
            y (int): Y-coordinate of the exit
        """
        super().__init__("Exit", x, y)


class Room(RoomConstructor):
    """
    Represents a room that may contain items, pits, or pillars
    """

    def __init__(self, x, y):
        """
        Creates a room

        Args:
            x (int): X-coordinate of the room
            y (int): Y-coordinate of the room
        """
        super().__init__("Room", x, y)
        self._items = []
        self._pit = None
        self._pillar = None

    def assign_pillar(self, pillar):
        """
        Assigns a pillar to the room

        Args:
            pillar (str): Name of the pillar
        """
        self._pillar = pillar

    def get_pillar(self):
        """
        Returns the pillar in the room if one exists

        Returns:
            str | None: Pillar name or None
        """
        return self._pillar if self._pillar else None

    def add_item(self, item):
        """
        Adds an item to the room

        Args:
            item (Item): Item object to add
        """
        self._items.append(item)

    def add_pit(self, pit):
        """
        Adds a pit trap to the room

        Args:
            pit (Pit): Pit object to add
        """
        self._pit = pit

    def get_items(self):
        """
        Returns all items in the room

        Returns:
            list: List of items
        """
        return self._items

    def get_pit(self):
        """
        Returns the pit in the room if one exists

        Returns:
            Pit | None: Pit object or None
        """
        return self._pit

    def pick_items(self):
        """
        Removes and returns all items from the room

        Returns:
            list: Picked-up items
        """
        items_to_pick = self._items.copy()
        self._items.clear()
        return items_to_pick

    def pick_pillar(self):
        """
        Removes and returns the pillar from the room

        Returns:
            str | None: Picked-up pillar name or None
        """
        if self._pillar is None:
            return None

        pillar = self._pillar
        self._pillar = None
        return pillar


class RoomFactory:
    """
    Factory class for creating rooms
    """

    @staticmethod
    def create_room(x, y):
        """
        Creates and returns a room

        Args:
            x (int): X-coordinate
            y (int): Y-coordinate

        Returns:
            Room: A new Room object
        """
        return Room(x, y)

    @staticmethod
    def create_entrance(start_x, start_y):
        """
        Creates and returns an entrance room

        Args:
            start_x (int): X-coordinate
            start_y (int): Y-coordinate

        Returns:
            Entrance: A new Entrance object
        """
        return Entrance(start_x, start_y)

    @staticmethod
    def create_exit(end_x, end_y):
        """
        Creates and returns an exit room

        Args:
            end_x (int): X-coordinate
            end_y (int): Y-coordinate

        Returns:
            Exit: A new Exit object
        """
        return Exit(end_x, end_y)

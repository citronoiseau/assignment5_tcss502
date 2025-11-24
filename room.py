from abc import ABC, abstractmethod
import math

items = ["healing_potion", "vision_potion", "pit", "empty"]


class RoomConstructor(ABC):

    def __init__(self, type, x, y):
        self._type = type
        self._x = x
        self._y = y
        self._neighbors = {"N": None, "S": None, "E": None, "W": None}

    def get_type(self):
        return self._type

    def get_display_char(self):
        if self.get_type() == "Entrance":
            return "i"
        elif self.get_type() == "Exit":
            return "O"
        elif self._pillar is not None:
            pillar_namings = {
                "abstraction": "A",
                "encapsulation": "E",
                "inheritance": "I",
                "polymorphism": "P",
            }
            return pillar_namings.get(self._pillar)
        elif len(self._items) > 1:
            return "M"
        elif "pit" in self._items:
            return "X"
        elif "healing_potion" in self._items:
            return "H"
        elif "vision_potion" in self._items:
            return "V"
        else:
            return " "

    def has_door(self, direction):
        return self._neighbors[direction] is not None

    def get_neighbors(self):
        return self._neighbors

    def set_neighbor(self, direction, room):
        if direction in self._neighbors:
            self._neighbors[direction] = room

    def __str__(self):
        top = "*" + ("-" if self.has_door("N") else "*") + "*"

        # middle (left door, content, right door)
        left = "|" if self.has_door("W") else "*"
        right = "|" if self.has_door("E") else "*"
        middle = f"{left}{self.get_display_char()}{right}"

        bottom = "*" + ("-" if self.has_door("S") else "*") + "*"

        return f"{top}\n{middle}\n{bottom}"


class Entrance(RoomConstructor):
    def __init__(self, x, y):
        super().__init__("Entrance", x, y)


class Exit(RoomConstructor):
    def __init__(self, x, y):
        super().__init__("Exit", x, y)


class Room(RoomConstructor):
    def __init__(self, x, y):
        super().__init__("Room", x, y)
        self._items = []
        self._pillar = None

    def assign_pillar(self, pillar):
        self._pillar = pillar

    def get_pillar(self):
        return self._pillar if self._pillar else None

    def add_item(self, item):
        self._items.append(item)

    def get_items(self):
        return self._items


class RoomFactory:
    @staticmethod
    def create_room(x, y):
        return Room(x, y)

    @staticmethod
    def create_entrance(start_x, start_y):
        return Entrance(start_x, start_y)

    @staticmethod
    def create_exit(end_x, end_y):
        return Exit(end_x, end_y)

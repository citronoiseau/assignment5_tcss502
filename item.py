import random
from abc import ABC, abstractmethod


class Item(ABC):
    def __init__(self, type):
        self._type = type

    def get_type(self):
        return self._type

    @abstractmethod
    def display_char(self):
        pass


class HealingPotion(Item):
    def __init__(self):
        super().__init__("healing_potion")

    def display_char(self):
        return "H"


class VisionPotion(Item):
    def __init__(self):
        super().__init__("vision_potion")

    def display_char(self):
        return "V"


class Pit(Item):
    def __init__(self):
        super().__init__("pit")
        self._damage = random.randint(5, 20)

    def display_char(self):
        return "X"

    def get_damage(self):
        return self._damage


class ItemFactory:
    @staticmethod
    def create_healing_potion():
        return HealingPotion()

    @staticmethod
    def create_vision_potion():
        return VisionPotion()

    @staticmethod
    def create_pit():
        return Pit()

from abc import ABC, abstractmethod


class Item(ABC):
    @abstractmethod
    def display_char(self):
        pass


class HealingPotion(Item):
    def display_char(self):
        return "H"


class VisionPotion(Item):
    def display_char(self):
        return "V"


class Pit(Item):
    def display_char(self):
        return "X"


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

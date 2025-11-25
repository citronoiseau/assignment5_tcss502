from abc import ABC, abstractmethod
import random


# need to work on it when adventurer class is ready
# for now im just assuming the behavior that adventurer might have
class Item(ABC):
    @abstractmethod
    def use(self, adventurer):
        pass

    @abstractmethod
    def display_char(self):
        pass


class HealingPotion(Item):
    def __init__(self):
        self.healing_amount = random.randint(5, 15)

    def use(self, adventurer):
        adventurer.get_heal(self.healing_amount)

    def display_char(self):
        return "H"


class VisionPotion(Item):
    def use(self, adventurer):
        adventurer.reveal_vision()

    def display_char(self):
        return "V"


class Pit(Item):
    def __init__(self):
        self.damage = random.randint(1, 20)

    def use(self, adventurer):
        adventurer.get_damage(self.damage)

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

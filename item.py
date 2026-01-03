import random
from abc import ABC, abstractmethod


class Item(ABC):
    """
    Abstract class that represents an item in the dungeon
    """
    def __init__(self, type, name):
        """
        Initializes the item with a specific type

        Args:
            type (str): The type of the item.
        """
        self._type = type
        self._name = name

    def get_type(self):
        """
        Returns the type of the item.

        Returns:
            str: The item's type.
        """
        return self._type
    
    def get_name(self):
        """
        Returns the name of the item.
        Returns:
            str: The item's name.
        """
        return self._name
        

    @abstractmethod
    def display_char(self):
        """
        Returns the character used to display the item in the dungeon

        Returns:
            str: A single character representing the item
        """
        pass


class HealingPotion(Item):
    """
    Represents a healing potion item.
    """
    def __init__(self):
        """
        Creates an item with type "healing_potion)
        """
        super().__init__("healing_potion", "Healing Potion")

    def display_char(self):
        """
        Returns the display character for a Healing Potion

        Returns:
            str: 'H'
        """
        return "H"


class VisionPotion(Item):
    """
    Represents a vision potion item
    """
    def __init__(self):
        """
        Creates an item with type "vision_potion)
        """
        super().__init__("vision_potion", "Vision Potion")

    def display_char(self):
        """
        Returns the display character for a Vision Potion

        Returns:
            str: 'V'
        """
        return "V"


class Pit(Item):
    """
    Represents a pit that deals random damage
    """

    def __init__(self):
        """
        Creates a Pit with random damage between 5 and 20
        """
        super().__init__("pit", "Pit")
        self._damage = random.randint(5, 20)

    def display_char(self):
        """
        Returns the display character for a Pit.

        Returns:
            str: 'X'
        """
        return "X"

    def get_damage(self):
        """
        Returns the damage value of the pit.

        Returns:
            int: Damage dealt by the pit.
        """
        return self._damage



class ItemFactory:
    """
    Factory class used to create item objects
    """

    @staticmethod
    def create_healing_potion():
        """
        Creates and returns a Healing Potion

        Returns:
            HealingPotion: A new healing potion object
        """
        return HealingPotion()

    @staticmethod
    def create_vision_potion():
        """
        Creates and returns a Vision Potion

        Returns:
            VisionPotion: A new vision potion object
        """
        return VisionPotion()

    @staticmethod
    def create_pit():
        """
        Creates and returns a Pit

        Returns:
            Pit: A new pit object
        """
        return Pit()
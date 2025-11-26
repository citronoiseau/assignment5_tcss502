import random
from dungeon import Dungeon

START_RANGE = 75 
END_RANGE = 100

class Adventurer:
    def __init__(self, name, healing_potions, vision_potions, pillars_found):
        self.name = name
        self.hit_points = random.choices(range(START_RANGE, END_RANGE + 1), k=1)
        self.healing_potions = healing_potions
        self.vision_potions = vision_potions
        self.pillars_found = pillars_found

    """ Ability to move in Dungeon (you might decide to place this behavior elsewhere)
        need to know: 
            where I am
            where can I go to
            what's in the room

        could make fxn where the correct effect takes place when I enter the room:
            healing
            tell if pillar is found
            tell if exit is found
            tell if we're hurt (what would hurt us?)"""

    """Increases or decreases the Hit Points accordingly"""
    
    """Contains a _ _ str _ _ () method that builds a String containing:
    Name
    Hit Points
    Total Healing Potions
    Total Vision Potions
    List of Pillars Pieces Found"""

    def __str__(self, name, hit_points, healing_potions, vision_potions, pillars_found):
        return f"Name: {name}\n Hit points: {hit_points}\n Total healing potions: {healing_potions}\n Total Vision Potions: {vision_potions}\n List of Pillars Pieces Found: {pillars_found}\n"
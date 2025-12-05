import random
from dungeon import Dungeon

START_RANGE = 75 
END_RANGE = 100

class Adventurer:
    """ A class to represent an adventurer
    """

    def init(self, name):
        """Constructs the attributes needed for the adventurer

        Args:
            name (str): Name of the adventurer
        """
        
        self.name = name
        self.hit_points = random.randint(START_RANGE, END_RANGE)
        self.healing_potions = 0
        self.vision_potions = 0
        self.pillars_found = []
   
    def __str__(self):
        """A string that displays the characteristics of the adventurer

        Returns:
            str: Name of the adventurer, hit points, total healing potions, total vision potions, list of pillars found
        """
        return f"Name: {self.name}\n Hit points: {self.hit_points}\n Total healing potions: {self.healing_potions}\n Total Vision Potions: {self.vision_potions}\n List of Pillars found: {self.pillars_found}\n"

    def take_damage(self, damage):
        """ Inflicts damage on the adventurer

        Args:
            damage (int): How much damage is inflicted on the adventurer
        """
        self.hit_points -= damage
        if self.hit_points < 0:
            self.hit_points = 0
    
    def is_alive(self):
        """ Keeps track of if the adventurer is alive

        Returns:
            bool: Tells whether the adventurer is alive or not
        """
        if self.hit_points > 0:
            return True
        
    def get_pillars(self):
        """ Gets the pillars

        Returns:
            int: How many pillars were found
        """
        return self.pillars_found

    def heal(self, amount): # make sure that no more than 100 hp
        """ Heals the adventurer

        Args:
            amount (int): The amount to heal the adventurer

        Returns:
            int: How many healing potions the adventurer has
        """
        self.hit_points += amount
        if self.hit_points > 100:
            self.hit_points == 100
            return "Adventurer has reached max HP. Health: 100"
        return self.healing_potions
    
    def add_healing_potion(self):
        """ Adds a healing potion to the adventurer's inventory
        """
        self.healing_potions += 1

    def add_vision_potion(self):
        """ Adds a vision potion to the adventurer's inventory
        """
        self.vision_potions += 1
    
    def use_healing_potion(self):
        """ Uses the adventurer's healing potion
        """
        if self.healing_potions > 0:
            heal_amount = random.randint(15, 25)
            self.heal(heal_amount)
            self.healing_potions -= 1
            print(f"You used a Healing Potion and healed {heal_amount} HP!")
        else:
            print("You have no Healing Potions")

    def use_vision_potion(self, neighbors):
        """ Uses the adventurer's vision potion
        """
        if self.vision_potions > 0:
            self.vision_potions -= 1
            print("\nVision Potion used! You see:\n")

            for direction, room in neighbors.items():
                print(f"--- {direction} ---")
                if room:
                    print(room)
                else:
                    print("### WALL ###")

        else:
            print("You have no Vision Potions")

    def add_pillar(self, pillar):
        """ Adds a pillar to the adventurer's inventory
        """
        if pillar not in self.pillars_found:
            self.pillars_found.append(pillar)
    
    
    

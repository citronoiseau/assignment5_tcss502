import random
from dungeon import Dungeon

START_RANGE = 75 
END_RANGE = 100

class Adventurer:
    """ A class to represent an adventurer
    """

    def __init__(self, name):
        """Constructs the attributes needed for the adventurer

        Args:
            name (str): Name of the adventurer
        """
        
        self.name = name
        self.hit_points = random.randint(START_RANGE, END_RANGE)
        self.healing_potions = 0
        self.vision_potions = 0
        self.pillars_found = []
        self.last_event = ""
   
    def __str__(self):
        """A string that displays the characteristics of the adventurer

        Returns:
            str: Name of the adventurer, hit points, total healing potions, total vision potions, list of pillars found
        """
        # nicer pillars formatting
        if self.pillars_found:
            pillars = ", ".join(self.pillars_found)
        else:
            pillars = "None"
        return f"Name: {self.name}\n Hit points: {self.hit_points}\n Total healing potions: {self.healing_potions}\n Total Vision Potions: {self.vision_potions}\n List of Pillars found: {pillars}\n"

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
        """
        if self.hit_points >= 100:
            return 0   # no healing possible

        before_heal = self.hit_points
        self.hit_points = min(100, self.hit_points + amount)
        return self.hit_points - before_heal
    
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
        if self.healing_potions <= 0:
            self.last_event = "You have no Healing Potions."
            return self.last_event

        if self.hit_points >= 100:
            self.last_event = "Your health is already full."
            return self.last_event

        heal_amount = random.randint(15, 25)
        actual_heal = self.heal(heal_amount)
        self.healing_potions -= 1

        self.last_event = f"You used a Healing Potion and healed {actual_heal} HP!"
        return self.last_event

    def use_vision_potion(self, neighbors):
        if self.vision_potions <= 0:
            self.last_event = "You have no Vision Potions."
            return self.last_event

        self.vision_potions -= 1

        lines = ["Vision Potion used! You see:"]

        for direction, room in neighbors.items():
            if not room:
                continue

            description = [room.get_type()]

            # pillar
            if hasattr(room, "get_pillar") and room.get_pillar():
                description.append(f"Pillar: {room.get_pillar().title()}")

            # pit
            if hasattr(room, "get_pit") and room.get_pit():
                description.append("Pit!")

            # items
            if hasattr(room, "get_items"):
                items = room.get_items()
                if items:
                    item_names = ", ".join(item.get_name() for item in items)
                    description.append(f"Items: {item_names}")

            lines.append(f"{direction}: " + " | ".join(description))

        self.last_event = "\n".join(lines)
        return self.last_event

    def add_pillar(self, pillar):
        """ Adds a pillar to the adventurer's inventory
        """
        if pillar not in self.pillars_found:
            self.pillars_found.append(pillar)
    
    
    

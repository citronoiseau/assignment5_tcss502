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
   
    def __str__(self, name, hit_points, healing_potions, vision_potions, pillars_found):
        return f"Name: {name}\n Hit points: {hit_points}\n Total healing potions: {healing_potions}\n Total Vision Potions: {vision_potions}\n List of Pillars Pieces Found: {pillars_found}\n"

    def take_damage(self, damage):
        self.hit_points -= damage
    
    def is_alive(self):
        if self.hit_points > 0:
            return True
        
    def get_pillars(self):
        return self.pillars_found

    def heal(self, amount): # make sure that no more than 100 hp
        self.healing_potions += amount
        if self.healing_potions == 100:
            return "Adventurer has reached max HP. Health: 100"
        return self.healing_potions
    
    #def add_healing_potion(self): 

    def add_vision_potion(self):
        self.vision_potions += 1

    def use_healing_potion(self):
        self.healing_potions -= 1

    def use_vision_potion(self, neighbors): # i can help you with this one because its complicated
        pass
    
    def add_pillar(self, pillar):
        self.pillars_found += 1
    
    
    
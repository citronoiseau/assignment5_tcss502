import random
from dungeon import Dungeon

START_RANGE = 75 
END_RANGE = 100

class Adventurer:
    def init(self, name):
        self.name = name
        self.hit_points = random.randint(START_RANGE, END_RANGE)
        self.healing_potions = 0
        self.vision_potions = 0
        self.pillars_found = []
   
    def __str__(self):
        return f"Name: {self.name}\n Hit points: {self.hit_points}\n Total healing potions: {self.healing_potions}\n Total Vision Potions: {self.vision_potions}\n List of Pillars found: {self.pillars_found}\n"

    def take_damage(self, damage):
        self.hit_points -= damage
        if self.hit_points < 0:
            self.hit_points = 0
    
    def is_alive(self):
        if self.hit_points > 0:
            return True
        
    def get_pillars(self):
        return self.pillars_found

    def heal(self, amount): # make sure that no more than 100 hp
        self.hit_points += amount
        if self.hit_points > 100:
            self.hit_points == 100
            return "Adventurer has reached max HP. Health: 100"
        return self.healing_potions
    
    def add_healing_potion(self):
        self.healing_potions += 1

    def add_vision_potion(self):
        self.vision_potions += 1
    
    def use_healing_potion(self):
        if self.healing_potions > 0:
            heal_amount = random.randint(15, 25)
            self.heal(heal_amount)
            self.healing_potions -= 1
            print(f"You used a Healing Potion and healed {heal_amount} HP!")
        else:
            print("You have no Healing Potions")

    def use_vision_potion(self, neighbors):
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
        if pillar not in self.pillars_found:
            self.pillars_found.append(pillar)
    
    
    

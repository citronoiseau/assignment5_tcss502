from dungeon import Dungeon
from adventurer import Adventurer


class DungeonAdventure:
    def __init__(self):
        name = input("Enter your name: ")
        size = input("Enter the Dungeon size: ")
        position = (0, 0)

        self._dungeon = Dungeon(size)
        self._dungeon.generate()
        self._adventurer = Adventurer(name, position)

    def print_actions(self):
        print("Possible actions:")
        print("M - Move")
        print("H - Use a healing potion")
        print("H - Use a vision potion")

    def handle_movement(self):
        print("Possible movement:")
        directions = self._room.get_neighbors()
        print(directions)
        adventurer_direction = input("Direction: ")
        # also do a loop to ensure correct direction
        if adventurer_direction in directions:
            self._dungeon.move_adventurer(adventurer_direction)
        else:
            print("invalid")

    def start_game(self):
        print("Game started")
        print("Tour goal is to find all 4 pillars of OOP and Exit to win the game")

        # process the room
        self._dungeon._process_room()  # collect potions/pillars etc

        while self._adventurer.is_alive() and self._adventurer.get_pillars().length < 4:
            # print the room
            print(self._adventurer)
            print(self._dungeon.adventurer_room())

            # print the possible actions
            self.print_actions()
            # do an infinite loop until a good action is choosen
            choice = input("Choose an action: ")
            if choice == "M":
                self.handle_movement()
            elif choice == "H":
                self._adventurer.use_healing_potion()

            elif choice == "V":
                self._adventurer.use_vision_potion(neighbors)
            else:
                print("Invalid Option")

        if not self._adventurer.is_alive():
            print("you lost")
        print("Final map")
        print(self._dungeon)

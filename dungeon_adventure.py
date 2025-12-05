from dungeon import Dungeon
from adventurer import Adventurer


class DungeonAdventure:
    """ A class to represent an the logic for playing the game
    """
    def __init__(self):
        """ A constructor for the game
        """
        name = input("Enter your name: ")
        size = 0
        while size < 3:
            size = int(input("Enter the Dungeon size (Cannot be less than 3x3): "))

        self._dungeon = Dungeon(size)
        self._dungeon.generate()
        self._adventurer = Adventurer(name)
        self._dungeon.set_adventurer(self._adventurer)

    def print_actions(self):
        """ Actions the user can use to interact with the game
        """
        print("Possible actions:")
        print("M - Move")
        print("H - Use a healing potion")
        print("V - Use a vision potion")
        print("CHEAT - Show the entire dungeon")

    def handle_movement(self):
        """ Tells which direction the adventurer is going
        """
        print("Possible movement:")
        neighbors = self._dungeon.get_current_room().get_neighbors()
        valid_directions = [d for d, r in neighbors.items() if r is not None]
        print(valid_directions)
        # also do a loop to ensure correct direction
        while True:
            adventurer_direction = input("Direction: ").upper()

            if adventurer_direction in valid_directions:
                self._dungeon.move_adventurer(adventurer_direction)
                break
            else:
                print("Please enter a valid direction")

    def start_game(self):
        """ Starts the game
        """
        print("Game started")
        print("Tour goal is to find all 4 pillars of OOP and Exit to win the game")

        # process the room
        self._dungeon.process_room()  # collect potions/pillars etc

        while self._adventurer.is_alive():
            print(self._adventurer)
            # print the possible actions
            self.print_actions()
            current_room = self._dungeon.get_current_room()
            if (
                current_room.get_type() == "Exit"
                and len(self._adventurer.get_pillars()) == 4
            ):
                print("You reached the Exit with all 4 pillars! You won!")
                break
            # do an infinite loop until a good action is choosen
            choice = input("\nChoose an action: ")
            if choice == "M":
                self.handle_movement()
            elif choice == "H":
                self._adventurer.use_healing_potion()

            elif choice == "V":
                self._adventurer.use_vision_potion(
                    self._dungeon.get_current_room().get_neighbors()
                )
            elif choice == "CHEAT":
                print(self._dungeon)
            else:
                print("Invalid Option")

        if not self._adventurer.is_alive():
            print("You lost! :(")

        print("\nFinal map:")
        print(self._dungeon)


def main():
    """ Runs the game
    """
    game = DungeonAdventure()
    game.start_game()


if __name__ == "__main__":
    main()

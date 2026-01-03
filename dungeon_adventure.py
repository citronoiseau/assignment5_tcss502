from dungeon import Dungeon
from adventurer import Adventurer


class DungeonAdventure:
    """ A class to represent an the logic for playing the game
    """
    def __init__(self, name, size):
        """ A constructor for the game
        """
        self._dungeon = Dungeon(size)
        self._dungeon.generate()
        self._adventurer = Adventurer(name)
        self._dungeon.set_adventurer(self._adventurer)

        self._dungeon.process_room()

        self._last_event = "Game started!"

        self._room_ui_snapshot = None

    
    def get_game_state(self):
        return {
            "adventurer": self._adventurer,
            "current_room": self._dungeon.get_current_room(),
            "neighbors": self._dungeon.get_current_room().get_neighbors(),
            "won": self.is_won(),
            "lost": self.is_lost(),
            "event": self._last_event,
            "room_snapshot": self._room_ui_snapshot,
        }

    def is_won(self):
        room = self._dungeon.get_current_room()
        return (
            room.get_type() == "Exit"
            and len(self._adventurer.get_pillars()) == 4
        )

    def is_lost(self):
        return not self._adventurer.is_alive()

    def is_game_over(self):
        return self.is_won() or self.is_lost()


    def move(self, direction):
        if self.is_game_over():
            return

        room = self._dungeon.move_adventurer(direction)
        if not room:
            self._last_event = "You can't go that way."
            return

        # room copy for UI
        if room.get_type() != "Exit" and room.get_type() != "Entrance": 
            self._room_ui_snapshot = {
                "pillar": room.get_pillar(),
                "pit": room.get_pit(),
                "items": list(room.get_items()) 
            }

        messages = self._dungeon.process_room()
        if messages:
            self._last_event = "\n".join(messages)
        else:
            self._last_event = "You enter a new room."

    def use_healing(self):
        if self.is_game_over():
            return
        self._last_event = self._adventurer.use_healing_potion()

    def use_vision(self):
        if self.is_game_over():
            return
        self._last_event = self._adventurer.use_vision_potion(
        self._dungeon.get_current_room().get_neighbors()
    )

    def dungeon_map(self):
        return str(self._dungeon)

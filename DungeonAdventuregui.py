import tkinter as tk
from tkinter import messagebox
import random


# ----------------------------------------------------------
# ROOM CLASS
# ----------------------------------------------------------
class Room:
    def __init__(self):
        # Available items: pit, potion, pillar
        self.items = []
        self.generate_contents()

    def generate_contents(self):
        """Randomly give the room some items."""
        possible = ["pit", "potion", "pillar", None]
        item = random.choice(possible)
        if item:
            self.items.append(item)


# ----------------------------------------------------------
# DUNGEON CLASS (Grid)
# ----------------------------------------------------------
class Dungeon:
    def __init__(self, size):
        self.size = size
        self.grid = [[Room() for _ in range(size)] for _ in range(size)]

    def get_room(self, x, y):
        return self.grid[y][x]  # row-major


# ----------------------------------------------------------
# ADVENTURER CLASS
# ----------------------------------------------------------
class Adventurer:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, direction, dungeon_size):
        if direction == "N" and self.y > 0:
            self.y -= 1
        elif direction == "S" and self.y < dungeon_size - 1:
            self.y += 1
        elif direction == "W" and self.x > 0:
            self.x -= 1
        elif direction == "E" and self.x < dungeon_size - 1:
            self.x += 1
        # Diagonals
        elif direction == "NW" and self.x > 0 and self.y > 0:
            self.x -= 1
            self.y -= 1
        elif direction == "NE" and self.x < dungeon_size - 1 and self.y > 0:
            self.x += 1
            self.y -= 1
        elif direction == "SW" and self.x > 0 and self.y < dungeon_size - 1:
            self.x -= 1
            self.y += 1
        elif direction == "SE" and self.x < dungeon_size - 1 and self.y < dungeon_size - 1:
            self.x += 1
            self.y += 1


# ----------------------------------------------------------
# UI CLASS
# ----------------------------------------------------------
class DungeonUI:
    def __init__(self, root, dungeon, adventurer):
        self.root = root
        self.dungeon = dungeon
        self.adventurer = adventurer

        self.canvas_size = 300
        self.box_size = 200
        self.offset = (self.canvas_size - self.box_size) // 2

        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack()

        self.draw_room()
        self.draw_item_icons()
        self.draw_direction_buttons()

    # ---------------- ROOM -----------------
    def draw_room(self):
        self.canvas.delete("all")

        # Square
        self.canvas.create_rectangle(
            self.offset, self.offset,
            self.offset + self.box_size, self.offset + self.box_size,
            width=3
        )

    # ---------------- ITEMS ----------------
    def draw_item_icons(self):
        """Draw items inside the current room."""
        room = self.dungeon.get_room(self.adventurer.x, self.adventurer.y)
        items = room.items

        cx = cy = self.canvas_size // 2
        spacing = 40

        item_positions = {
            "pit":    (cx - spacing, cy),
            "potion": (cx,          cy),
            "pillar": (cx + spacing, cy),
        }

        for item in items:
            x, y = item_positions[item]

            if item == "pit":
                color = "black"
                label = "Pit"
            elif item == "potion":
                color = "blue"
                label = "Potion"
            elif item == "pillar":
                color = "gold"
                label = "Pillar"

            self.canvas.create_oval(x-15, y-15, x+15, y+15,
                                    fill=color, outline="")
            self.canvas.create_text(x, y+25, text=label, font=("Arial", 10))

    # ---------------- MOVEMENT -------------
    def direction_clicked(self, direction):
        self.adventurer.move(direction, self.dungeon.size)
        self.draw_room()
        self.draw_item_icons()
        self.draw_direction_buttons()

    def make_button(self, text, x, y):
        btn = tk.Button(self.root, text=text, width=6,
                        command=lambda d=text: self.direction_clicked(d))
        self.canvas.create_window(x, y, window=btn)

    def draw_direction_buttons(self):
        cx = self.canvas_size // 2
        cy = self.canvas_size // 2

        coords = {
            "N":  (cx, self.offset - 25),
            "NE": (self.offset + self.box_size + 35, self.offset - 25),
            "E":  (self.offset + self.box_size + 35, cy),
            "SE": (self.offset + self.box_size + 35, self.offset + self.box_size + 25),
            "S":  (cx, self.offset + self.box_size + 25),
            "SW": (self.offset - 35, self.offset + self.box_size + 25),
            "W":  (self.offset - 35, cy),
            "NW": (self.offset - 35, self.offset - 25),
        }

        for direction, (x, y) in coords.items():
            self.make_button(direction, x, y)


# ----------------------------------------------------------
# RUN GAME
# ----------------------------------------------------------
def main():
    root = tk.Tk()
    dungeon = Dungeon(size=4)
    adventurer = Adventurer()
    ui = DungeonUI(root, dungeon, adventurer)
    root.mainloop()

main()

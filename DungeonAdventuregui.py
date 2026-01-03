import tkinter as tk
from dungeon_adventure import DungeonAdventure

def start_game(player_name, dungeon_size):
    root = tk.Tk()
    root.title("Dungeon Adventure")
    game = DungeonAdventure(player_name, dungeon_size)

    def describe_room(room, items_copy):
            lines = []

            if room.get_type() == "Entrance":
                lines.append("🏁 Entrance")
            elif room.get_type() == "Exit":
                lines.append("🚪 Exit")
            else:
                lines.append("🧱 Room")

                if items_copy["pillar"]:
                    lines.append(f"🏛 Pillar:\n{items_copy['pillar'].title()}")
                if items_copy["pit"]:
                    lines.append("⚠ Pit!")
                if items_copy["items"]:
                    item_names = ", ".join(item.get_name() for item in items_copy["items"])
                    lines.append(f"🎒 Items: {item_names}")
            return "\n".join(lines)

    def disable_all_buttons():
        for btn in move_buttons.values():
            btn.config(state="disabled")
        heal_btn.config(state="disabled")
        vision_btn.config(state="disabled")
        cheat_btn.config(state="disabled")

    def update_ui():
        state = game.get_game_state()
        neighbors = state["neighbors"]

        room_label.config(
    text=describe_room(state["current_room"], state["room_snapshot"])
)
        event_label.config(text=state["event"])
        adventurer_label.config(text=str(state["adventurer"]))

        for d, btn in move_buttons.items():
            if neighbors[d]:
                btn.config(state="normal") 
            else:
                btn.config(state="disabled", bg="#ccc", fg="#666")  

        if state["won"]:
            room_label.config(text="🎉 You won!")
            event_label.config(text="You reached the Exit with all 4 pillars! You won!")
            disable_all_buttons()
        elif state["lost"]:
            room_label.config(text="💀 You lost!")
            disable_all_buttons()

    def cheat():
        if ui_state["map_visible"]:
            cheat_label.config(text="")
            cheat_btn.config(text="Cheat")
            ui_state["map_visible"] = False
        else:
            cheat_label.config(text=game.dungeon_map())
            cheat_btn.config(text="Hide Map")
            ui_state["map_visible"] = True
    # ui
    ui_state = {"map_visible": False}

    def start_over():
        root.destroy()
        setup_screen()
    tk.Button(root, text="Start Over", command=start_over).pack()

    tk.Button(root, text="Exit", command=root.destroy).pack()

    cheat_btn = tk.Button(root, text="Cheat", command=cheat)
    cheat_btn.pack()

    cheat_label = tk.Label(
    root,
    font=("Courier", 10),
    justify="left"
)
    cheat_label.pack()

    room_frame = tk.Frame(root, padx=10, pady=10)
    room_frame.pack()

    room_label = tk.Label(
        room_frame,
        width=22,
        height=7,
        relief="ridge",
        borderwidth=3,
        font=("Arial", 12),
        justify="center"
    )
    room_label.grid(row=1, column=1)

    move_buttons = {
        "N": tk.Button(room_frame, text="↑", width=5),
        "S": tk.Button(room_frame, text="↓", width=5),
        "W": tk.Button(room_frame, text="←", width=5),
        "E": tk.Button(room_frame, text="→", width=5),
    }

    move_buttons["N"].grid(row=0, column=1)
    move_buttons["S"].grid(row=2, column=1)
    move_buttons["W"].grid(row=1, column=0)
    move_buttons["E"].grid(row=1, column=2)

    for d, btn in move_buttons.items():
        btn.config(command=lambda d=d: (game.move(d), update_ui()))

    heal_btn = tk.Button(root, text="Heal",
                         command=lambda: (game.use_healing(), update_ui()))
    heal_btn.pack()

    vision_btn = tk.Button(root, text="Vision",
                           command=lambda: (game.use_vision(), update_ui()))
    vision_btn.pack()

    event_label = tk.Label(root, fg="blue", wraplength=300, justify="left")
    event_label.pack()

    adventurer_label = tk.Label(root, justify="left", font=("Courier", 10))
    adventurer_label.pack()

    update_ui()
    root.mainloop()

def setup_screen():
    setup = tk.Tk()
    setup.title("Dungeon Adventure")

    tk.Label(setup, text="Adventurer name:").pack()
    name_entry = tk.Entry(setup)
    name_entry.pack()

    tk.Label(setup, text="Dungeon size (min 3):").pack()
    size_entry = tk.Entry(setup)
    size_entry.pack()

    error_label = tk.Label(setup, fg="red")
    error_label.pack()

    tk.Label(setup, text="Your goal is to find all 4 pillars of OOP and Exit to win the game").pack()

    def start():
        name = name_entry.get().strip() or "Hero"

        try:
            size = int(size_entry.get())
        except ValueError:
            error_label.config(text="Dungeon size must be a number.")
            return

        if size < 3:
            error_label.config(text="Dungeon size must be at least 3.")
            return

        setup.destroy()
        start_game(name, size)

    tk.Button(setup, text="Start Game", command=start).pack(pady=10)

    setup.mainloop()


if __name__ == "__main__":
    setup_screen()
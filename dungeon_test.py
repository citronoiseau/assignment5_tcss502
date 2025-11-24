# plain_test_dungeon.py
from dungeon import Dungeon

# create a small dungeon
size = 4
dungeon = Dungeon(size)

# generate maze, rooms, doors, pillars, and items
dungeon.generate()

# print info about all rooms
for coord, room in dungeon._rooms.items():
    print(f"Room at {coord}:")
    print(f"  Type: {room.get_type()}")
    print(f"  Doors: {room.get_doors()}")
    if room.get_type() == "Room":
        print(f"  Pillar: {room.get_pillar()}")
        print(f"  Items: {room.get_items()}")
    print(room)
    print("-" * 10)

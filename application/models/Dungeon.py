from GameMath import create_matrix, create_list
from dice import dungeon_dice_roll
from asyncinit import asyncinit
from monster_factory import create_list_monsters, create_single_monster
from models.DungeonRoom import DungeonRoom

@asyncinit
class Dungeon:
    async def __init__(self, size) -> None:
        self.biome = await self.choose_biome()
        self.size = size
        self.room_mons = await self.populate_dungeon()
        self.rooms = await self.populate_rooms()

    async def populate_rooms(self):
        rooms = []
        for mons in self.room_mons:
            room = DungeonRoom()
            if mons == 1:
                monster = await create_single_monster(self)
                print(f"this is the monster: {monster}")
                room.monsters.append(monster)
                rooms.append(room)
            else:
                monsters = await create_list_monsters(self, mons)
                for monster in monsters:
                    print(f"this is the monster: {monster}")
                room.monsters = monsters
                room.building_mat_loot = await room.generate_building_mat_loot(self.biome, room.monsters)
                rooms.append(room)
        for room in rooms:
            print(f"this is the room: {room.monsters}")
        return rooms

    async def populate_dungeon(self):
        dungeon = await create_list(self.size)
        element = len(dungeon)
        dungeon[element - 1] = 1
        return dungeon
    
    async def choose_biome(self):
        biomes = ["Enki", "Ahab", "Kirkjufell", "Air"]
        print(len(biomes))
        biome_choice = await dungeon_dice_roll(1, len(biomes) - 1)
        return biomes[biome_choice]

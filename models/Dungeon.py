from GameMath import create_matrix, create_list
from dice import dungeon_dice_roll
from asyncinit import asyncinit

@asyncinit
class Dungeon:
    async def __init__(self, size) -> None:
        self.biome = await self.choose_biome()
        self.size = size
        self.room_mons = await self.populate_dungeon()

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


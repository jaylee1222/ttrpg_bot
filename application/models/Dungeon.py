from GameMath import create_matrix, create_list
from dice import dungeon_dice_roll
class Dungeon:
    def __init__(self, size) -> None:
        self.biome = self.choose_biome()
        self.size = size
        self.room_mons = self.populate_dungeon()

    def populate_dungeon(self):
        dungeon = create_list(self.size)
        element = len(dungeon)
        dungeon[element - 1] = 1
        return dungeon
    
    def choose_biome(self):
        biomes = ["Enki", "Ahab", "Kirkjufell", "Air"]
        print(len(biomes))
        biome_choice = dungeon_dice_roll(1, len(biomes) - 1)
        return biomes[biome_choice]


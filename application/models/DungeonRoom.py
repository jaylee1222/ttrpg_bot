import yaml
from dice import dungeon_dice_roll

class DungeonRoom:
    def __init__(self) -> None:
        self.monsters = []
        self.building_mat_loot = []
        self.item_loot = []
    
    async def generate_building_mat_loot(self, biome, monsters):
        with open('dungeon_attributes.yml', 'r') as file:
            dungeon_monsters = yaml.safe_load(file)
        with open('dungeon_loot.yml', 'r') as file:
            dungeon_loot_options = yaml.safe_load(file)
        common_items = []
        biome_items = []
        common_loot_num = 0
        biome_loot_num = 0
        for monster in monsters:
            if monster in dungeon_monsters['common']['monsters']:
                common_loot_num += 1
            else:
                biome_loot_num += 1
        common_loot = dungeon_loot_options['common']['house materials']
        biome_loot = dungeon_loot_options[biome]['house materials']    
        common_choice = await dungeon_dice_roll(common_loot_num, len(common_loot))
        biome_choice = await dungeon_dice_roll(biome_loot_num, len(biome_loot))
        for i in range(common_loot_num):
            common_items.append(common_loot[common_choice[i]])
        for i in range(biome_loot_num):
            biome_items.append(biome_loot[biome_choice[i]])
        items = common_items + biome_items
        return items

    # create method to generate common loot - in the future maybe common loot is just building materials?
    
    # create method for generating biome loot - maybe there are specific bosses with specific loot?
    # I think it'd be really cool to have specific biomes you want to farm for certain base things

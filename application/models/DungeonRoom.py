import yaml
from dice import dungeon_dice_roll

class DungeonRoom:
    def __init__(self) -> None:
        self.monsters = []
        self.building_mat_loot = []
        self.item_loot = []
    
    async def generate_building_mat_loot(self, biome, num_mons):
        with open('config_files/dungeon_loot.yml', 'r') as file:
            dungeon_loot_options = yaml.safe_load(file)

        common_loot = dungeon_loot_options['common']['house materials']
        biome_loot = dungeon_loot_options[biome]['house materials']    
        loot = common_loot + biome_loot

        items = await self.choose_loot(loot, num_mons)
        return items

    async def choose_loot(self, item_choices, loot_num):
        item_list = []
        choices = await dungeon_dice_roll(loot_num, len(item_choices))

        if isinstance(choices, int):
            item_list.append(item_choices[choices - 1])
        else:
            for i in range(len(choices)):
                item_list.append(item_choices[choices[i] - 1])
        return item_list
    
    # create method for generating biome loot - maybe there are specific bosses with specific loot?
    # I think it'd be really cool to have specific biomes you want to farm for certain base things

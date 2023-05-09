from models.Monster import Monster
from dice import weighted_dungeon_dice_roll, weighted_modifier_dice_roll
import yaml

with open('dungeon_attributes.yml', 'r') as file:
    attributes = yaml.safe_load(file)


def create_single_monster(dungeon):
    dungeon_modifier = dungeon.biome
    common_monsters = attributes['common']['monsters']
    biome_monsters = attributes[dungeon_modifier]['monsters']
    biome_modifiers = attributes[dungeon_modifier]['modifiers']
    modifier = weighted_modifier_dice_roll(biome_modifiers, 1)
    monster_name = weighted_dungeon_dice_roll(common_monsters, biome_monsters, 1)
    monster = Monster(modifier[0], monster_name[0])
    print(f"{monster.modifier} {monster.name}")
    return monster

def create_list_monsters(dungeon, mon_num):
    monsters = []
    dungeon_modifier = dungeon.biome
    common_monsters = attributes['common']['monsters']
    biome_monsters = attributes[dungeon_modifier]['monsters']
    biome_modifiers = attributes[dungeon_modifier]['modifiers']
    modifiers = weighted_modifier_dice_roll(biome_modifiers, mon_num)
    monster_names = weighted_dungeon_dice_roll(common_monsters, biome_monsters, mon_num)
    for (modifier, monster) in zip(modifiers, monster_names):
        mon = Monster(modifier, monster)
        print(f"{mon.modifier} {mon.name}")
        monsters.append(mon)
    return monsters
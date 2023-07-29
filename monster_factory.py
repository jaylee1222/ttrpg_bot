from models.Monster import Monster
from dice import weighted_dungeon_dice_roll, weighted_modifier_dice_roll
from CharacterCreation import generate_speed
import yaml

with open('dungeon_attributes.yml', 'r') as file:
    attributes = yaml.safe_load(file)


async def create_single_monster(dungeon):
    dungeon_modifier = dungeon.biome
    common_monsters = attributes['common']['monsters']
    biome_monsters = attributes[dungeon_modifier]['monsters']
    biome_modifiers = attributes[dungeon_modifier]['modifiers']
    modifier = await weighted_modifier_dice_roll(biome_modifiers, 1)
    monster = await weighted_dungeon_dice_roll(common_monsters, biome_monsters, 1)
    speed = await generate_speed(monster[0]['speed'])
    monster = Monster(modifier[0], monster[0]['name'], speed, monster[0]['attacks'], monster[0]['health'], monster[0]['defense'], monster[0]['damage'])
    print(f"{monster.modifier} {monster.name} {monster.speed} {monster.attacks} {monster.health} {monster.defense} {monster.damage}")
    return monster

async def create_list_monsters(dungeon, mon_num):
    monsters = []
    dungeon_modifier = dungeon.biome
    common_monsters = attributes['common']['monsters']
    biome_monsters = attributes[dungeon_modifier]['monsters']
    biome_modifiers = attributes[dungeon_modifier]['modifiers']
    modifiers = await weighted_modifier_dice_roll(biome_modifiers, mon_num)
    monster_names = await weighted_dungeon_dice_roll(common_monsters, biome_monsters, mon_num)
    for (modifier, monster) in zip(modifiers, monster_names):
        speed = await generate_speed(monster['speed'])
        print(speed)
        mon = Monster(modifier, monster['name'], speed, monster['attacks'], monster['health'], monster['defense'], monster['damage'])
        print(f"{mon.modifier} {mon.name} {mon.speed} {mon.attacks} {mon.health} {mon.defense} {mon.damage}")
        monsters.append(mon)
    return monsters
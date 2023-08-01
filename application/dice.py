import random

def dice_roll(dice_no, dice_sides):
    numbers = []
    for _ in range(dice_no):
        number = random.randint(1, dice_sides)
        if dice_no == 1:
            return number
        numbers.append(number)
    return numbers

def dungeon_dice_roll(dice_no, dice_sides):
    numbers = []
    for _ in range(dice_no):
        number = random.randint(0, dice_sides)
        if dice_no == 1:
            return number
        numbers.append(number)
    return numbers

def weighted_dungeon_dice_roll(common_choices, biome_choices, num_choices):
    if num_choices == 1:
        monster = random.choices(biome_choices)
        print(monster)
        return monster
    else:
        i = 0
        weight_nums = []
        choices = common_choices + biome_choices
        while i < 10 :
            weight_nums.append(10)
            i += 1
        i = 0
        while i < len(biome_choices):
            weight_nums.append(40)
            i +=1

        monsters = random.choices(choices, weights=weight_nums, k=num_choices)

        return monsters

def weighted_modifier_dice_roll(modifiers, num_choices):
    modifiers = random.choices(modifiers, k=num_choices)
    print(modifiers)
    return modifiers

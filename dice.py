import random

def dice_roll(dice_no, dice_sides):
    numbers = []
    for _ in range(dice_no):
        number = random.randint(1,dice_sides)
        numbers.append(number)
    return numbers

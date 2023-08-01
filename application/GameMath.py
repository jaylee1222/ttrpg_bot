import numpy as np
from dice import dice_roll

def create_matrix(size):
    dungeon = np.empty(size)
    nums = np.array(dice_roll(4, 4))
    mon_array = np.split(nums, 2)
    dungeon = np.append(mon_array[0], mon_array[1], axis=0).reshape(2, 2)
    return dungeon

def create_list(size):
    dungeon = []
    mon_nums = dice_roll(size, 4)
    for mon in mon_nums:
        dungeon.append(mon)
    return dungeon
import asyncio
import random
from Database import check_for_homes

response_timeout = 10.0
async def get_name_response(client, ctx):
    def check(m):
        print(m.content)
        return isinstance(m.content, str)
    try:
        response = await client.wait_for('message', check=check, timeout=response_timeout)
        print(response.content)
        return response.content
    except asyncio.TimeoutError:
        return await ctx.send(f'Sorry, you took too long to answer.')
    
async def get_home_response(client, ctx):
    def check(m):
        print(m.content)
        name_exists = True if check_for_homes(str(m.content)) else False
        return isinstance(m.content, str) and name_exists
    try:
        response = await client.wait_for('message', check=check, timeout=response_timeout)
        print(response.content)
        return response.content
    except asyncio.TimeoutError:
        return await ctx.send(f'Sorry, you took too long to answer.')

async def get_weapon_response(client, ctx, configList):
    def weaponcheck(m):
        if m.content.lower() in configList.lower():
            return True
    try:
        response = await client.wait_for('message', check=weaponcheck, timeout=response_timeout)
        print(response.content)
        return response.content
    except asyncio.TimeoutError:
        return await ctx.send(f'Sorry, you took too long to answer.')

async def generate_character_traits(configList):
    dice_size = len(configList)
    character_trait = random.choice(configList)
    print(character_trait['name'])
    return character_trait['name']

async def generate_personality(personalityList):
    personality_traits = []
    new_personality_traits = []
    personality_traits = random.sample(personalityList, 3)
    for personality in personality_traits:
        print(personality['name'])
        new_personality_traits.append(personality['name'])
    return new_personality_traits

async def generate_speed(speed):
    print(speed)
    return random.randrange(speed[0], speed[1])

async def generate_class(configList):
    dice_size = len(configList)
    character_trait = random.choice(configList)
    print(character_trait['name'])
    return character_trait['name']
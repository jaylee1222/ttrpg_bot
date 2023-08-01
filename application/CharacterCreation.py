import asyncio
import random

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
    print(dice_size)
    character_trait = random.choice(configList).strip("\n")
    return character_trait

async def generate_personality(personalityList):
    personality_traits = []
    personality_traits = random.sample(personalityList, 3)
    stripped_personality_traits = [x[:-1] for x in personality_traits]
    return stripped_personality_traits
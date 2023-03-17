#!/usr/local/bin/python3
import os
import string
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio
from DiscordUtilities import get_channel
from CharacterCreation import get_name_response, get_weapon_response, generate_character_traits, generate_personality
from Database import database_connection, insert
from Character import Character
from Player import Player

class MyClient(commands.Bot, discord.Client):
    def __init__(self):
        load_dotenv()
        self.DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    # async def on_message(self, message):
    #     print(f'Message from {message.author}: {message.content}')
    #     if message.author.id == self.user.id:
    #         return
    #     if message.channel.name != 'discord-bot-test':
    #         return

    #     if message.content.startswith('$createCharacter'):
    #         await message.channel.send('Greetings traveller! What is your name?')


            # try:
            #     guess = await self.wait_for('message', check=is_correct, timeout=5.0)
            # except asyncio.TimeoutError:
            #     return await message.channel.send(f'Sorry, you took too long it was {answer}.')


# client = commands.Bot(command_prefix='$', intents=intents)
client = MyClient()

@client.command(name="createCharacter")
async def create_character(ctx):
    weaponList = None
    weaponElementList = None
    classList = None
    armorList = None
    personalityList = None
    occupationList = None
    aspirationList = None
    weaponfilename = "character_creation/weapons.txt"
    weaponelementfilename = "character_creation/weaponelements.txt"
    classfilename = "character_creation/classes.txt"
    armorfilename = "character_creation/armortypes.txt"
    personalityfilename = "character_creation/personalitytraits.txt"
    occupationfilename = "character_creation/occupations.txt"
    aspirationfilename = "character_creation/aspirations.txt"
    with open(classfilename, 'r') as classes:
        classList = "".join(classes)
    with open(weaponfilename, 'r') as weapons:
        weaponList = "".join(weapons)
    with open(weaponelementfilename, 'r') as weaponelements:
        weaponElementList = "".join(weaponelements)
    with open(armorfilename, 'r') as armor:
        armorList = "".join(armor)
    with open(personalityfilename, 'r') as personalities:
        personalityList = "".join(personalities)
    with open(occupationfilename, 'r') as occupations:
        occupationList = "".join(occupations)
    with open(aspirationfilename, 'r') as aspirations:
        aspirationList = "".join(aspirations)
    characterName = None
    firstClass = None
    secondClass = None
    weaponChoice = None
    weaponElementChoice = None
    armorChoice = None
    personalityChoice = None
    occupationChoice = None
    aspirationChoice = None

    print(ctx.message)
    if (ctx.message.channel.name != "discord-bot-test"):
        return
    if ctx.message.author.bot == True:
        return
    print(f'{ctx.message.author.bot}')
    await ctx.send("Greetings traveller! What would you like the name of your character to be?")
    characterName = await get_name_response(client=client, ctx=ctx)
    await ctx.send(f"Greetings {characterName}! What class would you like to play?")
    await ctx.send(classList)
    firstClass = await get_weapon_response(client=client, ctx=ctx, configList=classList)
    await ctx.send(f"Oh mighty {firstClass}! You must be feared. What other class would you like to complement that?")
    await ctx.send(classList)
    secondClass = await get_weapon_response(client=client, ctx=ctx, configList=classList)
    await ctx.send(f"YES!!!! A {firstClass}/{secondClass} You must be a mighty warrior indeed! What weapon do you swing at your foes?")
    await ctx.send(weaponList)
    weaponChoice = await get_weapon_response(client=client, ctx=ctx, configList=weaponList)
    await ctx.send(f"Ahhhh, yes. The {weaponChoice}. I love a good slog with that one. What is that around your weapon?")
    await ctx.send(weaponElementList)
    weaponElementChoice = await get_weapon_response(client=client, ctx=ctx, configList=weaponElementList)
    await ctx.send(f"Of course it's {weaponElementChoice}! How could I be so blind. What is that armor you're wearing?")
    armorChoice = await get_weapon_response(client=client, ctx=ctx, configList=armorList)
    await ctx.send(f"{armorChoice}??? I wouldn't wear that but...what's your personality like?")
    await ctx.send(personalityList)
    personalityChoice = await get_weapon_response(client=client, ctx=ctx, configList=personalityList)
    await ctx.send(f"Of course you're {personalityChoice}. You ooze it! What do you do for your community?")
    await ctx.send(occupationList)
    occupationChoice = await get_weapon_response(client=client, ctx=ctx, configList=occupationList)
    await ctx.send(f"A {occupationChoice} you say? Wow, you're community is lucky to have you. What do you desire for your future?")
    await ctx.send(aspirationList)
    aspirationChoice = await get_weapon_response(client=client, ctx=ctx, configList=aspirationList)
    split_choice = aspirationChoice.split()
    shortened_aspiration = split_choice[0].replace(".", "")
    await ctx.send(f"{shortened_aspiration}? That's beautiful mate. I bet you're a successful delver.")
    pass

@client.command(name="fastCreateCharacter")
async def create_character(ctx):
    weaponList = None
    weaponElementList = None
    classList = None
    armorList = None
    personalityList = None
    occupationList = None
    aspirationList = None
    weaponfilename = "character_creation/weapons.txt"
    weaponelementfilename = "character_creation/weaponelements.txt"
    classfilename = "character_creation/classes.txt"
    armorfilename = "character_creation/armortypes.txt"
    personalityfilename = "character_creation/personalitytraits.txt"
    occupationfilename = "character_creation/occupations.txt"
    aspirationfilename = "character_creation/aspirations.txt"
    with open(classfilename, 'r') as classes:
        classList = classes.readlines()
    with open(weaponfilename, 'r') as weapons:
        weaponList = weapons.readlines()
    with open(weaponelementfilename, 'r') as weaponelements:
        weaponElementList = weaponelements.readlines()
    with open(armorfilename, 'r') as armor:
        armorList = armor.readlines()
    with open(personalityfilename, 'r') as personalities:
        personalityList = personalities.readlines()
    with open(occupationfilename, 'r') as occupations:
        occupationList = occupations.readlines()
    with open(aspirationfilename, 'r') as aspirations:
        aspirationList = aspirations.readlines()
    characterName = None
    firstClass = None
    secondClass = None
    weaponChoice = None
    weaponElementChoice = None
    armorChoice = None
    personalityChoice = []
    occupationChoice = None
    aspirationChoice = None
    await ctx.send("Greetings would-be-Delver! You want to Delve do ya? My name is Sally and I will be your tavernkeep of sorts." + 
    " All adventures begin there, don’t they? Anyways, tell me your name?")
    characterName = await get_name_response(client=client, ctx=ctx)
    weaponChoice = await generate_character_traits(weaponList)
    weaponElementChoice = await generate_character_traits(weaponElementList)
    firstClass = await generate_character_traits(classList)
    secondClass = await generate_character_traits(classList)
    armorChoice = await generate_character_traits(armorList)
    personalityChoice = await generate_personality(personalityList)
    occupationChoice = await generate_character_traits(occupationList)
    aspirationChoice = await generate_character_traits(aspirationList)
    split_choice = aspirationChoice.split()
    shortened_aspiration = split_choice[0].replace(".", "")
    disc_name = str(ctx.message.author)
    print(ctx.message.author)
    print(type(ctx.message.author))
    await ctx.send(f"Great to meet ya, {characterName}! Let’s get you set up shall we? This process is called Evocation." + 
    f" To keep it simple, I’ll bring out from you your Delving self from your Spark, the Bits that gave you life. Here we go.\n\n" + 
    
    f"Your weapon of choice is the {weaponChoice}, I see it is {weaponElementChoice} as well." + 
    f" The Data flows around you as a {firstClass} and a {secondClass} it seems." + 
    f" For your defense, {armorChoice} will keep you safe.\n\n" + 
    
    f"Now, who are you… It seems your Code sings mostly of {personalityChoice[0]}, {personalityChoice[1]} and {personalityChoice[2]}." + 
    f" In the Hamlet you are a {occupationChoice} it would seem. But yes, deeper still, you yearn for… {aspirationChoice}." + 
    f" We all yearn for something. I hope you find yours.\n\n" + 

    f"Good luck out there. Don’t die okay?")

    c1 = Character(char_name = characterName, first_class = firstClass, second_class = secondClass, weapon = weaponChoice, weapon_element = weaponElementChoice, armor = armorChoice, personality = personalityChoice, occupation = occupationChoice, aspiration = aspirationChoice)
    p1 = Player(disc_name = disc_name, char_id = c1.char_id)
    result = insert(p1, c1)
    print(result)
    await create_channel(ctx, c1.char_name)
    channel = await get_channel(ctx, client, "text", c1.char_name)
    print(channel.name)
    await channel.send(
        f"character name: {c1.char_name}\n" + 
        f"first class: {c1.first_class}\n" + 
        f"second class: {c1.second_class}\n" + 
        f"weapon: {c1.weapon}\n" +
        f"weapon element: {c1.weapon_element}\n" +
        f"armor: {c1.armor}\n" + 
        f"personality: {c1.personality[0]}, {c1.personality[1]}, {c1.personality[2]}\n" +
        f"occupation: {c1.occupation}\n" +
        f"aspiration: {c1.aspiration}")
    
    pass

@client.command()
async def load_character(ctx):
    print(ctx.author)
    pass

@client.command()
async def create_channel(ctx, channel_name):
    guild = ctx.guild
    channel = await guild.create_text_channel(channel_name)

    pass

@client.command(name="partyCreate")
async def party_create_characters(ctx):
    members = await get_members(ctx)
    for member in members:
        await create_character(ctx)
    if (len(members) > 1):
        await ctx.send(f"Ok delvers. It's time to take on your first challenge!")
    else:
        await ctx.send(f"Ok, delver. You must be pretty brave to take on this challenge alone. It's time for your first challenge.")
    pass

@client.command(name="getMembers")
async def get_members(ctx):
    for channel in ctx.guild.voice_channels:
        print(channel.id and channel.name)
        if channel.name == "the-tavern":
            channel_to_check = client.get_channel(channel.id)
            members = channel_to_check.members
            for member in members:
                print(member)
            return members
    
    pass

client.run(client.DISCORD_TOKEN)


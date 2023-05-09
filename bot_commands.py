#!/usr/local/bin/python3
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from DiscordUtilities import get_channel
from CharacterCreation import get_name_response, get_weapon_response, generate_character_traits, generate_personality
from Database import insert, select_characters, load_selected_character
from models.DatabaseTables import Player, Character
from models.Dungeon import Dungeon
from monster_factory import create_list_monsters, create_single_monster
# import requests

# base_url = "https://discord.com/oauth2/token"
# scope = "bot"
class PlayerCharacter():
    def __init__(self, player_name, character_name):
        self.player_name = player_name
        self.character_name = character_name
        pass

# class Token():
#     def __init__(self):
#         load_dotenv()
#         self.client_id = os.environ.get("CLIENT_ID")
#         self.permissions = os.environ.get("PERMISSIONS")
#         self.discord_token = os.environ.get("DISCORD_TOKEN")
#         request = requests.post(f"{base_url}client_id={self.client_id}&permissions={self.permissions}&scope={scope}").json()
#         print(request['access_token'])
#         self.token = request.access_tokens

class MyClient(commands.Bot, discord.Client):
    def __init__(self):
        load_dotenv()
        self.DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
        # self.DISCORD_TOKEN = Token().token
        intents = discord.Intents.default()
        intents.message_content = True
        self.characters = []
        self.dungeons = []

        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

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
async def fast_create_character(ctx):
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
    discord_name = str(ctx.message.author)
    await ctx.send(f"Great to meet ya, {characterName}! Let’s get you set up shall we? This process is called Evocation." + 
    f" To keep it simple, I’ll bring out from you your Delving self from your Spark, the Bits that gave you life. Here we go.\n\n" + 
    
    f"Your weapon of choice is the {weaponChoice}, I see it is {weaponElementChoice} as well." + 
    f" The Data flows around you as a {firstClass} and a {secondClass} it seems." + 
    f" For your defense, {armorChoice} will keep you safe.\n\n" + 
    
    f"Now, who are you… It seems your Code sings mostly of {personalityChoice[0]}, {personalityChoice[1]} and {personalityChoice[2]}." + 
    f" In the Hamlet you are a {occupationChoice} it would seem. But yes, deeper still, you yearn for… {aspirationChoice}." + 
    f" We all yearn for something. I hope you find yours.\n\n" + 

    f"Good luck out there. Don’t die okay?")
    c1 = []
    c1.append(characterName)
    c1.append(discord_name)
    c1.append(firstClass)
    c1.append(secondClass)
    c1.append(weaponChoice)
    c1.append(weaponElementChoice)
    c1.append(armorChoice)
    c1.append(personalityChoice)
    c1.append(occupationChoice)
    c1.append(aspirationChoice)
    p1 = []
    p1.append(discord_name)
    insert(p1, c1)
    await create_channel(ctx, characterName)
    channel = await get_channel(ctx, client, "text", characterName)
    new_character = PlayerCharacter(discord_name, characterName)
    client.characters.append(new_character)
    await channel.send(
        f"character name: {c1[0]}\n" + 
        f"first class: {c1[2]}\n" + 
        f"second class: {c1[3]}\n" + 
        f"weapon: {c1[4]}\n" +
        f"weapon element: {c1[5]}\n" +
        f"armor: {c1[6]}\n" + 
        f"personality: {c1[7][0]}, {c1[7][1]}, {c1[7][2]}\n" +
        f"occupation: {c1[8]}\n" +
        f"aspiration: {c1[9]}")
    pass

@client.command()
async def load_character_options(ctx):
    choices = []
    disc_name = str(ctx.message.author)
    characters = select_characters(disc_name)
    await ctx.send(f"Oi, you've played before would you like to use one of your characters? Here are your choices:")
    for character in characters:
        choices.append(character[0].char_name)
    await ctx.send('\n'.join(choices))
    pass

@client.command()
async def load_character(ctx, *, arg):
    disc_name = str(ctx.message.author)
    character = await load_selected_character(arg, disc_name)
    print(type(character))
    character = character[0]
    for attribute, value in character.__dict__.items():
        print(value)
    await ctx.send(f"You have loaded {character.char_name}")
    await create_channel(ctx, character.char_name)
    channel = await get_channel(ctx, client, "text", character.char_name)
    print(channel.name)
    new_character = PlayerCharacter(disc_name, character.char_name)
    client.characters.append(new_character)
    await channel.send(
        f"character name: {character.char_name}\n" + 
        f"first class: {character.first_class}\n" + 
        f"second class: {character.second_class}\n" + 
        f"weapon: {character.weapon}\n" +
        f"weapon element: {character.weapon_element}\n" +
        f"armor: {character.armor}\n" + 
        f"personality: {character.personality}\n" +
        f"occupation: {character.occupation}\n" +
        f"aspiration: {character.aspiration}")
    pass

@client.command()
async def create_channel(ctx, channel_name):
    guild = ctx.guild
    channel = await guild.create_text_channel(channel_name)
    pass

@client.command(name="endSession")
async def end_session(ctx):
    for char in client.characters:
        channel = await get_channel(ctx, client, "text", char.character_name)
        await channel.delete()
    client.characters.clear()
    await ctx.send("Thank you for playing!")

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

@client.command()
async def create_dungeon(ctx):
    dungeon = Dungeon(4)
    dungeon.room_mons = dungeon.populate_dungeon()
    client.dungeons.append(dungeon)
    await ctx.send(f"the first dungeon is {dungeon.biome}, each room will have this number of monsters: {dungeon.room_mons[0]}, {dungeon.room_mons[1]}, {dungeon.room_mons[2]}, {dungeon.room_mons[3]} and the size is {dungeon.size}")
    pass

@client.command()
async def first_room(ctx):
    dungeon = client.dungeons[len(client.dungeons) - 1]
    dungeon.room_mons[0] = 0
    dungeon.room_mons[1] = 0
    dungeon.room_mons[2] = 0
    dungeon.room_mons[3] = 0
    is_all_dead = False
    is_all_dead = all([ v == 0 for v in dungeon.room_mons ])
    if is_all_dead:
        client.dungeons.pop(len(client.dungeons) - 1)
        await ctx.send(f"You've cleared the {dungeon.biome} dungeon! Congratulations!")
    else:
        for mons in dungeon.room_mons:
            if mons != 0:
                room = mons
                break
        print(room)
        printing_monsters = []
        if room == 1:
            monster = create_single_monster(dungeon)
            await ctx.send(f"These are the monsters you're fighting!:")
            await ctx.send(monster.printMonster())
        else:
            monsters = create_list_monsters(dungeon, room)
            for enemy in monsters:
                printing_monsters.append(enemy.printMonster())
            await ctx.send(f"These are the monsters you're fighting!:")
            await ctx.send('\n'.join(printing_monsters))

client.run(client.DISCORD_TOKEN)

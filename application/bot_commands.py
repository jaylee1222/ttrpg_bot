#!/usr/local/bin/python3
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from DiscordUtilities import get_channel
from CharacterCreation import get_name_response, get_weapon_response, generate_character_traits, generate_personality, generate_speed, generate_class
from Database import insert, select_characters, load_selected_character, select_homes
from models.DatabaseTables import Player, Character
from models.Dungeon import Dungeon
from models.Monster import Monster
from dice import dungeon_dice_roll
from combat_utilities import check_player_health, get_attack_response
import yaml
from models.PlayerCharacter import PlayerCharacter
import sys
# import requests

# base_url = "https://discord.com/oauth2/token"
# scope = "bot"

# class Token():
#     def __init__(self):
#         load_dotenv()
#         API_ENDPOINT = 'https://discord.com/api/v10'
#         self.client_id = os.environ.get("CLIENT_ID")
#         self.client_secret = os.environ.get("CLIENT_SECRET")
#         # self.permissions = os.environ.get("PERMISSIONS")
#         # self.discord_token = os.environ.get("DISCORD_TOKEN")
#         data = {
#             'grant_type': 'client_credentials',
#             'scope': 'identify connections'
#         }
#         headers = {
#             'Content-Type': 'application/x-www-form-urlencoded'
#         }
#         request = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, auth=(self.client_id, self.client_secret))
#         print(request['access_token'])
#         self.token = request.access_token

class MyClient(commands.Bot, discord.Client):
    def __init__(self):
        load_dotenv()
        self.DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
        # self.DISCORD_TOKEN = Token().token
        intents = discord.Intents.default()
        intents.message_content = True
        self.characters = []
        self.dungeons = []
        self.dungeon_room = 0

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
    with open('character_creation.yml', 'r') as file:
        character_create_options = yaml.safe_load(file)
    weaponList = None
    weaponElementList = None
    classList = None
    armorList = None
    personalityList = None
    occupationList = None
    aspirationList = None
    weaponList = character_create_options['character_attributes']['weapons']
    weaponElementList = character_create_options['character_attributes']['weapon_elements']
    classList = character_create_options['character_attributes']['classes']
    armorList = character_create_options['character_attributes']['armor_types']
    personalityList = character_create_options['character_attributes']['personality_traits']
    occupationList = character_create_options['character_attributes']['occupations']
    aspirationList = character_create_options['character_attributes']['aspirations']
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
    firstClass = await generate_class(classList)
    secondClass = await generate_class(classList)
    armorChoice = await generate_character_traits(armorList)
    personalityChoice = await generate_personality(personalityList)
    occupationChoice = await generate_character_traits(occupationList)
    aspirationChoice = await generate_character_traits(aspirationList)
    split_choice = aspirationChoice.split()
    firstClassProperties = next((x for x in classList if x['name'] == firstClass), None)
    defenseChoice = next((x for x in armorList if x['name'] == armorChoice), None)
    damageChoice = next((x for x in weaponList if x['name'] == weaponChoice), None)
    speed = await generate_speed(firstClassProperties['speed'])
    defense = defenseChoice['defense']
    damage = damageChoice['damage']
    health = firstClassProperties['health']
    shortened_aspiration = split_choice[0].replace(".", "")
    discord_name = str(ctx.message.author)
    await ctx.send(f"Great to meet ya, {characterName}! Let’s get you set up shall we? This process is called Evocation." + 
    f" To keep it simple, I’ll bring out from you your Delving self from your Spark, the Bits that gave you life. Here we go.\n\n" + 
    
    f"Your weapon of choice is the {weaponChoice}, I see it is {weaponElementChoice} as well." + 
    f" The Data flows around you as a {firstClass} and a {secondClass} it seems." + 
    f" For your defense, {armorChoice} will keep you safe.\n\n" + 
    
    f"Now, who are you… It seems your Code sings mostly of {personalityChoice[0]}, {personalityChoice[1]} and {personalityChoice[2]}." + 
    f" In the Hamlet you are a {occupationChoice} it would seem. But yes, deeper still, you yearn for… {aspirationChoice}." + 
    f" We all yearn for someguy. I hope you find yours.\n\n" + 

    f"Good luck out there. Don’t die okay?")
    await ctx.send(f"You know...there's a space out on the edge of town...nobody is staying there and honestly. I just don't have space for you here." +
                   " This might be the perfect spot for you and your gang to call home! It's called 'The Farm'! You and your gang can rename it to" +
                   " whatever you would like.")
    # create logic that asks player for the house name and save it to the database
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
    c1.append(speed)
    c1.append(damage)
    c1.append(defense)
    c1.append(health)
    p1 = []
    p1.append(discord_name)
    insert(p1, c1)
    await create_channel(ctx, characterName)
    channel = await get_channel(ctx, client, "text", characterName)
    new_character = PlayerCharacter(discord_name, characterName, speed, damage, defense, health)
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
        f"aspiration: {c1[9]}\n" +
        f"speed: {c1[10]}\n" +
        f"damage: {c1[11]}\n" +
        f"defense: {c1[12]}\n" +
        f"health: {c1[13]}")
    pass

@client.command()
async def load_character_options(ctx):
    choices = []
    disc_name = str(ctx.message.author)
    characters = select_characters(disc_name)
    if (len(characters) <= 0):
        await ctx.send(f"Looks like you've never played before, hon...go instantiate yourself in the delves to see who you truly are!")
        return
    else:
        await ctx.send(f"Oi, you've played before would you like to use one of your characters? Here are your choices:")
    for character in characters:
        choices.append(character[0].char_name)
    await ctx.send('\n'.join(choices))
    pass

@client.command()
async def load_housing_options(ctx):
    choices = []
    disc_name = str(ctx.message.author)
    homes = await select_homes(disc_name)
    if (len(homes) <= 0):
        await ctx.send(f"Looks like you don't have a home here amongst the delves...you should try creating your own gang to be given a home amonst the delves")
        return
    else:
        await ctx.send("You've played before! Which house are you living in these days?")
    for home in homes:
        choices.append(home[0].home_name)
    await ctx.send('\n'.join(choices))
    pass

@client.command()
async def load_character(ctx, *, arg):
    disc_name = str(ctx.message.author)
    homes = []
    character = await load_selected_character(arg, disc_name)
    print(type(character))
    character = character[0]
    for attribute, value in character.__dict__.items():
        print(value)
    await ctx.send(f"You have loaded {character.char_name}")
    await create_channel(ctx, character.char_name)
    channel = await get_channel(ctx, client, "text", character.char_name)
    print(channel.name)
    new_character = PlayerCharacter(disc_name, character.char_name, character.speed, character.damage, character.defense, character.health)
    client.characters.append(new_character)
    homes = await select_homes(disc_name)
    print(f"These are homes: #{homes}")
    await channel.send(
        f"character name: {character.char_name}\n" + 
        f"first class: {character.first_class}\n" + 
        f"second class: {character.second_class}\n" + 
        f"weapon: {character.weapon}\n" +
        f"weapon element: {character.weapon_element}\n" +
        f"armor: {character.armor}\n" + 
        f"personality: {character.personality}\n" +
        f"occupation: {character.occupation}\n" +
        f"aspiration: {character.aspiration}\n" +
        f"speed: {character.speed}\n" +
        f"damage: {character.damage}\n" +
        f"defense: {character.defense}\n" +
        f"health: {character.health}")
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
    client.dungeons.clear()
    client.dungeon_room = 0
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
    dungeon = await Dungeon(4)
    client.dungeons.append(dungeon)
    await ctx.send(f"the first dungeon is {dungeon.biome}, each room will have this number of monsters: {dungeon.room_mons[0]}, {dungeon.room_mons[1]}, {dungeon.room_mons[2]}, {dungeon.room_mons[3]} and the size is {dungeon.size}")
    pass

@client.command()
async def next_room(ctx):
    dungeon = client.dungeons[len(client.dungeons) - 1]
    print(f"this is the fight mons: {dungeon.rooms[client.dungeon_room]}")
    if not dungeon.rooms[client.dungeon_room].monsters:
        dungeon.room_mons[client.dungeon_room] = 0
    print(f"this is the dungeon: {dungeon}")
    print(f"this is the room_mons: {all([ v == 0 for v in dungeon.room_mons ])}")
    is_all_dead = False
    is_all_dead = all([ v == 0 for v in dungeon.room_mons ])
    if is_all_dead:
        client.dungeons.pop(len(client.dungeons) - 1)
        await ctx.send(f"You've cleared the {dungeon.biome} dungeon! Congratulations!")
        return
    else:
        if dungeon.room_mons[client.dungeon_room] == 0:
            client.dungeon_room += 1
        printing_monsters = []
        await ctx.send(f"These are the monsters you're fighting!:")
        for monster in dungeon.rooms[client.dungeon_room].monsters:
            printing_monsters.append(monster.name)
        await ctx.send('\n'.join(printing_monsters))

@client.command()
async def start_combat(ctx):
    print("-----STARTING COMBAT----")
    players = client.characters
    mons = client.dungeons[len(client.dungeons) - 1].rooms[client.dungeon_room].monsters
    loot = client.dungeons[len(client.dungeons) - 1].rooms[client.dungeon_room].building_mat_loot
    combat_order = [*players, *mons]
    monster_names = []
    combat_order.sort(key=lambda x: int(x.speed), reverse=True)
    print("COMBAT ORDER:")
    print(str(combat_order))
    has_mons = True
    while has_mons:
        for guy in combat_order:
            print(f"this is inside the while loop: {guy}")
            print(f"this is the len of mons: {len(mons)}")
            if (len(mons) == 0):
                has_mons = False
                break
            if guy.health <= 0:
                if (isinstance(guy, Monster)):
                    print(f"skipping {guy.name}'s turn")
                if (isinstance(guy, PlayerCharacter)):
                    print(f"skpping {guy.character_name}'s turn")
                continue
            else:
                if isinstance(guy, Monster):
                    print(f"it is {guy.name}'s turn")
                    player = await check_player_health(players)
                    damage = await guy.attack(player)
                    player.health -= damage
                    await ctx.send(f"{guy.name} has attacked {player.character_name} for {damage} damage!")
                    # send to players how much health player has remaining this will allow players to know when to use items
                    # need to put item use and items into the game
                    if player.health < 0:
                        player.health = 0
                    if player.health == 0:
                        players.remove(player)
                        await ctx.send(f"Oh no! Your party number dwindles. {player.character_name} has fallen. {guy.name} has attacked {player} for {damage} damage!")
                elif isinstance(guy, PlayerCharacter):
                    monster_names.clear()
                    print(f"it is {guy.character_name}'s turn")
                    await ctx.send(f"The enemy awaits an attack! {guy.character_name} who would you like to attack?")
                    print(f"these are the mons {mons}")
                    for mon in mons:
                        monster_names.append(mon.name)
                    await ctx.send(f"\n".join(monster_names))
                    mon = await get_attack_response(client, ctx, monster_names)
                    monster = next((x for x in mons if x.name == mon), None)
                    print(f"{guy.character_name} is attacking {monster.name}")
                    damage = await guy.attack(monster)
                    monster.health = monster.health - damage
                    print(f"{monster.name}'s health is at {monster.health}")
                    await ctx.send(f"{guy.character_name} you attack {monster.name} for {damage} damage!")
                    if monster.health < 0:
                        monster.health = 0
                    if monster.health == 0:
                        print(f"{monster.name} has been killed with health: {monster.health}")
                        mons.remove(monster)
                        await ctx.send(f"You killed {monster.name}! This is a small win but keep your head in the fight!")
    await ctx.send(f"You've killed all of the monsters! You cleared the dungeon! You've been awarded {', '.join(str(item) for item in loot)}!")
    # give loot here
    # how will I keep track of the loot? database...
    # a player owns a base? a group owns a base?
    # when loot is earned by a group is automatically added to the base inventory
    # at the end of the dungeon list all of the loot gathered from all of the rooms
    client.dungeons[len(client.dungeons) - 1].rooms[client.dungeon_room].monsters = []

@client.command()
async def list_loot(ctx):
    with open('dungeon_loot.yml', 'r') as file:
        dungeon_loot = yaml.safe_load(file)
    biomes = ["common", "Enki", "Ahab", "Kirkjufell", "Air"]
        # print(f"{dungeon_loot[0]['house_materials']}")
    for biome in biomes:
        await ctx.send('\n'.join(dungeon_loot[biome]['house materials']))
        

# @client.command()
# async def draw_stables(ctx):
#     draw_square()

client.run(client.DISCORD_TOKEN)

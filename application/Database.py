# import sqlite3
from datetime import datetime
import sqlalchemy as db
from models.DatabaseTables import Player, Character, PlayerHome
from sqlalchemy import inspect, select, insert, create_engine, MetaData, and_
from sqlalchemy.orm import Session

def database_connection():
    engine = create_engine('sqlite:///ttrpg_bot.db', echo = True)
    PlayerHome.__table__.create(engine, checkfirst=True)
    Player.__table__.create(engine, checkfirst=True)
    Character.__table__.create(engine, checkfirst=True)

    return engine

def insert(person, character):
    traits = ', '.join(character[7])
    engine = database_connection()
    characterModel = Character(time_created = datetime.now(), char_name = character[0], first_class=character[2], second_class=character[3], weapon=character[4], weapon_element=character[5], armor=character[6], personality=traits, occupation=character[8], aspiration=character[9], speed=character[10], damage=character[11], defense=character[12], health=character[13])
    with Session(engine) as session:
        result = session.add(characterModel)
        session.commit()
        session.refresh(characterModel)
        print(f"id of the inserted row is {characterModel.char_id}")
    playerModel = Player(disc_name=person[0], character=characterModel.char_id)
    with Session(engine) as session:
        session.add(playerModel)
        session.commit()
        session.refresh(playerModel)
    player_home = PlayerHome(player_owner = playerModel.player_id, home_name = 'The Farm', gear_items = '')
    with Session(engine) as session:
        result = session.add(player_home)
        session.commit()

def select_characters(player):
    engine = database_connection()
    player_chars = []
    session = Session(engine)
    ids = select(Player).where(Player.disc_name == player)
    for id in session.scalars(ids):
        chars = select(Character).where(Character.char_id == id.player_id)
        char_info = session.execute(chars).fetchone()
        player_chars.append(char_info)
    return player_chars

async def select_homes(player):
    engine = database_connection()
    player_homes = []
    session = Session(engine)
    ids = select(Player).where(Player.disc_name == player)
    for id in session.scalars(ids):
        homes = select(PlayerHome).where(PlayerHome.home_id == id.player_id)
        home_info = session.execute(homes).fetchone()
        player_homes.append(home_info)
    return player_homes

async def load_selected_character(desired_char_name, player):
    engine = database_connection()
    statement = select(Character).where(Character.char_name == desired_char_name)
    with Session(engine) as session:
        char_info = session.execute(statement).fetchone()
        ids = select(Player).where(and_(Player.disc_name == player, Player.character == char_info[0].char_id))
        result = session.execute(ids)
        if result != None:
            print(f"this is from database: {type(char_info)}")
            return char_info
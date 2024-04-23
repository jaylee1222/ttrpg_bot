# import sqlite3
from datetime import datetime
import sqlalchemy as db
from models.DatabaseTables import Player, Character, PlayerHome, updatePlayerHome
from sqlalchemy import inspect, select, insert, create_engine, MetaData, and_, update
from sqlalchemy.orm import Session

def database_connection():
    engine = create_engine('sqlite:///ttrpg_bot.db', echo = True)
    PlayerHome.__table__.create(engine, checkfirst=True)
    Player.__table__.create(engine, checkfirst=True)
    Character.__table__.create(engine, checkfirst=True)

    return engine

def insert(person, character, home):
    traits = ', '.join(character[7])
    engine = database_connection()
    characterModel = Character(time_created = datetime.now(), char_name = character[0], first_class=character[2], second_class=character[3], weapon=character[4], weapon_element=character[5], armor=character[6], personality=traits, occupation=character[8], aspiration=character[9], speed=character[10], damage=character[11], defense=character[12], health=character[13])
    with Session(engine) as session:
        result = session.add(characterModel)
        session.commit()
        session.refresh(characterModel)
        print(f"id of the inserted row is {characterModel.char_id}")
    with Session(engine) as session:
        result = session.add(home)
        session.commit()
        session.refresh(home)
    playerModel = Player(disc_name=person[0], character=characterModel.char_id, playerHome=home.home_id)
    with Session(engine) as session:
        session.add(playerModel)
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
    home_statement = select(Player, PlayerHome).join(PlayerHome).where(Player.disc_name == player).order_by(Player.player_id, PlayerHome.home_id)
    with Session(engine) as session:
        home_info = session.execute(home_statement).fetchall()
        for player, home in home_info:
            player_homes.append(home)
    return player_homes

async def select_char_home(player, char):
    engine = database_connection()
    session = Session(engine)
    home_statement = select(Player, PlayerHome).join(PlayerHome).join(Character).where(Player.disc_name == player).where(Character.char_name == char).order_by(Player.player_id, PlayerHome.home_id)
    with Session(engine) as session:
        player, home = session.execute(home_statement).fetchone()
    return home

async def select_homes_on_home_name(home_name):
    engine = database_connection()
    player_homes = []
    session = Session(engine)
    home_statement = select(Player, PlayerHome).join(PlayerHome).where(PlayerHome.home_name == home_name).order_by(Player.player_id, PlayerHome.home_id)
    with Session(engine) as session:
        player, home = session.execute(home_statement).fetchone()
    return home

async def check_for_homes(home_name):
    engine = database_connection()
    player_homes = []
    session = Session(engine)
    home_statement = select(Player, PlayerHome).join(PlayerHome).where(PlayerHome.home_name == home_name).order_by(Player.player_id, PlayerHome.home_id)
    with Session(engine) as session:
        home_info = session.execute(home_statement).fetchall()
    if (len(home_info) > 0):
        return False

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
        
async def update_home(home, new_home_data, player):
    engine = database_connection()
    home_statement = select(Player, PlayerHome).join(PlayerHome).where(Player.disc_name == player)\
                    .where(PlayerHome.home_name == home)\
                    .order_by(Player.player_id, PlayerHome.home_id)
    with Session(engine) as session:
        returned_player, returned_home = session.execute(home_statement).fetchone()
        session.query(PlayerHome).filter(PlayerHome.home_id == returned_home.home_id).update(new_home_data)
        session.commit()
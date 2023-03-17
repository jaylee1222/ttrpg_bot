# import sqlite3
from datetime import datetime
import sqlalchemy as db
from Player import Player
from Character import Character
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import insert

def database_connection():
    engine = db.create_engine('sqlite:///ttrpg_bot.db', echo = True)
    connection = engine.connect(close_with_result=True)
    mymetadata = db.MetaData()
    Base = db.ext.declarative.declarative_base(metadata=mymetadata)
    characters = db.Table(
        "Characters", mymetadata,
        db.Column("char_id", db.Integer, primary_key=True),
        db.Column("time_created", db.DateTime),
        db.Column("char_name", db.String(25)),
        db.Column("first_class", db.String(25)),
        db.Column("second_class", db.String(25)),
        db.Column("weapon", db.String(25)),
        db.Column("weapon_element", db.String(25)),
        db.Column("armor", db.String(25)),
        db.Column("personality", db.String(50)),
        db.Column("occupation", db.String(25)),
        db.Column("aspiration", db.String(50))
    )

    players = db.Table(
        "Players", mymetadata,
        db.Column("player_id", db.Integer, primary_key=True),
        db.Column("disc_name", db.Integer()),
        db.Column("char_id", db.Integer, db.ForeignKey("Characters.char_id"))
    )
    mymetadata.create_all(engine, checkfirst= True)
    players_ins = players.insert()
    characters_ins = characters.insert()

    return engine

def insert(person, character):
    traits = ', '.join(character.personality)
    engine = database_connection()
    metadata = db.MetaData(bind=engine)
    db.MetaData.reflect(metadata)
    characters = metadata.tables['Characters']
    players = metadata.tables['Players']
    print(type(characters))
    characters_ins = db.insert(characters).values(time_created = datetime.now(), char_name = character.char_name, first_class = character.first_class, second_class = character.second_class, weapon = character.weapon, weapon_element = character.weapon_element, armor = character.armor, personality = traits, occupation = character.occupation, aspiration = character.aspiration)
    result = engine.execute(characters_ins)
    print(result)
    character_id = result.inserted_primary_key._asdict()
    players_ins = db.insert(players).values(disc_name = person.disc_name, char_id = character_id['char_id'])
    result = engine.execute(players_ins)
    print(result)

    s = select([players, characters]).where(players.c.char_id == characters.c.char_id)
    result = engine.execute(s)

    for row in result:
        print (row)
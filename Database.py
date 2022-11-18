# import sqlite3
import sqlalchemy as db
from Player import Player
from Character import Character
from sqlalchemy import inspect
from sqlalchemy import select

def database_connection(person, character):
    engine = db.create_engine('sqlite:///ttrpg_bot.db', echo = True)
    connection = engine.connect()
    print(type(character.personality))
    mymetadata = db.MetaData()
    Base = db.ext.declarative.declarative_base(metadata=mymetadata)
    characters = db.Table(
        "Characters", mymetadata,
        db.Column("char_id", db.Integer, primary_key=True),
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
    traits = ', '.join(character.personality)
    insp = inspect(Player)
    insp2 = inspect(Character)
    print(insp.all_orm_descriptors.keys())
    print(insp2.all_orm_descriptors.keys())
    print(Base.metadata)
    print(Player.__table__)
    print(Character.__table__)
    mymetadata.create_all(engine, checkfirst= True)
    print(vars(person))
    print(vars(character))
    players_ins = players.insert()
    characters_ins = characters.insert()
    characters_ins = characters.insert().values(char_name = character.char_name, first_class = character.first_class, second_class = character.second_class, weapon = character.weapon, weapon_element = character.weapon_element, armor = character.armor, personality = traits, occupation = character.occupation, aspiration = character.aspiration)
    result = connection.execute(characters_ins)
    print(result)
    character_id = result.inserted_primary_key._asdict()
    players_ins = players.insert().values(disc_name = person.disc_name, char_id = character_id['char_id'])
    result = connection.execute(players_ins)
    print(result)

    s = select([players, characters]).where(players.c.char_id == characters.c.char_id)
    result = connection.execute(s)

    for row in result:
        print (row)

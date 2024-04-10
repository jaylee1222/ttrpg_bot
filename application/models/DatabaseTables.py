from sqlalchemy import Integer, String, ForeignKey, create_engine, MetaData, DateTime, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from datetime import datetime

engine = create_engine('sqlite:///ttrpg_bot.db', echo = True)
metadata_obj = MetaData()

class Base(DeclarativeBase):
    metadata_obj = MetaData()

class PlayerHome(Base):
    __tablename__ = "PlayerHomes"
    metadata_obj
    home_id: Mapped[int] = mapped_column(primary_key=True)
    home_name: Mapped[str] = mapped_column(String(20))
    gear_items: Mapped[str] = mapped_column(String(999))
    wood: Mapped[int] = mapped_column(Integer)
    stone: Mapped[int] = mapped_column(Integer)
    raw_monster_meat: Mapped[int] = mapped_column(Integer)
    primordial_crystal: Mapped[int] = mapped_column(Integer)
    daisies: Mapped[int] = mapped_column(Integer)
    fire_crystal: Mapped[int] = mapped_column(Integer)
    fire_stone: Mapped[int] = mapped_column(Integer)
    flame_crysanthemum: Mapped[int] = mapped_column(Integer)
    flame_broiled_monster_liver: Mapped[int] = mapped_column(Integer)
    water_crystal: Mapped[int] = mapped_column(Integer)
    seaweed_covered_stone: Mapped[int] = mapped_column(Integer)
    driftwood: Mapped[int] = mapped_column(Integer)
    water_chestnut: Mapped[int] = mapped_column(Integer)
    raw_salmon: Mapped[int] = mapped_column(Integer)
    earth_crystal: Mapped[int] = mapped_column(Integer)
    moss_covered_stone: Mapped[int] = mapped_column(Integer)
    synthflower: Mapped[int] = mapped_column(Integer)
    carrot: Mapped[int] = mapped_column(Integer)
    sunflower: Mapped[int] = mapped_column(Integer)
    air_crystal: Mapped[int] = mapped_column(Integer)
    porous_stone: Mapped[int] = mapped_column(Integer)
    dandelion: Mapped[int] = mapped_column(Integer)
    cotton_candy: Mapped[int] = mapped_column(Integer)
    def __init__(self, home_name, gear_items = '', wood = 0, stone = 0, raw_monster_meat = 0, primordial_crystal = 0, daisies = 0, fire_crystal = 0, fire_stone = 0, 
                 flame_crysanthemum = 0, flame_broiled_monster_liver = 0, water_crystal = 0, seaweed_covered_stone = 0, driftwood = 0, water_chestnut = 0, raw_salmon = 0, 
                 earth_crystal = 0, moss_covered_stone = 0, synthflower = 0, carrot = 0, sunflower = 0, air_crystal = 0, porous_stone = 0, dandelion = 0, cotton_candy = 0):
        self.home_name = home_name
        self.gear_items = gear_items
        self.wood = wood
        self.stone = stone
        self.raw_monster_meat = raw_monster_meat
        self.primordial_crystal = primordial_crystal
        self.daisies = daisies
        self.fire_crystal = fire_crystal
        self.fire_stone = fire_stone
        self.flame_crysanthemum = flame_crysanthemum
        self.flame_broiled_monster_liver = flame_broiled_monster_liver
        self.water_crystal = water_crystal
        self.seaweed_covered_stone = seaweed_covered_stone
        self.driftwood = driftwood
        self.water_chestnut = water_chestnut
        self.raw_salmon = raw_salmon
        self.earth_crystal = earth_crystal
        self.moss_covered_stone = moss_covered_stone
        self.synthflower = synthflower
        self.carrot = carrot
        self.sunflower = sunflower
        self.air_crystal = air_crystal
        self.porous_stone = porous_stone
        self.dandelion = dandelion
        self.cotton_candy = cotton_candy

class Player(Base):
    __tablename__ = "Players"
    metadata_obj
    player_id: Mapped[int] = mapped_column(primary_key=True)
    disc_name: Mapped[str] = mapped_column(String(25))
    character: Mapped[int] = mapped_column(ForeignKey("Characters.char_id"))
    playerHome: Mapped[int] = mapped_column(ForeignKey("PlayerHomes.home_id"))
    def __init__(self, disc_name, character, playerHome):
        self.disc_name = disc_name
        self.character = character
        self.playerHome = playerHome

class Character(Base):
    __tablename__ = "Characters"
    metadata_obj
    char_id: Mapped[int] = mapped_column(primary_key=True)
    time_created: Mapped[datetime] = mapped_column(DateTime)
    char_name: Mapped[str] = mapped_column(String(25))
    first_class: Mapped[str] = mapped_column(String(25))
    second_class: Mapped[str] = mapped_column(String(25))
    weapon: Mapped[str] = mapped_column(String(25))
    weapon_element: Mapped[str] = mapped_column(String(25))
    armor: Mapped[str] = mapped_column(String(25))
    personality: Mapped[str] = mapped_column(String(40))
    occupation: Mapped[str] = mapped_column(String(25))
    aspiration: Mapped[str] = mapped_column(String(50))
    speed: Mapped[int] = mapped_column(Integer)
    damage: Mapped[int] = mapped_column(Integer)
    defense: Mapped[int] = mapped_column(Integer)
    health: Mapped[int] = mapped_column(Integer)
    def __init__(self, time_created, char_name, first_class, second_class, weapon, weapon_element, armor, personality, occupation, aspiration, speed, damage, defense, health):
        self.time_created = time_created
        self.char_name = char_name
        self.first_class = first_class
        self.second_class = second_class
        self.weapon = weapon
        self.weapon_element = weapon_element
        self.armor = armor
        self.personality = personality
        self.occupation = occupation
        self.aspiration = aspiration
        self.speed = speed
        self.damage = damage
        self.defense = defense
        self.health = health
    
Base.metadata_obj.create_all(engine, checkfirst=True)
        
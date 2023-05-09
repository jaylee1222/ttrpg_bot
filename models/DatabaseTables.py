from sqlalchemy import String, ForeignKey, create_engine, MetaData, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from datetime import datetime

engine = create_engine('sqlite:///ttrpg_bot.db', echo = True)
metadata_obj = MetaData()

class Base (DeclarativeBase):
    metadata_obj = MetaData()

class Player(Base):
    __tablename__ = "Players"
    metadata_obj
    player_id: Mapped[int] = mapped_column(primary_key=True)
    disc_name: Mapped[str] = mapped_column(String(25))
    character: Mapped[int] = mapped_column(ForeignKey("Characters.char_id"))
    def __init__(self, disc_name, character):
        self.disc_name = disc_name
        self.character = character

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
    def __init__(self, time_created, char_name, first_class, second_class, weapon, weapon_element, armor, personality, occupation, aspiration):
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
    
Base.metadata_obj.create_all(engine, checkfirst=True)
        
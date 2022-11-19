from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Character(Base):
    __tablename__ = "Characters"
    char_id = Column(Integer, primary_key=True)
    time_created = Column(DateTime)
    char_name = Column(String(25))
    disc_name = Column(Integer, ForeignKey('Players.player_id'))
    first_class = Column(String(25))
    second_class = Column(String(25))
    weapon = Column(String(25))
    weapon_element = Column(String(25))
    armor = Column(String(25))
    personality = Column(String(40))
    occupation = Column(String(25))
    aspiration = Column(String(50))

    # def __init__(self, char_name, disc_name, first_class, second_class, weapon, weapon_element, armor, personality, occupation, aspiration):
    #     self.char_name = char_name
    #     self.disc_name = disc_name
    #     self.first_class = first_class
    #     self.second_class = second_class
    #     self.weapon = weapon
    #     self.weapon_element = weapon_element
    #     self.armor = armor
    #     self.personality = personality
    #     self.occupation = occupation
    #     self.aspiration = aspiration
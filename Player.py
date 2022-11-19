from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from Character import Character

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Player(Base):
    __tablename__ = "Players"
    player_id = Column(Integer, primary_key=True)
    disc_name = Column(String(25))
    char_id = Column(Integer, ForeignKey("Characters.char_id"))
    
    
    # def __init__(self, disc_name, char_name):
    #     self.disc_name = disc_name
    #     self.char_name = char_name
        
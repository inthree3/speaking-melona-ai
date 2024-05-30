from sqlalchemy import Column, Integer, String
from .database import Base
from pydantic import BaseModel

class Character(Base):
  __tablename__ = "characters"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  barcode = Column(String, unique=True)
  prompt = Column(String)
  image = Column(String)

  
class Item(BaseModel):
  characters: list
  persona: dict
  ending: str
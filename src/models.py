from sqlalchemy import ARRAY, Column, Integer, String
from .database import Base
from pydantic import BaseModel

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    barcodes = Column(ARRAY(String), nullable=False)
    prompt = Column(String, nullable=True)
    image = Column(String, nullable=True)

  
class Item(BaseModel):
  characters: list
  persona: dict
  ending: str

class StoryGeneratorInput(BaseModel):
  barcodes: list[str]
  
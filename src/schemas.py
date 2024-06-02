from pydantic import BaseModel

class CharacterBase(BaseModel):
  name: str
  barcode: str
  prompt: str
  image: str

class CharacterCreate(CharacterBase):
  pass

class Character(CharacterBase):
  id: int

  class Config:
    orm_mode = True

    
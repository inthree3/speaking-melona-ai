from sqlalchemy.orm import Session
from . import models, schemas

def get_character(db: Session, barcode: str):
  return db.query(models.Character).filter(models.Character.barcode == barcode).first()

def create_character(db: Session, character: schemas.CharacterCreate):
  db_character = models.Character(barcode=character.barcode, name=character.name, prompt=character.prompt, image=character.image)
  db.add(db_character)
  db.commit()
  db.refresh(db_character)
  return db_character
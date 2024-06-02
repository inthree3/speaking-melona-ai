from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import array
from . import models, schemas

def get_characters(db: Session, skip: int, limit: int):
    return db.query(models.Character).offset(skip).limit(limit).all()

def get_character(db: Session, barcode: str):
    return db.query(models.Character).filter(models.Character.barcodes.contains([barcode])).first()

def create_character(db: Session, character: schemas.CharacterCreate):
    db_character = db.query(models.Character).filter(models.Character.barcodes.contains([character.barcodes[0]])).first()
    if db_character:
        db_character.name = character.name
        db_character.prompt = character.prompt
        db_character.image = character.image
        db_character.barcodes = character.barcodes
    else:
        db_character = models.Character(
            barcodes=character.barcodes, 
            name=character.name, 
            prompt=character.prompt, 
            image=character.image
        )
        db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character

def add_barcode_to_character(db: Session, character_id: int, barcode: str):
    db_character = db.query(models.Character).filter(models.Character.id == character_id).first()
    if db_character:
        if barcode not in db_character.barcodes:
            db_character.barcodes.append(barcode)
            db.commit()
            db.refresh(db_character)
    return db_character

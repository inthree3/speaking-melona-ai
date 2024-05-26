from sqlalchemy.orm import Session
from . import models, schemas

def get_character(db: Session, barcode: str):
  return db.query(models.Character).filter(models.Character.barcode == barcode).first()
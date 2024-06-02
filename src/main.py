# %%
from functools import lru_cache
import config
from . import generate_story
from dotenv import load_dotenv
import uvicorn
from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, HTTPException

from . import crud, models, schemas
from .database import SessionLocal, engine
from X_bot import create_tweet

load_dotenv(override=True)
# %%
models.Base.metadata.create_all(bind=engine)

app=FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache
def get_settings():
    return config.Settings()


@app.get('/')
async def root():
    return {"message": "Hello speaking-melona"}


@app.get('/character/{barcode}', response_model=schemas.Character)
def read_character(barcode: str, db: Session = Depends(get_db)):
    db_character = crud.get_character(db, barcode=barcode)
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return db_character


@app.post('/character', response_model=schemas.Character)
def create_character(character: schemas.CharacterCreate, db: Session = Depends(get_db)):
    return crud.create_character(db=db, character=character)


@app.post('/generate_drama_plot')
def story(barcodes: list[str], db: Session = Depends(get_db)):
    character_persona_pairs = []
    for barcode in barcodes:
        character_persona_pairs.append(crud.get_character(db, barcode=barcode))

    characters = map(lambda x: x.name, character_persona_pairs)

    try:
        personas = {character.name: character.prompt for character in character_persona_pairs}
    except:
        raise HTTPException(status_code=404, detail="Character not found")

    item = {
        "characters": characters,
        "persona": personas,
        "ending": "",
    }

    return generate_story.generate_drama_plot(item)

@app.post('/X_upload')
def upload_X(content: str):
    create_tweet(content)
    return {"message": "Tweet sent! \n Content: " + content}
# %%
# if __name__=="__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
# # %%

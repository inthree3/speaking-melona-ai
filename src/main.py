from functools import lru_cache
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from dotenv import load_dotenv
import config
from . import generate_story
from . import X_bot
from . import utils
import httpx
import json

load_dotenv(override=True)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@lru_cache
def get_settings():
    return config.Settings()

# Set up CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",  # Add the URLs you want to allow
    "https://melona.chat",  # Example of a production domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get('/')
async def root():
    return {"message": "Hello speaking-melona"}

@app.get('/characters', response_model=list[schemas.Character])
def read_characters(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    characters = crud.get_characters(db, skip=skip, limit=limit)
    return characters

@app.get('/character/{barcode}', response_model=schemas.Character)
def read_character(barcode: str, db: Session = Depends(get_db)):
    db_character = crud.get_character(db, barcode=barcode)
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return db_character

@app.post('/character', response_model=schemas.Character)
def create_character(character: schemas.CharacterCreate, db: Session = Depends(get_db)):
    return crud.create_character(db=db, character=character)

@app.post('/character/{character_id}/add_barcode', response_model=schemas.Character)
def add_barcode_to_character(character_id: int, barcode: str, db: Session = Depends(get_db)):
    db_character = crud.add_barcode_to_character(db=db, character_id=character_id, barcode=barcode)
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found or barcode already exists")
    return db_character

@app.post('/generate_drama_plot')
def story(body: models.StoryGeneratorInput, db: Session = Depends(get_db)):
    character_persona_pairs = []
    for barcode in body.barcodes:
        character = crud.get_character(db, barcode=barcode)
        if character is not None:
            character_persona_pairs.append(character)

    characters = list(map(lambda x: x.name, character_persona_pairs))

    if len(character_persona_pairs) == 0:
        raise HTTPException(status_code=404, detail="Character not found")

    try:
        personas = {character.name: character.prompt for character in character_persona_pairs}
    except:
        raise HTTPException(status_code=404, detail="Character not found")

    item = {
        "characters": characters,
        "persona": personas,
        "ending": "",
    }

    story = generate_story.generate_drama_plot(item)

    for 캐릭터 in story["캐릭터"]:
        캐릭터["이미지"] = character_persona_pairs[characters.index(캐릭터["이름"])].image

    tweets = utils.format_for_twitter(story)

    X_bot.post_tweet_thread(tweets)

    return story

@app.post('/X_upload')
def upload_X(content: str):
    print(content)
    X_bot.create_tweet(content)
    return {"message": "Tweet sent! \n Content: " + content}

@app.post('/request')
async def request(barcode: str, content: str):
    async with httpx.AsyncClient() as client:
        r = await client.post("https://hooks.slack.com/workflows/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", data=json.dumps({"email": barcode, "result": content}))
        print(r.text)

    return {"message": "Request received! \n Content: " + content}

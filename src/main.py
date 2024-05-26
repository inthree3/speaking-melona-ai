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

@app.post('/generate_story')
def story(body: dict):
    barcodes = body.get('barcodes', [])
    return generate_story.generate_message(barcodes)
# %%
# %%
# if __name__=="__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
# # %%

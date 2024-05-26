# %%
from functools import lru_cache
import config
import generate_story
from dotenv import load_dotenv
import uvicorn

from fastapi import FastAPI

from . import crud, models, schemas
from .database import SessionLocal, engine

load_dotenv(override=True)
# %%
models.Base.metadata.create_all(bind=engine)

app=FastAPI()

@lru_cache
def get_settings():
    return config.Settings()

@app.get('/')
async def root():
    return {"message": "Hello speaking-melona"}

@app.post('/generate_story')
def story(body: dict):
    barcodes = body.get('barcodes', [])
    return generate_story.generate_message(barcodes)
# %%
# %%
if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
# %%

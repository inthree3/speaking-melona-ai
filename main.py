# %%
from functools import lru_cache
import config
from src import generate_story
from dotenv import load_dotenv
import uvicorn

from fastapi import FastAPI
from pyngrok import ngrok
load_dotenv(override=True)
# %%
app=FastAPI()

@lru_cache
def get_settings():
    return config.Settings()

@app.get('/')
async def root():
    return {"message": "Hello speaking-melona"}

@app.post('/generate_story')
def story(characters: list[str], persona: dict[str], ending: str):
    return generate_story.generate_message(characters, persona, ending)
# %%
# %%
if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
# %%

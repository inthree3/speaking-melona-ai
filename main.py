# %%
from functools import lru_cache
import config
import generate_story
from dotenv import load_dotenv
import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel
from pyngrok import ngrok
load_dotenv(override=True)
# %%
app=FastAPI()

class Item(BaseModel):
    characters: list
    persona: dict
    ending: str

@lru_cache
def get_settings():
    return config.Settings()

@app.get('/')
async def root():
    return {"message": "Hello speaking-melona"}

@app.post('/generate_drama_plot')
def story(item: Item):
    return item, type(item)
    return generate_story.generate_drama_plot(item)

# %%
if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
# %%

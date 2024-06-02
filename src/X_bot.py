# %%
import tweepy
import os
from dotenv import load_dotenv
import tweepy.list

load_dotenv(override=True)
# %%
X_API_KEY=os.getenv("X_API_KEY")
X_API_KEY_SECRET=os.getenv("X_API_KEY_SECRET")
ACCESS_TOKEN=os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET=os.getenv("ACCESS_TOKEN_SECRET")
# %%
print(X_API_KEY)
print(X_API_KEY_SECRET)
print(ACCESS_TOKEN)
print(ACCESS_TOKEN_SECRET)
# %%
client = tweepy.Client(
    consumer_key=X_API_KEY,
    consumer_secret=X_API_KEY_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)
# %%
def create_tweet(text):
    return client.create_tweet(text)
# %%
client.create_tweet(text="TEST TWEET")

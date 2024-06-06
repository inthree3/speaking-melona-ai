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
client = tweepy.Client(
    consumer_key=X_API_KEY,
    consumer_secret=X_API_KEY_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)
# %%
def create_tweet(text, in_reply_to_status_id=None):
    print(f"Creating tweet: {text}")
    return client.create_tweet(text=text, in_reply_to_tweet_id=in_reply_to_status_id)

def post_tweet_thread(tweets):
    prev_tweet_id = None
    for tweet in tweets:
        status = create_tweet(text=tweet, in_reply_to_status_id=prev_tweet_id)
        prev_tweet_id = status.data['id']

import csv
import json
import os
import re
import tweepy
from dotenv import load_dotenv

# Load .env variables
load_dotenv('twitter.env')
CONSUMER_API = os.getenv('CONSUMER_API')
CONSUMER_API_SECRET = os.getenv('CONSUMER_API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Twitter API setup
auth = tweepy.OAuthHandler(CONSUMER_API, CONSUMER_API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Load tweet store
with open('data/tweets_raw.json') as f:
    tweets_data: dict = json.load(f)
    tweets = {}
    racist, not_racist = 0, 0
    for k, v in tweets_data.items():
        if v and racist < 10000:
            racist += 1
            tweets[k] = v
        elif not v and not_racist < 10000:
            not_racist += 1
            tweets[k] = v
# Batch get tweet text
tweet_ids = list(tweets.keys())
with open('data/tweets.csv', 'a', newline='\n', encoding='utf-8') as f:
    w = csv.writer(f, dialect='excel')
    for i in range(0, len(tweet_ids), 100):
        chunk = tweet_ids[i:i + 100]
        res = api.statuses_lookup(chunk)
        for tweet in res:
            try:
                w.writerow([str(tweet.text), tweets[tweet.id_str]])
            except Exception as e:
                print(e)
        print(min(len(tweet_ids), i + 100), 'tweets processed...')

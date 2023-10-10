import tweepy
import configparser
import json
import pandas as pd
import os 

# Get the directory of your script
script_dir = os.path.dirname(__file__)

# Form a relative path to the config.ini file
config_path = os.path.join(script_dir, 'config.ini')

#Read configs 
config = configparser.ConfigParser()
config.read(config_path)

api_key = config.get('twitter','api_key')
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

#Athentication 
auth = tweepy.OAuthHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()

#My Hastag of interest
hashtag = 'Liverpool'

# Retrieving the latest tweet with my hastag
tweets = tweepy.Cursor(api.search, q=f'#{hashtag}', lang='en').items(1)

tweet_data = []

for tweet in tweets:
    tweet_info = {
        'Timestamp': tweet.created_at,
        'Content': tweet.text,
        'Username': tweet.user.screen_name,
        'Retweets': tweet.retweet_count,
        'Favorites': tweet.favorite_count,
        'Hashtags': [hashtag['text'] for hashtag in tweet.entities['hashtags']]
    }
    tweet_data.append(tweet_info)

# Saving the latest tweet as JSON for field analysis
with open('latest_tweet.json', 'w') as json_file:
    json.dump(tweet_data, json_file, indent=4)

#CSV Store
df = pd.DataFrame(tweet_data)
df.to_csv('sample_tweet.csv', index=False)
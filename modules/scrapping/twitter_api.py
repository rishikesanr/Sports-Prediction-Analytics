import tweepy
import configparser

#Read configs 
config = configparser.ConfigParser()
config.read('./config.ini')
print("Are you here???")
api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

print(api_key)


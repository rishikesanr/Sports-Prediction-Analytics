import os
import time
from connectors.mongodb import MongoDB
from utils import constants as const
from datetime import datetime, timedelta
from pymongo import MongoClient
import praw
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

class RedditScraper:
    def __init__(self, league_name, match):
        self.league_name = league_name
        self.match = match
        self.db_name = league_name
        self.collection_name = f"{match.lower().replace(' ','-')}-{datetime.now().date()}"
        self.mongo = MongoDB(self.db_name, self.collection_name)
        self.client, self.db, self.collection = self.mongo.connect()
        load_dotenv()
        self.reddit = praw.Reddit(user_agent=os.getenv('USER_AGENT'),
                                  client_id=os.getenv('CLIENT_ID'),
                                  client_secret=os.getenv('CLIENT_SECRET'),
                                  username=os.getenv('USERNAME'),
                                  password=os.getenv('PASSWORD'))
        self.subreddit = self.reddit.subreddit(self.league_name)

    def scrape(self):
        keywords = [team.lower() for team in self.match.split(' vs ')]
        time_ago = (datetime.now() - timedelta(days=const.SCRAPING_TIMEFRAME_IN_DAYS)).timestamp()
        for post in self.subreddit.new(limit=const.NEW_POST_LIMIT):
            if post.created_utc < time_ago:
                break
            title = post.title.lower()
            if any(key in title for key in keywords):
                time.sleep(const.SLEEP_TIME_IN_SEC)
                post_obj = self.reddit.submission(id=post.id)
                title = post_obj.title
                description = post_obj.selftext
                post_obj.comments.replace_more(limit=None)
                comments = []
                for comment in post_obj.comments.list():
                    comments.append(comment.body)
                data = {
                    "title": title,
                    "description": description,
                    "comments": comments,
                    "source": "reddit",
                    "time": post.created_utc
                }
                
                doc_insert = self.collection.insert_one(data)



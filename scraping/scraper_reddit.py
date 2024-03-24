import os
import time
from connectors.mongodb import MongoDB
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
        self.subreddit = self.reddit.subreddit(league_name)

    def scrape(self):
        keywords = [team.lower() for team in self.match.split(' vs ')]
        three_days_ago = (datetime.now() - timedelta(days=3)).timestamp()
        for post in self.subreddit.new(limit=300):
            if post.created_utc < three_days_ago:
                break
            title = post.title.lower()
            if any(key in title for key in keywords):
                time.sleep(5)
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



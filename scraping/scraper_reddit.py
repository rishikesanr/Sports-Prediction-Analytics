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
import re
import pytz

class RedditScraper:
    def __init__(self, league_name, match,match_date_time):
        self.league_name = league_name
        self.match = match
        self.db_name = league_name
        self.match_date = re.findall(r'(\d{4}-\d{2}-\d{2})',match_date_time)[0]
        self.match_date_time = datetime.strptime(match_date_time, '%Y-%m-%d %H:%M:%S')
        self.collection_name = f"{match.lower().replace(' ','-')}-{self.match_date}"
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

        # local_tz = pytz.timezone("America/Los_Angeles")  # Replace with your local timezone, e.g., 'America/New_York'
        
        # Localize the match_date_time to the local timezone and then convert to UTC
        # local_match_date_time = local_tz.localize(self.match_date_time)
        utc_match_date_time = self.match_date_time.astimezone(pytz.utc)
        
        # Get the current time in UTC
        now = datetime.now(pytz.utc)
        # now = datetime.now()
        
        # Compare match_date_time with now
        if utc_match_date_time > now:
            # If match_date_time is in the future, use now
            target_time = now - timedelta(days=const.SCRAPING_TIMEFRAME_IN_DAYS)
        else:
            # If match_date_time is in the past, use match_date_time
            target_time = utc_match_date_time - timedelta(days=const.SCRAPING_TIMEFRAME_IN_DAYS)
        
        # Convert target_time to timestamp
        time_ago = target_time.timestamp()
        # time_ago = (datetime.now() - timedelta(days=const.SCRAPING_TIMEFRAME_IN_DAYS)).timestamp()
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



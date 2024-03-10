import praw
import json
import configparser
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os


load_dotenv()

reddit = praw.Reddit(user_agent=os.getenv('USER_AGENT'),
                     client_id=os.getenv('CLIENT_ID'),
                     client_secret=os.getenv('CLIENT_SECRET'),
                     username=os.getenv('USERNAME'),
                     password=os.getenv('PASSWORD'))

subreddit = reddit.subreddit("PremierLeague")

#Define the match here 
match = "Liverpool vs Manchester City" #This will be an input from the user through main, TBU 
teams = [team.lower() for team in match.split(' vs ')]

#Get the current time and subtract 3 days from it, as we'll only be scraping the last 3 days of data
three_days_ago = (datetime.now() - timedelta(days=3)).timestamp()

#Create a dictionary to store all the data
data = {}

#Get the posts
for submission in subreddit.new(limit=100):  #For now, we'll only be scraping the last 100 posts
    if submission.created_utc < three_days_ago:
        break  #If the post is older than 3 days, stop scraping
    title = submission.title.lower()
    if any(team in title for team in teams):
        time.sleep(5)  # sleep for 5 seconds to avoid hitting the API too hard
        post = reddit.submission(id=submission.id)

        #Get the post's title and description
        post_title = post.title
        post_selftext = post.selftext

        #Now get the comments
        comments = []
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            comments.append(comment.body)

        #Add the post's data to the dictionary
        data[post_title] = {
            "description": post_selftext,
            "comments": comments
        }

#Now save the data to a JSON file
''' 
A sample of this data is also available in the repository for reference.
Please note that they only seem to contain a general discussion about football, 
and not containing any personally identifiable information or sensitive data 
about the users as far as I can tell from using the API, with only its title and comments.
'''       
with open('test_sample.json', 'w') as f:
    json.dump(data, f)
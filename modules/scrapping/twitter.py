import pandas as pd 
from tqdm.notebook import tqdm
import snscrape.modules.twitter as sntwitter

####################
## Test Data 
####################

#Pulling sample data from twitter under the hashtag 
scrapper = sntwitter.TwitterSearchScraper("#Liverpool")

#### ** IMPORTANT ** ####
#### Code not working from here 
#### due to the latest takeover of X from Twitter.
#### The API connections are not open anymore 

tweets = []
for tweet in scrapper.get_items():
    break

for i, tweet in enumerate(scrapper.get_items()):
    data =[
        tweet.date,
        tweet.id,
        tweet.content,
        tweet.user.username,
        tweet.retweetCount,
        tweet.likeCount,
    ]

    tweets.append(data)
    if i>50: #Pulling only 50 tweets 
        break 
print("\nAre you here as well?")
sample_data = pd.DataFrame(tweets,columns=["date","id","content","usernmame","retweet","like"])

#Storing it in the csv file 
sample_data.to_csv("./sample.csv")
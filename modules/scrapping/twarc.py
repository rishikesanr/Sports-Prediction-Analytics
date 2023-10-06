import twarc
import pandas as pd

# Set the hashtag to scrape
hashtag = "Liverpool"

# Create a Twarc client
twarc_client = twarc.Twarc()

# Search for tweets containing the hashtag
tweets = twarc_client.search(q=hashtag, count=50)

# Create a Pandas DataFrame to store the data
df = pd.DataFrame(columns=["username", "tweet_text", "likes", "retweets", "created_at"])

# Iterate through the tweets and add them to the DataFrame
for tweet in tweets:
    df = df.append({
        "username": tweet.user.screen_name,
        "tweet_text": tweet.full_text,
        "likes": tweet.favorite_count,
        "retweets": tweet.retweet_count,
        "created_at": tweet.created_at
    }, ignore_index=True)

# Save the DataFrame to a CSV file
df.to_csv("liverpool_tweets.csv", index=False)

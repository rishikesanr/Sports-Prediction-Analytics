import argparse
from scraping.scraper_reddit import RedditScraper
from scraping.scraper_results import match_results
from processing.reddit_processor import RedditProcessor
from analytics.bagofwords import BagOfWords
from analytics.textblob_sentiment import TextBlobSentiment
from analytics.bert_sentiment import BertSentiment
from connectors.postgresql import PostgreSQL
from utils.credentials import sentiment_pg_credentials


def run_sentiment_analysis(db_name, collection_name, match_date_time, skip_scraping=False):
    if not skip_scraping:
        # Scrape data from Reddit
        scraper = RedditScraper(db_name, collection_name, match_date_time)
        scraper.scrape()

    # Process the scraped data
    processor = RedditProcessor(db_name, collection_name, match_date_time)
    data_fans = processor.process_data(collection_name)

    # Add debug print to check the structure
    print(data_fans.head())

    if 'message' not in data_fans.columns:
        raise ValueError("The 'message' column is missing from the processed data. Check the transformation logic.")

    # Analyze using the custom bag of words method
    bag_of_words = BagOfWords()
    sentiment_props_bow = bag_of_words.analyze(data_fans)
    print(sentiment_props_bow)

    # Analyze using textblob data
    textblob = TextBlobSentiment()
    textblob_sentiment_summary = textblob.analyze(data_fans)
    print(textblob_sentiment_summary)

    # Analyze the processed data using BERT Sentiment
    bert_sentiment = BertSentiment()
    bert_sentiment_summary = bert_sentiment.analyze(data_fans)
    print("BERT Sentiment Analysis Results:")
    print(bert_sentiment_summary)

    match_result, scoreline = match_results(collection_name, match_date_time)
    print(f"Match Result: {match_result}, Scoreline: {scoreline}")

    # Insert results into PostgreSQL
    db = PostgreSQL(**sentiment_pg_credentials,
                    league=db_name, 
                    match=collection_name,
                    match_datetime=match_date_time,
                    match_result=match_result,
                    match_scoreline=scoreline)
    db.connect()
    db.insert_data(sentiment_props_bow, 'BagOfWords')
    db.insert_data(textblob_sentiment_summary, 'TextBlob')
    db.insert_data(bert_sentiment_summary, 'Bert')
    db.close()


    return sentiment_props_bow, textblob_sentiment_summary, bert_sentiment_summary, match_result, scoreline


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Welcome to sports Prediction. Please provide the following arguments to get started. \
                                     Check the docs for more information')
    parser.add_argument('db_name', help='Name of the League in Reddit')
    parser.add_argument('collection_name', help='Match Details (Example: "Liverpool vs United")')
    parser.add_argument('match_date_time', help='Date and Time of the match as per UTC (Example: "2021-10-24T16:30:00Z"')
    parser.add_argument('--skip_scraping', action='store_true', help='Skip the scraping step if data already exists')

    args = parser.parse_args()

    run_sentiment_analysis(args.db_name, args.collection_name, args.match_date_time, args.skip_scraping)
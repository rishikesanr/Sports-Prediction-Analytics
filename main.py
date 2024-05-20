import argparse
from scraping.scraper_reddit import RedditScraper
from processing.reddit_processor import RedditProcessor
from analytics.bagofwords import BagOfWords

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Welcome to sports Prediction. Please provide the following arguments to get started. \
                                     Check the docs for more information')
    parser.add_argument('db_name', help='Name of the MongoDB database')
    parser.add_argument('collection_name', help='Match Details (Example: "Liverpool vs United")')
    parser.add_argument('--skip_scraping', action='store_true', help='Skip the scraping step if data already exists')

    args = parser.parse_args()

    if not args.skip_scraping:
        # Scrape data from Reddit
        scraper = RedditScraper(args.db_name, args.collection_name)
        scraper.scrape()

    # Process the scraped data
    processor = RedditProcessor(args.db_name, args.collection_name)
    data_fans = processor.process_data(args.collection_name)

    # Add debug print to check the structure
    print(data_fans.head())

    if 'message' not in data_fans.columns:
        raise ValueError("The 'message' column is missing from the processed data. Check the transformation logic.")

    # Analyze the processed data
    bag_of_words = BagOfWords()
    sentiment_props = bag_of_words.analyze(data_fans)

    print(sentiment_props)

import argparse
from scraping.scraper_reddit import RedditScraper

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Welcome to sports Prediction. Please provide the following arguments to get started. \
                                     Check the docs for more information')
    parser.add_argument('league', help='Name of the league')
    parser.add_argument('match', 
                        help='Match Details (Example: "Liverpool vs United")'
                        )

    args = parser.parse_args()

    scraper = RedditScraper(args.league, args.match)
    scraper.scrape()
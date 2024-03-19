import argparse
from scraping.scraper_reddit import RedditScraper

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape Reddit for a specific match in a league.')
    parser.add_argument('--league', required=True, help='Name of the league (Must have a subreddit)')
    parser.add_argument('--match', 
                        required=True, 
                        help='Match to scrape data for(Should describe each team with a single word. Example: "Liverpool vs United")'
                        )

    args = parser.parse_args()

    scraper = RedditScraper(args.league, args.match)
    scraper.scrape()
import argparse
from scrapers.scraper_reddit import RedditWebsiteScraper

def main(url):
    custom_website_scraper = RedditWebsiteScraper(url)
    custom_website_scraper.scrape_with_beautiful_soup()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape a website.')
    parser.add_argument('url', help='The URL of the website to scrape')
    args = parser.parse_args()
    main(args.url)
from bs4 import BeautifulSoup
from .scraper import WebsiteScraper
import requests

class RedditWebsiteScraper(WebsiteScraper):
    def scrape_with_beautiful_soup(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')




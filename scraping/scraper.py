from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time 

class WebsiteScraper:
    def __init__(self, url):
        self.url = url

    #Add a input timeframe function for all the connectors (** IMPORTANT **)
    def get_timeframe(self):
        '''
        '''

    def scrape_with_beautiful_soup(self):
        '''
        Scrap with Beautiful Soup
        '''
        #Sleep for 5 seconds to avoid getting blocked
        self.delay(5)

        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')

    def scrape_with_selenium(self):
        '''
        Scrap with Selenium
        '''
        driver = webdriver.Chrome()
        driver.get(self.url)

    def scrape_with_api(self):
        '''
        Scrap with API'''
        pass

    def delay(self,seconds):
        '''
        Delay requests by seconds
        '''
        time.sleep(seconds)
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def scrap_espn():
    '''
    Function to scrap data from ESPN.
    '''
    # Scraping from ESPN 
    
    match = "Liverpool vs Chelsea" 
    
    #Create a driver object for the chrome 
    driver = webdriver.Chrome()
    
    #We'll wait for 5 sec before sending each request
    
    #Go to ebay.com
    time.sleep(5)
    driver.get('https://espn.com/')
    
    #search for "Cell Phones"
    time.sleep(5)
    search = driver.find_element(By.CSS_SELECTOR,'a[id="global-search-trigger"]')
    search.click()
    
    time.sleep(5)
    input=driver.find_element(By.CSS_SELECTOR,'input[id="global-search-input"]')
    input.send_keys(f'{match} \n')
    
    #Click the articles filter
    time.sleep(5)
    articles = driver.find_element(By.XPATH, '//a[text()="Articles" and @data-track-filtername="articles"]')
    articles.click()

scrap_espn()
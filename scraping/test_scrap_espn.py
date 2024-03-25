from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def scrape_espn(match,collection):
    '''
    Function to scrape data from ESPN.
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

    #Check for the recent articles based on similar timeframe as reddit, default: 3 days
    #li.class_='time-elapsed', re.compile(r'(\d{1,24}h|[1-3]d)',li.text)

    #Get the page source 
    page_html = driver.page_source
    
    soup = BeautifulSoup(page_html,'html.parser')

    #Just take the first article for now. This will be ideally done based on the timeframe given gloabally i.e for both reddit and espn. 
    article_url="https://www.espn.com"+soup.find_all('ul',class_='article__Results')[0].find_all('a')[0].get('href')
    
    time.sleep(5)
    page_article = requests.get(article_url, headers = {'User-agent': 'Mozilla/5.0'})
    soup_article = BeautifulSoup(page_article.content,'html.parser')

    #Title of the article 
    title = soup_article.find_all('h1')[0].text

    #Description of the article
    description=""
    for p in range(len(soup_article.find_all('p'))):
        description+=soup_article.find_all('p')[p].text

    #Timestamp of the published article
    article_time = soup_article.find_all('span',class_='timestamp')[-2].text


    #Add the article's data to the dictionary
    data = {}
    data = {
        "title":title, #Title of the article 
        "description": description, # Description of the article
        "source": "espn",
        "time": article_time
    }
    print("Sample Article Document shown below:\n")
    print(data)
    doc_insert = collection.insert_one(data)  

'''
This part is still work in progress, as there are some minor issues while scraping articles from ESPN.
'''

scrape_espn(match,collection)

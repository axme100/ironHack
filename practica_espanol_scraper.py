from bs4 import BeautifulSoup
import requests
import re
import unicodedata
import pymongo
import os
from tqdm import tqdm
import time
import article
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from urllib3.util.retry import Retry

# Get the mongodb password from an environment variable
mongoPass = os.environ['mongoPass']

# Establish the remote connection to the mongo data base:
# myclient = pymongo.MongoClient("mongodb+srv://axme100:{}@cluster0-5jopz.mongodb.net/test?retryWrites=true&w=majority".format(mongoPass))
myclient = pymongo.MongoClient()

# This is the name of the cluster stored on mongo atlas
mydb = myclient["finalProject"]

# Create a new colection called efe articles
mycol = mydb["efeArticles"]


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:73.0) Gecko/20100101 Firefox/73.0'}



# Class used for storing objects inside of database
class efe_article:
    def __init__(self, url, resumen, title, category, level, date, text):
        self.url = url
        self.resumen = resumen
        self.title = title
        self.category = category
        self.level = level
        self.date = date
        self.article_text = text

    def save_to_database(self):

        # Save the entry into the mongo database
        mycol.insert_one({'url': self.url,
                          'resumen': self.resumen,
                          'title': self.title,
                          'category': self.category,
                          'level': self.level,
                          'date': self.date,
                          'articleText': self.article_text})



def get_target_urls(url):
    html_soup = requests.get(url, headers=headers)
    parsed_soup = BeautifulSoup(html_soup.content, 'html.parser')
    # Get total number of pages of articles
    numberPages = parsed_soup.find('span', {"class": "pages"}).get_text()

    # Parse this number as an int
    numberPages = int(re.search(r'\w+\d$', numberPages).group())

    # Get the number of target URLS
    targetURLs = []
    for page in range(146, numberPages + 1):
        targetURL = "https://www.practicaespanol.com/noticias/page/" + str(page) + "/"
        targetURLs.append(targetURL)

    print(targetURLs)
    return targetURLs


def scrape_pages(targetPages):

    for targetURL in tqdm(targetPages):
        html_soup = requests.get(targetURL, headers=headers)
        parsed_soup = BeautifulSoup(html_soup.content, 'html.parser')
        articles = parsed_soup.find_all('article')

        for my_article in articles:
            
            # Get link
            article_link = my_article.find('h2', {'class': 'entry-title'}).findChild("a", recursive=False, href=True)
            article_link = article_link['href']
            print(article_link)

            if check_for_url_duplicate(article_link):
                print("article already in database")
            else:
                scrape_article_meta_data(my_article, article_link)

# A beautiful soup object is passed into this method
def scrape_article_meta_data(my_article, article_link):

        try:
            # Get title
            article_title = my_article.find('h2', {'class': 'entry-title'}).get_text()
        except:
            print("No Article title found")
            article_title = ''

        try:
            # Get category
            article_category = my_article.find('span', {'class': 'categoria2'}).get_text()
        except:
            print("No article category found")
            article_category = ''

        try:
            # Get level
            article_level = [img['alt'] for img in my_article.find_all('img', alt=True) if 'Nivel' in img['alt']]
            article_level = article_level[0][-2:]
        except:
            print("No article level found")
            article_level = ''


        try:

            html_soup = session.get(article_link, headers=headers, allow_redirects=False)
            parsed_soup = BeautifulSoup(html_soup.content, 'html.parser')
            article_text, article_resumen, article_date = scrape_article_text_page(article_link)
            new_article = efe_article(article_link, article_resumen, article_title, article_category, article_level, article_date, article_text)
            new_article.save_to_database()

        except:
            print("Error getting article")

def scrape_article_text_page(url):

    # Remove HTML page
    try:
        for script in parsed_soup('script'):
            script.decompose()
    except:
        pass

    coloredSpans = parsed_soup.find_all('span', attrs={'style': 'color: #993366;'})
    targetColorSan = [span.get_text() for span in coloredSpans if 'EFE/' in span.get_text()]

    try:
        date = targetColorSan[0].split(',')[0]
    except:
        date = ''

    try:
        resumen = parsed_soup.find('h2').get_text()
        resumen = unicodedata.normalize("NFKD", resumen)
    except:
        resumen = ''

    # Get article text
    # Get all the ps in the aticle conent
    textChunks = parsed_soup.find('div', {'class': 'entry-content'}).findChildren("p")

    article_text = " ".join([chunk.get_text() for chunk in textChunks]).replace("\n", "")

    article_text = unicodedata.normalize("NFKD", article_text).strip()

    return article_text, resumen, date



def configure_transport_adapter(domain):

    # See notes in scrape.py for more information
    session = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])

    transport_adapter = HTTPAdapter(max_retries=retries)

    session.mount(domain, transport_adapter)

    return session

def check_for_url_duplicate(url):
    duplicate = list(mycol.find({'url': url}, {"_id": 1}))
    if duplicate:
        return True
    else:
        return False


# Configure session to article domain name
session = configure_transport_adapter("https://www.practicaespanol.com")

# Execute program here:
targetPages = get_target_urls("https://www.practicaespanol.com/noticias/")

scrape_pages(targetPages)
import os
import pymongo
from pymongo import MongoClient
import feedparser
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

# Get the mongodb password from an environment variable
mongoPass = os.environ['mongoPass']

# Establish the remote connection to the mongo data base
#myclient = pymongo.MongoClient("mongodb+srv://axme100:{}@cluster0-5jopz.mongodb.net/test?retryWrites=true&w=majority".format(mongoPass))
myclient = pymongo.MongoClient()

# This is the name of the cluster stored on mongo atlas
mydb = myclient["finalProject"]

# Create a new colection called raw article 
mycol = mydb["rawArticles"]


# Define the class that will be created
class rawArticle:
    def __init__(self, url, title, date, publication, xml_author):
        self.url = url
        self.title = title
        self.date = date
        self.publication = publication
        self.article_text = ''
        self.errors = []
        self.xml_author = xml_author
        
    def set_article_text(self, article_text):
        self.article_text = article_text
    
    def add_error(self, error):
        self.errors.append(error)
    
    def get_url(self):
        print (self.url)
        return self.url

    def get_domain(self):
        return self.url.split("//")[-1].split("/")[0].split('?')[0]

    def save_to_database(self):
        # Save the entry into the mongo database
        mycol.insert_one({'url': self.url,
                         'title': self.title,
                         'date': self.date,
                         'publication': self.publication,
                         'articleText': self.article_text,
                         'authors': self.xml_author,
                         'errors': self.errors})

    # This method is used for printing output to console
    # In order to monitor scraping in real time
    def printInfo(self): 
        print('url: ' + self.url)
        print('errors' + str(self.errors))

# Define a class of scraper
class daily_scraper:

    def __init__(self, target_xml_url, publication, div_info):
        self.publication = publication
        self.articles_scraped_no_errors = []
        self.articles_scraped_with_errors = []
        self.target_xml_url = target_xml_url
        # In this case, the  list attribute urls to scrape is
        # automatically set as soon as the object is created
        self.articles_to_scrape = []
        self.div_info = div_info
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:73.0) Gecko/20100101 Firefox/73.0'}


    def trackScrapes(self, rawArticle):

        # If the raw articles does not have any errors
        if not rawArticle.errors:
            # Add the URL to the list of articles that were
            # sraped with sucsess
            self.articles_scraped_no_errors.append(rawArticle.url)

        # In case the aricles does have errors
        else:
            self.articles_scraped_with_errors.append([rawArticle.url, rawArticle.errors])

    def get_daily_stats(self):
        
        print("Total Number of Articles Attempted To Scrape: " + str(len(self.articles_scraped_no_errors) + len(self.articles_scraped_with_errors)))
        print("Articles With Errors: " + str(len(self.articles_scraped_with_errors)))
        
        print("Errors: ")
        
        for problemArticle in self.articles_scraped_with_errors:
            print("url: " + problemArticle[0])
            print("")
            for error in problemArticle[1]:
                print(error)

    # Go through the XML feed and create a bunch of article objects
    def get_target_articles_to_scrape(self):

        
        parsed_xml = feedparser.parse(self.target_xml_url)

        for entry in parsed_xml['entries']:

            # Get the author field of the XML document
            # If there is none leave it blank
            try:
                xml_author = entry['author']
            except KeyError as keyError:
                xml_author = ''


            # Create an article object
            target_article = rawArticle(url=entry['link'],
                                  title=entry['title'],
                                  date=entry['published'],
                                  publication=self.publication,
                                  xml_author= xml_author)

            # Add the target article object to the scraper obje t
            self.articles_to_scrape.append(target_article)


    # Go through the article objects and scrape each one
    def scrape_articles(self):


        for article in self.articles_to_scrape:

            # In order to set the max_retries we need to:
            # create a re request.Session()
            # And Mount the transport adapter to it:
            # https://realpython.com/python-requests/#ssl-certificate-verification
            # The specific implementation strategy here is more similar to:
            # https://stackoverflow.com/questions/15431044/can-i-set-max-retries-for-requests-request
            session = requests.Session()
            retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])

            transport_adapter = HTTPAdapter(max_retries=retries)
            
            session.mount(article.get_domain(), transport_adapter)

            try:
                html_soup = session.get(article.get_url(), headers=self.headers)
                parsed_soup = BeautifulSoup(html_soup.text, 'html.parser')

            except ConnectionError as ce:
                article.add_error({"HTTP Connection Error": repr(ce)})

            # Get the text from the article
            try:
                # It appears that all of the text is located in a div caled text
                articleText = parsed_soup.find(self.div_info['target_tag'], {self.div_info['target_tag_att']: self.div_info['target_tag_att_value']}).get_text().replace('\n','').strip()
                article.set_article_text(articleText)
                print(articleText)
            except AttributeError as error:
                article.add_error({"Error getting article text: ": repr(error)})

            article.save_to_database()

            self.trackScrapes(article)
from scrape import daily_scraper
from scrape import rawArticle
import feedparser
import requests
from bs4 import BeautifulSoup
import re

class jornada(daily_scraper):

    def scrape_la_jornada(self):
        # Hard coded URL to be scraped
        url="https://www.jornada.com.mx/rss/edicion.xml?v=1"
        
        # Parse the XML feed
        feedBurner = feedparser.parse(url)
        
        # Loop through all of the entries
        for entry in feedBurner['entries']:

            errors = []
            authors = []

            # Get the page that we want to scrape
            html = requests.get(entry['link'])
        
            # Save the page as a beautiful soup object
            bs = BeautifulSoup(html.text, 'html.parser')

            
            # Get the authors of which are all stored in the same span tag
            try:
                authorTag = bs.find("span", {"itemprop": "name"})
                listOfAuthors = authorTag.get_text().replace('\n','').strip()
                # Split the authors into a list of naems using regex
                authors = re.split(r',| y',listOfAuthors)
                print(authors)
            except AttributeError as error:
                errors.append(repr(error))

            
            try:
                articleText = bs.find("div", {"id": "article-text"}).get_text().replace('\n','').strip()
            except AttributeError as error:
                articleText = ''
                errors.append(repr(error))

            # Create an article object
            myArticle = rawArticle(url=entry['link'],
                          title=entry['title'],
                          date=entry['published'],
                          publication="La Jornada",
                          authors=authors,
                          articleText=articleText,
                          errors=errors)

            myArticle.printInfo()

            # Call the inherited function to track the number of scrapes
            self.trackScrapes(myArticle)
        
            # Call the object's method to save to a mongo data base
            myArticle.saveToDatabase()
from scrape import daily_scraper
from scrape import rawArticle
import requests
from bs4 import BeautifulSoup
import feedparser
import re

class excelsior_scraper(daily_scraper):
        
    def scrape_excelsior(self):

        # Get the soup of the page where the sub rss links are posted
        url='https://www.excelsior.com.mx/rss.xml'
        
        # Parse the XML file provided by excelsior
        feedBurner = feedparser.parse('https://www.excelsior.com.mx/rss.xml')

        # We need to set user-agent headers because this page refuses get requests without them
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:73.0) Gecko/20100101 Firefox/73.0'}
        
        for entry in feedBurner['entries']:
            
            errors = []

            link = entry['link']
            
            html = requests.get(link, headers=headers)
                
            # Save the page as a beautiful soup object
            bs = BeautifulSoup(html.text, 'html.parser')
            
            # Get the text from the article
            try:
                # It appears that all of the text is located in a div caled text
                articleText = bs.find('div', {'id': 'node-article-body'}).get_text().replace('\n','').strip()
            except AttributeError as error:
                errors.append(repr(error))
                articleText=''

            # Get the author from the page  
            try:
                # It appears that the author si located in a div with the date
                authorDateString = bs.find('span', {'class': 'dblock'})
                authorDateString.span.decompose()
                author = authorDateString.get_text()
                author = re.sub(r" \/.*","",author)
            except AttributeError as error:
                print(error)
                errors.append(repr(error))
            

            # Create an article object
            myArticle = rawArticle(url=entry['link'],
                      title=entry['title'],
                      date=entry['published'],
                      publication="Excelsior",
                      articleText=articleText,
                      errors=errors,
                      authors=author)
    
            myArticle.printInfo()

            # Call the inherited function to track the number of scrapes
            self.trackScrapes(myArticle)

            # Call the object's method to save to a mongo data base
            myArticle.saveToDatabase()
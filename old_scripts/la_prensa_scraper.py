from scrape import daily_scraper
from scrape import rawArticle
import requests
from bs4 import BeautifulSoup
import feedparser

class la_prensa_scraper(daily_scraper):
        
    def scrape_la_prensa(self):

        # Get the soup of the page where the sub rss links are posted
        url='http://laprensa.mx/rss.asp'
        html = requests.get(url)
        bs = BeautifulSoup(html.text, 'html.parser')
        
        # Get a list of all the links that are part of the sub rss feed
        rssSections = bs.find_all("div", {"class": "secc"})
        rssSubLinks = []
        for section in rssSections:
            link = section.find('a', href=True)
            rssSubLinks.append(link['href'])
        
        
        # Iterate over and parse each of the links in the rssSubLinks
        for link in rssSubLinks:
            feedBurner = feedparser.parse(link)
    
            # Iterate over and parse each of the entries in the rss page
            for entry in feedBurner['entries']:
                
                errors = []

                # Get the soup page of to scrape
                html = requests.get(entry['link'])
                bs = BeautifulSoup(html.text, 'html.parser')

                try:
                    # It appears that all of the text is located in a div caled text
                    textDiv = bs.find('div', {'id': 'texto'})
                except AttributeError as error:
                    articleText = ''
                    errors.append(error)


                # Get rid of all the divs that are within this div because
                # some pages have tables and images with text that appear to be wrapped in divs
                for div in textDiv("div"):
                    div.decompose()
    
                # The result of the previous blocks, 
                articleText = textDiv.get_text().replace('\n','').strip()
                
                # Create an article object
                myArticle = rawArticle(url=entry['link'],
                          title=entry['title'],
                          date=entry['published'],
                          publication="La Prensa",
                          articleText=articleText,
                          errors=errors,
                          authors=[])
        
                myArticle.printInfo()

                # Call the inherited function to track the number of scrapes
                self.trackScrapes(myArticle)

                # Call the object's method to save to a mongo data base
                myArticle.saveToDatabase()

import os
import pymongo
from pymongo import MongoClient

# Get the mongodb password from an environment variable
mongoPass = os.environ['mongoPass']

# Establish the remote connection to the mongo data base
myclient = pymongo.MongoClient("mongodb+srv://axme100:{}@cluster0-5jopz.mongodb.net/test?retryWrites=true&w=majority".format(mongoPass))

# This is the name of the cluster stored on mongo atlas
mydb = myclient["finalProject"]

# Create a new colection called raw article 
mycol = mydb["rawArticles"]


# Define the class that will be created
class rawArticle:
    def __init__(self, url, title, date, authors, publication, articleText, errors):
        self.url = url
        self.title = title
        self.date = date
        self.publication = publication
        self.articleText = articleText
        self.errors = errors
        self.authors = authors
        
    def saveToDatabase(self):
        # Save the entry into the mongo database
        mycol.insert_one({'url': self.url,
                         'title': self.title,
                         'date': self.date,
                         'publication': self.publication,
                         'articleText': self.articleText,
                         'authors': self.authors,
                         'errors': self.errors})

    # This method is used for printing output to console
    # In order to monitor scraping in real time
    def printInfo(self): 
        print('url: ' + self.url)
        print('errors' + str(self.errors))

# Define a class of scraper
class daily_scraper:

    def __init__(self):
        self.articles_scraped_no_errors = []
        self.articles_scraped_with_errors = []

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
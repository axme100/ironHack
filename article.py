import pymongo
import os

# Get the mongodb password from an environment variable
mongoPass = os.environ['mongoPass']

# Establish the remote connection to the mongo data base:
# pymongo.MongoClient("mongodb+srv://axme100:{}@cluster0-5jopz.mongodb.net/test?retryWrites=true&w=majority".format(mongoPass))
myclient = pymongo.MongoClient()

# This is the name of the cluster stored on mongo atlas
mydb = myclient["finalProject"]

# Create a new colection called raw article
mycol = mydb["rawArticles"]


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
        # print(self.url)
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
        #print('url: ' + self.url)
        #print('errors' + str(self.errors))
        pass

    # This method is called within the sraper to see
    # if the article is already in the database from the url
    def check_for_url_duplicate(self):
        duplicate = list(mycol.find({'url': self.url}, {'url': 1, "_id": 0}))
        #print(duplicate)
        if duplicate:
            return True
        else:
            return False

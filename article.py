import pymongo
import os

# Get the mongodb password from an environment variable
mongoPass = os.environ['mongoPass']

# Establish the remote connection to the mongo data base:
# myclient = pymongo.MongoClient("mongodb+srv://axme100:{}@cluster0-5jopz.mongodb.net/test?retryWrites=true&w=majority".format(mongoPass))
myclient = pymongo.MongoClient()


# This is the name of the cluster stored on mongo atlas
mydb = myclient["finalProject"]

# Create a new colection called raw article
mycol = mydb["rawArticles"]

article_prepared = mydb["article_prepared_2"]


class raw_article:
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
        pass

    # This method is called within the sraper to see
    # if the article is already in the database from the url
    def check_for_url_duplicate(self):
        duplicate = list(mycol.find({'url': self.url}, {'url': 1, "_id": 0}))
        if duplicate:
            return True
        else:
            return False


class processed_article:
    def __init__(self, _id, list_of_sentences, bag_of_words, level, level_binary):
        self.unique_id = _id,
        self.list_of_sentences = list_of_sentences,
        self.bag_of_words = bag_of_words,
        self.level = level
        self.level_binary = level_binary

    def save_to_database(self):

        # Save the entry into the mongo database
        article_prepared.insert_one({'_id': self.unique_id[0],
                                     'bag_of_words': self.bag_of_words,
                                     'list_of_sentences': self.list_of_sentences,
                                     'level': self.level,
                                     'level_binary': self.level_binary})

    def check_for_id_duplicate(self):
        duplicate = list(mycol.find({'_id': self.unique_id}, {"_id": 1}))
        if duplicate:
            return True
        else:
            return False
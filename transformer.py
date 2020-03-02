import pymongo
import spacy
from nltk.corpus import stopwords
import re
import article

nlp = spacy.load("es_core_news_sm")

spacy_stopwords = spacy.lang.es.stop_words.STOP_WORDS
nltk_stopwords = set(stopwords.words('spanish'))
spanish_stop_words = spacy_stopwords.union(nltk_stopwords)


# Establish the remote connection to the mongo data base:
# myclient = pymongo.MongoClient("mongodb+srv://axme100:{}@cluster0-5jopz.mongodb.net/test?retryWrites=true&w=majority".format(mongoPass))
myclient = pymongo.MongoClient()

# This is the name of the cluster stored on mongo atlas
mydb = myclient["finalProject"]


class linguistic_transformer:

    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def connect_to_source(self):

        # Create a new colection called efe articles
        my_col_efe_articles = mydb[self.source]

        # This just gets every document in the database
        source_cursor = my_col_efe_articles.find()

        return source_cursor

    def check_for_id_duplicate(self, checked_id):

        my_col_efe_articles = mydb[self.destination]

        duplicate = list(my_col_efe_articles.find({'_id': checked_id}, {"_id": 1}))
        if duplicate:
            return True
        else:
            return False

    def parse(self, my_article):

        # Remove the last little bit of information that we do not need
        # my_article = re.sub(r"\(\d+ de.*$", "", my_article.strip())

        # Make everything undercase
        testArticle = my_article.casefold()

        # Parse the article using spacy
        doc = nlp(testArticle)

        return doc

    def create_bag_of_words(self, doc):

        # Get the bag of words that we want
        # Lemmatize, remove punctuation, remove stop words
        tokens = [token.lemma_ for token in doc if not token.is_punct]
        tokens = [token for token in tokens if token not in spanish_stop_words]
        tokens = ' '.join([token for token in tokens])

        return tokens

    def create_list_of_sentences(self, doc):
        my_sentences = []

        for sentence in doc.sents:
            my_sentences.append(str(sentence))

        return my_sentences

    def get_doc_json(self, doc):

        return str(doc.to_json)

    def transform(self):

        cursor = self.connect_to_source()

        for raw_article in cursor:

            # First check to see if the article is even in the database
            if self.check_for_id_duplicate(raw_article['_id']) is False:

                # First use spacy to parse the document and save in a file calle doc
                doc = self.parse(raw_article['articleText'])

                # Get the bag of words from teh doc
                bag_of_words = self.create_bag_of_words(doc)

                # Get the list of sentences from spacy
                list_of_sentences = self.create_list_of_sentences(doc)

                # Get spacy JSON
                spacy_json = self.get_doc_json(doc)

                # Get other things

                # Save the article in the processed corpu using the same ID as before
                new_processed_article = article.processed_main_article(_id=raw_article['_id'],
                                                                       title=raw_article['title'],
                                                                       publication=raw_article['publication'],
                                                                       date=raw_article['date'],
                                                                       list_of_sentences=list_of_sentences,
                                                                       bag_of_words=bag_of_words,
                                                                       level='',
                                                                       level_binary='',
                                                                       spacy_json=spacy_json,
                                                                       url=raw_article['url'])
                new_processed_article.save_to_database()

            else:
                print("Transformed article already in database")


# my_transformer = linguistic_transformer('efeArticles')
# my_transformer.transform()

my_transformer = linguistic_transformer('rawArticles', 'main_processed_article')
my_transformer.transform()

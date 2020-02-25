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

    def __init__(self, source):
        self.source = source

    def connect_to_source(self):

        # Create a new colection called efe articles
        my_col_efe_articles = mydb[self.source]

        # This just gets every document in the database
        source_cursor = my_col_efe_articles.find()

        return source_cursor

    def parse(self, my_article):

        # Remove the last little bit of information that we do not need
        my_article = re.sub(r"\(\d+ de.*$", "", my_article.strip())

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

    def transform(self):

        cursor = self.connect_to_source()

        for raw_article in cursor:

            advanced_levels = ['B2', 'C1', 'C2']
            if raw_article['level'] in advanced_levels:
                binary_level = 1
            else:
                binary_level = 0

            doc = self.parse(raw_article['articleText'])
            bag_of_words = self.create_bag_of_words(doc)
            list_of_sentences = self.create_list_of_sentences(doc)
            new_processed_article = article.processed_article(_id=raw_article['_id'],
                                                              list_of_sentences=list_of_sentences,
                                                              bag_of_words=bag_of_words,
                                                              level=raw_article['level'],
                                                              level_binary=binary_level)
            new_processed_article.save_to_database()


my_transformer = linguistic_transformer('efeArticles')
my_transformer.transform()

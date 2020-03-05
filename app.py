from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import os
import pymongo
from bson.objectid import ObjectId
import random


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Connect to users database
mongoPass = os.environ['mongoPass']

# myclient = pymongo.MongoClient()
myclient = pymongo.MongoClient("mongodb+srv://axme100:{}@cluster0-5jopz.mongodb.net/test?retryWrites=true&w=majority".format(mongoPass))

# This is the name of the cluster stored on mongo atlas
mydb = myclient["finalProject"]

# Create a new colection called raw article
user = mydb["users"]

main_articles = mydb["main_processed_article"]


@app.route('/getrec/<user_id>/')
@cross_origin()
def getrec(user_id):

    # Firts get the specific user with the object ID that we are intersted in:
    my_user_cursor = user.find({"_id": ObjectId(user_id)})

    my_user = list(my_user_cursor)

    print(my_user)

    # Get the categories and the level pertaining to this user
    user_categories = my_user[0]['categories']

    user_level = my_user[0]['level']

    # Convert to binary user level
    advanced_levels = ["B2", "C1", "C2"]

    if (user_level in advanced_levels):
        user_level_binary = 1
    else:
        user_level_binary = 0

    articles_to_return = query_articles(user_categories, user_level_binary)

    return jsonify(articles_to_return)


def query_articles(user_categories, user_level_binary):

    articles_to_return = []

    for category in user_categories:

        articles_cursor = main_articles.aggregate([{'$match': {'level_binary': user_level_binary,'category': category, 'articleText': {'$nin': [None, '']}}},
                                                   {'$sample': {'size': 5}},
                                                   {"$project": {"_id": {"$toString": "$_id"}, "publication": 1, "articleText": 1, "date": 1, "category": 1, "title": 1, "url": 1, "level_binary": 1}},
                                                   ])

        all_category_articles = list(articles_cursor)
        # my_articles_to_add = random.choices(all_category_articles, k=5)

        # Unpack all th articles and append them to a list
        for my_article in all_category_articles:

            # Convert the level of the article to a string
            # Most likely I could do this within a mongo query
            level = my_article['level_binary']
            if level == 0:
                my_article['level_binary'] = "beginner"
            elif level == 1:
                my_article['level_binary'] = "advanced"

            # Append the article to the list of articles that we are going to return
            articles_to_return.append(my_article)

    return(articles_to_return)


if __name__ == '__main__':
    app.run()

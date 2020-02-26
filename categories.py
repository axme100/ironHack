import pymongo
import os
mongoPass = os.environ['mongoPass']
myclient = pymongo.MongoClient("mongodb+srv://axme100:{}@cluster0-5jopz.mongodb.net/test?retryWrites=true&w=majority".format(mongoPass))
# This is the name of the cluster stored on mongo atlas
mydb = myclient["finalProject"]

# Create a new colection called raw article
mycol = mydb["rawArticles"]

cursor = mycol.find()


myPubs = []
for article in cursor:
    myPubs.append(article['publication'])

print(myPubs)
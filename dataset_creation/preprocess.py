from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

#
nltk.download('wordnet')
#
connection = MongoClient("mongodb://localhost:27017/")
#
db = connection.ININ
# Get collection from DB
CollectionName = 'myLeaderboards'
# set collection
collection = db[CollectionName]
#
stop_words = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")

# comments =
# for comment in db[collection].find():
# for comment in CollectionName.find({"short_tempered"}):
#     print(comment)
# import json
#
# data = db.CollectionName.find({})
#
# parsed = json.loads(data)

dataset = collection.find()
for row in dataset:
    for posts in row['Posts']:
        # preprocess_description(row['Codename'], posts['URL'], posts['Description'])
        # print(row['Codename'])
        # print(posts['Description'])
        for comment in posts['All Comments']:

            print(comment)
    # print(document['Posts'])


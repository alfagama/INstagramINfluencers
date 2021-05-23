import pandas as pd
import pymongo
from pandas import DataFrame

# MongoDB
uri = "mongodb://localhost:27017/"
# Mongo client
client = pymongo.MongoClient(uri)
# Import database by name
db = client.ININ
# Get collection from DB
CollectionName = 'myLeaderboards'
# set collection
collection = db[CollectionName]


class Db:
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        self.db = client['todo-db']

    def find_all(self, collection_name: str):
        return list(self.db[collection_name].find({}, {'_id': False}))

    def find(self, collection_name: str, query: dict):
        return list(self.db[collection_name].find(query, {'_id': False}))

    def find_influencers_count_by_category(self):
        cursor = collection.aggregate([
            {'$group': {'_id': '$category', "count": {"$sum": 1}}}
        ])
        return pd.DataFrame(list(cursor))

    def get_post_comments(self):
        comments = collection.find()
        df = DataFrame(list(comments))
        return df

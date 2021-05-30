import pymongo
import pandas as pd
import collections


# MongoDB
uri = "mongodb://localhost:27017/"
# Mongo client
client = pymongo.MongoClient(uri)
# Import database by name
db = client.ININ
# Get collection from DB
CollectionName = 'myLeaderboardsNew'
# set collection
collection = db[CollectionName]


class Db:
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        self.db = client['todo-db']


    def find_all(self, collection_name: str):
        return list(self.db[collection_name].find({}, {'_id': False}))


    def find(self, collection_name: str, query:dict):
        return list(self.db[collection_name].find(query, {'_id': False}))



    def get_influencers_count_by_category(self):
        """
        Creates a dataframe with the number of influencers by category
        :param: -
        :return df: dataframe with the number of influencers by category
        """

        cursor = collection.aggregate([
            {'$group': {'_id': '$category', "count": {"$sum": 1}}}
        ])
        return pd.DataFrame(list(cursor))


    def get_frequency_per_day(self):
        """
        Creates a dataframe with the number of posts by day
        :param: -
        :return df: dataframe with the number of posts by day
        """

        cursor = collection.find({}, {'_id': 0, 'Posts.Post Created Date': 1})

        post_list = []
        for element in cursor:
            post_list.append(element['Posts'])

        all_dates = []
        for posts in post_list:  # for each influencer
            for post in posts:  # for each post of each influencer
                if post.get('Post Created Date') != '2021-04-30':  # filter out this date because we have only 3 posts
                    all_dates.append(post.get('Post Created Date'))

        counter = collections.Counter(all_dates)  # count frequency of each date
        df = pd.DataFrame.from_dict(counter, orient='index').reset_index()  # convert conter to df
        df.columns = ['day', 'posts']
        return df


    def get_post_hashtags(self):
        """
        Creates a dataframe with the description of posts grouped by influencer's category
        :param: -
        :return posts_description_df: dataframe with posts' description
        """

        cursor = collection.aggregate([
            {'$group': {'_id': '$category',
                    'hashtags': {'$push': '$Posts.Hashtags'}}}
        ])

        posts_description_df = pd.DataFrame(list(cursor))
        posts_description_df.columns = ['category', 'hashtags']
        return posts_description_df


    def get_frequency_per_hour(self):
        """
        Creates a dataframe with the number of posts by hour
        :param: -
        :return df: dataframe with the number of posts by hour
        """

        cursor = collection.find({}, {'_id': 0, 'Posts.Post Created Time': 1})

        post_list = []
        for element in cursor:
            post_list.append(element['Posts'])

        all_hours = []
        for posts in post_list:  # for each influencer
            for post in posts:  # for each post of each influencer
                all_hours.append(post.get('Post Created Time'))

        all_hours_df = pd.DataFrame({'created_at': all_hours})
        all_hours_df['created_at'] = pd.to_datetime(all_hours_df['created_at'])
        all_hours_df['created_at'] = all_hours_df['created_at'].dt.hour

        counter = collections.Counter(all_hours_df['created_at'].tolist())  # count frequency of each date
        df = pd.DataFrame.from_dict(counter, orient='index').reset_index()  # convert conter to df
        df.columns = ['time', 'posts']

        df = df.sort_values(by=['time'], ascending=True)
        df['time'] = pd.to_datetime(df['time'], format='%H').dt.time
        # print(df)
        return df
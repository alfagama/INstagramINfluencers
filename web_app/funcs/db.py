import collections

import pandas as pd
import pymongo

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
from pandas import DataFrame


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


    def get_hashtags_distribution(self):
        """
        Creates a dataframe with the number of posts and number of hashtags
        :param: -
        :return df: dataframe with the number of posts and number of hashtags
        """

        cursor = collection.aggregate([
            {'$group': {'_id': '$category',
                        'hashtags': {'$push': '$Posts.Hashtags'}}}
        ])

        posts_description_df = pd.DataFrame(list(cursor))
        posts_description_df.columns = ['category', 'hashtags']
        # print(posts_description_df)

        all_hashtags = []
        for hashtag_list in posts_description_df['hashtags']:
            for influencer in hashtag_list:
                for post in influencer:
                    all_hashtags.append(post)

        # print(all_hashtags)
        posts_hashtag_count = []

        for hashtag_list in all_hashtags:
            posts_hashtag_count.append(len(hashtag_list))

        counter = collections.Counter(posts_hashtag_count)
        counter_df = pd.DataFrame.from_dict(counter, orient='index').reset_index()
        counter_df = counter_df.rename(columns={'index': 'Number of Hashtags', 0: 'Number of Posts'})

        return counter_df


    def get_top_hashtag_frequency(self):
        """
        Creates a dataframe with the most frequent hashtags and their count
        :param: -
        :return df: dataframe with the most frequent hashtags and their count
        """
        cursor = collection.find({}, {'_id': 0, 'Posts.Followers at Posting': 1, 'Posts.Hashtags': 1, 'Codename': 1})

        hashtags = []
        for influencer in cursor:
            # print(influencer['Posts'])
            for post in influencer['Posts']:
                if post:
                    for hashtag in post['Hashtags']:
                        hashtags.append(hashtag.lower())

        counter = collections.Counter(hashtags)
        df = pd.DataFrame.from_dict(counter, orient='index').reset_index()
        df.columns = ['hashtag', 'count']
        df = df.sort_values(by=['count'], ascending=False)
        df['hashtag'] = '#' + df['hashtag'].astype(str)
        return df.head(25)


    def get_no_of_hashtags_by_category(self):
        """
        Creates a dataframe with the total number of hashtags from each category
        :param: -
        :return df: dataframe with the total number of hashtags from each category
        """

        cursor = collection.aggregate([
            {'$group': {'_id': '$category',
                        'hashtags': {'$push': '$Posts.Hashtags'}}}
        ])
        df = pd.DataFrame(list(cursor))

        for index, row in df.iterrows():
            counter = 0
            for post in row['hashtags']:
                for hashtag_list in post:
                    if hashtag_list:
                        counter += len(hashtag_list)
            df.loc[index, 'count'] = counter

        df['count'] = df['count'].astype(int)
        df = df.drop(['hashtags'], axis=1)
        df = df.sort_values(by=['count'], ascending=False)
        df.columns = ['category', 'hashtags_count']
        return df


    def get_percentage_of_hashtags_by_category(self):
        """
            Creates a dataframe with the percentage of hashtags by post
            :param: -
            :return df: dataframe with the percentage of hashtags by post
        """

        cursor = collection.aggregate([
            {'$group': {'_id': '$category',
                        'hashtags': {'$push': '$Posts.Hashtags'}}}
        ])
        df = pd.DataFrame(list(cursor))

        for index, row in df.iterrows():
            counter = 0
            posts_count = 0
            for post in row['hashtags']:
                # print(post)
                for hashtag_list in post:
                    posts_count += 1
                    if hashtag_list:
                        counter += len(hashtag_list)
            df.loc[index, 'hashtag_count'] = counter
            df.loc[index, 'post_count'] = posts_count

        df['hashtag_count'] = df['hashtag_count'].astype(int)
        df['post_count'] = df['post_count'].astype(int)
        df['percentage'] = df['hashtag_count'] / df['post_count']
        df = df.drop(['hashtags', 'hashtag_count', 'post_count'], axis=1)
        df = df.sort_values(by=['percentage'], ascending=False)
        df.columns = ['category', 'hashtags_percentage']
        return df


    def get_hashtags_engagement_distribution(self):
        """
        Creates a dataframe with the ++
        :param: -
        :return posts_description_df:
        """

        cursor = collection.find({}, {'_id': 0, 'Posts.Hashtags': 1, 'Posts.Comments': 1, 'Posts.Likes': 1})

        posts_list = []
        for posts in cursor:
            posts_list.append(posts)

        data = []
        for posts in posts_list:
            for post in posts['Posts']:
                data.append(post)

        df = pd.DataFrame(data)
        df['hashtag_count'] = df['Hashtags'].str.len()
        df['engagement'] = df['Likes'] + df['Comments']
        df = df.drop(['Hashtags', 'Likes', 'Comments'], axis=1)
        df = df.sort_values(by=['hashtag_count'], ascending=True)
        return df


    def get_posts(self):
        posts = collection.find()
        df = DataFrame(list(posts))
        data = pd.DataFrame(columns=['Followers at Posting', 'Post Created', 'Post Created Date',
                                     'Post Created Time', 'Type', 'Total Interactions', 'Likes', 'Comments',
                                     'Views', 'URL', 'Link', 'Photo', 'Title', 'Description', 'Hashtags',
                                     'Image Text', 'Sponsor Id', 'Sponsor Name', 'Overperforming Score',
                                     'All Comments'])
        for i in df['Posts']:
            data = pd.concat([data, pd.DataFrame(i, columns=data.columns)], ignore_index=True)

        return data





import pandas as pd
import pymongo
import mongo
import os
import errno

# MongoDB
uri = "mongodb://localhost:27017/"
# Mongo client
client = pymongo.MongoClient(uri)
# Import database by name
db = client.ININ

# Options for pandas -----
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def get_influencers_names():
    """
    Connects to mongoDB and returns all influencers names in 'account_names'.
    :return: account_names (list)
    """
    # Get collection from DB
    CollectionName = 'myLeaderboards'
    # set collection
    collection = db[CollectionName]
    # get data in influencers variable
    influencers = collection.find()
    # set empty list to return influencers' usernames
    account_names = []
    # loop through all influencers
    for influencer in influencers:
        account_names.append(influencer['Codename'])
    # return names from all accounts
    return account_names


def get_urls(name):
    """
    For name inserted, returns all post URLs
    :param name: (string)
    :return: urls: (list)
    """
    # read csv of influencer's history
    data_set = pd.read_csv(f"data/history/{name}.csv",
                           # sep=',',
                           # header=0,
                           # skiprows=0
                           )

    # return only posts from April month -> '2021-04-'
    posts_to_scrape = data_set[data_set['Post Created'].str.match('2021-04-')]
    posts_to_scrape = posts_to_scrape.append(data_set[data_set['Post Created'].str.match('2021-03-')])
    print("Posts created by user: ", name, " from 1st of March to 30th of April: ", posts_to_scrape['Post Created'].count() + 1)

    # # return X last posts
    # num_of_posts = 25  # change to get more or less posts
    # posts_to_scrape = data_set[:num_of_posts]
    # print("Scraping last ", num_of_posts, " posts of user: ", name)

    # update MongoDB for user's posts
    mongo.update_posts(posts_to_scrape)

    # return URLs from selected month's posts
    return posts_to_scrape['URL']


def create_directory(name):
    """
    creates directory for scraped comments
    :param name: name of directory (string)
    :return: -
    """
    # create directory for user = name
    try:
        os.makedirs(f'data/scrape_comments/{name}')
        print("Created new directory for user: ", name)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
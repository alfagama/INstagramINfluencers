import pandas as pd
import pymongo
from dataset_creation import mongo
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
    CollectionName = 'myLeaderboardsNew'
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
    data_set = pd.read_csv(f"../data/history/{name}.csv",
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


def get_influencer_info():
    """
        Connects to mongoDB and returns all influencers' info.
        :return: in_info (dataframe)
    """
    # Get collection from DB
    CollectionName = 'myLeaderboardsNew'
    collection = db[CollectionName]

    # Make a query and exclude columns we don't need for our model
    cursor = collection.find({},{"_id": 0, "Account":0, "Codename":0, "URL":0, "Posts":0, "sex":0, "age":0, "marital_status":0,
     "likeable":0, "creative":0, "calm":0, "outgoing":0, "post_cohesion":0, "self_centered":0, "short_tempered":0, "professional":0,
    "fitness_advice":0, "general_advice":0})

    # Expand the cursor and construct the DataFrame
    in_info = pd.DataFrame(list(cursor))
    print(in_info.head(5))

    return in_info

def get_influencer_category(username):
    """
        Connects to mongoDB and returns the category of each influencer.
        :return: category
    """
    # Get collection from DB
    CollectionName = 'myLeaderboardsNew'
    collection = db[CollectionName]

    # Make a query and exclude columns we don't need for our model
    cursor = collection.find({'Codename': username}, {"category":1})
    for i in cursor:
       return i["category"]

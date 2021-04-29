import pandas as pd
import pymongo

# MongoDB
uri = "mongodb://localhost:27017/"
# Mongo client
client = pymongo.MongoClient(uri)
# Import database by name
db = client.ININ

# Options for pandas -----
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# get_data
def get_influencers_names():
    # Get collection from DB
    CollectionName = 'InstagramFitnessInfluencers'
    # set collection
    collection = db[CollectionName]
    # get data in influencers variable
    influencers = collection.find()
    # set empty list to return influencers' usernames
    account_names = []
    # loop through all influencers
    for influencer in influencers:
        account_names.append(influencer['Codename'])

    return account_names


def get_urls(name):
    # read csv of influencer's history
    data_set = pd.read_csv(f"data/history/{name}.csv",
                           # sep=',',
                           # header=0,
                           # skiprows=0
                           )
    return data_set['URL']

import pandas as pd
import pymongo

"""!!! IMPORTANT: !!!
1. Use this as 1st row of .csv using notepad++ :
"timestamp","influencer","sex","age","συμπαθές","δημιουργικό","ήρεμο/συναισθηματικά ισορροπημένο", "εξωστρεφές",
"συνοχή","εγωκεντρικό / νάρκισσος","ευέξαπτο","αξιόπιστο / σωστός επαγγελματίας","εμπιστευόμουν για 
θέματα fitness","εμπιστευόμουν για τομέα διαφορετικό","follow","reason"
Since MongoDB understands '1. Is this influencer..' As column named '1' with sub-level the follow-up question.
2. Again using notepad++ replace-> 
'(space)"' with-> '"'
, since many people answered 'username(space)' for some reason.
3. Run this from this file since it is not linked with the main execution.
"""


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

def get_questionnaire_answers():
    """
    Connects to mongoDB and prints questionnaire answers for collection entries
    :return: -
    """
    # Get collection from DB
    CollectionName = 'questionnaire'
    # set collection
    collection = db[CollectionName]
    # get data in influencers variable
    influencers = collection.find()
    # column names for dataframe
    column_names = ["timestamp", "influencer", "sex", "age",
                    "συμπαθές", "δημιουργικό", "ήρεμο/συναισθηματικά ισορροπημένο", "εξωστρεφές", "συνοχή",
                    "εγωκεντρικό / νάρκισσος", "ευέξαπτο", "αξιόπιστο / σωστός επαγγελματίας",
                    "εμπιστευόμουν για θέματα fitness", "εμπιστευόμουν για τομέα διαφορετικό",
                    "follow", "reason"]
    # create dataframe with column names
    df = pd.DataFrame(columns=column_names)
    # append all values retrieved from questionnaire in the dataframe
    for influencer in influencers:
        df = df.append({"timestamp": influencer['timestamp'],
                        "influencer": influencer['influencer'],
                        "sex": influencer['sex'],
                        "age": influencer['age'],
                        "συμπαθές": influencer['συμπαθές'],
                        "δημιουργικό": influencer['δημιουργικό'],
                        "ήρεμο/συναισθηματικά ισορροπημένο": influencer['ήρεμο/συναισθηματικά ισορροπημένο'],
                        "εξωστρεφές": influencer['εξωστρεφές'],
                        "συνοχή": influencer['συνοχή'],
                        "εγωκεντρικό / νάρκισσος": influencer['εγωκεντρικό / νάρκισσος'],
                        "ευέξαπτο": influencer['ευέξαπτο'],
                        "αξιόπιστο / σωστός επαγγελματίας": influencer['αξιόπιστο / σωστός επαγγελματίας'],
                        "εμπιστευόμουν για θέματα fitness": influencer['εμπιστευόμουν για θέματα fitness'],
                        "εμπιστευόμουν για τομέα διαφορετικό": influencer['εμπιστευόμουν για τομέα διαφορετικό'],
                        "follow": influencer['follow'],
                        "reason": influencer['reason']
                        },
                       ignore_index=True)

    # get list of names from our own collections
    influencers_names = get_influencers_names()
    # sort values
    # df = df.sort_values(by=['influencer'])
    # keep only influencers inside retrieved collection
    df = df[df['influencer'].isin(influencers_names)]
    # # print whole dataframe values
    # print(df)
    # print how many times each influencer was evaluated
    print(df['influencer'].value_counts())


# get questionnaire information
get_questionnaire_answers()

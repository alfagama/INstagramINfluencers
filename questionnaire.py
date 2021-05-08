import pandas as pd
import pymongo
from mongo import *

"""!!! IMPORTANT: !!!
Use this as 1st row of .csv using notepad++ :
>>>
"timestamp","influencer","sex","age","συμπαθές","δημιουργικό","ήρεμο/συναισθηματικά ισορροπημένο","εξωστρεφές","συνοχή","εγωκεντρικό / νάρκισσος","ευέξαπτο","αξιόπιστο / σωστός επαγγελματίας","εμπιστευόμουν για θέματα fitness","εμπιστευόμουν για τομέα διαφορετικό","follow","reason"
<<<
Since MongoDB understands '1. Is this influencer..' As column named '1' with sub-level the follow-up question.
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
    CollectionName = 'questionnaire2'
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
    print(df['age'].value_counts())
    # get list of names from our own collections
    influencers_names = get_influencers_names()
    # sort values
    # df = df.sort_values(by=['influencer'])
    # specific changes
    df['influencer'] = df['influencer'].replace('Ronnie Coleman', 'ronniecoleman8')
    df['influencer'] = df['influencer'].replace('flex_luis', 'flex_lewis')
    # replace ' "' with '"'
    df['influencer'] = df['influencer'].str.strip()
    # lowercase
    df['influencer'] = df['influencer'].str.lower()
    # keep only influencers inside retrieved collection
    df = df[df['influencer'].isin(influencers_names)]
    # # print whole dataframe values
    # print(df)
    # print how many times each influencer was evaluated
    print(df['influencer'].value_counts())

    # changes Yes and No to 1 and 0
    yes_no_dict = {'Ναι': 1, 'Όχι': 0}
    df = df.replace({"follow": yes_no_dict})

    df.to_csv('data/complete_csv_of_all_of_my_influencers.csv')

    # change datatypes to int from string
    # print(df.dtypes)
    df['συμπαθές'] = df['συμπαθές'].astype(str).astype(int)
    df['δημιουργικό'] = df['δημιουργικό'].astype(str).astype(int)
    df['ήρεμο/συναισθηματικά ισορροπημένο'] = df['ήρεμο/συναισθηματικά ισορροπημένο'].astype(str).astype(int)
    df['εξωστρεφές'] = df['εξωστρεφές'].astype(str).astype(int)
    df['συνοχή'] = df['συνοχή'].astype(str).astype(int)
    df['εγωκεντρικό / νάρκισσος'] = df['εγωκεντρικό / νάρκισσος'].astype(str).astype(int)
    df['ευέξαπτο'] = df['ευέξαπτο'].astype(str).astype(int)
    df['αξιόπιστο / σωστός επαγγελματίας'] = df['αξιόπιστο / σωστός επαγγελματίας'].astype(str).astype(int)
    df['εμπιστευόμουν για θέματα fitness'] = df['εμπιστευόμουν για θέματα fitness'].astype(str).astype(int)
    df['εμπιστευόμουν για τομέα διαφορετικό'] = df['εμπιστευόμουν για τομέα διαφορετικό'].astype(str).astype(int)
    df['follow'] = df['follow'].astype(str).astype(int)
    # print(df.dtypes)

    # get mean value for all questions 1-10 + follow probability
    df_new = df.groupby(['influencer']).agg({'συμπαθές': 'mean',
                                             'δημιουργικό': 'mean',
                                             'ήρεμο/συναισθηματικά ισορροπημένο': 'mean',
                                             'εξωστρεφές': 'mean',
                                             'συνοχή': 'mean',
                                             'εγωκεντρικό / νάρκισσος': 'mean',
                                             'ευέξαπτο': 'mean',
                                             'αξιόπιστο / σωστός επαγγελματίας': 'mean',
                                             'εμπιστευόμουν για θέματα fitness': 'mean',
                                             'εμπιστευόμουν για τομέα διαφορετικό': 'mean',
                                             'follow': 'mean',
                                             })

    # print(df.head(40))

    # create dataset with mean values
    df_new.to_csv('data/dataset_with_mean_values_to_pass_to_mongodb.csv')

    # pass dataframe to mongodb + skip 1st row
    # update_questionnaire_answers(df.iloc[1:])
    update_questionnaire_answers(df_new)


# get questionnaire information
get_questionnaire_answers()

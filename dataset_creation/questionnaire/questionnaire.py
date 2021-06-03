from dataset_creation.mongo import *

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


# Adapted from https://gist.github.com/ShinNoNoir/4749548
def fleiss_kappa(ratings, n):
    '''
    Computes the Fleiss' kappa measure for assessing the reliability of
    agreement between a fixed number n of raters when assigning categorical
    ratings to a number of items.

    Args:
        ratings: a list of (item, category)-ratings
        n: number of raters
        k: number of categories
    Returns:
        the Fleiss' kappa score

    See also:
        http://en.wikipedia.org/wiki/Fleiss'_kappa
    '''
    items = set()
    categories = set()
    n_ij = {}

    for i, c in ratings:
        items.add(i)
        categories.add(c)
        n_ij[(i, c)] = n_ij.get((i, c), 0) + 1

    N = len(items)

    p_j = dict(((c, sum(n_ij.get((i, c), 0) for i in items) / (1.0 * n * N)) for c in categories))
    P_i = dict(((i, (sum(n_ij.get((i, c), 0) ** 2 for c in categories) - n) / (n * (n - 1.0))) for i in items))

    P_bar = sum(P_i.values()) / (1.0 * N)
    P_e_bar = sum(value ** 2 for value in p_j.values())

    kappa = (P_bar - P_e_bar) / (1 - P_e_bar)
    print('Fleiss Kappa result is:',kappa)
    return kappa

def preprocess_for_fleiss_kappa(df):
    count2 = []
    count3 = []
    count4 = []
    count5 = []
    count6 = []
    count7 = []

    df_grouped = df.groupby(df['influencer'])

    for name, group in df_grouped:
        # print(name)
        # print(len(group))
        if (len(group)) == 2:
            count2.append(name)
        elif (len(group)) == 3:
            count3.append(name)
        elif (len(group)) == 4:
            count4.append(name)
        elif (len(group)) == 5:
            count5.append(name)
        elif (len(group)) == 6:
            count6.append(name)
        elif (len(group)) == 7:
            count7.append(name)

    counters = [count2, count3, count4, count5, count6, count7]

    myratings = []
    number_of_annotators = 2
    score = []
    for team in counters:
        print(team)
        counter_influencers = 1
        rating = []
        for name in team:
            yes = 0
            no = 0
            #print(name)
            d_specific = df.loc[df['influencer'] == name]
            # print(group['follow'])
            for i in d_specific['follow']:
                # print(i)
                if i == 'Ναι':
                    yes += 1
                else:
                    no += 1
            #print(yes)
            #print(no)
            rating = rating + ([(counter_influencers, 'yes')] * yes + [(counter_influencers, 'no')] * no)
            counter_influencers += 1
        score.append(fleiss_kappa(rating, number_of_annotators))
        number_of_annotators += 1
        myratings.append(rating)

    print(myratings)
    print(score)
    print('Fleiss Kappa final result is: ',sum(score) / len(score))

    """
    myratings = []
    counter_influencers = 1
    for name,group in df_grouped:
        print('name with 3', name)
        yes = 0
        no = 0
        print(name)
        print(group['follow'])
        c = 0
        for i in group['follow']:
            if c <5:
                #print(i)
                if i=='Ναι':
                    yes+=1
                else:
                    no+=1
            else:
                break
            c+=1
        print(yes)
        print(no)
        myratings = myratings + ([(counter_influencers,'yes')] * yes + [(counter_influencers,'no')] * no)
        counter_influencers += 1
    print(myratings)
    print(type(myratings))
    ratings = [(1, 'yes')] * 10 + [(1, 'no')] * 0 + \
              [(2, 'yes')] * 8 + [(2, 'no')] * 2 + \
              [(3, 'yes')] * 9 + [(3, 'no')] * 1 + \
              [(4, 'yes')] * 0 + [(4, 'no')] * 10 + \
              [(5, 'yes')] * 7 + [(5, 'no')] * 3
    print(ratings)

    fleiss_kappa(myratings, 3)
    """


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

    # print age groups and counts
    # print(df['age'].value_counts())

    # get list of names from our own collections
    influencers_names = get_influencers_names()
    # sort values
    # df = df.sort_values(by=['influencer'])
    # specific changes
    # df['influencer'] = df['influencer'].replace('Ronnie Coleman', 'ronniecoleman8')
    # df['influencer'] = df['influencer'].replace('flex_luis', 'flex_lewis')
    # df['influencer'] = df['influencer'].replace('willdabeast_', 'willdabeast__')
    # df['age'] = df['age'].replace('9999999999999999999999', '27')
    # replace ' "' with '"'
    df['influencer'] = df['influencer'].str.strip()
    # lowercase
    df['influencer'] = df['influencer'].str.lower()
    # keep only influencers inside retrieved collection
    df = df[df['influencer'].isin(influencers_names)]

    # # print whole dataframe values
    # print(df)

    # # print how many times each influencer was evaluated
    print(df['influencer'].value_counts())

    #Calculate the fleiss_kappa score
    preprocess_for_fleiss_kappa(df)

    # changes Yes and No to 1 and 0
    yes_no_dict = {'Ναι': 1, 'Όχι': 0}
    df = df.replace({"follow": yes_no_dict})

    df.to_csv('../../data/complete_csv_of_all_of_my_influencers.csv')

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

    # round decimals
    df_new = df_new.round(decimals=2)

    # create dataset with mean values
    df_new.to_csv('../../data/dataset_with_mean_values_to_pass_to_mongodb.csv')

    # pass dataframe to mongodb
    update_questionnaire_answers(df_new)


# get questionnaire information
get_questionnaire_answers()

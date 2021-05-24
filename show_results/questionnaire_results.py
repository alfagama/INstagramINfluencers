import pandas as pd
import plot_results
import matplotlib.pyplot as plt
from collections import Counter

# Options for pandas -----
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def read_and_sample_data():
    # reads data/category_columns_dataset.csv
    dataset = pd.read_csv("final_questionnaire.csv",
                          sep=',',
                          header=0,
                          skiprows=0)
    print('Dataset size is: ', len(dataset))
    print(dataset.head(5))

    #Convert "Ναι / Οχι" responses in Follow-Don't Follow
    dataset['follow'] = dataset['follow'].apply(lambda x: 'Follow' if x=='Όχι' else 'Don\'t follow')

    # Convert "Άντρας / Γυναίκα" responses in Male-Female
    dataset['gender'] = dataset['gender'].apply(lambda x: 'Male' if x == 'Άντρας' else 'Female')
    print(dataset.head(5))

    print(dataset.columns)
    print(dataset.shape)

    categorical_columns = ['name', 'gender', 'follow', 'reasons']
    #Convert all string values to numeric
    for x in dataset.columns:
        if x not in categorical_columns:
            dataset[x] = pd.to_numeric(dataset[x], errors='coerce')

    # Drop rows with age <0 and >100
    dataset.drop(dataset[dataset['age'] < 0].index, inplace=True)
    dataset.drop(dataset[dataset['age'] > 100].index, inplace=True)
    print(dataset.shape)

    # Drop examples (if any) that may contain NaN features
    # ---------------------------------------------------------------
    dataset.dropna(inplace=True)
    print(dataset.head(6))

    return dataset



def cluster_by_gender(dataset):

    # set the index to be the gender
    dataset.set_index(keys=['gender'], drop=False, inplace=True)

    # split to male/female dataframes
    male = dataset.loc[dataset.gender == 'Male']
    female = dataset.loc[dataset.gender == 'Female']

    print(male.shape)
    print(female.shape)

    # find the percentages of follow/unfollow
    male_follow = male.loc[male.follow == 'Follow']
    female_follow = female.loc[female.follow == 'Follow']

    #find the percentages for m/f
    clustering = [len(male)/len(dataset),len(female)/len(dataset)]
    print(clustering)

    info = []
    info.append(['male', len(male), len(male_follow)])
    info.append(['female', len(female), len(female_follow)])

    #Plot the pies
    plot_results.plot_pie(clustering, info, ['Men','Women'])

df = read_and_sample_data()
cluster_by_gender(df)
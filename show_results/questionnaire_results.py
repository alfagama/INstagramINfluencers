import pandas as pd
import plot_results
from dataset_creation import read_data
import os.path

# Options for pandas -----
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def read_questionnaire():
    # reads data/category_columns_dataset.csv
    dataset = pd.read_csv("final_questionnaire.csv",
                          sep=',',
                          header=0,
                          skiprows=0)
    print('Dataset size is: ', len(dataset))
    print(dataset.head(5))

    #Convert "Ναι / Οχι" responses in Follow-Don't Follow
    dataset['follow'] = dataset['follow'].apply(lambda x: 'Y' if x=='Ναι' else 'N')

    # Convert "Άντρας / Γυναίκα" responses in Male-Female
    dataset['gender'] = dataset['gender'].apply(lambda x: 'Male' if x == 'Άντρας' else 'Female')
    #print(dataset.head(5))

    print(dataset.shape)

    categorical_columns = ['name', 'gender', 'follow', 'reasons','category']
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
    #dataset.dropna(inplace=True)
    print(dataset.head(5))

    return dataset

def write_category_of_influencer_in_questionnaire():
    df = pd.read_csv("questionnaire.csv",
                          sep=',',
                          header=0,
                          skiprows=0)
    print('Dataset size is: ', len(df))
    categories = []
    for i in df['name'].tolist():
        name = i.lower()
        name = name.replace(" ", "")
        category = read_data.get_influencer_category(name)
        print(name)
        #print(category)
        categories.append(category)
        """
        if category:
            print(category)
            categories.append(category)
        """
    df["category"] = categories
    print(len(categories))
    df.to_csv('final_questionnaire.csv', index=False)


def cluster_by_gender(dataset):
    print("Cluster by gender")
    # set the index to be the gender
    dataset.set_index(keys=['gender'], drop=False, inplace=True)

    # split to male/female dataframes
    male = dataset.loc[dataset.gender == 'Male']
    female = dataset.loc[dataset.gender == 'Female']

    # find the percentages of follow/unfollow
    male_follow = male.loc[male.follow == 'Y']
    female_follow = female.loc[female.follow == 'Y']

    #find the percentages for m/f
    clustering = [len(male)/len(dataset),len(female)/len(dataset)]
    #print(clustering)

    info = []
    info.append(['male', len(male), len(male_follow)])
    info.append(['female', len(female), len(female_follow)])

    #Plot the pies
    plot_results.plot_pie(clustering, info, ['Men','Women'])

    #Create the respective dataframes in order to use them in the app
    gender_df = pd.DataFrame( {'Sex': ['Male', 'Female'], 'Counter': [len(male),len(female)]})
    willing_to_follow_male_df = pd.DataFrame({'Willing to follow': ['Yes', 'No'], 'Counter': [len(male_follow), len(male)-len(male_follow)]})
    willing_to_follow_female_df = pd.DataFrame({'Willing to follow': ['Yes', 'No'], 'Counter': [len(female_follow), len(female)-len(female_follow)]})

    return gender_df, willing_to_follow_male_df, willing_to_follow_female_df



def show_reasons(df):
    print("Reasons")
    follow_df = df.loc[df['follow'] == 'Y']
    print(follow_df.shape)
    reasons = follow_df.reasons.value_counts(sort=True)# Do we want to keep only px top-10??? .nlargest(10)

    # Plot the pie
    plot_results.plot_pie(reasons.values, [], reasons.index)

    total_reasons_df = pd.DataFrame({'Reason': reasons.index, 'Counter': reasons.values})
    #print(total_reasons_df)


    #Reasons per category
    follow_df.dropna(inplace=True)
    print(follow_df.shape)

    # Group the dataframe by category
    grouped = follow_df.groupby('category')

    grouped_lists = grouped["reasons"].apply(list)
    #count = follow_df.groupby(['reasons']).count()
    print(grouped_lists)
    """
    grouped_lists = grouped_lists.reset_index()
    print(grouped_lists)
    grouped_lists.to_csv('reasons_per_category.csv', index=False)
    """

    for name, group in grouped:
        print(name)
        #print(group['reasons'].value_counts())
        df = group['reasons'].value_counts().rename_axis('reasons').reset_index(name='counts')

        # Write the dataframe with reasons/counts columns for each category
        df.to_csv(name+'.csv', index=False)

    return total_reasons_df


if __name__ == '__main__':
    if os.path.isfile('final_questionnaire.csv'):
        pass
    elif os.path.isfile('questionnaire.csv'):
        write_category_of_influencer_in_questionnaire()

    df = read_questionnaire()
    cluster_by_gender(df)
    show_reasons(df)



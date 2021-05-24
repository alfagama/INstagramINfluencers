from dataset_creation.read_data import get_influencer_info
import plot_results
import matplotlib.pyplot as plt
import numpy
import numpy as np


def cluster_by_gender(dataset):

    # set the index to be the sex
    dataset.set_index(keys=['sex'], drop=False, inplace=True)

    # split to male/female dataframes
    male = dataset.loc[dataset.sex == 'm']
    female = dataset.loc[dataset.sex == 'f']

    #print(male.shape)
    #print(female.shape)

    # find the percentages of follow/unfollow
    male_follow = male.loc[male.follow_probability >= 0.5]
    female_follow = female.loc[female.follow_probability >= 0.5]

    #find the percentages for m/f
    clustering = [len(male)/len(dataset),len(female)/len(dataset)]

    info = []
    info.append(['male', len(male), len(male_follow)])
    info.append(['female', len(female), len(female_follow)])

    #Plot the pies
    plot_results.plot_pie(clustering, info, ['Men','Women'])


def store_category_info(name, number, follows):
    info = []
    info.append(name)
    info.append(number)
    info.append(follows)
    return info


def cluster_by_category(dataset):
    #print(dataset.head(5))

    # set the index to be the sex
    dataset.set_index(keys=['category'], drop=False, inplace=True)

    #Group the dataframe by category
    grouped = dataset.groupby(dataset.category)

    #Get all category names and counter
    categories = []
    counter = []
    map = []

    for name, group in grouped:
        categories.append(name)
        counter.append(len(group))
        follow = group.loc[group.follow_probability >= 0.5]
        info = store_category_info(name, len(group), len(follow))
        map.append(info)

    # Plot the pies
    plot_results.plot_pie(counter, map, categories)


dataset = get_influencer_info()
cluster_by_gender(dataset)
cluster_by_category(dataset)

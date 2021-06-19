import pymongo
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import collections
from mlxtend.frequent_patterns import fpgrowth
import plotly
import plotly.express as px
from sklearn import metrics


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


#def hashtags_distribution():


def get_top_features_cluster(tf_idf_array, prediction, n_feats):
    labels = np.unique(prediction)
    dfs = []
    for label in labels:
        id_temp = np.where(prediction==label) # indices for each cluster
        x_means = np.mean(tf_idf_array[id_temp], axis = 0) # returns average score across cluster
        sorted_means = np.argsort(x_means)[::-1][:n_feats] # indices with top 20 scores
        features = tfidf.get_feature_names()
        best_features = [(features[i], x_means[i]) for i in sorted_means]
        df = pd.DataFrame(best_features, columns = ['features', 'score'])
        dfs.append(df)
    return dfs



def get_post_hashtags():
    """
    Gets a dataframe with the description of posts grouped by influencer's category
    :param: -
    :return posts_description_df: dataframe with posts' description
    """

    print('\nLoading posts description from MongoDB..')

    cursor = collection.aggregate([
        {'$group': {'_id': '$category',
                    'hashtags': {'$push': '$Posts.Hashtags'}}}
    ])

    posts_description_df = pd.DataFrame(list(cursor))
    posts_description_df.columns = ['category', 'hashtags']
    return posts_description_df


def get_top_keywords(data, clusters, labels, n_terms):
    df = pd.DataFrame(data.todense()).groupby(clusters).mean()

    for i, r in df.iterrows():
        print('\nCluster {}'.format(i))
        print(','.join([labels[t] for t in np.argsort(r)[-n_terms:]]))


def plot_2d():
    # Tf idf vectorize
    vectorizer = TfidfVectorizer()
    tfidf_hashtags = vectorizer.fit_transform(all_hashtags)
    #print(tfidf_hashtags.shape)

    # PCA to 2 dimensions
    pca = PCA(n_components=2)
    pca_hashtags = pca.fit_transform(tfidf_hashtags.toarray())
    #print(pca_hashtags.shape)

    dataset = pd.DataFrame(pca_hashtags, columns=['x', 'y'])
    merged_df = pd.concat([df.reset_index(drop=True), dataset], axis=1)
    merged_df = merged_df.dropna()
    print(merged_df)
    #dataset['hashtags'] = df['hashtags']

    #merged_df.to_csv('web_app/data_csv/hashtags/hashtags_2d_2.csv', index=False)
    plt.scatter(pca_hashtags[:, 0], pca_hashtags[:, 1], s=50, cmap='viridis')
    plt.show()


def kmeans():
    vectorizer = TfidfVectorizer()
    tfidf_hashtags = vectorizer.fit_transform(all_hashtags)

    df = pd.DataFrame(tfidf_hashtags.toarray(), columns=vectorizer.get_feature_names())

    # PCA to 2 dimensions
    pca = PCA(n_components=2)
    pca_hashtags = pca.fit_transform(tfidf_hashtags.toarray())
    print(pca_hashtags.shape)

    kmeans = KMeans(n_clusters=3, random_state=0).fit(pca_hashtags)
    print(len(kmeans.labels_))






df = get_post_hashtags()
#print(df)
all_hashtags = []
categories_list = []
list_for_df = []
# Create a list of strings (each string consists of each post's hashtags)
for hashtag_list in df['hashtags']:
    categories_list.append(df['category'])
    for influencer in hashtag_list:
        for post in influencer:
            if post:
                hashtag_string = ''
                for hashtag in post:
                    list_for_df.append(hashtag)
                    if hashtag_string == '':
                        hashtag_string = hashtag
                    else:
                        hashtag_string = hashtag_string + ' ' + hashtag
                all_hashtags.append(hashtag_string)


df = pd.DataFrame({'hashtags': list_for_df})  # create dataframe with a column that has all hashtags
df = df.drop_duplicates(subset=['hashtags'])
print(df)
plot_2d()





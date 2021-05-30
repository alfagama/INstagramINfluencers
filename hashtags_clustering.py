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

# MongoDB
uri = "mongodb://localhost:27017/"
# Mongo client
client = pymongo.MongoClient(uri)
# Import database by name
db = client.ININ
# Get collection from DB
CollectionName = 'myLeaderboards'
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




df = get_post_hashtags()

all_hashtags = []
''''for hashtag_list in df['hashtags']:
    print(type(hashtag_list))
    for influencer in hashtag_list:
        for post in influencer:
            if post: #check if list is not empty
                for hashtag in post:
                    all_hashtags.append(hashtag)'''

list_for_df = []
# Create a list of strings (each string consists of each post's hashtags)
for hashtag_list in df['hashtags']:
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


# Tf idf vectorize
vectorizer = TfidfVectorizer()
tfidf_hashtags = vectorizer.fit_transform(all_hashtags)

'''print(type(tfidf_hashtags))

df1 = pd.DataFrame(tfidf_hashtags.toarray(), columns=vectorizer.get_feature_names())
print(df1)
res = pd.concat([df, df1], axis=1)
print(res)'''
x=1
# PCA to 2 dimensions
sklearn_pca = PCA(n_components=2)
pca_hashtags = sklearn_pca.fit_transform(tfidf_hashtags.toarray())
print(type(pca_hashtags))
x=2
# K-means clustering
NUMBER_OF_CLUSTERS = 3
kmeans = KMeans(n_clusters=NUMBER_OF_CLUSTERS, max_iter=600, algorithm='auto')
kmeans.fit(pca_hashtags)
prediction = kmeans.predict(pca_hashtags)



'''fig, ax = plt.subplots()
ax.scatter(pca_hashtags[:, 0], pca_hashtags[:, 1], c=prediction, s=50, cmap='viridis')

for i, txt in enumerate(n):
    ax.annotate(txt, (z[i], y[i]))

plt.show()'''


plt.scatter(pca_hashtags[:, 0], pca_hashtags[:, 1], c=prediction, s=50, cmap='viridis')

centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=300, alpha=0.6)
plt.show()


print("Top terms per cluster:")
order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
print(order_centroids)
terms = vectorizer.get_feature_names()

for i in range(NUMBER_OF_CLUSTERS):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind])


'''word_positions = {v: k for k, v in vectorizer.vocabulary_.items()}
cluster_ids = set(prediction)

min_support = 0.3
dist_words = sorted(v for k, v in word_positions.items()) # distinct words in the vocabulary
for cluster_id in cluster_ids:
    print(f"FP-Growth results on Cluster {cluster_id} with min support {min_support}")
    tfidf = tfidf_hashtags[prediction == cluster_id]
    # encoded as binary "presence/absence" representation as required by mlxtend
    tfidf[tfidf > 0] = 1
    # df is a pandas sparse dataframe
    df = pd.DataFrame.sparse.from_spmatrix(tfidf, columns=dist_words)
    fset = fpgrowth(df, min_support=min_support, use_colnames=True).sort_values(by='support', ascending=False)
    print(fset, '\n')'''




#----------------------------------------------------------------------
'''TAGS_IN_CATEGORY = 3
model = KMeans(
    n_clusters=TAGS_IN_CATEGORY,
    init='k-means++',
    max_iter=5,
    n_init=1,
    verbose=True
)
groups = model.fit_predict(posts_coordinates)

centroids = model.cluster_centers_


ordered_centroids = model.cluster_centers_.argsort()[:, ::-1]
tags = vectorizer.get_feature_names()

for idx, centroids in enumerate(ordered_centroids):
    print("Centroid %s:" % idx)
    for centroid_tag in centroids[:TAGS_IN_CATEGORY]:
        print("#%s" % tags[centroid_tag])'''


#----------------------------------------------------------------------

''''tfidf = TfidfVectorizer(
    min_df = 5,
    max_df = 0.95,
    max_features = 8000,
    stop_words = 'english'
)
tfidf.fit(all_hashtags)
hashtags_tfidf = tfidf.transform(all_hashtags)
tf_idf_array = hashtags_tfidf.toarray()

#kmeans = KMeans(n_clusters=5).fit(hashtags_tfidf)
sklearn_pca = PCA(n_components=2)
Y_sklearn = sklearn_pca.fit_transform(tf_idf_array)
kmeans = KMeans(n_clusters=3, max_iter=600, algorithm = 'auto')
fitted = kmeans.fit(Y_sklearn)
prediction = kmeans.predict(Y_sklearn)

plt.scatter(Y_sklearn[:, 0], Y_sklearn[:, 1], c=prediction, s=50, cmap='viridis')

centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=300, alpha=0.6)
plt.show()

#get_top_keywords(all_hashtags, kmeans, tfidf.get_feature_names(), 10)

dfs = get_top_features_cluster(tf_idf_array, prediction, 15)'''''



import pymongo
from dataset_creation.preprocess_and_sentiment import *
import pandas as pd


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


def update_comments(comments, account_name, post_url):
    """
    Updates db with post's comments (deriving from scraper)
    !It should be run only once for each post, otherwise it will create duplicate posts!

    :param comments: dataframe with the comments of the post
    :param account_name: influencer name (string)
    :param post_url: url of the post
    :return: None
    """
    inc_number = 0
    for index, comment in comments.iterrows():
        # increment + 1
        inc_number = inc_number + 1
        # get preprocessed comment
        comment_spaces, comment_no_stopwords = preprocess_comment(comment['comment'])
        # get sentiment score from comment
        sentiment_score = get_sentiment(comment_no_stopwords)
        # update collection with comments
        collection.update_one(
            {
                'Codename': account_name,
                'Posts.URL': post_url
            },
            {
                '$push': {
                    'Posts.$.All Comments': {'comment_id': inc_number,
                                             'user': comment['user'],
                                             'comment': comment['comment'],
                                             'comment_no_stopwords': comment_no_stopwords,
                                             'comment_spaces': comment_spaces,
                                             'like': comment['like'],
                                             'sentiment_score': sentiment_score
                                             }
                }
            }
        )


def update_posts(accounts):
    """
    Updates db with account's posts (deriving from get history from crowdtangle)
    :param accounts: dataframe with the accounts
    :return: None
    """
    # print(account.columns)
    for index, post in accounts.iterrows():

        # If a post with this URL already exists in database, then continue with next one
        if collection.count_documents({'Posts.URL': post['URL']}, limit=1) != 0:
            print('Post with url ', post['URL'], ' already exists')
            continue
        # Get tags from all posts
        # hashtags = []
        try:
            hashtags = list({tag.strip("#") for tag in post['Description'].split() if tag.startswith("#")})
        except:
            hashtags = []
        # get preprocessed description
        description_without_hashtags, description_preprocessed = preprocess_description(str(post['Description']))
        # update collection with posts
        collection.update_one(
            {
                'Codename': post['User Name']
            },
            {
                '$push': {
                    'Posts': {'Followers at Posting': post['Followers at Posting'],
                              'Post Created': post['Post Created'],
                              'Post Created Date': post['Post Created Date'],
                              'Post Created Time': post['Post Created Time'],
                              'Type': post['Type'],
                              'Total Interactions': post['Total Interactions'],
                              'Likes': post['Likes'],
                              'Comments': post['Comments'],
                              'Views': post['Views'],
                              'URL': post['URL'],
                              'Link': post['Link'],
                              'Photo': post['Photo'],
                              'Title': post['Title'],  # not
                              'Description': post['Description'],
                              'description_without_hashtags': description_without_hashtags,
                              'description_preprocessed': description_preprocessed,
                              'Hashtags': hashtags,
                              'Image Text': post['Image Text'],
                              'Sponsor Id': post['Sponsor Id'],
                              'Sponsor Name': post['Sponsor Name'],
                              'Overperforming Score': post['Overperforming Score (weighted  ???  Likes 1x Comments 1x )']
                              }
                }
            }
        )


def update_questionnaire_answers(dataframe):
    """
    Updates mongoDB with questionnaire answers
    :param: -
    :return: -
    """
    # update collection with questionnaire answers
    for index, row in dataframe.iterrows():
        collection.update_one(
            {
                'Codename': row.name
            },
            {
                '$set': {
                    'likeable': row['????????????????'],
                    'creative': row['??????????????????????'],
                    'calm': row['??????????/???????????????????????????? ????????????????????????'],
                    'outgoing': row['????????????????????'],
                    'post_cohesion': row['????????????'],
                    'self_centered': row['?????????????????????? / ??????????????????'],
                    'short_tempered': row['????????????????'],
                    'professional': row['?????????????????? / ???????????? ??????????????????????????'],
                    'fitness_advice': row['?????????????????????????? ?????? ???????????? fitness'],
                    'general_advice': row['?????????????????????????? ?????? ?????????? ??????????????????????'],
                    'follow_probability': row['follow'],
                }
            }
        )


def update_demographics(dataframe):
    """
    Updates mongoDB with demographics (age, sex, marital status and category)
    :param: -
    :return: -
    """

    # update collection with questionnaire answers
    for index, row in dataframe.iterrows():
        collection.update_one(
            {
                'Codename': row['username']
            },
            {
                '$set': {
                    'sex': row['sex'],
                    'age': row['age'],
                    'marital_status': row['marital_status'],
                    'category': row['category']
                }
            }
        )


def get_post_description():
    """
    Gets a dataframe with the description of posts grouped by influencer's category
    :param: -
    :return posts_description_df: dataframe with posts' description
    """

    print('\nLoading posts description from MongoDB..')

    cursor = collection.aggregate([
        {'$group': {'_id': '$category',
                    'posts_description': {'$push': '$Posts.description_preprocessed'}}}
    ])

    posts_description_df = pd.DataFrame(list(cursor))
    return posts_description_df


def get_post_comments():
    """
    Gets a dataframe with the comments of posts grouped by influencer's category
    :param: -
    :return comments_df: dataframe with posts' comments
    """

    print('\nLoading post comments from MongoDB..')

    cursor = collection.aggregate([
        {'$group': {'_id': '$category',
                    'comments': {'$push': '$Posts.All Comments.comment_no_stopwords'}}}
    ])

    comments_df = pd.DataFrame(list(cursor))
    return comments_df


def get_post_comments():
    """
    Gets a dataframe with the comments of posts grouped by influencer's category
    :param: -
    :return comments_df: dataframe with posts' comments
    """

    print('\nLoading post comments from MongoDB..')

    cursor = collection.aggregate([
        {'$group': {'_id': '$category',
                    'comments': {'$push': '$Posts.All Comments.comment_no_stopwords'}}}
    ])

    comments_df = pd.DataFrame(list(cursor))
    return comments_df

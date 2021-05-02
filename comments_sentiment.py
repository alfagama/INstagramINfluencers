import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')  # do this once: grab the trained model from the web

# Create a SentimentIntensityAnalyzer object.
sid = SentimentIntensityAnalyzer()


def preprocess_comment(comment):
    """

    :param comment:  user comment from post (string)
    :return:  preprocessed user comment from post (string)
    """
    # preprocessing stage

    return comment


def get_sentiment(comment):
    """
    returns sentiment score
    :param comment: user comment from post (string)
    :return: sentiment_score: -1 for negative, 0 for neutral, 1 for positive (integer)
    :return: sentiment_score: 'negative' for negative, 'neutral' for neutral, 'positive' for positive (string)
    """
    # call preprocess_comment()
    comment = preprocess_comment(comment)
    # get polarity score for comment
    v_scores = sid.polarity_scores(comment['comment'])
    # define sentiment score (integer)
    sentiment_score = 1 if v_scores['compound'] > 0 else -1 if v_scores['compound'] < 0 else 0
    # define sentiment score (string)
    # sentiment_score = 'positive' if v_scores['compound'] > 0 else 'negative' if v_scores['compound'] < 0 else
    # 'neutral'

    return sentiment_score

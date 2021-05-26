import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import regex as re

# download('vader_lexicon')
nltk.download('vader_lexicon')  # do this once: grab the trained model from the web

# Create a SentimentIntensityAnalyzer object.
sid = SentimentIntensityAnalyzer()

# stopwords in egnlish
eng_stopwords = stopwords.words('english')


def preprocess_comment(comment):
    """
    returns comments after getting preprocessed
    :param comment:  user comment from post (string)
    :return:  comment_no_stopwords (string), comment_spaces (string)
    """

    # ### get comment with spaces between all emoji ###
    comment_spaces = ''
    for character in comment:
        if not str.isalpha(character) and character != ' ':
            try:
                if comment_spaces[-1] != ' ':
                    comment_spaces += ' '
                comment_spaces += character
                comment_spaces += ' '
            except:
                comment_spaces += character
        else:
            comment_spaces += character
    comment_spaces = re.sub(r"  ️", " ", comment_spaces)

    # ### get comment without stopwords, emoji, numbers -> plain text ###

    # lower text
    comment = comment.lower()
    # split into tokens
    comment = comment.split()

    comment = [token for token in comment
               if not token.startswith('http')
               if not token.startswith('#')
               if not token.startswith('@')
               if not token.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))
               if token.islower()
               ]

    #   We deTokenize here in order to use RE more efficinetly
    comment = TreebankWordDetokenizer().detokenize(comment)

    #   We use RE to remove any unwanted characters from the stings
    comment = re.sub(r'[0-9]', ' ', comment)
    comment = re.sub(r'[!@#$%^&*(){}=_;:"“”‘’?.>,<`~.\\\[\]\-]', ' ', comment)
    comment = re.sub(r"[']", ' ', comment)
    comment = re.sub(r"[⁦⁩]", ' ', comment)
    comment = re.sub(r"[/]", ' ', comment)
    comment = re.sub(r"\t", " ", comment)
    comment = re.sub(r"'\s+\s+'", " ", comment)
    comment = re.sub(r" ️", "", comment)
    comment = re.sub(r'\b\w{1,1}\b', '', comment)

    # Tokenized
    comment = comment.split()

    # Removed stop_words
    final_stop_words = [x for x in eng_stopwords]
    comment = [w for w in comment if w not in final_stop_words]

    # WordNetLemmatizer from the nltk library as a final step
    lemmatizer = WordNetLemmatizer()
    # tokens_lemmatized = [lemmatizer.lemmatize(l) for l in tokens_no_stop_words]
    #   We also decided to use pos_tagging to enhance our lemmatization model
    tokens_lemmatized = []
    for word, tag in pos_tag(comment):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        tokens_lemmatized.append(lemmatizer.lemmatize(word, pos))
    # return TreebankWordDetokenizer().detokenize(tokens_lemmatized)
    comment = TreebankWordDetokenizer().detokenize(tokens_lemmatized)
    # print comment to see results
    # print(comment)

    comment_no_stopwords = comment

    return comment_spaces, comment_no_stopwords


def preprocess_description(description):
    """
    returns description after getting preprocessed
    :param description:
    :return: description_preprocessed (string), description_without_hashtags (string)
    """
    # # lower text
    # description = description.lower()
    # split into tokens
    description = description.split()

    description_without_hashtags = [token for token in description
                                    if not token.startswith('http')
                                    if not token.startswith('#')
                                    if not token.startswith('@')
                                    # if token.islower()
                                    ]

    #   We deTokenize here in order to use RE more efficinetly
    description_without_hashtags = TreebankWordDetokenizer().detokenize(description_without_hashtags)

    #   We use RE to remove any unwanted characters from the stings
    description_preprocessed = description_without_hashtags
    description_preprocessed = re.sub(r'[0-9]', ' ', description_preprocessed)
    description_preprocessed = re.sub(r'[!@#$%^&*(){}=_;:"“”‘’?.>,<`~.\\\[\]\-]', ' ', description_preprocessed)
    description_preprocessed = re.sub(r"[']", ' ', description_preprocessed)
    description_preprocessed = re.sub(r"[⁦⁩]", ' ', description_preprocessed)
    description_preprocessed = re.sub(r"[/]", ' ', description_preprocessed)
    description_preprocessed = re.sub(r"\t", " ", description_preprocessed)
    description_preprocessed = re.sub(r"'\s+\s+'", " ", description_preprocessed)
    description_preprocessed = re.sub(r" ️", "", description_preprocessed)
    description_preprocessed = re.sub(r'\b\w{1,1}\b', '', description_preprocessed)

    # Tokenized
    description_preprocessed = description_preprocessed.split()

    # Remove emoji
    description_preprocessed = [token for token in description_preprocessed if token.islower()]

    # Removed stop_words
    final_stop_words = [x for x in eng_stopwords]
    description_preprocessed = [w for w in description_preprocessed if w not in final_stop_words]

    # WordNetLemmatizer from the nltk library as a final step
    lemmatizer = WordNetLemmatizer()
    # tokens_lemmatized = [lemmatizer.lemmatize(l) for l in tokens_no_stop_words]
    #   We also decided to use pos_tagging to enhance our lemmatization model
    tokens_lemmatized = []
    for word, tag in pos_tag(description_preprocessed):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        tokens_lemmatized.append(lemmatizer.lemmatize(word, pos))
    # return TreebankWordDetokenizer().detokenize(tokens_lemmatized)
    description_preprocessed = TreebankWordDetokenizer().detokenize(tokens_lemmatized)

    return description_without_hashtags, description_preprocessed


def get_sentiment(comment):
    """
    returns sentiment score
    :param comment: user comment from post (string)
    :return: sentiment_score: -1 for negative, 0 for neutral, 1 for positive (integer)
    OR
    :return: sentiment_score: 'negative' for negative, 'neutral' for neutral, 'positive' for positive (string)
    """
    # call preprocess_comment()
    # comment = preprocess_comment(comment['comment'])
    # get polarity score for comment
    v_scores = sid.polarity_scores(comment)
    # define sentiment score (integer)
    sentiment_score = 1 if v_scores['compound'] > 0 else -1 if v_scores['compound'] < 0 else 0
    # define sentiment score (string)
    # sentiment_score = 'positive' if v_scores['compound'] > 0 else 'negative' if v_scores['compound'] < 0 else
    # 'neutral'

    return sentiment_score

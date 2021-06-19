import re

# from dataset_creation.mongo import get_post_comments, get_post_description
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from web_app.funcs.db import Db

db = Db()


def wordCloud_posts(text, file_name, title):
    posts = ' '.join(map(str, text))
    words = re.findall(r'\b\S+\b', posts)
    temp_string = ' '.join(words)
    long_string = re.sub(r'\b\w{1,3}\b', '', temp_string)
    word(long_string, file_name, title)


def wordCloud_descriptions(text, file_name, title):
    words = re.findall(r'\b\S+\b', text)
    temp_string = ' '.join(words)
    long_string = re.sub(r'\b\w{1,3}\b', '', temp_string)
    word(long_string, file_name, title)


def word(text, file_name, title):
    # posts = ' '.join(map(str, text))
    # words = re.findall(r'\b\S+\b', posts)
    #
    # temp_string = ' '.join(words)
    # long_string = re.sub(r'\b\w{1,3}\b', '', temp_string)

    # stopwords_removal(long_string)
    # fig, (ax1, ax2) = plt.subplots(2)
    # wordcloud1 = WordCloud(collocations=True, width=1600, height=800, background_color="black").generate(long_string)
    wordcloud1 = WordCloud(collocations=True, width=2000, height=1000, background_color="black").generate(text)
    # # wordcloud2 = WordCloud(collocations=True).generate(long_string)
    # # subplot(1, 2, 1)
    # # subplot(1, 2, 2)
    # # plot the wordcloud object
    # # ax1.imshow(wordcloud1, interpolation='bilInear')
    # # ax2.imshow(wordcloud2, interpolation='bilInear')
    # # plt.axis('off')
    plt.figure(figsize=[20, 10])
    plt.imshow(wordcloud1.recolor(colormap='Pastel2', random_state=17), alpha=0.98,
               interpolation="bilinear")
    plt.axis("off")
    # plt.title(title)
    # plt.show()
    plt.savefig(file_name, transparent=True)
    # cloud.to_file('N.png'))

    import stylecloud

    # stylecloud.gen_stylecloud(text=long_string, icon_name='fas fa-grin', collocations=False,
    #                           size=800, output_name='gi.png')
    stylecloud.gen_stylecloud(text=text, icon_name='fas fa-grin', collocations=False,
                              size=800, output_name='gi.png')
    # stylecloud.show
    # Visualize word cloud in jupyter


def all_descriptions():
    """
    Post Descriptions
    :return: wordcloud for all descriptions of posts
    """
    data = db.get_posts()
    posts = ' '.join(map(str, data.Description.values))
    words = re.findall(r'\b\S+\b', posts)
    wordcloud1 = WordCloud(collocations=True, width=2000, height=1000, background_color="black").generate(
        ' '.join(words))
    plt.figure(figsize=[20, 10])
    plt.imshow(wordcloud1.recolor(colormap='Pastel2', random_state=17), alpha=0.98,
               interpolation="bilinear")
    plt.axis("off")
    plt.savefig('Description', transparent=True)
    # fig = plotly_wordcloud(' '.join(words))
    plt.show()


def all_comments():
    """
    All comments for each Influencer
    :return: wordcloud with all comments
    """
    comments_list = []
    comments = db.get_post_comments()
    for index, row in comments.iterrows():
        comments_list = []
        for influencer in row['comments']:
            for post in influencer:
                for something in post:
                    if something:
                        comments_list.append(something)
    posts = ' '.join(map(str, comments_list))
    words = re.findall(r'\b\S+\b', posts)
    wordcloud1 = WordCloud(collocations=True, width=2000, height=1000, background_color="black").generate(
        ' '.join(words))
    plt.figure(figsize=[20, 10])
    plt.imshow(wordcloud1.recolor(colormap='Pastel2', random_state=17), alpha=0.98,
               interpolation="bilinear")
    plt.axis("off")
    plt.savefig('All_comments', transparent=True)
    # fig = plotly_wordcloud(' '.join(words))
    plt.show()


def word_clouds_per_category():
    # data = db.get_posts()
    # data2 = db.get_post_description()

    comments = db.get_post_comments()
    descriptions = db.get_post_description()

    tmp = {}
    for index, row in descriptions.iterrows():
        tmp[row['_id']] = ''
        for inner_index, row_value in enumerate(row['description']):
            try:
                tmp[row['_id']] += ' ' + " ".join(filter(None, row_value))
            except:
                # tmp[row['_id']] += ' ' + " ".join(row_value)
                print(type(row_value), row_value)

    for category, descriptions in tmp.items():
        wordCloud_descriptions(descriptions, category + '_description', category + ' Description')

    print(comments)
    pilates_list = []
    yoga_list = []
    nutrition_list = []
    athlete_list = []
    body_building_list = []
    fitness_list = []
    dance_list = []

    for index, row in comments.iterrows():
        comments_list = []
        for influencer in row['comments']:
            for post in influencer:
                for something in post:
                    if something:
                        comments_list.append(something)
        if row['_id'] == 'pilates':
            pilates_list = comments_list
            wordCloud_posts(pilates_list, 'pilates_comments', 'pilates Comments')
        if row['_id'] == 'yoga':
            yoga_list = comments_list
            wordCloud_posts(yoga_list, 'yoga_comments', 'yoga Comments')
        if row['_id'] == 'nutrition':
            nutrition_list = comments_list
            wordCloud_posts(nutrition_list, 'nutrition_comments', 'nutrition Comments')
        if row['_id'] == 'athlete':
            athlete_list = comments_list
            wordCloud_posts(athlete_list, 'athlete_comments', 'athlete Comments')
        if row['_id'] == 'body_building':
            body_building_list = comments_list
            wordCloud_posts(body_building_list, 'body_building_comments', 'body_building Comments')
        if row['_id'] == 'fitness_model':
            fitness_list = comments_list
            wordCloud_posts(fitness_list, 'fitness_model_comments', 'fitness_model Comments')
        if row['_id'] == 'dance':
            dance_list = comments_list
            wordCloud_posts(dance_list, 'dance_comments', 'dance Comments')


if __name__ == '__main__':
    choice = input('Enter your preference:')
    if choice == 'all_comments':
        all_comments()
    if choice == 'all_descriptions':
        all_descriptions()
    if choice == 'word_clouds_per_category':
        word_clouds_per_category()

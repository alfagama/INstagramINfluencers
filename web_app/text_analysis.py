import json

import plotly
import plotly.express as px
import plotly.graph_objs as go
from flask import Flask  # Flask -> class name
from flask import jsonify
from flask import render_template
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from web_app.funcs.db import Db

# declare application. initialize with Flask instance/class
app = Flask(__name__, template_folder='static/stylesheets')

# get MongoDB instance
db = Db()
import re


def plotly_wordcloud(text):
    # wc = WordCloud(stopwords=set(STOPWORDS),
    #                max_words=200,
    #                max_font_size=100)
    # wc.generate(text)

    # posts = ' '.join(map(str, text))
    # words = re.findall(r'\b\S+\b', posts)
    #
    # temp_string = ' '.join(words)
    long_string = re.sub(r'\b\w{1,3}\b', '', text)

    wordcloud1 = WordCloud(collocations=True, max_words=200, max_font_size=50, stopwords=set(STOPWORDS),
                           width=1600, height=800, background_color="black").generate(long_string)

    word_list = []
    freq_list = []
    fontsize_list = []
    position_list = []
    orientation_list = []
    color_list = []

    for (word, freq), fontsize, position, orientation, color in wordcloud1.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)

    # get the positions
    x = []
    y = []
    for i in position_list:
        x.append(i[0])
        y.append(i[1])

    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i * 100)

    print('\n'.join(word_list) )
    trace = go.Scatter(x=x,
                       y=y,
                       textfont=dict(size=new_freq_list,
                                     color=color_list),
                       hoverinfo='text',
                       hovertext=['{0} {1}'.format(w, f) for w, f in zip(word_list, freq_list)],
                       mode='text',
                       text=word_list
                       )

    layout = go.Layout({ 'title': "jkdsajkhsdahkjdasjhkdaskjhbdsahjsdaw",
        'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
        'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}})

    fig = go.Figure(data=[trace], layout=layout)

    return fig


def stopwords_removal(long_string):
    wordcloud = WordCloud(stopwords=STOPWORDS,
                          collocations=True).generate(long_string)

    # plot the wordcloud object
    plt.imshow(wordcloud, interpolation='bilInear')
    plt.axis('off')
    plt.show()


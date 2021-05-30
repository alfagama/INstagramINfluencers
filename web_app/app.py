from flask import Flask  # Flask -> class name
from flask import render_template, request
from flask import jsonify
import os
from web_app.funcs.db import Db
import plotly
import plotly.express as px
import pandas as pd
import json
import collections


# declare application. initialize with Flask instance/class
app = Flask(__name__, template_folder='static/stylesheets')

# get MongoDB instance
db = Db()


@app.route('/wordclouds')
def word_loud():
    return render_template('wordclouds.html')


# declare route # can also declare methods to accept. like -> 'GET'
@app.route("/", methods=['GET'])
@app.route("/static/stylesheets/home.html")
def index():
    influencer_count_by_category_df = db.find_influencers_count_by_category()
    #fig = px.bar(influencer_count_by_category_df, x='_id', y='count', barmode='group')
    fig = px.pie(influencer_count_by_category_df, values='count', names='_id', title='Percentage of influencers from each category')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("home.html", graph=graphJSON)


@app.route("/static/stylesheets/statistics.html")
def statistics():
    '''if request.method == "POST":
        app.logger.warning('dfsdfdsfsdfsd')
        category = request.form["category"]
        app.logger.warning(category)'''
    df = db.get_date_frequency()
    #fig = px.line(df, x="date", y="frequency", title='Posts frequency by date')
    fig = px.bar(df, x="date", y="frequency", title="Posts frequency by date")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("statistics.html", graph=graphJSON)


@app.route("/static/stylesheets/clustering.html")
def clustering():
    df = db.get_post_hashtags()

    all_hashtags = []
    for hashtag_list in df['hashtags']:
        for influencer in hashtag_list:
            for post in influencer:
                all_hashtags.append(post)

    print(all_hashtags)
    posts_hashtag_count = []

    for list in all_hashtags:
        posts_hashtag_count.append(len(list))

    counter = collections.Counter(posts_hashtag_count)
    counter_df = pd.DataFrame.from_dict(counter, orient='index').reset_index()
    counter_df = counter_df.rename(columns={'index': 'Number of Hashtags', 0: 'Number of Posts'})

    fig = px.bar(counter_df, x="Number of Hashtags", y="Number of Posts", title="Hashtags Distribution")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("clustering.html", number_of_hashtags=graphJSON)


@app.route("/todo/<importance_val>")
def get_todo(importance_val):
    todos = db.find('todos', {"importance": int(importance_val)})
    return jsonify(todos)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5110)

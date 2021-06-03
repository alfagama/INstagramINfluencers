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
from show_results.questionnaire_results import read_questionnaire, cluster_by_gender, show_reasons


# declare application. initialize with Flask instance/class
app = Flask(__name__, template_folder='static/stylesheets')

# get MongoDB instance
db = Db()

# @app.route("/", methods=['GET'])
# @app.route('/wordclouds')
# def word_loud():
#     return render_template('wordclouds.html')
#

# declare route # can also declare methods to accept. like -> 'GET'
@app.route("/", methods=['GET'])
@app.route("/home.html")
def index():
    influencer_count_by_category_df = db.get_influencers_count_by_category()
    #fig = px.bar(influencer_count_by_category_df, x='_id', y='count', barmode='group')
    fig = px.pie(influencer_count_by_category_df, values='count', names='_id', title='Percentage of influencers from each category')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("home.html", graph=graphJSON)


@app.route("/topic_modeling.html")
def topic_modeling():
    return render_template("topic_modeling.html")


@app.route("/machine_learning.html")
def machine_learning():
    return render_template("machine_learning.html")

@app.route("/clustering.html")
def clustering():
    return render_template("clustering.html")

@app.route("/wordclouds.html")
def wordclouds():
    return render_template("wordclouds.html")

@app.route("/statistics.html")
def statistics():

    # --------------- Number of influencer by category ---------------
    influencer_count_by_category_df = db.get_influencers_count_by_category()
    fig = px.pie(influencer_count_by_category_df, values='count', names='_id',
                 title='Percentage of influencers from each category')
    influencer_count_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Number of posts per day -----------------
    day_freq_df = db.get_frequency_per_day()
    fig = px.bar(day_freq_df, x="day", y="posts",
                 labels={
                     "day": "Day",
                     "posts": "No. of posts",
                 },
                 title="No. of posts by day")
    day_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Number of posts per hour -----------------
    hour_freq_df = db.get_frequency_per_hour()
    fig = px.bar(hour_freq_df, x="time", y="posts",
                 labels={
                     "time": "Time",
                     "posts": "No. of posts",
                 },
                 title="No. of posts by hour")
    hour_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("statistics.html", influencerCountGraphJSON=influencer_count_graphjson,
                           dayGraph=day_graphjson, hourGraph=hour_graphjson)


@app.route("/questionaire_statistics.html")
def questionaire_statistics():
    df = read_questionnaire()

    gender_df, willing_to_follow_male_df, willing_to_follow_female_df = cluster_by_gender(df)
    fig = px.pie(gender_df, values='Counter', names='Sex', title='Annotators - Gender Percentage')
    hour_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    fig = px.pie(willing_to_follow_male_df, values='Counter', names='Willing to follow', title='Male Annotators - Probability of Following')
    willing_to_follow_male_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    fig = px.pie(willing_to_follow_female_df, values='Counter', names='Willing to follow', title='Female Annotators - Probability of Following')
    willing_to_follow_female_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    #total_reasons_df = show_reasons(df)
    return render_template("questionaire_statistics.html", hour_graph=hour_graphjson, willing_to_follow_male_graph=willing_to_follow_male_graphjson,
                           willing_to_follow_female_graph=willing_to_follow_female_graphjson)


@app.route("/hashtags.html")
def hashtags():

    # ----------------- Hashtags distribution -----------------
    df = db.get_hashtags_distribution()
    fig = px.bar(df, x="Number of Hashtags", y="Number of Posts",
                 labels={
                     "Number of Hashtags": "No. of hashtags",
                     "Number of Posts": "No. of posts",
                 },
                 title="Hashtags Distribution")
    hashtags_distribution_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Top hashtag frequencies -----------------
    df = db.get_top_hashtag_frequency()
    fig = px.bar(df, x="hashtag", y="count",
                 labels={
                     "hashtag": "Hashtags",
                     "count": "No. of posts",
                 },
                 title="Most Frequent Hashtags")
    hashtags_frequency_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Total number of hashtags from each category -----------------
    df = db.get_no_of_hashtags_by_category()
    fig = px.bar(df, x="category", y="hashtags_count",
                 labels={
                     "category": "Category",
                     "hashtags_count": "No. of total hashtags",
                 },
                 title="No. of total hashtags by category")
    no_of_hashtags_by_category_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Percentage of hashtags from each category -----------------
    df = db.get_percentage_of_hashtags_by_category()
    fig = px.bar(df, x="category", y="hashtags_percentage",
                 labels={
                     "category": "Category",
                     "hashtags_percentage": "Percentage of hashtags",
                 },
                 title="Percentage of hashtags by category")
    percentage_of_hashtags_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Hashtags engagement distribution -----------------
    df = db.get_hashtags_engagement_distribution()
    fig = px.line(df, x="hashtag_count", y="engagement",
                 labels={
                     "hashtag_count": "Category",
                     "engagement": "Percentage of hashtags",
                 },
                 title="Percentage of hashtags by category")
    hashtags_engagement_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("hashtags.html", hashtags_distribution=hashtags_distribution_graphjson, hashtags_frequency=hashtags_frequency_graphjson,
                           no_of_hashtags_by_category=no_of_hashtags_by_category_graphjson, percentage_of_hashtags=percentage_of_hashtags_graphjson,
                           hashtags_engagement=hashtags_engagement_graphjson)


@app.route("/todo/<importance_val>")
def get_todo(importance_val):
    todos = db.find('todos', {"importance": int(importance_val)})
    return jsonify(todos)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5110)

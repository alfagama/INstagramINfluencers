import json
from PIL import Image
import plotly.graph_objs as go
from wordcloud import WordCloud, STOPWORDS
import plotly
import plotly.express as px
from flask import Flask  # Flask -> class name
from flask import jsonify
from flask import render_template
from web_app.funcs.db import Db
from text_analysis import plotly_wordcloud, stopwords_removal
from show_results.questionnaire_results import read_questionnaire, cluster_by_gender, show_reasons
import re
import pandas as pd


# declare application. initialize with Flask instance/class
app = Flask(__name__, template_folder='static/stylesheets')
import matplotlib.pyplot as plt
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
    data = db.get_posts()
    posts = ' '.join(map(str, list(data.Description.values)))
    words = re.findall(r'\b\S+\b', posts)
    fig = plotly_wordcloud(' '.join(words))
    graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('wordclouds.html', word_cloud=graphJSON2)


@app.route("/statistics.html")
def statistics():

    # --------------- Number of influencer by category ---------------
    influencer_count_by_category_df = pd.read_csv("data_csv/statistics/influencers_count_by_category.csv", sep=',', header=0, skiprows=0)
    fig = px.pie(influencer_count_by_category_df, values='count', names='_id',
                 title='Percentage of influencers from each category')
    influencer_count_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Number of posts per day -----------------
    day_freq_df = pd.read_csv("data_csv/statistics/post_frequency_per_day.csv", sep=',', header=0, skiprows=0)
    fig = px.bar(day_freq_df, x="day", y="posts",
                 labels={
                     "day": "Day",
                     "posts": "No. of posts",
                 },
                 title="No. of posts by day")
    day_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Number of posts per hour -----------------
    hour_freq_df = pd.read_csv("data_csv/statistics/post_frequency_per_hour.csv", sep=',', header=0, skiprows=0)
    fig = px.bar(hour_freq_df, x="time", y="posts",
                 labels={
                     "time": "Time",
                     "posts": "No. of posts",
                 },
                 title="No. of posts by hour")
    hour_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    #df = db.find_all()
    #df['Likes'] = df['Likes'].str.replace(',', '').astype(float)
    #df['Views'] = df['Views'].str.replace(',', '').astype(float)
    #df['Total Posts'] = pd.to_numeric(df['Total Posts'], errors='coerce')

    #likes_per_category_sex = df.groupby(['category', 'sex'], as_index=False)['Likes'].sum()
    #views_per_category_sex = df.groupby(['category', 'sex'], as_index=False)['Views'].sum()
    #posts_per_category_sex = df.groupby(['category', 'sex'], as_index=False)['Total Posts'].sum()
    #likes_per_category = df.groupby(['category'], as_index=False)['Likes'].sum()

    # category = df['category'].value_counts().to_frame().reset_index()
    # category.rename(columns={'index': 'category', 'category': 'frequency'}, inplace=True)
    #
    # maritalStatus = df['marital_status'].value_counts().to_frame().reset_index()
    # maritalStatus.rename(columns={'index': 'marital_status', 'marital_status': 'frequency'}, inplace=True)
    #
    # age = df['age'].value_counts().to_frame().reset_index()
    # age.rename(columns={'index': 'age', 'age': 'frequency'}, inplace=True)
    #
    # sex = df['sex'].value_counts().to_frame().reset_index()
    # sex.rename(columns={'index': 'sex', 'sex': 'frequency'}, inplace=True)
    #
    # fig = px.bar(category, x='category', y='frequency')
    # category_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #
    # fig = px.bar(maritalStatus, x='category', y='frequency')
    # maritalStatus_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #
    # fig = px.bar(age, x='age', y='frequency')
    # maritalStatus_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #
    # fig = px.bar(sex, x='sex', y='frequency')
    # maritalStatus_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #
    # fig = px.bar(maritalStatus, x='category', y='frequency')
    # maritalStatus_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #

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
    df = pd.read_csv("data_csv/hashtags/hashtag_distribution.csv", sep=',', header=0, skiprows=0)
    fig = px.bar(df, x="Number of Hashtags", y="Number of Posts",
                 labels={
                     "Number of Hashtags": "No. of hashtags",
                     "Number of Posts": "No. of posts",
                 },
                 title="Hashtags Distribution")
    hashtags_distribution_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Top hashtag frequencies -----------------
    df = pd.read_csv("data_csv/hashtags/top_hashtag_frequency.csv", sep=',', header=0, skiprows=0).head(25)
    fig = px.bar(df, x="hashtag", y="count",
                 labels={
                     "hashtag": "Hashtags",
                     "count": "No. of posts",
                 },
                 title="Most Frequent Hashtags")
    hashtags_frequency_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Total number of hashtags from each category -----------------
    df = pd.read_csv("data_csv/hashtags/no_of_hashtags_by_category.csv", sep=',', header=0, skiprows=0)
    fig = px.bar(df, x="category", y="hashtags_count",
                 labels={
                     "category": "Category",
                     "hashtags_count": "No. of total hashtags",
                 },
                 title="No. of total hashtags by category")
    no_of_hashtags_by_category_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Percentage of hashtags from each category -----------------
    df = pd.read_csv("data_csv/hashtags/percentage_of_hashtags_by_category.csv", sep=',', header=0, skiprows=0)
    fig = px.bar(df, x="category", y="hashtags_percentage",
                 labels={
                     "category": "Category",
                     "hashtags_percentage": "Percentage of hashtags",
                 },
                 title="Percentage of hashtags by category")
    percentage_of_hashtags_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Hashtags engagement distribution -----------------
    df = pd.read_csv("data_csv/hashtags/hashtags_engagement_distribution.csv", sep=',', header=0, skiprows=0)
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

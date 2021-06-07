import json

import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objs as go
from flask import Flask  # Flask -> class name
from flask import jsonify
from flask import render_template

from web_app.funcs.db import Db

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
    influencer_count_by_category_df = pd.read_csv("data_csv/statistics/influencers_count_by_category.csv", sep=',', header=0, skiprows=0)
    fig = px.bar(influencer_count_by_category_df, x='_id', y='count', barmode='group')
    fig = px.pie(influencer_count_by_category_df, values='count', names='_id', title='Percentage of influencers from each category')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("home.html", graph=graphJSON)


@app.route("/topic_modeling.html")
def topic_modeling():
    return render_template("topic_modeling.html")


@app.route("/machine_learning.html")
def machine_learning():
    f_importance_q = pd.read_csv("static/predictions/f_importance_questionnaire.csv", sep=',',
                                            header=0, skiprows=0)
    fig = go.Figure(data=[go.Bar(
        x=f_importance_q['feature'],
        y=f_importance_q['score'],
        marker_color='rgb(0, 179, 179)')
    ])

    fig.update_layout(title='Feature Importance - Questionnaire', title_x=0.5,
                      xaxis=dict(title='Feautures', showgrid=False, linecolor='rgb(204, 204, 204)'),
                      yaxis=dict(title='Score', showgrid=True, linecolor='rgb(204, 204, 204)', showline=True,
                                 gridcolor="rgb(204, 204, 204)"),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )
    f_importance_q_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    #-----------------------------------------------------------------------------------------
    f_importance_m = pd.read_csv("static/predictions/f_importance_mongo.csv", sep=',',
                                 header=0, skiprows=0)
    fig = go.Figure(data=[go.Bar(
        x=f_importance_m['feature'],
        y=f_importance_m['score'],
        marker_color='rgb(0, 179, 179)')
    ])

    fig.update_layout(title='Feature Importance - Crowdtangle', title_x=0.5,
                      xaxis=dict(title='Features', showgrid=False, linecolor='rgb(204, 204, 204)'),
                      yaxis=dict(title='Score', showgrid=True, linecolor='rgb(204, 204, 204)', showline=True,
                                 gridcolor="rgb(204, 204, 204)"),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )
    f_importance_m_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("machine_learning.html", f_importance_q=f_importance_q_graphjson, f_importance_mongo=f_importance_m_graphjson)


@app.route("/clustering.html")
def clustering():
    return render_template("clustering.html")


@app.route("/wordclouds.html")
def wordclouds():
    return render_template('wordclouds.html')


@app.route("/statistics.html")
def statistics():

    # --------------- Number of influencer by category ---------------
    influencer_count_by_category_df = pd.read_csv("data_csv/statistics/influencers_count_by_category.csv", sep=',', header=0, skiprows=0)

    fig = go.Figure(data=[go.Pie(labels=influencer_count_by_category_df['_id'], values=influencer_count_by_category_df['count'],
                                 textinfo='percent',
                                 insidetextorientation='radial'
                                 )])
    fig.update_layout(title='Percentage of influencers from each category', title_x=0.5,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )
    #colors = ['gold', 'mediumturquoise']
    #fig.update_traces(hoverinfo='label+percent', marker=dict(colors=colors))

    influencer_count_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Number of posts per day -----------------
    day_freq_df = pd.read_csv("data_csv/statistics/post_frequency_per_day.csv", sep=',', header=0, skiprows=0)

    fig = go.Figure(data=[go.Bar(
        x=day_freq_df['day'],
        y=day_freq_df['posts'],
        marker_color='rgb(0, 179, 179)')
    ])

    fig.update_layout(title='No. of posts by day', title_x=0.5,
                      xaxis=dict(title='Day', showgrid=False, linecolor='rgb(204, 204, 204)'),
                      yaxis=dict(title='No. of posts', showgrid=True, linecolor='rgb(204, 204, 204)', showline=True,
                                 gridcolor="rgb(204, 204, 204)"),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )

    '''fig = px.bar(day_freq_df, x="day", y="posts",
                 labels={
                     "day": "Day",
                     "posts": "No. of posts",
                 },
                 title="No. of posts by day")'''
    day_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Number of posts per hour -----------------
    hour_freq_df = pd.read_csv("data_csv/statistics/post_frequency_per_hour.csv", sep=',', header=0, skiprows=0)

    fig = go.Figure(data=[go.Scatter(
        x=hour_freq_df['time'],
        y=hour_freq_df['posts'],
        line_color='rgb(0, 179, 179)',
        mode='lines+markers')
    ])

    fig.update_layout(title='No. of posts by hour', title_x=0.5,
                      xaxis=dict(title='Time', showgrid=False, linecolor='rgb(204, 204, 204)'),
                      yaxis=dict(title='No. of posts', showgrid=True, linecolor='rgb(204, 204, 204)', showline=True, gridcolor="rgb(204, 204, 204)"),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )

    '''fig = px.bar(hour_freq_df, x="time", y="posts",
                 labels={
                     "time": "Time",
                     "posts": "No. of posts",
                 },
                 title="No. of posts by hour")'''

    hour_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    posts = db.myLeaderboardsNew_db.find()
    df = pd.DataFrame(list(posts))
    df['Likes'] = df['Likes'].str.replace(',', '').astype(float)
    df['Views'] = df['Views'].str.replace(',', '').astype(float)
    df['Total Posts'] = pd.to_numeric(df['Total Posts'], errors='coerce')

    likes_per_category_sex = df.groupby(['category', 'sex'], as_index=False)['Likes'].sum()
    # views_per_category_sex = df.groupby(['category', 'sex'], as_index=False)['Views'].sum()
    posts_per_category_sex = df.groupby(['category', 'sex'], as_index=False)['Total Posts'].sum()
    likes_per_category = df.groupby(['category'], as_index=False)['Likes'].sum()
    # comments_per_category = df.groupby(['category'], as_index=False)['Comments'].sum()

    # data = likes_per_category.copy()
    # data['posts'] = posts_per_category_sex['posts']
    # data['likes'] = likes_per_category['Likes']
    # data['comments'] = comments_per_category
    # data['calc'] = (data['likes'] + data['comments']) / df['Followers'] * data['posts']

    category = df['category'].value_counts().to_frame().reset_index()
    category.rename(columns={'index': 'category', 'category': 'frequency'}, inplace=True)

    maritalStatus = df['marital_status'].value_counts().to_frame().reset_index()
    maritalStatus.rename(columns={'index': 'marital_status', 'marital_status': 'frequency'}, inplace=True)

    age = df['age'].value_counts().to_frame().reset_index()
    age.rename(columns={'index': 'age', 'age': 'frequency'}, inplace=True)

    sex = df['sex'].value_counts().to_frame().reset_index()
    sex.rename(columns={'index': 'sex', 'sex': 'frequency'}, inplace=True)
    # 1
    fig = go.Figure(data=[go.Bar(
        x=category['category'],
        y=category['frequency'],
        marker_color='rgb(0, 179, 179)')
    ])
    # fig = px.bar(category, x='category', y='frequency')
    fig.update_layout(title='Bar-chart-category', title_x=0.5,
                      xaxis=dict(title='Category', showgrid=False, linecolor='rgb(204, 204, 204)'),
                      yaxis=dict(title='Frequency', showgrid=True, linecolor='rgb(204, 204, 204)', showline=True,
                                 gridcolor="rgb(204, 204, 204)"),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )
    category_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)




    # 2
    #fig = px.bar(maritalStatus, x='marital_status', y='frequency')
    fig = go.Figure(data=[go.Bar(
        x=maritalStatus['marital_status'],
        y=maritalStatus['frequency'],
        marker_color='rgb(0, 179, 179)')
    ])
    fig.update_layout(title='Marital status', title_x=0.5,
                      xaxis=dict(title='Marital Status', showgrid=False, linecolor='rgb(204, 204, 204)'),
                      yaxis=dict(title='Frequency', showgrid=True, linecolor='rgb(204, 204, 204)', showline=True,
                                 gridcolor="rgb(204, 204, 204)"),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )
    maritalStatus_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # 3
    # fig = px.bar(age, x='age', y='frequency')
    fig = go.Figure(data=[go.Bar(
        x=age['age'],
        y=age['frequency'],
        marker_color='rgb(0, 179, 179)')
    ])
    fig.update_layout(title='Age Distribution', title_x=0.5,
                      xaxis=dict(title='Age', showgrid=False, linecolor='rgb(204, 204, 204)'),
                      yaxis=dict(title='Frequency', showgrid=True, linecolor='rgb(204, 204, 204)', showline=True,
                                 gridcolor="rgb(204, 204, 204)"),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )
    age_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # 4
    fig = go.Figure(data=[go.Bar(
        x=sex['sex'],
        y=sex['frequency'],
        marker_color='rgb(0, 179, 179)')
    ])
    # fig = px.bar(sex, x='sex', y='frequency')
    fig.update_layout(title='Sex', title_x=0.5,
                      xaxis=dict(title='Sex', showgrid=False, linecolor='rgb(204, 204, 204)'),
                      yaxis=dict(title='Frequency', showgrid=True, linecolor='rgb(204, 204, 204)', showline=True,
                                 gridcolor="rgb(204, 204, 204)"),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )
    sex_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    fig = go.Figure(
        data=[go.Pie(labels=likes_per_category['category'], values=likes_per_category['Likes'],
                     textinfo='percent',
                     insidetextorientation='radial',
                     title='Percentage of likes per category'
                     )])
    # fig = px.pie(labels=likes_per_category['category'], values=likes_per_category['Likes'],
    #              title='Percentage of likes per category',
    #              )
    fig.update_layout(title='No. of posts by day', title_x=0.5,
                      xaxis=dict(title='Day', showgrid=False, linecolor='rgb(204, 204, 204)'),
                      yaxis=dict(title='No. of posts', showgrid=True, linecolor='rgb(204, 204, 204)', showline=True,
                                 gridcolor="rgb(204, 204, 204)"),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )
    likes_per_category_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # fig = px.Figure(data=[go.bar(likes_per_category_sex, x='category', y='Likes', color='sex')])

    fig = px.bar(likes_per_category_sex, x="category", y="Likes",
                 color="sex", barmode='group')

    fig.update_layout(title='likes_per_category_sex', title_x=0.5,
                      xaxis=dict(title='Category', showgrid=False, linecolor='rgb(204, 204, 204)'),
                      yaxis=dict(title='Likes', showgrid=True, linecolor='rgb(204, 204, 204)', showline=True,
                                 gridcolor="rgb(204, 204, 204)"),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )
    category_sex_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    fig = px.scatter(df, x='Total Posts', y='Likes', color='category', hover_name='sex', log_x=True, log_y=True)
    fig.update_layout(title='Posts - Likes per user', title_x=0.5,
                      xaxis=dict(title='Total Posts', showgrid=False, linecolor='rgb(204, 204, 204)'),
                      yaxis=dict(title='Likes', showgrid=True, linecolor='rgb(204, 204, 204)', showline=True,
                                 gridcolor="rgb(204, 204, 204)"),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )
    posts_likes_scatter_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # fig = px.line(posts_per_category_sex, x='category', y='Total Posts', color='sex')
    fig = px.bar(posts_per_category_sex, x="category", y="Total Posts",
                 color="sex", barmode='group')
    fig.update_layout(title='Posts per category', title_x=0.5,
                      xaxis=dict(title='Category', showgrid=False, linecolor='rgb(204, 204, 204)'),
                      yaxis=dict(title='Total Posts', showgrid=True, linecolor='rgb(204, 204, 204)', showline=True,
                                 gridcolor="rgb(204, 204, 204)"),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )
    posts_per_category = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    fig = px.scatter(df, x='Views', y='Total Posts', color='category', hover_name='sex', log_x=True, log_y=True)
    fig.update_layout(title='Video posts - Views per user', title_x=0.5,
                      xaxis=dict(title='Category', showgrid=False, linecolor='rgb(204, 204, 204)'),
                      yaxis=dict(title='Likes', showgrid=True, linecolor='rgb(204, 204, 204)', showline=True,
                                 gridcolor="rgb(204, 204, 204)"),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )
    views_posts_scatter_graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # fig = px.bar(likes_per_category_sex, x='category', y='Likes')
    fig = go.Figure(data=[go.Bar(
        x=likes_per_category_sex['category'],
        y=likes_per_category_sex['Likes'],
        marker_color='rgb(0, 179, 179)')
    ])

    fig.update_layout(title='likes-category-Bar-chart', title_x=0.5,
                      xaxis=dict(title='Category', showgrid=False, linecolor='rgb(204, 204, 204)'),
                      yaxis=dict(title='Likes', showgrid=True, linecolor='rgb(204, 204, 204)', showline=True,
                                 gridcolor="rgb(204, 204, 204)"),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )
    likes_per_category_sex_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # fig = px.pie(likes_per_category['Likes'], values='Likes', names='category',
    #              title='Percentage of influencers from each category')
    # likes_per_category_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("statistics.html", influencerCountGraphJSON=influencer_count_graphjson,
                           dayGraph=day_graphjson, hourGraph=hour_graphjson, category_Graphjson=category_graphjson,
                           age_Graphjson=age_graphjson, maritalStatus_Graphjson=maritalStatus_graphjson,
                           sex_Graphjson=sex_graphjson,
                           likes_per_category_sex_Graphjson=likes_per_category_sex_graphjson,
                           likes_per_category_Graphjson=likes_per_category_graphjson,
                           category_sex_Graphjson=category_sex_graphjson,
                           posts_likes_scatter_Graphjson=posts_likes_scatter_json,
                           posts_per_category_Graphjson=posts_per_category,
                           views_posts_scatter_Graph_json=views_posts_scatter_graph_json,
                           likes_per_category_sex_Graphjson2=likes_per_category_sex_graphjson
                           )


@app.route("/questionaire_statistics.html")
def questionaire_statistics():
    """
    df = read_questionnaire()

    gender_df, willing_to_follow_male_df, willing_to_follow_female_df = cluster_by_gender(df)
    fig = px.pie(gender_df, values='Counter', names='Sex', title='Annotators - Gender Percentage')
    hour_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    fig = px.pie(willing_to_follow_male_df, values='Counter', names='Willing to follow', title='Male Annotators - Probability of Following')
    willing_to_follow_male_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    fig = px.pie(willing_to_follow_female_df, values='Counter', names='Willing to follow', title='Female Annotators - Probability of Following')
    willing_to_follow_female_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    """

    gender_graph_json = pd.read_csv("data_csv/gender_df.csv", sep=',',
                                                  header=0, skiprows=0)

    fig = go.Figure(data=[go.Pie(values=gender_graph_json['Counter'], labels=gender_graph_json['Sex'],
                                 textinfo='label+percent',
                                 insidetextorientation='radial'
                                 )])
    fig.update_layout(title='Annotators - Gender Percentage', title_x=0.5,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )
    colors = ['#198DE8', '#EF1453']
    fig.update_traces(hoverinfo='label+percent', marker=dict(colors=colors))
    gender_graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #-------------------------------------------------------------------------------------
    colorsYesNo = ['#85e085', '#ffa64d']
    willing_to_follow_male_df = pd.read_csv("data_csv/willing_to_follow_male_df.csv", sep=',',
                                    header=0, skiprows=0)

    fig = go.Figure(data=[go.Pie(values=willing_to_follow_male_df['Counter'], labels=willing_to_follow_male_df['Willing to follow'],
                                 textinfo='label+percent',
                                 insidetextorientation='radial'
                                 )])
    fig.update_layout(title='Male Annotators - Probability of following', title_x=0.5,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )
    fig.update_traces(hoverinfo='label+percent', marker=dict(colors=colorsYesNo))
    willing_to_follow_male_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # -------------------------------------------------------------------------------------
    willing_to_follow_female_df = pd.read_csv("data_csv/willing_to_follow_female_df.csv", sep=',',
                                    header=0, skiprows=0)
    fig = go.Figure(
        data=[go.Pie(values=willing_to_follow_female_df['Counter'], labels=willing_to_follow_female_df['Willing to follow'],
                     textinfo='label+percent',
                     insidetextorientation='radial'
                     )])
    fig.update_layout(title='Female Annotators - Probability of following', title_x=0.5,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )
    fig.update_traces(hoverinfo='label+percent', marker=dict(colors=colorsYesNo))
    willing_to_follow_female_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # -------------------------------------------------------------------------------------

    ########## pies with reasons
    total_reasons = pd.read_csv("data_csv/total_reasons.csv", sep=',',
                          header=0, skiprows=0, nrows=10)
    fig = go.Figure(
        data=[go.Pie(values=total_reasons['Counter'],
                     labels=total_reasons['Reason'],
                     textinfo='percent',
                     insidetextorientation='radial'
                     )])
    fig.update_layout(title='All categories - Top 10 reasons to follow', title_x=0.5,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)', legend=dict(font=dict(size=5,color="black")))
    fig.update_traces(hoverinfo='label+percent')
    total_reasons_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # -------------------------------------------------------------------------------------
    athlete = pd.read_csv("data_csv/athlete.csv", sep=',',
                                              header=0, skiprows=0)
    fig = go.Figure(
        data=[go.Pie(values=athlete['counts'],
                     labels=athlete['reasons'],
                     textinfo='percent',
                     insidetextorientation='radial'
                     )])
    fig.update_layout(title='Athlete category - Reasons to follow', title_x=0.5,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)', legend=dict(font=dict(size=6, color="black")))
    fig.update_traces(hoverinfo='label+percent')
    athlete_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # -------------------------------------------------------------------------------------
    dance = pd.read_csv("data_csv/dance.csv", sep=',',
                          header=0, skiprows=0)
    fig = go.Figure(
        data=[go.Pie(values=dance['counts'],
                     labels=dance['reasons'],
                     textinfo='percent',
                     insidetextorientation='radial'
                     )])
    fig.update_layout(title='Dance category - Reasons to follow', title_x=0.5,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)', legend=dict(font=dict(size=5, color="black")))
    fig.update_traces(hoverinfo='label+percent')
    dance_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # -------------------------------------------------------------------------------------
    ballet = pd.read_csv("data_csv/ballet.csv", sep=',',
                        header=0, skiprows=0)
    fig = go.Figure(
        data=[go.Pie(values=ballet['counts'],
                     labels=ballet['reasons'],
                     textinfo='percent',
                     insidetextorientation='radial'
                     )])
    fig.update_layout(title='Ballet category - Reasons to follow', title_x=0.5,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)', legend=dict(font=dict(size=8, color="black")))
    fig.update_traces(hoverinfo='label+percent')
    ballet_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # -------------------------------------------------------------------------------------
    nutrition = pd.read_csv("data_csv/nutrition.csv", sep=',',
                         header=0, skiprows=0)
    fig = go.Figure(
        data=[go.Pie(values=nutrition['counts'],
                     labels=nutrition['reasons'],
                     textinfo='percent',
                     insidetextorientation='radial'
                     )])
    fig.update_layout(title='Nutrition category - Reasons to follow', title_x=0.5,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)', legend=dict(font=dict(size=6, color="black")))
    fig.update_traces(hoverinfo='label+percent')
    nutrition_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # -------------------------------------------------------------------------------------
    pilates = pd.read_csv("data_csv/pilates.csv", sep=',',
                            header=0, skiprows=0)
    fig = go.Figure(
        data=[go.Pie(values=pilates['counts'],
                     labels=pilates['reasons'],
                     textinfo='percent',
                     insidetextorientation='radial'
                     )])
    fig.update_layout(title='Pilates category - Reasons to follow', title_x=0.5,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)', legend=dict(font=dict(size=5, color="black")))
    fig.update_traces(hoverinfo='label+percent')
    pilates_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # -------------------------------------------------------------------------------------
    body_building = pd.read_csv("data_csv/body_building.csv", sep=',',
                          header=0, skiprows=0)
    fig = go.Figure(
        data=[go.Pie(values=body_building['counts'],
                     labels=body_building['reasons'],
                     textinfo='percent',
                     insidetextorientation='radial'
                     )])
    fig.update_layout(title='Body building category - Reasons to follow', title_x=0.5,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)', legend=dict(font=dict(size=5, color="black")))
    fig.update_traces(hoverinfo='label+percent')
    body_building_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # -------------------------------------------------------------------------------------
    fitness_model = pd.read_csv("data_csv/fitness_model.csv", sep=',',
                                header=0, skiprows=0)
    fig = go.Figure(
        data=[go.Pie(values=fitness_model['counts'],
                     labels=fitness_model['reasons'],
                     textinfo='percent',
                     insidetextorientation='radial'
                     )])
    fig.update_layout(title='Fitness model category - Reasons to follow', title_x=0.5,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)', legend=dict(font=dict(size=5, color="black")))
    fig.update_traces(hoverinfo='label+percent')
    fitness_model_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # -------------------------------------------------------------------------------------

    #total_reasons_df = show_reasons(df)
    return render_template("questionaire_statistics.html", hour_graph=gender_graph_json, willing_to_follow_male_graph=willing_to_follow_male_graphjson,
                           willing_to_follow_female_graph=willing_to_follow_female_graphjson,
                           athlete=athlete_graphjson, dance=dance_graphjson,ballet=ballet_graphjson, nutrition=nutrition_graphjson,
                           body_building=body_building_graphjson,pilates=pilates_graphjson, fitness_model=fitness_model_graphjson,
                           total_reasons=total_reasons_graphjson)


@app.route("/hashtags.html")
def hashtags():
    # ----------------- Total number of hashtags from each category -----------------
    df = pd.read_csv("data_csv/hashtags/no_of_hashtags_by_category.csv", sep=',', header=0, skiprows=0)

    fig = go.Figure(data=[go.Bar(
        x=df['category'],
        y=df['hashtags_count'],
        marker_color='rgb(175, 122, 197)')
    ])

    fig.update_layout(title='No. of total hashtags by category', title_x=0.5,
                      xaxis=dict(title='Category', showgrid=False, linecolor='rgb(204, 204, 204)'),
                      yaxis=dict(title='No. of total hashtags', showgrid=True, linecolor='rgb(204, 204, 204)',
                                 showline=True, gridcolor="rgb(204, 204, 204)"),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )

    no_of_hashtags_by_category_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Percentage of hashtags from each category -----------------
    df = pd.read_csv("data_csv/hashtags/percentage_of_hashtags_by_category.csv", sep=',', header=0, skiprows=0)

    fig = go.Figure(data=[go.Bar(
        x=df['category'],
        y=df['hashtags_percentage'],
        marker_color='rgb(175, 122, 197)')
    ])

    fig.update_layout(title='Percentage of hashtags by category', title_x=0.5,
                      xaxis=dict(title='Category', showgrid=False, linecolor='rgb(204, 204, 204)'),
                      yaxis=dict(title='Percentage of hashtags', showgrid=True, linecolor='rgb(204, 204, 204)',
                                 showline=True, gridcolor="rgb(204, 204, 204)"),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )

    percentage_of_hashtags_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Hashtags distribution -----------------
    df = pd.read_csv("data_csv/hashtags/hashtag_distribution.csv", sep=',', header=0, skiprows=0).sort_values(by=['Number of Hashtags'], ascending=True)

    fig = go.Figure(data=[go.Scatter(
        x=df['Number of Hashtags'],
        y=df['Number of Posts'],
        line_color='rgb(0, 179, 179)',
        mode='lines+markers')
    ])

    '''fig.me = [
        dict(
            type="buttons",
            direction="left",
            buttons=list([
                dict(
                    args=[{'yaxis': {'type': 'linear'}}],
                    label="Linear Scale",
                    method="update"
                ),
                dict(
                    args=[{'yaxis': {'type': 'log'}}],
                    label="Log Scale",
                    method="update"
                )
            ])
        ),
    ]'''
    fig.update_layout(title='Hashtags Distribution', title_x=0.5,
                      xaxis=dict(title='No. of hashtags', showgrid=False, linecolor='rgb(204, 204, 204)', zeroline=False),
                      yaxis=dict(title='No. of posts', showgrid=True, linecolor='rgb(204, 204, 204)', showline=True, gridcolor="rgb(204, 204, 204)",
                                 zeroline=True, zerolinecolor='rgb(204, 204, 204)', zerolinewidth=1),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      updatemenus=[
                          dict(
                              x=1.01,
                              xanchor="left",
                              buttons=list([
                                  dict(label="Linear",
                                       method="relayout",
                                       args=[{"yaxis.type": "linear"}]),
                                  dict(label="Log",
                                       method="relayout",
                                       args=[{"yaxis.type": "log"}])
                              ]))]
                      )

    hashtags_distribution_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Top hashtag frequencies -----------------
    df = pd.read_csv("data_csv/hashtags/top_hashtag_frequency.csv", sep=',', header=0, skiprows=0).head(25)

    fig = go.Figure(data=[go.Bar(
        x=df['hashtag'],
        y=df['count'],
        marker_color='rgb(0, 179, 179)')
    ])

    fig.update_layout(title='Most Popular Hashtags', title_x=0.5,
                      xaxis=dict(title='Hashtags', showgrid=False, linecolor='rgb(204, 204, 204)'),
                      yaxis=dict(title='No. of posts', showgrid=True, linecolor='rgb(204, 204, 204)', showline=True, gridcolor="rgb(204, 204, 204)"),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)'
                      )

    hashtags_frequency_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Hashtags engagement distribution -----------------
    df = pd.read_csv("data_csv/hashtags/hashtags_engagement_distribution.csv", sep=',', header=0, skiprows=0)

    fig = go.Figure(data=[go.Scatter(
        x=df['hashtag_count'],
        y=df['engagement'],
        line_color='rgb(0, 179, 179)',
        mode='lines+markers')
    ])
    fig.update_yaxes(type="log")


    fig.update_layout(title='User engagement - Νumber of hashtags', title_x=0.5,
                      xaxis=dict(title='No. of hashtags', showgrid=False, linecolor='rgb(204, 204, 204)',
                                 zeroline=False),
                      yaxis=dict(title='User engagement (comments & likes)', showgrid=True, linecolor='rgb(204, 204, 204)',
                                 showline=True, gridcolor="rgb(204, 204, 204)", zeroline=True, zerolinecolor='rgb(204, 204, 204)', zerolinewidth=1),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      updatemenus=[
                          dict(
                              x=1.01,
                              xanchor="left",
                              buttons=list([
                                  dict(label="Linear",
                                       method="relayout",
                                       args=[{"yaxis.type": "linear"}]),
                                  dict(label="Log",
                                       method="relayout",
                                       args=[{"yaxis.type": "log"}])
                              ]))]
                      )

    hashtags_engagement_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Hashtags PCA 2D -----------------
    df = pd.read_csv("data_csv/hashtags/hashtags_2d.csv", sep=',', header=0, skiprows=0)
    #print(df)
    fig = go.Figure(data=[go.Scatter(
        x=df['x'],
        y=df['y'],
        hovertext= df['hashtags'],
        mode='markers')
    ])
    fig.update_traces(go.Scatter(
        mode="markers",
        name="Markers and Text",
        textposition="bottom center",
        marker=dict(
            color='rgba(0,0,0,0)',
            size=0,
            line=dict(
                color='rgb(175, 122, 197)',
                width=1.5
            )
        )
    ))

    fig.update_layout(
        height=800,
        title_text='Hashtags PCA 2D Representation', title_x=0.5,
        xaxis=dict(title='x', showgrid=True, linecolor='rgb(204, 204, 204)', showline=True, gridcolor="rgb(204, 204, 204)",
                   zeroline=False),
        yaxis=dict(title='y', showgrid=True, linecolor='rgb(204, 204, 204)',
                   showline=True, gridcolor="rgb(204, 204, 204)", zeroline=True, zerolinecolor='rgb(204,204,204)', zerolinewidth=1),

        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    hashtags_PCA_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # ----------------- Hashtags PCA 3D -----------------
    df = pd.read_csv("data_csv/hashtags/hashtags_2d.csv", sep=',', header=0, skiprows=0)
    print(df)
    fig = go.Figure(data=[go.Scatter3d(
        x=df['x'],
        y=df['y'],
        z=df['z'],
        hovertext=df['hashtags'],
        mode='markers')
    ])

    fig.update_traces(go.Scatter3d(
        mode="markers",
        name="Markers and Text",
        textposition="bottom center",
        marker=dict(
            color='rgb(175, 122, 197)',
            size=2,
            line=dict(
                #color='rgb(175, 122, 197)',
                width=0
            )
        )
    ))

    fig.update_layout(
        height=800,
        title_x = 0.5,
        title_text='Hashtags PCA 3D Representation',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    hashtags_PCA_3d_graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


    return render_template("hashtags.html", hashtags_distribution=hashtags_distribution_graphjson, hashtags_frequency=hashtags_frequency_graphjson,
                           no_of_hashtags_by_category=no_of_hashtags_by_category_graphjson, percentage_of_hashtags=percentage_of_hashtags_graphjson,
                           hashtags_engagement=hashtags_engagement_graphjson, hashtags_PCA=hashtags_PCA_graphjson,
                           hashtags_PCA_3d=hashtags_PCA_3d_graphjson)


@app.route("/todo/<importance_val>")
def get_todo(importance_val):
    todos = db.find('todos', {"importance": int(importance_val)})
    return jsonify(todos)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5111)

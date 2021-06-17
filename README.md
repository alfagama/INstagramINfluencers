# ININ
### INstagramINfluencers
----------------------------------------------------
## MSc Data & Web Science, Aristotle University of Thessaloniki (AUTH)
### Course: Web Mining
#### Project: *“Exploring the effects of fitness influencers personality on audience acceptance and motivation”*
----------------------------------------------------
**Team Members**:
1. Georgios Arampatzis
2. Alexia Fytili
3. Eleni Tsiolaki
4. Leonidas Vogiatzis

----------------------------------------------------
## [Technical Report] (pdf)

----------------------------------------------------
**Project Overview**:
@settings {
  font-size: 100;
}
The goal of this project is to study and explore in depth the effects of fitness influencers personality on audience acceptance and motivation, aiming at a better overview of the topic. This includes analyzing behavioural patterns of influencers active on the Instagram social media platform and detecting which aspects of their activities are more commonly endorsed by other users.
----------------------------------------------------

## Create a python virtual environment:

```sh
python3 -m venv INstagramINfluencers_env
source INstagramINfluencers_env/bin/activate
pip install -r requirements.txt
```
----------------------------------------------------
**Code Structure**:
```
.
└── INstagramINfluencers
    ├── dataset_creation
    │   └── questionnaire
    │   │   ├── questionnaire.py
    │   ├── credentials.py
    │   ├── directories.py
    │   ├── main.py
    │   ├── mongo.py
    │   ├── preprocess.py
    │   ├── preprocess_and_sentiment.py
    │   ├── read_data.py
    │   ├── scraper.py
    │   └── update_influencer_demographics.py
    ├── hashtags_analysis
    │   └── hashtags_clustering.py
    ├── predictions
    │   ├── final_questionnaire.csv
    │   ├── mongoInfo.png
    │   └── prediction.py
    ├── show_results
    │   ├── influencers_results.py
    │   ├── plot_results.py
    │   └── questionnaire_results.py
    ├── topic_modeling
    │   └── topic_modeling.py
    ├── web_app
    │   ├── data_csv
    │   │   ├── hashtags
    │   │   │   └── .csv
    │   │   └── statistics
    │   │   │   └── .csv
    │   │   └── .csv
    │   ├── funcs
    │   │   └── db.py
    │   └── static
    │       ├── predictions
    │       │   └── .csv
    │       └── stylesheets
    │       │   ├── pics
    │       │   │   └── .png
    │       │   ├── visualizations/LDA
    │       │   │   └── .html
    │       │   ├── .html
    │       │   └── .css
    │       ├── wordCloud_plots
    │       │   └── .png
    │       │   ├── .css
    │       │   └── .js
    │       └── app.py
    ├── .gitingnore
    ├── LICENSE
    └── README.md
```

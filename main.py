from read_data import *
from scraper import *
import os

if __name__ == '__main__':
    """
    you need a:
    ----> data/history/ <----- 
    directory with:
     influencer1_name.csv
     ...
     influencerN_name.csv
    """
    if os.path.isdir('data/scrape_comments') & os.path.isdir('data/history'):
        # get all influencers' names
        account_names = get_influencers_names()
        # for all of them get the URL posts
        for name in account_names:
            # get all URLs
            urls = get_urls(name)
            # create scraper object
            scraper = scraper()
            # call initialize_scrapper <- this will take said list and scrape ALL comments from ALL posts!
            # #awesome! :D
            initialize_scrapper(name, urls)
    else:
        print("Needed directory/ies not found!")

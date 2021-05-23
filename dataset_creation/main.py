from dataset_creation.read_data import *
from dataset_creation.scraper import *
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

if __name__ == '__main__':
    # check if needed directory/ies exist!
    # if os.path.isdir('data/scrape_comments') & os.path.isdir('data/history'):
    if os.path.isdir('../data/history'):
        # get all influencers' names
        account_names = get_influencers_names()
        # # exclude account names
        # account_names.remove('name1')
        # manual ChromeDriverManager()
        driver = webdriver.Chrome(ChromeDriverManager().install())
        # initialize scraper
        initialize_scraper(driver)
        # for all of them get the URL posts
        for name in account_names:
            # # create directory for each name to store scraped comments
            # create_directory(name)
            # new object name for each user
            scraper_name = name
            if name == "something.somethingelse":
                scraper_name = 'does_not_matter'
            else:
                exec(scraper_name + f" = '{name}' ")
            # create scraper object
            scraper_name = scraper()
            # get all URLs
            urls = get_urls(name)
            # call get_comments method
            scraper.get_comments(scraper_name, urls, driver, name, 500)  # can add extra argument in the end for max_comments
    else:
        print("Needed directory/ies not found!")

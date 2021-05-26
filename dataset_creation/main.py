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
        account_names.remove('therock')
        account_names.remove('sommerray')
        account_names.remove('tammyhembrow')
        account_names.remove('iamyanetgarcia')
        account_names.remove('nastya_nass_')
        account_names.remove('ulissesworld')
        account_names.remove('simeonpanda')
        account_names.remove('andreideiu_')
        account_names.remove('sergiconstance')
        account_names.remove('yarishna')
        account_names.remove('eva_andressa')
        account_names.remove('hannahstocking')
        account_names.remove('anllela_sagra')
        account_names.remove('saschafitness')
        account_names.remove('schwarzenegger')
        account_names.remove('hannaoeberg')
        account_names.remove('espana927')
        account_names.remove('demibagby')
        account_names.remove('jeff_seid')
        account_names.remove('martynfordofficial')
        account_names.remove('casssmartin')
        account_names.remove('sadikhadzovic')
        account_names.remove('frank_medrano')
        account_names.remove('jenselter')
        account_names.remove('kaigreene')
        account_names.remove('stevecook')
        account_names.remove('big_ramy')
        # manual ChromeDriverManager()
        driver = webdriver.Chrome(ChromeDriverManager().install())
        # initialize scraper
        initialize_scraper(driver)
        # for all of them get the URL posts
        for name in account_names:
            # # create directory for each name to store scraped comments
            # create_directory(name)
            # new object name for each user
            obj_name = name.replace(".", "")
            scraper_name = obj_name
            exec(scraper_name + f" = '{name}' ")
            # create scraper object
            scraper_name = scraper()
            # get all URLs
            urls = get_urls(name)
            # call get_comments method
            scraper.get_comments(scraper_name, urls, driver, name, 500)  # can add extra argument in the end for
            # max_comments
    else:
        print("Needed directory/ies not found!")
